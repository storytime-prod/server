from sqlmodel import Field, SQLModel


class Story(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str
    genre: str | None = Field(default=None, index=True)
