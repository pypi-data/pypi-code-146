CONFIG = {
    "DEV": {
        "LOCAL": {
            "TEST_URL": "https://rec-dev.shinsegae.ai/v1",
            "MLOPS_REC_URL": "https://rec-dev.shinsegae.ai/v1",
            "MLOPS_DATA_URL": "https://data-dev.shinsegae.ai/v1",
        },
        "MLOPS": {
            "TEST_URL": "https://rec-dev.shinsegae.ai/v1",
            "MLOPS_REC_URL": "https://rec-dev.shinsegae.ai/v1",
            "MLOPS_DATA_URL": "http://internal-data-dev-v1.shinsegae.ai",
        },
    },
    "STG": {
        "LOCAL": {
            "TEST_URL": "https://rec-stg.shinsegae.ai/v1",
            "MLOPS_REC_URL": "https://rec-stg.shinsegae.ai/v1",
            "MLOPS_DATA_URL": "http://internal-data-stg-v1.shinsegae.ai",
        },
        "MLOPS": {
            "TEST_URL": "https://rec-stg.shinsegae.ai/v1",
            "MLOPS_REC_URL": "https://rec-stg.shinsegae.ai/v1",
            "MLOPS_DATA_URL": "http://internal-data-stg-v1.shinsegae.ai",
        },
    },
    "PRD": {
        "LOCAL": {
            "TEST_URL": "https://rec.shinsegae.ai/v1",
            "MLOPS_REC_URL": "https://rec.shinsegae.ai/v1",
            "MLOPS_DATA_URL": "http://internal-data-prd-v1.shinsegae.ai",
        },
        "MLOPS": {
            "TEST_URL": "https://rec.shinsegae.ai/v1",
            "MLOPS_REC_URL": "https://rec.shinsegae.ai/v1",
            "MLOPS_DATA_URL": "http://internal-data-prd-v1.shinsegae.ai",
        },
    },
}


class Config:
    def __init__(self, env: str, apikey: str, runtime_env: str = None):
        assert env in CONFIG.keys(), f"`env` must be in {CONFIG.keys()}"

        setattr(self, "ENV", env)
        setattr(self, "APIKEY", apikey)

        if runtime_env:
            setattr(self, "RUNTIME_ENV", runtime_env)
            try:
                for key, url in CONFIG[env][runtime_env].items():
                    setattr(self, key, url)
            except KeyError:
                raise Exception(f"BAP {env} does not support this {runtime_env} environment.")

            return

        if env == "LOCAL":
            setattr(self, "RUNTIME_ENV", "LOCAL")
            for key, url in CONFIG[env]["LOCAL"].items():
                setattr(self, key, url)
            return

        for runtime_env, urls in CONFIG[env].items():
            try:
                setattr(self, "RUNTIME_ENV", runtime_env)
                for key, url in urls.items():
                    setattr(self, key, url)
                break
            except Exception:
                continue

        if not hasattr(self, "RUNTIME_ENV"):
            raise Exception(f"BAP {env} does not support this runtime environment.")
