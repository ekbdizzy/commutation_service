from pydantic_settings import BaseSettings
from environs import Env

env = Env()
env.read_env()


class Settings(BaseSettings):

    # Switch settings
    SWITCH_IP: str = env.str("SWITCH_IP")
    SWITCH_USERNAME: str = env.str("SWITCH_USERNAME")
    SWITCH_PASSWORD: str = env.str("SWITCH_PASSWORD")
