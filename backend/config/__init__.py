from pydantic_settings import BaseSettings


class CommonSettings(BaseSettings):
    APP_NAME: str = "Дефекты дорожного покрытия"
    DEBUG_MODE: bool = True
    is_development: bool = False
    client_id: str = "1"


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 9090


class DatabaseSettings(BaseSettings):
    DB_URL: str = "mongodb://mongoadmin:secret@localhost:27017"
    DB_NAME: str = "road_defects"

class Constants(BaseSettings):
    defects: dict = { "crack": 0, "pothole":1, "rutting":2, "patch":3}


class Settings(CommonSettings, ServerSettings, DatabaseSettings, Constants):
    pass


settings = Settings()
