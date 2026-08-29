"""
OSINT Ilegal Module — Massive Identity Data Mining
Untuk security awareness & authorized penetration testing only
"""
__version__ = "1.0.0"
__description__ = "500+ data points per target | 30+ scanners | Export Excel 12+ sheet"

# Trigger all scanner registrations
from . import scanners
from .engine import ScanEngine
from .reporters.excel_reporter import ExcelReporter
