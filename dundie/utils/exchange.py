from decimal import Decimal
from typing import Dict, List

import httpx
from pydantic import BaseModel, Field

from dundie.utils.log import log


class USDRate(BaseModel):
    code: str = Field(default="USD")
    codein: str = Field(default="USD")
    name: str = Field(default="Dolar/Dolar")
    value: Decimal = Field(alias="high")


def get_rates(currencies: List[str], url: str) -> Dict[str, USDRate]:
    """get current rate for USD vs Currency"""
    return_data = {}
    for currency in currencies:
        if currency == "USD":
            return_data[currency] = USDRate(high=1)
        else:
            response = httpx.get(url.format(currency=currency))
            if response.status_code == 200:
                data = response.json()[f"USD{currency}"]
                return_data[currency] = USDRate(**data)
                log.info(response.text)
            else:
                return_data[currency] = USDRate(name="api/error", high=0)
                log.error(response.text)

    return return_data
