from repo.db import db


class ConfigRepo:
    def __init__(self):
        pass

    @classmethod
    def get_configs(cls):
        return db.select("SELECT * FROM CONFIGS")

    @classmethod
    def get_config_by_id(cls, config_id: int):
        data = db.select(f"SELECT * FROM CONFIGS WHERE id = {config_id}")
        return data[0] if data else None


