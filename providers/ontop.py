from .base_provider import BaseProvider
import pandas as pd
from omegaconf import DictConfig


class OntopProvider(BaseProvider):
    name = "Ontop"

    def transfer(
        self, config: DictConfig, amount: float, currency_from: str = "USD", currency_to: str = "USD"
    ) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "Descripción": ["Costo por transferencia", "Monto tras comisión", "Recibes en USD"],
                "Valor": [f"{amount * 0.01:.2f} USD", f"{amount - 5:.2f} USD", f"{(amount - 5) * 4120:.2f} COP"],
            }
        )

    def convert(
        self, config: DictConfig, amount: float, currency_from: str = "USD", currency_to: str = "COP"
    ) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "Descripción": ["Costo por conversión", "Monto tras comisión", "Tasa de cambio", "Recibes en COP"],
                "Valor": [
                    f"{amount * 0.01:.2f} USD",
                    f"{amount - 5:.2f} USD",
                    "4120 COP/USD",
                    f"{(amount - 5) * 4120:.2f} COP",
                ],
            }
        )
