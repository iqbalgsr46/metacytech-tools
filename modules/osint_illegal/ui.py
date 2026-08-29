"""
OSINT Ilegal — Terminal User Interface
Untuk security awareness training / authorized penetration testing
"""
import os
import sys
import time
import asyncio

# Ensure we can import from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .config import C, SCANNER_REGISTRY, RESULTS_DIR
from .engine import ScanEngine
from .utils.formatters import fmt_table


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    cls()
    print(f"\n{C.B}{C.CYN}  ╔══════════════════════════════════════════════════╗{C.RST}")
    print(f"{C.B}{C.CYN}  ║     OSINT ILEGAL — Massive Data Miner           ║{C.RST}")
    print(f"{C.B}{C.CYN}  ╚══════════════════════════════════════════════════╝{C.RST}")
    print(f"  {C.DIM}500+ data points/target | 63 scanners | 24 database bocor{C.RST}")
    print(f"  {C.DIM}Untuk security awareness & authorized testing only{C.RST}\n")


def show_scanner_menu():
    print(f"  {C.B}Pilih jenis scan:{C.RST}\n")
    print(f"  {C.BLU}[1]{C.RST}  {C.B}Scan by NIK{C.RST}         — data kependudukan")
    print(f"  {C.BLU}[2]{C.RST}  {C.B}Scan by KK{C.RST}          — data keluarga")
    print(f"  {C.BLU}[3]{C.RST}  {C.B}Scan by NPWP{C.RST}        — data perpajakan")
    print(f"  {C.BLU}[4]{C.RST}  {C.B}Scan by Nama{C.RST}        — cross-reference identitas")
    print(f"  {C.BLU}[5]{C.RST}  {C.B}Scan by No. HP{C.RST}      — profil telepon")
    print(f"  {C.BLU}[6]{C.RST}  {C.B}Scan by Email{C.RST}       — jejak digital")
    print(f"  {C.MAG}[7]{C.RST}  {C.B}{C.MAG}DEEP SCAN{C.RST}     — 63 scanners (500+ data points)")
    print(f"  {C.RED}[8]{C.RST}  {C.B}{C.RED}TELUSURI BREACH{C.RST} — cari database bocor (NIK, KK, alamat, dll)")
    print(f"  {C.GRN}[9]{C.RST}  {C.B}Lihat Hasil{C.RST}         — hasil scan terkumpul")
    print(f"  {C.YLW}[10]{C.RST} {C.B}Export Excel{C.RST}        — export ke .xlsx")
    print(f"  {C.DIM}[0]{C.RST}  Kembali\n")


def run_deep_scan(engine: ScanEngine, target: str):
    print(f"\n  {C.B}{C.CYN}═══ DEEP SCAN: {target} ═══{C.RST}\n")
    
    def callback(current, total, name):
        bar_width = 30
        percent = current / total
        filled = int(bar_width * percent)
        bar = f"{C.GRN}{'█' * filled}{C.RST}{C.DIM}{'░' * (bar_width - filled)}{C.RST}"
        sys.stdout.write(f"\r  {bar}  {C.B}{name}{C.RST}  ({current}/{total})  ")
        sys.stdout.flush()
    
    print(f"  {C.DIM}Menjalankan {len(SCANNER_REGISTRY)} scanners...{C.RST}\n")
    
    results = asyncio.run(engine.run_deep_scan(target, callback))
    
    print(f"\n\n  {C.GRN}✓ Deep scan selesai!{C.RST}")
    print(f"  {C.DIM}Total scanner dijalankan: {engine.total_scans}{C.RST}")
    print(f"  {C.DIM}Data terkumpul dari: {len(results.get('all_results', {}))} kategori{C.RST}")
    
    # Summary per category
    print(f"\n  {C.B}{C.CYN}═══ HASIL SCAN ═══{C.RST}\n")
    headers = ["Kategori", "Status", "Data Points"]
    rows = []
    for scanner_name, result in results.get("all_results", {}).items():
        if isinstance(result, dict):
            cat = result.get("category", "?")
            stat = result.get("status", "?")
            fields = len(result.get("fields", {}))
            rows.append([cat, stat, str(fields)])
    
    print(fmt_table(headers, rows[:25]))  # Show top 25
    
    input(f"\n  {C.DIM}Tekan Enter untuk melanjutkan...{C.RST}")


def show_results(engine: ScanEngine):
    results = engine.results
    if not results.get("all_results"):
        print(f"\n  {C.YLW}Belum ada hasil scan. Jalankan scan terlebih dahulu.{C.RST}")
        input(f"\n  {C.DIM}Tekan Enter...{C.RST}")
        return
    
    print(f"\n  {C.B}{C.CYN}═══ HASIL OSINT SCAN ═══{C.RST}\n")
    print(f"  Target     : {C.B}{results.get('target', 'N/A')}{C.RST}")
    print(f"  Tipe       : {results.get('target_type', 'N/A')}")
    print(f"  Timestamp  : {results.get('timestamp', 'N/A')}")
    print(f"  Total Data : {len(results.get('all_results', {}))} entries\n")
    
    for cat, items in [
        ("DATA KEPENDUDUKAN", results.get("kependudukan", {})),
        ("DOKUMEN BOCOR", results.get("dokumen_bocor", {})),
        ("BREACH DATABASE", results.get("breach_db", {})),
        ("MEDIA SOSIAL", results.get("media_sosial", {})),
        ("FINANSIAL", results.get("finansial", {})),
        ("KOMUNIKASI", results.get("komunikasi", {})),
        ("JEJAK DIGITAL", results.get("jejak_digital", {})),
    ]:
        if items:
            print(f"  {C.CYN}{cat}{C.RST}")
            for name in items:
                print(f"    {C.GRN}✓{C.RST} {name}")
    
    input(f"\n  {C.DIM}Tekan Enter...{C.RST}")


def browse_breaches(engine: ScanEngine):
    """Browse and search known breach databases — no input target needed"""
    while True:
        print_header()
        print(f"  {C.B}{C.RED}═══ TELUSURI DATABASE BOCOR ═══{C.RST}\n")
        print(f"  {C.DIM}Cari database yang mengandung data spesifik yang bocor{C.RST}")
        print(f"  {C.DIM}(tanpa perlu input NIK/Email — browse berdasarkan kejadian breach){C.RST}\n")
        
        print(f"  {C.BLU}[1]{C.RST}  Lihat Semua Breach (24 database bocor)")
        print(f"  {C.BLU}[2]{C.RST}  Cari berdasarkan jenis data (misal: NIK, KK, alamat, rekening)")
        print(f"  {C.BLU}[3]{C.RST}  Cari berdasarkan platform (misal: Tokopedia, BPJS, PLN)")
        print(f"  {C.BLU}[4]{C.RST}  Cari berdasarkan tahun")
        print(f"  {C.BLU}[5]{C.RST}  Cari berdasarkan status (TERKONFIRMASI / TERSANGKA)")
        print(f"  {C.DIM}[0]{C.RST}  Kembali ke menu utama\n")
        
        try:
            print(f"  {C.CYN}Pilih: {C.RST}", end="")
            ch = input().strip()
            
            if ch == "0":
                break
            
            elif ch == "1":  # All breaches
                all_b = engine.get_all_breaches()
                display_breach_list(all_b)
            
            elif ch == "2":  # Search by data type
                print(f"\n  {C.CYN}Masukkan jenis data (contoh: NIK, KK, alamat, rekening, email, hp):{C.RST}")
                dtype = input(f"  {C.CYN}Jenis data: {C.RST}").strip()
                if dtype:
                    results = engine.get_breaches_by_data_type(dtype)
                    print(f"\n  {C.DIM}Menemukan {len(results)} database bocor mengandung '{dtype}'{C.RST}")
                    display_breach_list(results)
                input(f"  {C.DIM}Tekan Enter...{C.RST}")
            
            elif ch == "3":  # Search by platform name
                print(f"\n  {C.CYN}Masukkan nama platform (contoh: Tokopedia, BPJS, PLN, Facebook):{C.RST}")
                kw = input(f"  {C.CYN}Nama: {C.RST}").strip()
                if kw:
                    results = engine.search_breaches(kw)
                    display_breach_list(results)
                input(f"  {C.DIM}Tekan Enter...{C.RST}")
            
            elif ch == "4":  # Search by year
                print(f"\n  {C.CYN}Masukkan tahun (2019-2024):{C.RST}")
                try:
                    yr = int(input(f"  {C.CYN}Tahun: {C.RST}").strip())
                    results = engine.get_breaches_by_year(yr)
                    print(f"\n  {C.DIM}Database bocor tahun {yr}: {len(results)} ditemukan{C.RST}")
                    display_breach_list(results)
                except:
                    print(f"\n  {C.YLW}Tahun tidak valid!{C.RST}")
                input(f"  {C.DIM}Tekan Enter...{C.RST}")
            
            elif ch == "5":  # Search by status
                print(f"\n  {C.CYN}Pilih status:{C.RST}")
                print(f"  [1] TERKONFIRMASI — sudah diverifikasi")
                print(f"  [2] TERSANGKA — masih dalam investigasi")
                st = input(f"  {C.CYN}Pilih: {C.RST}").strip()
                status_map = {"1": "TERKONFIRMASI", "2": "TERSANGKA"}
                if st in status_map:
                    results = engine.get_breaches_by_status(status_map[st])
                    print(f"\n  {C.DIM}Database status {status_map[st]}: {len(results)} ditemukan{C.RST}")
                    display_breach_list(results)
                input(f"  {C.DIM}Tekan Enter...{C.RST}")
            
            else:
                print(f"\n  {C.YLW}Pilihan tidak valid!{C.RST}")
                time.sleep(0.5)
                
        except (KeyboardInterrupt, EOFError):
            break


def display_breach_list(breaches: list):
    """Display breach list with detail option"""
    if not breaches:
        print(f"\n  {C.YLW}Tidak ada hasil ditemukan.{C.RST}")
        input(f"  {C.DIM}Tekan Enter...{C.RST}")
        return
    
    for i, b in enumerate(breaches, 1):
        print(f"\n  {C.B}{C.RED}[{i}]{C.RST} {C.B}{b.get('name', '?')}{C.RST} ({b.get('year', '?')})")
        print(f"      {C.DIM}Records   :{C.RST} {b.get('records', '?')}")
        print(f"      {C.DIM}Status    :{C.RST} {C.GRN if b.get('status') == 'TERKONFIRMASI' else C.YLW}{b.get('status', '?')}{C.RST}")
        print(f"      {C.DIM}Sumber    :{C.RST} {b.get('source', '?')}")
        print(f"      {C.DIM}Data bocor:{C.RST} {', '.join(b.get('data_leaked', []))}")
        print(f"      {C.DIM}Keterangan:{C.RST} {b.get('description', '')[:150]}...")
    
    print(f"\n  {C.CYN}Ketik nomor untuk detail lengkap, atau 0 untuk kembali:{C.RST} ", end="")
    try:
        sel = input().strip()
        if sel.isdigit():
            idx = int(sel) - 1
            if 0 <= idx < len(breaches):
                show_breach_detail(breaches[idx])
    except:
        pass


def show_breach_detail(b: dict):
    """Show full detail of a breach"""
    print_header()
    print(f"\n  {C.B}{C.RED}═══ DETAIL BREACH: {b.get('name', '?')} ═══{C.RST}\n")
    print(f"  {C.B}Nama Platform   :{C.RST} {b.get('name', '?')}")
    print(f"  {C.B}Tahun Kejadian  :{C.RST} {b.get('year', '?')}")
    print(f"  {C.B}Jumlah Records  :{C.RST} {b.get('records', '?')} data")
    print(f"  {C.B}Status          :{C.RST} {C.GRN if b.get('status') == 'TERKONFIRMASI' else C.YLW}{b.get('status', '?')}{C.RST}")
    print(f"  {C.B}Sumber Informasi:{C.RST} {b.get('source', '?')}")
    print(f"  {C.B}Deskripsi       :{C.RST} {b.get('description', '')}\n")
    
    print(f"  {C.RED}{C.B}DATA YANG BOCOR:{C.RST}\n")
    for d in b.get("data_leaked", []):
        print(f"    {C.RED}⚠{C.RST} {d}")
    
    print(f"\n  Total {len(b.get('data_leaked', []))} jenis data bocor dari platform ini.")
    input(f"\n  {C.DIM}Tekan Enter untuk kembali...{C.RST}")

def osint_illegal_menu():
    """Main entry point — called from launcher.py"""
    engine = ScanEngine()
    
    while True:
        print_header()
        show_scanner_menu()
        
        try:
            print(f"  {C.CYN}Pilih menu: {C.RST}", end="")
            choice = input().strip()
            
            if choice == "0":
                print(f"\n  {C.DIM}Kembali ke launcher utama...{C.RST}")
                time.sleep(0.5)
                break
            
            elif choice == "1":  # NIK
                target = input(f"\n  {C.CYN}Masukkan NIK (16 digit): {C.RST}").strip()
                if target and len(target) >= 16:
                    asyncio.run(engine.run_single_scan("NIKScanner", target))
                    print(f"\n  {C.GRN}✓ Scan selesai{C.RST}")
                input(f"  {C.DIM}Tekan Enter...{C.RST}")
            
            elif choice == "2":  # KK
                target = input(f"\n  {C.CYN}Masukkan No KK (16 digit): {C.RST}").strip()
                if target:
                    asyncio.run(engine.run_single_scan("KKScanner", target))
                    print(f"\n  {C.GRN}✓ Scan selesai{C.RST}")
                input(f"  {C.DIM}Tekan Enter...{C.RST}")
            
            elif choice == "3":  # NPWP
                target = input(f"\n  {C.CYN}Masukkan NPWP: {C.RST}").strip()
                if target:
                    asyncio.run(engine.run_single_scan("NPWPScanner", target))
                    print(f"\n  {C.GRN}✓ Scan selesai{C.RST}")
                input(f"  {C.DIM}Tekan Enter...{C.RST}")
            
            elif choice == "4":  # Nama
                target = input(f"\n  {C.CYN}Masukkan Nama/Lokasi: {C.RST}").strip()
                if target and len(target) >= 3:
                    asyncio.run(engine.run_single_scan("IdentityScanner", target))
                    print(f"\n  {C.GRN}✓ Scan selesai{C.RST}")
                input(f"  {C.DIM}Tekan Enter...{C.RST}")
            
            elif choice == "5":  # Phone
                target = input(f"\n  {C.CYN}Masukkan No HP: {C.RST}").strip()
                if target:
                    asyncio.run(engine.run_single_scan("PhoneScanner", target))
                    print(f"\n  {C.GRN}✓ Scan selesai{C.RST}")
                input(f"  {C.DIM}Tekan Enter...{C.RST}")
            
            elif choice == "6":  # Email
                target = input(f"\n  {C.CYN}Masukkan Email: {C.RST}").strip()
                if target:
                    asyncio.run(engine.run_single_scan("EmailScanner", target))
                    print(f"\n  {C.GRN}✓ Scan selesai{C.RST}")
                input(f"  {C.DIM}Tekan Enter...{C.RST}")
            
            elif choice == "7":  # DEEP SCAN
                print(f"\n  {C.CYN}Pilih input:{C.RST}")
                print(f"  [1] NIK")
                print(f"  [2] KK")
                print(f"  [3] NPWP")
                print(f"  [4] Nama")
                print(f"  [5] No HP")
                print(f"  [6] Email\n")
                target_type = input(f"  {C.CYN}Pilih tipe target: {C.RST}").strip()
                type_map = {"1": "NIK", "2": "KK", "3": "NPWP", "4": "Nama", "5": "HP", "6": "Email"}
                label = type_map.get(target_type, "unknown")
                target = input(f"  {C.CYN}Masukkan {label}: {C.RST}").strip()
                if target:
                    run_deep_scan(engine, target)
            
            elif choice == "8":  # TELUSURI BREACH
                browse_breaches(engine)
            
            elif choice == "9":  # Lihat Hasil
                show_results(engine)
            
            elif choice == "10":  # Export Excel
                export_to_excel(engine)
            
            else:
                print(f"\n  {C.YLW}Pilihan tidak valid!{C.RST}")
                time.sleep(0.5)
        
        except (KeyboardInterrupt, EOFError):
            print(f"\n  {C.CYN}Kembali ke launcher...{C.RST}")
            break
        except Exception as e:
            print(f"\n  {C.RED}Error: {e}{C.RST}")
            input(f"  {C.DIM}Tekan Enter...{C.RST}")
