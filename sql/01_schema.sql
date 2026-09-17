-- =====================================================================
-- Digital Public Grievance Redressal System
-- 01_schema.sql : DDL - Sequences, Tables, Constraints, Auto-ID
-- =====================================================================

SET SERVEROUTPUT ON;

-- Clean slate

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

-- Sequences

CREATE SEQUENCE seq_citizen
START WITH 1
INCREMENT BY 1;

CREATE SEQUENCE seq_department
START WITH 1
INCREMENT BY 1;

CREATE SEQUENCE seq_complaint
START WITH 1
INCREMENT BY 1;

CREATE SEQUENCE seq_escalation
START WITH 1
INCREMENT BY 1;

CREATE SEQUENCE seq_closure
START WITH 1
INCREMENT BY 1;

-- Citizen

CREATE TABLE Citizen (
Citizen_ID NUMBER(6) DEFAULT ON NULL seq_citizen.NEXTVAL PRIMARY KEY,
First_Name VARCHAR2(100) NOT NULL,
Last_Name VARCHAR2(100) NOT NULL,
Phone_Number VARCHAR2(15) NOT NULL,
Email VARCHAR2(100) UNIQUE,
Password VARCHAR2(256)
);

-- Department

CREATE TABLE Department (
DepartmentID NUMBER(4) DEFAULT ON NULL seq_department.NEXTVAL PRIMARY KEY,
Dept_Name VARCHAR2(100) NOT NULL UNIQUE,
Contact_No VARCHAR2(15)
);

-- Complaint

CREATE TABLE Complaint (
Complaint_ID NUMBER(6) DEFAULT ON NULL seq_complaint.NEXTVAL PRIMARY KEY,
Complaint_Title VARCHAR2(150) NOT NULL,
Description VARCHAR2(1000) NOT NULL,
Complaint_Date DATE NOT NULL,
Status VARCHAR2(20) NOT NULL,
Priority VARCHAR2(10) NOT NULL,
Citizen_ID NUMBER(6) NOT NULL,
DepartmentID NUMBER(4) NOT NULL
);

-- Escalation

CREATE TABLE Escalation (
Escalation_ID NUMBER(6) DEFAULT ON NULL seq_escalation.NEXTVAL PRIMARY KEY,
Escalated_To VARCHAR2(100) NOT NULL,
Escalation_Date DATE DEFAULT SYSDATE,
Reason VARCHAR2(500),
Complaint_ID NUMBER(6) NOT NULL
);

-- Closure

CREATE TABLE Closure (
Closure_ID NUMBER(6) DEFAULT ON NULL seq_closure.NEXTVAL PRIMARY KEY,
Closure_Date DATE DEFAULT SYSDATE,
Resolution VARCHAR2(1000),
Feedback VARCHAR2(500),
Complaint_ID NUMBER(6) NOT NULL
);

-- Citizen constraint

ALTER TABLE Citizen
ADD CONSTRAINT chk_citizen_phone_len
CHECK (LENGTH(Phone_Number) >= 10);

-- Complaint foreign keys

ALTER TABLE Complaint
ADD CONSTRAINT fk_complaint_citizen
FOREIGN KEY (Citizen_ID)
REFERENCES Citizen(Citizen_ID);

ALTER TABLE Complaint
ADD CONSTRAINT fk_complaint_department
FOREIGN KEY (DepartmentID)
REFERENCES Department(DepartmentID);

-- Escalation constraints

ALTER TABLE Escalation
ADD CONSTRAINT uq_escalation_complaint
UNIQUE (Complaint_ID);

ALTER TABLE Escalation
ADD CONSTRAINT fk_escalation_complaint
FOREIGN KEY (Complaint_ID)
REFERENCES Complaint(Complaint_ID);

-- Closure constraints

ALTER TABLE Closure
ADD CONSTRAINT uq_closure_complaint
UNIQUE (Complaint_ID);

ALTER TABLE Closure
ADD CONSTRAINT fk_closure_complaint
FOREIGN KEY (Complaint_ID)
REFERENCES Complaint(Complaint_ID);

-- Commit

COMMIT;

PROMPT ===== Schema created successfully =====