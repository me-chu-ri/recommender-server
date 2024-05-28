def to_lower_case(string: str) -> str:
    return string.lower()


def snake_to_camel(string: str) -> str:
    words: list = to_lower_case(string).split('_')
    words: list = [words[0]] + [word.capitalize() for word in words[1:]]
    return ''.join(words)
