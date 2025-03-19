from typing import Annotated
from ..cores.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from ..models.olhcv import Olhcv, mysql_upsert
from ..services.olhcv_service import yfinance2olhcvs

sessionDep = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/olhcvs",
    tags=["olhcvs"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def olhcvs(
    session: sessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 1
) -> list[Olhcv]:
    olhcvs = session.exec(select(Olhcv).offset(offset).limit(limit)).all()
    return olhcvs


@router.get("/yfinance")
def fetch_yfinance(
    session: sessionDep,
    symbol: str,
    start: str = None,
    end: str = None,
    period: str = "1d",
    interval: str = "1d",
) -> list[Olhcv]:
    olhcvs = yfinance2olhcvs(symbol, start, end, period, interval)
    session.exec(mysql_upsert(olhcvs))
    session.commit()
    return olhcvs


@router.get("/{id}")
def show_olhcv(id: str, session: sessionDep) -> Olhcv:
    olhcv = session.get(Olhcv, id)
    if not olhcv:
        raise HTTPException(status_code=404, detail="Olhcv not found")
    return olhcv
