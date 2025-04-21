from pydantic_settings import BaseSettings

class Config(BaseSettings):
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_SECRET: str
    SPOTIFY_REDIRECT_URI: str
    SPOTIFY_USER_ID: str

    model_config = {
        "env_file":".env", 
        "extra":"allow"
    }

settings = Config()

if __name__ == "__main__":
    print(settings.SPOTIFY_CLIENT_ID)