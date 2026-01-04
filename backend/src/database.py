from sqlmodel import SQLModel, create_engine, Session

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}

engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    """Cria as tabelas no banco se elas não existirem."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency Injection para o FastAPI."""
    with Session(engine) as session:
        yield session