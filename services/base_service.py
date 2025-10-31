import pandas as pd


class BaseService:
    name = ""

    def run(self, config, provider, amount: float, currency_from: str, currency_to: str) -> pd.DataFrame:
        raise NotImplementedError("Service must implement run()")
