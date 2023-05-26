def strToFloat(string: str) -> float:
    value: float
    try:
        value = float(string)
    except Exception as e:
        raise e  # TODO: Improve Raise exceptions
    return value
