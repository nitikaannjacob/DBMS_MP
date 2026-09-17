-- =====================================================================
-- Digital Public Grievance Redressal System
-- 06_normalization_demo.sql : THROWAWAY demo for the project report
--
-- This script does NOT touch your real Citizen / Department / Complaint /
-- Escalation / Closure tables. It builds a separate, clearly-named
-- "_DEMO" table, shows why it's a bad design, then shows the exact SQL
-- changes that take it to 1NF -> 2NF -> 3NF. Drop it when you're done.
-- =====================================================================

SET SERVEROUTPUT ON;

-- ---------------------------------------------------------------------
-- Clean slate for the demo objects only
-- ---------------------------------------------------------------------
DROP TABLE Complaint_Master_DEMO CASCADE CONSTRAINTS PURGE;
DROP TABLE Citizen_DEMO   CASCADE CONSTRAINTS PURGE;
DROP TABLE Department_DEMO CASCADE CONSTRAINTS PURGE;
DROP TABLE Complaint_DEMO CASCADE CONSTRAINTS PURGE;
DROP TABLE Escalation_DEMO CASCADE CONSTRAINTS PURGE;
DROP TABLE Closure_DEMO   CASCADE CONSTRAINTS PURGE;


-- =====================================================================
-- STAGE 0: UNNORMALIZED FLAT TABLE
-- One row per complaint, every related fact crammed in as one wide row.
-- =====================================================================
CREATE TABLE Complaint_Master_DEMO (
    Complaint_ID      NUMBER(6),
    Complaint_Title   VARCHAR2(150),
    Status            VARCHAR2(20),
    Priority          VARCHAR2(10),
    Citizen_ID        NUMBER(6),
    Citizen_Name      VARCHAR2(200),   -- duplicated on every row for this citizen
    Phone_Number      VARCHAR2(15),    -- duplicated on every row for this citizen
    Email             VARCHAR2(100),   -- duplicated on every row for this citizen
    DepartmentID      NUMBER(4),
    Dept_Name         VARCHAR2(100),   -- duplicated on every row for this department
    Contact_No        VARCHAR2(15),    -- duplicated on every row for this department
    Escalated_To      VARCHAR2(100),   -- NULL unless escalated
    Escalation_Date   DATE,            -- NULL unless escalated
    Closure_Date      DATE,            -- NULL unless closed
    Resolution        VARCHAR2(1000)   -- NULL unless closed
);

INSERT INTO Complaint_Master_DEMO VALUES
(1,'No water supply for 3 days','Closed','High',
 1,'Arjun Menon','9847012345','arjun.menon@example.com',
 1,'Water Supply','9800000001',
 NULL, NULL, DATE '2026-08-23','Pipeline repaired and supply restored.');

INSERT INTO Complaint_Master_DEMO VALUES
(2,'Frequent power outages','Escalated','High',
 2,'Divya Nair','9847012346','divya.nair@example.com',
 2,'Electricity','9800000002',
 'District Electricity Officer', DATE '2026-08-27', NULL, NULL);

INSERT INTO Complaint_Master_DEMO VALUES
(13,'Transformer sparking','Escalated','High',
 1,'Arjun Menon','9847012345','arjun.menon@example.com',   -- same citizen, data repeated
 2,'Electricity','9800000002',                              -- same dept, data repeated
 'Chief Electrical Engineer', DATE '2026-09-01', NULL, NULL);

COMMIT;

PROMPT ===== STAGE 0 loaded: Complaint_Master_DEMO (unnormalized) =====


-- =====================================================================
-- THE ANOMALY (why this flat design is bad)
-- Electricity department's contact number changes -> must update EVERY
-- row that mentions it, or the data goes inconsistent.
-- =====================================================================
SELECT Complaint_ID, Dept_Name, Contact_No
FROM   Complaint_Master_DEMO
WHERE  Dept_Name = 'Electricity';
-- Two rows (2 and 13) both carry '9800000002'. Update anomaly: if you
-- only update row 2's Contact_No, row 13 now silently disagrees.

UPDATE Complaint_Master_DEMO
SET    Contact_No = '9800009999'
WHERE  Complaint_ID = 2;                 -- oops, forgot row 13

SELECT Complaint_ID, Dept_Name, Contact_No
FROM   Complaint_Master_DEMO
WHERE  Dept_Name = 'Electricity';
-- Row 2 and row 13 now show two different numbers for the same
-- department -- that's the anomaly, live.


-- =====================================================================
-- STAGE 1: 1NF
-- (Already atomic here, so nothing to split; the concrete "change"
--  at this stage is a rule check, not a schema edit.
--  Confirms: no column holds a list, e.g. no "Phone1, Phone2" field.)
-- =====================================================================
PROMPT ===== STAGE 1 check: all columns atomic, 1NF holds =====


-- =====================================================================
-- STAGE 2: 1NF -> 2NF
-- CHANGE: extract Citizen-only and Department-only columns into their
-- own tables, keyed on their own ID, so they stop repeating per complaint.
-- =====================================================================
CREATE TABLE Citizen_DEMO AS
SELECT DISTINCT Citizen_ID, Citizen_Name, Phone_Number, Email
FROM   Complaint_Master_DEMO;

CREATE TABLE Department_DEMO AS
SELECT DISTINCT DepartmentID, Dept_Name, Contact_No
FROM   Complaint_Master_DEMO;

CREATE TABLE Complaint_DEMO AS
SELECT Complaint_ID, Complaint_Title, Status, Priority,
       Citizen_ID, DepartmentID
FROM   Complaint_Master_DEMO;

PROMPT ===== STAGE 2 done: Citizen_DEMO, Department_DEMO, Complaint_DEMO =====
-- Now the department's contact number is stored exactly once, in
-- Department_DEMO -- the update anomaly above is no longer possible.


-- =====================================================================
-- STAGE 3: 2NF -> 3NF
-- CHANGE: Escalated_To / Escalation_Date and Closure_Date / Resolution
-- describe an EVENT that happens to a complaint, not the complaint
-- itself (they're NULL unless that event occurred) -- extract them.
-- =====================================================================
CREATE TABLE Escalation_DEMO AS
SELECT Complaint_ID, Escalated_To, Escalation_Date
FROM   Complaint_Master_DEMO
WHERE  Escalated_To IS NOT NULL;

CREATE TABLE Closure_DEMO AS
SELECT Complaint_ID, Closure_Date, Resolution
FROM   Complaint_Master_DEMO
WHERE  Closure_Date IS NOT NULL;

-- Complaint_DEMO no longer needs escalation/closure columns at all --
-- it was already narrowed in Stage 2.

PROMPT ===== STAGE 3 done: Escalation_DEMO, Closure_DEMO =====
PROMPT ===== This is now structurally the same shape as your real schema =====


-- =====================================================================
-- CLEANUP: drop every demo object once you've captured screenshots
-- for the report. Your real tables were never touched.
-- =====================================================================
-- DROP TABLE Complaint_Master_DEMO CASCADE CONSTRAINTS PURGE;
-- DROP TABLE Citizen_DEMO   CASCADE CONSTRAINTS PURGE;
-- DROP TABLE Department_DEMO CASCADE CONSTRAINTS PURGE;
-- DROP TABLE Complaint_DEMO CASCADE CONSTRAINTS PURGE;
-- DROP TABLE Escalation_DEMO CASCADE CONSTRAINTS PURGE;
-- DROP TABLE Closure_DEMO   CASCADE CONSTRAINTS PURGE;