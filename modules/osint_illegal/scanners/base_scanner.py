import asyncio
import aiohttp
from typing import Optional, Dict, Any, List

class BaseScanner:
    """Base class for all OSINT scanners"""
    
    def __init__(self):
        self.name = self.__class__.__name__
        self.category = "UNKNOWN"
        self.fields: List[str] = []
        self.results: Dict[str, Any] = {}
        self.session: Optional[aiohttp.ClientSession] = None

    async def scan(self, target: str) -> Dict[str, Any]:
        """Main scan method — override in subclasses"""
        if not self.validate_target(target):
            return {"error": f"Invalid target format: {target}", "status": "INVALID"}
        return {"message": "Not implemented", "status": "UNKNOWN"}

    def validate_target(self, target: str) -> bool:
        return bool(target and target.strip())

    def get_fields(self) -> List[str]:
        return self.fields.copy()

    def get_category(self) -> str:
        return self.category
    
    async def get_session(self) -> aiohttp.ClientSession:
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession(
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            )
        return self.session
    
    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
    
    def __del__(self):
        if hasattr(self, '_close_warning'):
            return
