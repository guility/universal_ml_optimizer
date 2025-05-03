from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    INPUT_FEATURES: list[str]
    OUTPUT_FEATURES: list[str]

    INPUT_QUEUE_NAME: str
    OUTPUT_QUEUE_NAME: str