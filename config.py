import os


def get_env(value: str, default: str = "", required: bool = False) -> str:
    """
    Get environment variable.

    Args:
        value (str): Environment variable name.
        default (str): Default value.
        required (bool): Whether the environment variable is required.

    Returns:
        str: Environment variable value.
    """
    try:
        return os.environ[value]
    except KeyError:
        if required:
            raise Exception(f"Environment variable '{value}' is required.")
        return default


class Config:
    """
    Configuration class.
    """

    def __init__(self):
        self.token = get_env("TOKEN", required=True)
        self.openai_api_key = get_env("OPENAI_API_KEY", required=True)
