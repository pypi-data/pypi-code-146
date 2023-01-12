__version__ = "0.2.12"

try:
    from ai_dashboard.api.client import Client
except ModuleNotFoundError:
    pass
except Exception as e:
    import traceback

    traceback.print_exc()
