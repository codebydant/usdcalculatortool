from .base_service import BaseService
import pandas as pd


class ConversionService(BaseService):
    name = "Conversión"

    def run(self, config, provider, amount: float, currency_from: str, currency_to: str) -> pd.DataFrame:
        return provider.convert(config, amount, currency_from, currency_to)
