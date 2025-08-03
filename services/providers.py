import pandas as pd
from omegaconf import DictConfig


class Global66:
    def __init__(self, config: DictConfig):
        self.config = config

    def get_summary(self) -> pd.DataFrame:
        uvt_threshold_cop = self.config.tax.uvt_2025 * self.config.tax.uvt_units
        resumen = [
            {
                "Concepto": "Costo por recibir USD (wire/swift)",
                "Valor": f"{self.config.g66.receive_fee_usd:.2f} USD",
            },
            {
                "Concepto": "Costo por enviar USD (ACH)",
                "Valor": f"{self.config.g66.usd_to_usd_fee:.2f} USD",
            },
            {
                "Concepto": "Costo por tipo de cambio USD-COP (%)",
                "Valor": f"{self.config.g66.conversion_fee_by_type_of_change * 100:.2f}%",
            },
            {
                "Concepto": "Tasa de cambio Global66",
                "Valor": f"{self.config.g66.rate:,.2f} COP/USD",
            },
            {
                "Concepto": "Costo servicio COP",
                "Valor": f"{self.config.g66.service_fee_cop:,.0f} COP",
            },
            {"Concepto": "IVA servicio", "Valor": f"{self.config.g66.iva_fee:,.0f} COP"},
            {
                "Concepto": "GMF (4x1000) UVT 2025",
                "Valor": f"{self.config.tax.uvt_2025:,.0f} COP",
            },
            {
                "Concepto": "GMF (4x1000) Unidades UVT 2025",
                "Valor": f"{self.config.tax.uvt_units:,.0f} UVT",
            },
            {
                "Concepto": "GMF (4x1000) rate",
                "Valor": f"{self.config.g66.gmf_rate * 1000:.2f}%",
            },
            {
                "Concepto": "GMF (4x1000) Umbral COP",
                "Valor": f"{uvt_threshold_cop:,.0f} COP",
            },
        ]
        return pd.DataFrame(resumen)

    def calculate_convertion_usd_to_cop(self, amount: float) -> pd.DataFrame:
        usd_after_pct_fee = amount * (1 - self.config.g66.conversion_fee_by_type_of_change)
        conversion_fee_amount = amount * self.config.g66.conversion_fee_by_type_of_change
        cop_received = round(usd_after_pct_fee * self.config.g66.rate)

        df = pd.DataFrame(
            {
                "Descripción": [
                    "Costo por conversión (3%)",
                    "Monto tras comisión por conversión",
                    "Tasa de cambio",
                    "Recibes en COP",
                ],
                "Valor": [
                    f"{conversion_fee_amount:.2f} USD",
                    f"{usd_after_pct_fee:.2f} USD",
                    f"{self.config.g66.rate:,.2f} COP/USD",
                    f"{cop_received:,.2f} COP",
                ],
            }
        )
        return df

    def calculate_transfer_usd_to_usd(self, amount: float) -> pd.DataFrame:
        usd_after_fixed_fee = amount + self.config.g66.usd_to_usd_fee
        df = pd.DataFrame(
            {
                "Descripción": [
                    "Costo por enviar USD (ACH)",
                    "Monto tras comisión por enviar USD",
                    "Recibes en USD",
                ],
                "Valor": [
                    f"{self.config.g66.usd_to_usd_fee:.2f} USD",
                    f"{usd_after_fixed_fee:.2f} USD",
                    f"{amount:,.2f} USD",
                ],
            }
        )
        return df

    def calculate_transfer_cop_to_cop(self, cop_amount: float) -> pd.DataFrame:
        total_cost = self.config.g66.iva_fee + self.config.g66.service_fee_cop
        uvt_threshold = self.config.tax.uvt_units * self.config.tax.uvt_2025
        gmf = round(cop_amount * self.config.g66.gmf_rate) if cop_amount >= uvt_threshold else 0
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
                    f"{self.config.g66.service_fee_cop:.2f} COP",
                    f"{self.config.g66.iva_fee:.2f} COP",
                    f"{gmf:,.0f} COP",
                    f"{total_cost:,.2f} COP",
                    f"{final_received:,.2f} COP",
                ],
            }
        )

        return df

    def calculate(self, operation: str, amount: float) -> pd.DataFrame:
        if operation == "Conversion USD a COP":
            return self.calculate_convertion_usd_to_cop(amount)
        elif operation == "Enviar USD a USD":
            return self.calculate_transfer_usd_to_usd(amount)
        elif operation == "Enviar COP a COP":
            return self.calculate_transfer_cop_to_cop(amount)
        else:
            print(f"Operation not recognized: {operation}")
            return pd.DataFrame()


class Remitly:
    def __init__(self, config: DictConfig):
        self.config = config

    def calculate(self, operation: str, amount: float) -> pd.DataFrame:
        # Placeholder for Remitly calculations
        # Implement similar methods as in Global66

        usd_after_fee = amount - self.config.remitly.remitly_fee
        # cop_received = usd_after_fee * self.config.remitly.remitly_rate

        # st.subheader("Resultado: Schwab + Remitly")
        # st.write(f"Remitly cobra: **{self.config.remitly.remitly_fee:.2f} USD**")
        # st.write(f"Tasa de cambio: **{self.config.remitly.remitly_rate:,.2f} COP/USD**")
        # st.write(f"USD enviados: **{usd_after_fee:.2f} USD**")
        # st.write(f"**Total recibido: {cop_received:,.2f} COP**")

        # total_cost_usd = self.config.remitly.remitly_fee + receive_fee_g66 + usd_to_usd_fee
        # st.write(f"**Costo total en USD por todo el flujo: {total_cost_usd:.2f} USD**")
