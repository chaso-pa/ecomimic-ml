from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.dialects.mysql import insert as mysql_insert
import cuid


class EconomicIndicator(SQLModel, table=True):
    __tablename__ = "economic_indicators"

    id: str = Field(default=cuid.cuid(), primary_key=True)
    timestamp: datetime = Field(
        nullable=False, sa_column_kwargs={"name": "timestamp"})
    country: str = Field(nullable=False, sa_column_kwargs={"name": "country"})
    name: str = Field(nullable=False, sa_column_kwargs={"name": "name"})
    value: float = Field(nullable=False, sa_column_kwargs={"name": "value"})

    __table_args__ = (
        (UniqueConstraint("timestamp", "country", "name")),
        {"mysql_collate": "utf8mb4_unicode_ci"},
    )


def mysql_upsert(values: list[EconomicIndicator]):
    value_dicts = [v.dict() for v in values]

    stmt = mysql_insert(EconomicIndicator).values(value_dicts)
    stmt = stmt.on_duplicate_key_update(
        value=stmt.inserted.value,
    )
    return stmt
