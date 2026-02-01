#!/usr/bin/env python3
"""
Generate migration SQL for manual execution.

Use this when `alembic upgrade head` hangs (common with Supabase pooler).
Run the output in Supabase Dashboard > SQL Editor.

Usage:
  python scripts/run_migrations_manual.py

Then copy the SQL and run it in Supabase SQL Editor.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def main():
    print("Migration SQL for manual execution (no DB connection needed)\n")
    print("If 'alembic upgrade head' hangs, run this SQL in Supabase SQL Editor.\n")

    # Standalone SQL for manual execution
    print("=" * 60)
    print("STEP 1 - Run only if: SELECT version_num FROM alembic_version = '002'")
    print("MIGRATION 003 - Add energy price fields to zones")
    print("=" * 60)
    m003 = """
ALTER TABLE zones ADD COLUMN IF NOT EXISTS energy_price_usd_mwh FLOAT;
ALTER TABLE zones ADD COLUMN IF NOT EXISTS fuel_price_usd_mmbtu FLOAT;
ALTER TABLE zones ADD COLUMN IF NOT EXISTS currency VARCHAR(10) DEFAULT 'USD';
UPDATE alembic_version SET version_num='003' WHERE version_num='002';
"""
    print(m003)

    print("=" * 60)
    print("STEP 2 - Run only if: SELECT version_num FROM alembic_version = '003'")
    print("MIGRATION 004 - Add regional codes to zones")
    print("=" * 60)
    m004 = """
ALTER TABLE zones ADD COLUMN IF NOT EXISTS country_code VARCHAR(3);
ALTER TABLE zones ADD COLUMN IF NOT EXISTS state_code VARCHAR(5);
UPDATE alembic_version SET version_num='004' WHERE version_num='003';
"""
    print(m004)

    out_file = ROOT / "migrations_manual.sql"
    with open(out_file, "w") as f:
        f.write("-- Run in order. Check alembic_version first: SELECT * FROM alembic_version;\n\n")
        f.write(m003)
        f.write("\n")
        f.write(m004)
    print(f"\nSQL saved to: {out_file}")
    print("\n1. In Supabase: SQL Editor > New query")
    print("2. Paste and run each block (003 then 004)")
    print("3. Or use direct DB URL: postgresql://postgres:PASS@db.PROJECT.supabase.co:5432/postgres")


if __name__ == "__main__":
    main()
