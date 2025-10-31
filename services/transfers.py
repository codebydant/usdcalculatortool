from .base_service import BaseService
import pandas as pd


class TransferService(BaseService):
    name = "Transferencia"

    def run(self, config, provider, amount: float, currency_from: str, currency_to: str) -> pd.DataFrame:
        return provider.transfer(config, amount, currency_from, currency_to)
