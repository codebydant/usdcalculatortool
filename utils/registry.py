import importlib
import os


PROVIDERS = {}


def load_providers() -> dict:
    providers_dir = os.path.join(os.path.dirname(__file__), "..", "providers")

    for file in os.listdir(providers_dir):
        if file.endswith(".py") and file not in ("__init__.py", "base_provider.py"):
            module_name = file[:-3]
            module = importlib.import_module(f"providers.{module_name}")

            for attr in dir(module):
                obj = getattr(module, attr)
                try:
                    from providers.base_provider import BaseProvider

                    if isinstance(obj, type) and issubclass(obj, BaseProvider) and obj is not BaseProvider:
                        PROVIDERS[obj.name] = obj()
                except Exception:
                    pass

    return PROVIDERS
