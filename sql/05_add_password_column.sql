-- =====================================================================
-- Digital Public Grievance Redressal System
-- 05_add_password_column.sql : Adds login support to Citizen
-- Run this once against your live schema (after 01-03).
-- =====================================================================

SET SERVEROUTPUT ON;

-- ---------------------------------------------------------------------
-- Add a Password column to store a SHA-256 hash (never plaintext).
-- Nullable so it doesn't break any existing rows; the app enforces it
-- as required for every NEW registration.
-- ---------------------------------------------------------------------
ALTER TABLE Citizen ADD Password VARCHAR2(256);

-- ---------------------------------------------------------------------
-- OPTIONAL: give every pre-existing sample citizen (IDs 1-12 from
-- 02_sample_data.sql) a demo password so you can log in and test right
-- away. This is the SHA-256 hash of the string:  changeme123
-- Tell any test users that password so they can log in, or just re-run
-- this after re-hashing a different demo password of your choice.
-- ---------------------------------------------------------------------
UPDATE Citizen
SET Password = '494a715f7e9b4071aca61bac42ca858a309524e5864f0920030862a4ae7589be'
WHERE Password IS NULL;

COMMIT;

PROMPT ===== Password column added; demo citizens can log in with "changeme123" =====
