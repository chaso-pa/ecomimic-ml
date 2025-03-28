from sqlmodel import SQLModel, Field
from sqlalchemy.schema import UniqueConstraint
import cuid


class FredIndex(SQLModel, table=True):
    __tablename__ = "fred_indices"

    id: str = Field(default=cuid.cuid(), primary_key=True)
    crawl_status: bool = Field(default=False, sa_column_kwargs={
                               "name": "crawl_status"})
    country: str = Field(nullable=False, sa_column_kwargs={"name": "country"})
    symbol: str = Field(nullable=False, sa_column_kwargs={"name": "symbol"})

    __table_args__ = (
        (UniqueConstraint("country", "symbol")),
        {"mysql_collate": "utf8mb4_unicode_ci"},
    )
