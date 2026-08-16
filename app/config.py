from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "fantasy-valoracion"    
    DEBUG: bool = True    

    class Config:
        env_file = ".env"


settings = Settings()
