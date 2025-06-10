from dotenv import find_dotenv, load_dotenv

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    API_HOST: str
    API_PORT: int

    RABBITMQ_HOST: str

    MVID_CITY_ID: str
    MVID_REGION_ID: str
    MVID_TIMEZONE_OFFSET: str
    MVID_REGION_SHOP: str

    TG_BOT_TOKEN: str

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @property
    def API_BASE_URL(self):
        return f'http://{self.API_HOST}:{self.API_PORT}'

    @property
    def RABBITMQ_URL(self):
        return f'amqp://guest:guest@{self.RABBITMQ_HOST}:5672'

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


load_dotenv(find_dotenv(".env"))
settings = Settings()
