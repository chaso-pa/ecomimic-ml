from typing import Annotated
from ..cores.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from ..models.fred_index import FredIndex
from ..models.economic_indicator import EconomicIndicator, mysql_upsert
from ..services.economic_indicator_service import fred2indicators

sessionDep = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/economic_indicators",
    tags=["economic_indicators"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def economic_indicators(
    session: sessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 1
) -> list[EconomicIndicator]:
    indicators = session.exec(
        select(EconomicIndicator).offset(offset).limit(limit)
    ).all()
    return indicators


@router.get("/fred")
def fetch_fred(
    session: sessionDep,
    country: str,
    name: str,
    limit: Annotated[int, Query(le=10000)] = 100,
) -> list[EconomicIndicator]:
    indicators = fred2indicators(country, name, limit)
    session.exec(mysql_upsert(indicators))
    session.commit()
    return indicators


@router.get("fred/fetch_all")
def fetch_all_fred(session: sessionDep) -> list[EconomicIndicator]:
    indices = session.exec(select(FredIndex).where(
        FredIndex.crawl_status)).all()
    indicators = []
    for index in indices:
        indicators += fred2indicators(index.country, index.symbol)
    session.exec(mysql_upsert(indicators))
    session.commit()
    return indicators


@router.get("/{id}")
def show_economic_indicator(id: str, session: sessionDep) -> EconomicIndicator:
    olhcv = session.get(EconomicIndicator, id)
    if not olhcv:
        raise HTTPException(
            status_code=404, detail="Economic indicator not found")
    return olhcv
