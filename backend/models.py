from dataclasses import dataclass
from typing import List

@dataclass
class ParsedQuery:
    must: List[str]
    should: List[str]
    must_not: List[str]
    phrases: List[str]
