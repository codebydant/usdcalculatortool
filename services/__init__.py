from .transfers import TransferService
from .conversions import ConversionService

SERVICES = {
    "Conversión": ConversionService(),
    "Transferencia": TransferService(),
}
