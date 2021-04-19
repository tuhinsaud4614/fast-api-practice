import os
from typing import Text, AnyStr

def get_path(file_name: AnyStr) -> AnyStr:
    return os.path.dirname(os.path.dirname(os.path.abspath(file_name)))

def join_path(*paths: str) -> Text:
    return os.path.join(get_path(__file__), *paths)