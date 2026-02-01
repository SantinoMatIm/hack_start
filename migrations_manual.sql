-- Run in order. Check alembic_version first: SELECT * FROM alembic_version;


ALTER TABLE zones ADD COLUMN IF NOT EXISTS energy_price_usd_mwh FLOAT;
ALTER TABLE zones ADD COLUMN IF NOT EXISTS fuel_price_usd_mmbtu FLOAT;
ALTER TABLE zones ADD COLUMN IF NOT EXISTS currency VARCHAR(10) DEFAULT 'USD';
UPDATE alembic_version SET version_num='003' WHERE version_num='002';


ALTER TABLE zones ADD COLUMN IF NOT EXISTS country_code VARCHAR(3);
ALTER TABLE zones ADD COLUMN IF NOT EXISTS state_code VARCHAR(5);
UPDATE alembic_version SET version_num='004' WHERE version_num='003';
