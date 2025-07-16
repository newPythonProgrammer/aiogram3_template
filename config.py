from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel



class BotConfig(BaseModel):
    token: str
    admins: List[int] = []


class DBConfig(BaseModel):
    mysql_host: str
    mysql_port: int
    mysql_user: str
    mysql_password: str
    mysql_db: str

    @property
    def dsn(self) -> str:
        return (
            f"mysql+aiomysql://{self.mysql_user}:{self.mysql_password}@"
            f"{self.mysql_host}:{self.mysql_port}/{self.mysql_db}"
        )


class CryptoBotConfig(BaseModel):
    api_key: str


class YooKassaConfig(BaseModel):
    shop_id: str
    api_key: str


class Settings(BaseSettings):
    bot: BotConfig
    db: DBConfig
    cryptobot: CryptoBotConfig
    yookassa: YooKassaConfig

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__"
    )


# Единый доступ к конфигу
def get_settings():
    return Settings()
