from dataclasses import dataclass


@dataclass
class Book:
    id: int
    name: str
    author: str
    year: int
