from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.dialects.mysql import insert as mysql_insert
import cuid


class Olhcv(SQLModel, table=True):
    __tablename__ = "olhcvs"

    id: str = Field(default=cuid.cuid(), primary_key=True)
    timestamp: datetime = Field(nullable=False, sa_column_kwargs={"name": "timestamp"})
    symbol: str = Field(nullable=False, sa_column_kwargs={"name": "symbol"})
    open: float = Field(nullable=False, sa_column_kwargs={"name": "open"})
    high: float = Field(nullable=False, sa_column_kwargs={"name": "high"})
    low: float = Field(nullable=False, sa_column_kwargs={"name": "low"})
    close: float = Field(nullable=False, sa_column_kwargs={"name": "close"})
    volume: float = Field(nullable=False, sa_column_kwargs={"name": "volume"})

    __table_args__ = (
        (UniqueConstraint("timestamp", "symbol")),
        {"mysql_collate": "utf8mb4_unicode_ci"},
    )


def mysql_upsert(values: list[Olhcv]):
    value_dicts = [v.dict() for v in values]

    stmt = mysql_insert(Olhcv).values(value_dicts)
    print(stmt)
    stmt = stmt.on_duplicate_key_update(
        open=stmt.inserted.open,
        high=stmt.inserted.high,
        low=stmt.inserted.low,
        close=stmt.inserted.close,
        volume=stmt.inserted.volume,
    )
    return stmt
