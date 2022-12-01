def list_split(value: list, parts: int):
    return [value[i:i+parts] for i in range(0, len(value), parts)]
