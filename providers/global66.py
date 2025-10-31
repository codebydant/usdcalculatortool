import pandas as pd
from .base_provider import BaseProvider
from omegaconf import DictConfig


def get_summary(config) -> pd.DataFrame:
    uvt_threshold_cop = config.tax.uvt_2025 * config.tax.uvt_units
    resumen = [
        {
            "Concepto": "Costo por recibir USD (wire/swift)",
            "Valor": f"{config.g66.receive_fee_usd:.2f} USD",
        },
        {
            "Concepto": "Costo por enviar USD (ACH)",
            "Valor": f"{config.g66.usd_to_usd_fee:.2f} USD",
        },
        {
            "Concepto": "Costo por tipo de cambio USD-COP (%)",
            "Valor": f"{config.g66.conversion_fee_by_type_of_change * 100:.2f}%",
        },
        {
            "Concepto": "Tasa de cambio Global66",
            "Valor": f"{config.g66.rate:,.2f} COP/USD",
        },
        {
            "Concepto": "Costo servicio COP",
            "Valor": f"{config.g66.service_fee_cop:,.0f} COP",
        },
        {"Concepto": "IVA servicio", "Valor": f"{config.g66.iva_fee:,.0f} COP"},
        {
            "Concepto": "GMF (4x1000) UVT 2025",
            "Valor": f"{config.tax.uvt_2025:,.0f} COP",
        },
        {
            "Concepto": "GMF (4x1000) Unidades UVT 2025",
            "Valor": f"{config.tax.uvt_units:,.0f} UVT",
        },
        {
            "Concepto": "GMF (4x1000) rate",
            "Valor": f"{config.g66.gmf_rate * 1000:.2f}%",
        },
        {
            "Concepto": "GMF (4x1000) Umbral COP",
            "Valor": f"{uvt_threshold_cop:,.0f} COP",
        },
    ]
    return pd.DataFrame(resumen)


def calculate_transfer_usd_to_usd(config, amount: float) -> pd.DataFrame:
    usd_after_fixed_fee = amount + config.g66.usd_to_usd_fee
    df = pd.DataFrame(
        {
            "Descripción": [
                "Costo por enviar USD (ACH)",
                "Monto tras comisión por enviar USD",
                "Recibes en USD",
            ],
            "Valor": [
                f"{config.g66.usd_to_usd_fee:.2f} USD",
                f"{usd_after_fixed_fee:.2f} USD",
                f"{amount:,.2f} USD",
            ],
        }
    )
    return df


def calculate_transfer_cop_to_cop(config, cop_amount: float) -> pd.DataFrame:
    total_cost = config.g66.iva_fee + config.g66.service_fee_cop
    uvt_threshold = config.tax.uvt_units * config.tax.uvt_2025
    gmf = round(cop_amount * config.g66.gmf_rate) if cop_amount >= uvt_threshold else 0
    total_cost = total_cost + gmf
    final_received = cop_amount - total_cost
    df = pd.DataFrame(
        {
            "Descripción": [
                "Costo por enviar COP",
                "IVA",
                "GMF (4x1000)",
                "Costo total",
                "Recibes en COP",
            ],
            "Valor": [
                f"{config.g66.service_fee_cop:.2f} COP",
                f"{config.g66.iva_fee:.2f} COP",
                f"{gmf:,.0f} COP",
                f"{total_cost:,.2f} COP",
                f"{final_received:,.2f} COP",
            ],
        }
    )

    return df


class Global66Provider(BaseProvider):
    name = "Global66"

    def convert(
        self, config: DictConfig, amount: float, currency_from: str = "USD", currency_to: str = "COP"
    ) -> pd.DataFrame:
        # Only USD → COP supported (for now)
        if currency_from != "USD" or currency_to != "COP":
            raise ValueError(f"{self.name} only supports USD → COP conversions currently")

        fee_pct = config.g66.conversion_fee_by_type_of_change
        rate = config.g66.rate

        conversion_fee_amount = amount * fee_pct
        usd_after_fee = amount - conversion_fee_amount
        cop_received = round(usd_after_fee * rate)

        df = pd.DataFrame(
            {
                "Descripción": [
                    f"Costo por conversión ({fee_pct * 100:.0f}%)",
                    "Monto tras comisión",
                    "Tasa de cambio",
                    "Recibes en COP",
                ],
                "Valor": [
                    f"{conversion_fee_amount:.2f} USD",
                    f"{usd_after_fee:.2f} USD",
                    f"{rate:,.2f} COP/USD",
                    f"{cop_received:,.2f} COP",
                ],
            }
        )

        return df

    def transfer(
        self, config: DictConfig, amount: float, currency_from: str = "USD", currency_to: str = "USD"
    ) -> pd.DataFrame:
        # Only USD → USD and COP → COP supported (for now)
        if currency_from == "USD" and currency_to == "USD":
            return calculate_transfer_usd_to_usd(config=config, amount=amount)
        elif currency_from == "COP" and currency_to == "COP":
            return calculate_transfer_cop_to_cop(config=config, cop_amount=amount)
        else:
            raise ValueError(f"{self.name} only supports USD → USD and COP → COP transfers currently")
