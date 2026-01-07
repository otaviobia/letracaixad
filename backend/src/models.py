from datetime import datetime
from enum import IntEnum
from sqlmodel import Field, SQLModel

class RatingEnum(IntEnum):
    ABISMO = 1
    NAO_E_PRA_MIM = 2
    ESQUECIVEL = 3
    MANEIRO = 4
    PEAK_FICTION = 5

class ReviewBase(SQLModel):
    title: str = Field(index=True)
    content_type: str = Field(index=True) # filme, série, jogo, livro, etc
    cover_image_url: str 
    reaction_gif_url: str | None = None
    review_markdown: str
    rating: RatingEnum = Field(index=True)
    tags_list: str # string separada com vírgula "terror, sci-fi"
    external_link: str | None = None
    time_spent: str | None = None
    published: bool = True

class Review(ReviewBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(default_factory=datetime.now)

class ReviewCreate(ReviewBase):
    created_at: datetime | None = None

class ReviewUpdate(SQLModel):
    title: str | None = None
    content_type: str | None = None
    cover_image_url: str | None = None
    reaction_gif_url: str | None = None
    review_markdown: str | None = None
    rating: RatingEnum | None = None
    tags_list: str | None = None
    external_link: str | None = None
    time_spent: str | None = None
    created_at: datetime | None = None
    published: bool | None = None