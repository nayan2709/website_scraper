import json
import os

from pydantic import BaseModel


class Config(BaseModel):
    APP_HOST: str
    APP_PORT: int
    BASE_URL: str
    DB_URL: str
    REDIS_HOST: str
    REQUEST_RETRIES: int
    AUTH_TOKEN: str


def get_config() -> Config:
    env = os.getenv("ENV", "local")
    print(f"ENV ----- {env}")
    with open(f"env_{env}.json") as json_env_file:
        env_config = json.load(json_env_file)
    config_data = Config(**env_config)
    return config_data


config: Config = get_config()
