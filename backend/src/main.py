from typing import Annotated
import os
import json
from contextlib import asynccontextmanager
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Query, Security, status, WebSocket, WebSocketDisconnect
from fastapi.security import APIKeyHeader
from sqlmodel import Session, select

from src.database import create_db_and_tables, get_session
from src.models import Review, ReviewCreate, ReviewUpdate
from src.connection_manager import manager
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

api_key_header = APIKeyHeader(name="X-Admin-Token", auto_error=False)

async def get_admin_user(api_key_token: str = Security(api_key_header)):
    """
    Dependência que protege rotas de escrita.
    """
    secret = os.getenv("ADMIN_SECRET")
    
    if not secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="ERRO: ADMIN_SECRET não configurado no .env"
        )

    if api_key_token == secret:
        return True
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Acesso negado: Token inválido."
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Letracaixad API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    # Lista de origens permitidas (quem pode chamar a API)
    allow_origins=[
        "http://localhost:4321",    # Seu frontend local
        "http://127.0.0.1:4321",    # Variação do local
        # "https://seu-site-no-cloudflare.com" # Futuramente, adicione seu domínio aqui
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, DELETE, PATCH, OPTIONS
    allow_headers=["*"],  # Permite cabeçalhos customizados (Importante para o X-Admin-Token!)
)

SessionDep = Annotated[Session, Depends(get_session)]
AdminDep = Annotated[bool, Depends(get_admin_user)]

# --- ROTAS PÚBLICAS ---

@app.get("/")
def read_root():
    return {"status": "online", "msg": "Bem-vindo ao Blog Backend"}

@app.get("/reviews/", response_model=list[Review])
def read_reviews(
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=20, le=100),
    content_type: str | None = None,
    rating: int | None = None
):
    """
    Lista reviews com paginação e filtros opcionais.
    Ex: /reviews/?content_type=filme&rating=5
    """
    query = select(Review)
    
    if content_type:
        query = query.where(Review.content_type == content_type)
    if rating:
        query = query.where(Review.rating == rating)
        
    query = query.order_by(Review.created_at.desc()).offset(offset).limit(limit)
    
    return session.exec(query).all()

@app.get("/reviews/{review_id}", response_model=Review)
def read_review(review_id: int, session: SessionDep):
    """Lê um review específico."""
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review não encontrado")
    return review

# --- ROTAS PROTEGIDAS ---

@app.post("/reviews/", response_model=Review)
def create_review(
    review: ReviewCreate, 
    session: SessionDep,
    _is_admin: AdminDep 
):
    """Cria um novo review."""
    db_review = Review.model_validate(review)
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review

@app.patch("/reviews/{review_id}", response_model=Review)
def update_review(
    review_id: int,
    review_update: ReviewUpdate,
    session: SessionDep,
    _is_admin: AdminDep
):
    """
    Atualiza um review. Envie apenas os campos que quer mudar.
    Atualiza o 'updated_at' automaticamente.
    """
    db_review = session.get(Review, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review não encontrado")

    # Pega apenas os dados que foram enviados (excluindo os nulos)
    review_data = review_update.model_dump(exclude_unset=True)
    
    for key, value in review_data.items():
        setattr(db_review, key, value)

    # Atualiza a data de modificação
    db_review.updated_at = datetime.now()

    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review

@app.delete("/reviews/{review_id}")
def delete_review(
    review_id: int, 
    session: SessionDep,
    _is_admin: AdminDep
):
    """Apaga um review para sempre."""
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review não encontrado")
        
    session.delete(review)
    session.commit()
    return {"ok": True, "message": "Review deletado com sucesso"}

# --- ROTA WEBSOCKET ---

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    client_id: str, 
    page: str | None = Query(default="/")
):
    room_id = page or "/"
    
    await manager.connect(websocket, room_id)
    try:
        while True:
            data = await websocket.receive_text()
            data_json = json.loads(data)
            data_json["id"] = client_id
            
            await manager.broadcast(data_json, room_id=room_id, sender=websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
        await manager.broadcast(
            {"id": client_id, "type": "disconnect"}, 
            room_id=room_id, 
            sender=websocket
        )