import json
from .base_reporter import BaseReporter

class JSONReporter(BaseReporter):
    def export(self, data: dict, filepath: str = None) -> str:
        import os
        from datetime import datetime
        from ..config import RESULTS_DIR
        
        if not filepath:
            target_val = data.get("target", "unknown")
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(RESULTS_DIR, f"osint_{target_val}_{ts}.json")
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return f"OK: {filepath}"
        except Exception as e:
            return f"ERROR: {e}"
