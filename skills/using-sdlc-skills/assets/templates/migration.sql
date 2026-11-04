-- ==============================================================================
-- Canonical Artifact Template: Database Migration DDL
-- Stage: 5. Implementation & Construction / 10. Maintenance & Evolution
-- Primary Owner Skill: database-design, deprecation-and-migration
-- Purpose: Safe, reversible, transactional SQL schema migration with expand/contract support.
-- Verification Gate: sqlfluff lint <path> (or target DB dry-run runner)
-- ==============================================================================

-- Migration Metadata:
-- Migration ID: 20261104_001_create_resources_table
-- Author: [AUTHOR_OR_ROLE]
-- Reversible: Yes
-- Expand/Contract Phase: Expand (Additive)

-- -----------------------------------------------------------------------------
-- UP MIGRATION (Apply Changes)
-- -----------------------------------------------------------------------------
BEGIN;

-- 1. Create Core Table
CREATE TABLE IF NOT EXISTS resources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'draft',
    schema_version INT NOT NULL DEFAULT 1,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. Indexes for Primary Query Patterns
CREATE INDEX IF NOT EXISTS idx_resources_tenant_status 
    ON resources (tenant_id, status);

CREATE INDEX IF NOT EXISTS idx_resources_metadata_gin 
    ON resources USING gin (metadata);

-- 3. Automatic updated_at Trigger Function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_resources_updated_at ON resources;
CREATE TRIGGER trg_resources_updated_at
    BEFORE UPDATE ON resources
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

COMMIT;

-- -----------------------------------------------------------------------------
-- DOWN MIGRATION (Rollback Changes)
-- To execute rollback: run commands below in a separate transaction block
-- -----------------------------------------------------------------------------
/*
BEGIN;

DROP TRIGGER IF EXISTS trg_resources_updated_at ON resources;
DROP FUNCTION IF EXISTS update_updated_at_column();
DROP TABLE IF EXISTS resources;

COMMIT;
*/
