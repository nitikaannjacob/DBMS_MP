-- =====================================================================
-- Digital Public Grievance Redressal System
-- 01_schema.sql : DDL - Sequences, Tables, Constraints, Auto-ID Triggers
-- Run in SQL*Plus / Oracle as the target schema user
-- =====================================================================

SET SERVEROUTPUT ON;

-- ---------------------------------------------------------------------
-- Clean slate (ignore errors if objects don't exist yet)
-- ---------------------------------------------------------------------
DROP TABLE Closure CASCADE CONSTRAINTS PURGE;
DROP TABLE Escalation CASCADE CONSTRAINTS PURGE;
DROP TABLE Complaint CASCADE CONSTRAINTS PURGE;
DROP TABLE Department CASCADE CONSTRAINTS PURGE;
DROP TABLE Citizen CASCADE CONSTRAINTS PURGE;

DROP SEQUENCE seq_citizen;
DROP SEQUENCE seq_department;
DROP SEQUENCE seq_complaint;
DROP SEQUENCE seq_escalation;
DROP SEQUENCE seq_closure;

-- ---------------------------------------------------------------------
-- Sequences (used by BEFORE INSERT triggers below for auto-numbering)
-- ---------------------------------------------------------------------
CREATE SEQUENCE seq_citizen    START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_department START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_complaint  START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_escalation START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_closure    START WITH 1 INCREMENT BY 1;

-- ---------------------------------------------------------------------
-- Table: Citizen
-- ---------------------------------------------------------------------
CREATE TABLE Citizen (
    Citizen_ID    NUMBER(6)     PRIMARY KEY,
    First_Name    VARCHAR2(100) NOT NULL,
    Last_Name     VARCHAR2(100) NOT NULL,
    Phone_Number  VARCHAR2(15)  NOT NULL,
    Email         VARCHAR2(100) UNIQUE,
    Password      VARCHAR2(256),
    CONSTRAINT chk_citizen_phone_len
        CHECK (LENGTH(Phone_Number) >= 10)
);
-- ---------------------------------------------------------------------
-- Table: Department
-- ---------------------------------------------------------------------
CREATE TABLE Department (
    DepartmentID  NUMBER(4)     PRIMARY KEY,
    Dept_Name     VARCHAR2(100) NOT NULL UNIQUE,
    Contact_No    VARCHAR2(15)
);

-- ---------------------------------------------------------------------
-- Table: Complaint
-- ---------------------------------------------------------------------
CREATE TABLE Complaint (
    Complaint_ID       NUMBER(6)      PRIMARY KEY,
    Complaint_Title    VARCHAR2(150)  NOT NULL,
    Description        VARCHAR2(1000) NOT NULL,
    Complaint_Date     DATE           NOT NULL,
    Status             VARCHAR2(20)   NOT NULL,
    Priority           VARCHAR2(10)   NOT NULL,
    Citizen_ID         NUMBER(6)      NOT NULL,
    DepartmentID       NUMBER(4)      NOT NULL
);
-- ---------------------------------------------------------------------
-- Table: Escalation  (1:1 with Complaint -> Complaint_ID is UNIQUE)
-- ---------------------------------------------------------------------
CREATE TABLE Escalation (
    Escalation_ID    NUMBER(6)     PRIMARY KEY,
    Escalated_To     VARCHAR2(100) NOT NULL,
    Escalation_Date  DATE          DEFAULT SYSDATE,
    Reason           VARCHAR2(500),
    Complaint_ID     NUMBER(6)     NOT NULL UNIQUE,
    CONSTRAINT fk_escalation_complaint FOREIGN KEY (Complaint_ID) REFERENCES Complaint(Complaint_ID)
);

-- ---------------------------------------------------------------------
-- Table: Closure  (1:1 with Complaint -> Complaint_ID is UNIQUE)
-- ---------------------------------------------------------------------
CREATE TABLE Closure (
    Closure_ID    NUMBER(6)     PRIMARY KEY,
    Closure_Date  DATE          DEFAULT SYSDATE,
    Resolution    VARCHAR2(1000),
    Feedback      VARCHAR2(500),
    Complaint_ID  NUMBER(6)     NOT NULL UNIQUE,
    CONSTRAINT fk_closure_complaint FOREIGN KEY (Complaint_ID) REFERENCES Complaint(Complaint_ID)
);

-- ---------------------------------------------------------------------
-- Auto-increment triggers (BEFORE INSERT) — classic Oracle pattern
-- ---------------------------------------------------------------------
CREATE OR REPLACE TRIGGER trg_citizen_pk
BEFORE INSERT ON Citizen
FOR EACH ROW
WHEN (NEW.Citizen_ID IS NULL)
BEGIN
    :NEW.Citizen_ID := seq_citizen.NEXTVAL;
END;
/

CREATE OR REPLACE TRIGGER trg_department_pk
BEFORE INSERT ON Department
FOR EACH ROW
WHEN (NEW.DepartmentID IS NULL)
BEGIN
    :NEW.DepartmentID := seq_department.NEXTVAL;
END;
/

CREATE OR REPLACE TRIGGER trg_complaint_pk
BEFORE INSERT ON Complaint
FOR EACH ROW
WHEN (NEW.Complaint_ID IS NULL)
BEGIN
    :NEW.Complaint_ID := seq_complaint.NEXTVAL;
END;
/

CREATE OR REPLACE TRIGGER trg_escalation_pk
BEFORE INSERT ON Escalation
FOR EACH ROW
WHEN (NEW.Escalation_ID IS NULL)
BEGIN
    :NEW.Escalation_ID := seq_escalation.NEXTVAL;
END;
/

CREATE OR REPLACE TRIGGER trg_closure_pk
BEFORE INSERT ON Closure
FOR EACH ROW
WHEN (NEW.Closure_ID IS NULL)
BEGIN
    :NEW.Closure_ID := seq_closure.NEXTVAL;
END;
/

COMMIT;

PROMPT ===== Schema created successfully =====
