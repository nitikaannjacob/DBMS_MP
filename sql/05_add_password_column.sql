-- =====================================================================
-- Digital Public Grievance Redressal System
-- 05_add_password_column.sql : Password setup for Citizen login
-- =====================================================================

SET SERVEROUTPUT ON;

-- =====================================================================
-- NOTE:
-- The PASSWORD column already exists in the current Citizen table.
-- Therefore, no ALTER TABLE command is required.
-- =====================================================================

-- ---------------------------------------------------------------------
-- Set the demo password for all existing sample citizens.
--
-- Plain-text password:
--     changeme123
--
-- SHA-256 hash:
--     494a715f7e9b4071aca61bac42ca858a309524e5864f0920030862a4ae7589be
-- ---------------------------------------------------------------------

UPDATE Citizen
SET Password =
    '494a715f7e9b4071aca61bac42ca858a309524e5864f0920030862a4ae7589be';

COMMIT;

PROMPT ===== Demo citizen passwords configured successfully =====
PROMPT ===== Demo password: changeme123 =====