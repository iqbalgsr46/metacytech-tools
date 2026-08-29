from typing import Dict, Any

class BaseReporter:
    def __init__(self):
        self.name = self.__class__.__name__

    def export(self, data: Dict[str, Any], filepath: str) -> bool:
        raise NotImplementedError
