# Scanners Package — auto-import all scanner modules to trigger registration
from . import base_scanner

# Group A: Kependudukan
from .group_a_kependudukan import nik_scanner, kk_scanner, npwp_scanner, passport_scanner, driving_license, bpjs_scanner, identity_scanner

# Group B: Kontak
from .group_b_kontak import phone_scanner, email_scanner, address_scanner

# Group C: Media Sosial
from .group_c_media_sosial import social_scanners

# Group D: Dokumen Leak
from .group_d_dokumen_leak import doc_scanners

# Group E: Breach DB
from .group_e_breach_db import breach_scanners

# Group F: Platform
from .group_f_platform import platform_scanners

# Group G: Finansial
from .group_g_finansial import financial_scanners

# Group H: Pemerintahan
from .group_h_pemerintahan import gov_scanners

# Group I: Dark Web
from .group_i_dark_web import darkweb_scanners

# Group J: Lainnya
from .group_j_lainnya import misc_scanners
