"""Central configuration read from the environment. Owner: Person A.

All auth/DB settings live here so they are loaded once and shared. .env is loaded in
main.py (and seed.py) before this module's values are used.
"""
import os

# --- Auth / JWT -------------------------------------------------------------------
JWT_SECRET = os.getenv("JWT_SECRET", "dev-insecure-change-me")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "720"))  # 12h

# --- Database ---------------------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./govpath.db")

# --- Bootstrap Super-Admin (created on startup if absent) -------------------------
SUPERADMIN_NIC = os.getenv("SUPERADMIN_NIC", "199000000000")
SUPERADMIN_PASSWORD = os.getenv("SUPERADMIN_PASSWORD", "changeme123")
SUPERADMIN_NAME = os.getenv("SUPERADMIN_NAME", "System Administrator")
