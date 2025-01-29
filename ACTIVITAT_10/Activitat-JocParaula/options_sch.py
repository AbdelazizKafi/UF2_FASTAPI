from pydantic import BaseModel

class Option(BaseModel):
    option: str

def option_schema(option) -> dict:
    return {
        "option": option
    }

def options_schema(options) -> list:
    return [option_schema(option) for option in options]
