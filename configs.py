from repo.config_repo import ConfigRepo


class Config:
    @classmethod
    def get_configs(cls):
        configs = ConfigRepo.get_configs()
        return configs
