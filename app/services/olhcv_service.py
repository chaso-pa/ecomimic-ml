import yfinance as yf
import cuid
from ..models.olhcv import Olhcv


def yfinance2olhcvs(
    symbol, start=None, end=None, period="1d", interval="1m"
) -> list[Olhcv]:
    # Download data
    data = yf.download(symbol, start=start, end=end,
                       period=period, interval=interval)

    # Drop rows with missing values
    data = data.dropna()

    data.columns = ["open", "low", "high", "close", "volume"]
    data["symbol"] = symbol
    data["id"] = data.apply(lambda _: cuid.cuid(), axis=1)
    data["timestamp"] = data.index
    olhcvs = data.apply(lambda x: Olhcv(**x), axis=1)
    olhcvs = olhcvs.reset_index(drop=True).to_list()

    return olhcvs
