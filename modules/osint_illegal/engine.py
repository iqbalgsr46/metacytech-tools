import asyncio
import importlib
import inspect
from datetime import datetime
from typing import Dict, Any, Optional
from .config import C, SCANNER_REGISTRY, RESULTS_DIR
from .utils.validators import validate_nik, validate_kk, validate_npwp, validate_phone, validate_email
from .utils.formatters import progress_bar

class ScanEngine:
    """Main orchestrator for OSINT scanning"""
    
    def __init__(self):
        self.results: Dict[str, Any] = {
            "target": "",
            "target_type": "",
            "timestamp": datetime.now().isoformat(),
            "all_results": {},
            "kependudukan": {},
            "keluarga": {},
            "dokumen_bocor": {},
            "breach_db": {},
            "jejak_digital": {},
            "media_sosial": {},
            "finansial": {},
            "komunikasi": {},
            "pendidikan": {},
            "dark_web": {},
            "sumber": {}
        }
        self.total_scans = 0
        self.completed_scans = 0
    
    def _detect_type(self, target: str) -> str:
        valid, _ = validate_nik(target)
        if valid:
            return "NIK"
        if validate_kk(target):
            return "KK"
        if validate_npwp(target):
            return "NPWP"
        valid_phone, _ = validate_phone(target)
        if valid_phone:
            return "PHONE"
        if validate_email(target):
            return "EMAIL"
        if len(target) > 10 and (" " in target or any(c.isdigit() for c in target)):
            return "IDENTITY"
        return "USERNAME"
    
    async def run_single_scan(self, scanner_name: str, target: str) -> Dict:
        if scanner_name in SCANNER_REGISTRY:
            scanner_cls = SCANNER_REGISTRY[scanner_name]
            scanner = scanner_cls()
            try:
                result = await scanner.scan(target)
                await scanner.close()
                return result
            except Exception as e:
                return {"error": str(e), "status": "ERROR"}
        return {"error": f"Scanner {scanner_name} tidak ditemukan", "status": "ERROR"}
    
    async def run_deep_scan(self, target: str, callback=None) -> Dict:
        self.results["target"] = target
        self.results["target_type"] = self._detect_type(target)
        self.total_scans = len(SCANNER_REGISTRY)
        self.completed_scans = 0
        
        scanners_to_run = list(SCANNER_REGISTRY.items())
        
        for scanner_name, scanner_cls in scanners_to_run:
            scanner = scanner_cls()
            try:
                result = await scanner.scan(target)
                result["scanner"] = scanner_name
                result["category"] = scanner.category
                
                # Categorize results
                cat = scanner.category
                if cat == "DATA_KEPENDUDUKAN":
                    self.results["kependudukan"][scanner_name] = result
                elif cat == "DOKUMEN_BOCOR":
                    self.results["dokumen_bocor"][scanner_name] = result
                elif cat == "BREACH_DATABASE":
                    self.results["breach_db"][scanner_name] = result
                elif cat == "MEDIA_SOSIAL":
                    self.results["media_sosial"][scanner_name] = result
                elif cat == "FINANSIAL":
                    self.results["finansial"][scanner_name] = result
                elif cat == "KONTAK":
                    self.results["komunikasi"][scanner_name] = result
                elif cat == "PLATFORM":
                    self.results["jejak_digital"][scanner_name] = result
                elif cat == "PEMERINTAHAN":
                    self.results["pendidikan"][scanner_name] = result
                elif cat == "DARK_WEB":
                    self.results["dark_web"][scanner_name] = result
                elif cat in ["LAINNYA", "IDENTITAS"]:
                    self.results["jejak_digital"][scanner_name] = result
                
                self.results["all_results"][scanner_name] = result
                
            except Exception as e:
                self.results["all_results"][scanner_name] = {
                    "error": str(e), "status": "ERROR", "scanner": scanner_name
                }
            finally:
                try:
                    await scanner.close()
                except:
                    pass
            
            self.completed_scans += 1
            if callback:
                callback(self.completed_scans, self.total_scans, scanner_name)
        
        self.results["sumber"] = {
            "total_scanners": self.total_scans,
            "successful": self.completed_scans,
            "sources": list(SCANNER_REGISTRY.keys())
        }
        
        return self.results
    
    def export_excel(self, filepath: str = None) -> str:
        from .reporters.excel_reporter import ExcelReporter
        reporter = ExcelReporter()
        return reporter.export(self.results, filepath)
    
    def export_json(self, filepath: str = None) -> str:
        from .reporters.json_reporter import JSONReporter
        reporter = JSONReporter()
        return reporter.export(self.results, filepath)
    
    def get_stats(self) -> Dict:
        return {
            "total_scanners": self.total_scans,
            "completed": self.completed_scans,
            "target": self.results.get("target", ""),
            "target_type": self.results.get("target_type", ""),
            "kategor": {
                cat: len(items) for cat, items in self.results.get("all_results", {}).items()
                if isinstance(items, dict)
            }
        }
    
    # ─── LEAK SEARCH — browse based on what leaked, not input ───
    
    def get_all_breaches(self) -> list:
        """Return list of all known breach databases"""
        import json, os
        path = os.path.join(os.path.dirname(__file__), "data", "breach_signatures.json")
        if not os.path.exists(path):
            return []
        with open(path, "r") as f:
            data = json.load(f)
        return data.get("breaches", [])
    
    def search_breaches(self, keyword: str) -> list:
        """Search breaches by keyword (name, year, type of data leaked)"""
        breaches = self.get_all_breaches()
        results = []
        keyword = keyword.lower()
        for b in breaches:
            if (keyword in b.get("name", "").lower() or
                keyword in str(b.get("year", "")) or
                keyword in b.get("status", "").lower() or
                any(keyword in d.lower() for d in b.get("data_leaked", []))):
                results.append(b)
        return results
    
    def get_breaches_by_data_type(self, data_type: str) -> list:
        """Find all breaches that contain a specific type of leaked data"""
        breaches = self.get_all_breaches()
        results = []
        data_type = data_type.lower()
        for b in breaches:
            if any(data_type in d.lower() for d in b.get("data_leaked", [])):
                results.append(b)
        return results
    
    def get_breaches_by_year(self, year: int) -> list:
        return [b for b in self.get_all_breaches() if b.get("year") == year]
    
    def get_breaches_by_status(self, status: str) -> list:
        return [b for b in self.get_all_breaches() if b.get("status", "").upper() == status.upper()]
