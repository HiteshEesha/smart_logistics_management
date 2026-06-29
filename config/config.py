import yaml
from pathlib import Path


class Config:

    _config = None

    @classmethod
    def load_config(cls):

        if cls._config is None:

            config_path = (
                Path(__file__).parent / "config.yaml"
            )

            with open(config_path, "r") as file:

                cls._config = yaml.safe_load(file)

        return cls._config

    @classmethod
    def get_database_config(cls):

        return cls.load_config()["database"]

    @classmethod
    def get_application_config(cls):

        return cls.load_config()["application"]

    @classmethod
    def get_validation_config(cls):

        return cls.load_config()["validation"]

    @classmethod
    def get_file_config(cls):

        return cls.load_config()["files"]