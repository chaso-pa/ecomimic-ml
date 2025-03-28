import pandas as pd
import cuid
from fredapi import Fred
from ..models.economic_indicator import EconomicIndicator


def fred2indicators(country, name, limit=100) -> list[EconomicIndicator]:
    fred = Fred(api_key="6df528ba9360628175d6f8e715e1211b")
    data = pd.DataFrame(fred.get_series(name), columns=["value"])
    # Drop rows with missing values
    data = data.dropna()
    data = data.tail(limit)

    data["id"] = data.apply(lambda _: cuid.cuid(), axis=1)
    data["country"] = country
    data["name"] = name
    data["timestamp"] = data.index
    indicators = data.apply(lambda x: EconomicIndicator(**x), axis=1)
    indicators = indicators.reset_index(drop=True).to_list()

    return indicators
