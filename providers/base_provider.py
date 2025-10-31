import pandas as pd
from omegaconf import DictConfig


class BaseProvider:
    name = "Base"

    def __init__(self, config=None):
        self.config = config

    def convert(
        self, config: DictConfig, amount: float, currency_from: str = "USD", currency_to: str = "COP"
    ) -> pd.DataFrame:
        """
        Perform currency conversion. Must return a pandas DataFrame or dict.

        :param amount: amount to convert
        :param currency_from: input currency (default USD)
        :param currency_to: target currency (default COP)
        """
        raise NotImplementedError("Provider must implement convert()")

    def transfer(
        self, config: DictConfig, amount: float, currency_from: str = "USD", currency_to: str = "COP"
    ) -> pd.DataFrame:
        """
        Perform currency transfer. Must return a pandas DataFrame or dict.
        :param amount: amount to transfer
        :param currency_from: input currency (default USD)
        :param currency_to: target currency (default COP)
        """
        raise NotImplementedError("Provider must implement transfer()")
