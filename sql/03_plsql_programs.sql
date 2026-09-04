-- =====================================================================
-- Digital Public Grievance Redressal System
-- 03_plsql_programs.sql : Triggers, Functions, Procedures (Cursors)
-- Run after 01_schema.sql and 02_sample_data.sql
-- =====================================================================

SET SERVEROUTPUT ON;

-- =====================================================================
-- TRIGGER 1: Auto-close a complaint's status when a Closure row is
-- inserted for it.
-- =====================================================================
CREATE OR REPLACE TRIGGER trg_closure_updates_status
AFTER INSERT ON Closure
FOR EACH ROW
BEGIN
    UPDATE Complaint
    SET    Status = 'Closed'
    WHERE  Complaint_ID = :NEW.Complaint_ID;
END;
/

-- =====================================================================
-- TRIGGER 2: When a complaint is escalated, auto-raise its priority to
-- 'High' and mark status as 'Escalated'.
-- =====================================================================
CREATE OR REPLACE TRIGGER trg_escalation_raises_priority
AFTER INSERT ON Escalation
FOR EACH ROW
BEGIN
    UPDATE Complaint
    SET    Priority = 'High',
           Status   = 'Escalated'
    WHERE  Complaint_ID = :NEW.Complaint_ID
    AND    Status <> 'Closed';   -- don't reopen an already closed complaint
END;
/

-- =====================================================================
-- FUNCTION 1: Number of days a complaint has been open.
-- If closed, counts days between complaint date and closure date.
-- If still open, counts days between complaint date and today.
-- =====================================================================
CREATE OR REPLACE FUNCTION fn_days_open (
    p_complaint_id IN Complaint.Complaint_ID%TYPE
) RETURN NUMBER
IS
    v_complaint_date Complaint.Complaint_Date%TYPE;
    v_closure_date   Closure.Closure_Date%TYPE;
    v_days           NUMBER;
BEGIN
    SELECT Complaint_Date INTO v_complaint_date
    FROM   Complaint
    WHERE  Complaint_ID = p_complaint_id;

    BEGIN
        SELECT Closure_Date INTO v_closure_date
        FROM   Closure
        WHERE  Complaint_ID = p_complaint_id;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            v_closure_date := NULL;
    END;

    IF v_closure_date IS NOT NULL THEN
        v_days := v_closure_date - v_complaint_date;
    ELSE
        v_days := SYSDATE - v_complaint_date;
    END IF;

    RETURN v_days;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN -1; -- complaint not found
END fn_days_open;
/

-- =====================================================================
-- FUNCTION 2: Count of complaints handled by a given department.
-- =====================================================================
CREATE OR REPLACE FUNCTION fn_dept_complaint_count (
    p_department_id IN Department.DepartmentID%TYPE
) RETURN NUMBER
IS
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM   Complaint
    WHERE  DepartmentID = p_department_id;

    RETURN v_count;
END fn_dept_complaint_count;
/

-- =====================================================================
-- PROCEDURE 1: Auto-escalate complaints that have been open longer than
-- p_days and are not already Escalated or Closed. Uses an explicit
-- cursor to loop through qualifying complaints and inserts an
-- Escalation record for each (which in turn fires trg_escalation_raises_priority).
-- =====================================================================
CREATE OR REPLACE PROCEDURE prc_auto_escalate (
    p_days IN NUMBER DEFAULT 5
)
IS
    CURSOR c_pending IS
        SELECT c.Complaint_ID, c.Complaint_Title, d.Dept_Name, d.Contact_No
        FROM   Complaint c
        JOIN   Department d ON d.DepartmentID = c.DepartmentID
        WHERE  c.Status NOT IN ('Escalated', 'Closed')
        AND    (SYSDATE - c.Complaint_Date) > p_days;

    v_count NUMBER := 0;
BEGIN
    FOR rec IN c_pending LOOP
        INSERT INTO Escalation (Escalated_To, Escalation_Date, Reason, Complaint_ID)
        VALUES (rec.Dept_Name || ' Head Office',
                SYSDATE,
                'Auto-escalated: open for more than ' || p_days || ' days.',
                rec.Complaint_ID);

        v_count := v_count + 1;
        DBMS_OUTPUT.PUT_LINE('Escalated Complaint #' || rec.Complaint_ID ||
                              ' (' || rec.Complaint_Title || ') -> ' || rec.Dept_Name);
    END LOOP;

    IF v_count = 0 THEN
        DBMS_OUTPUT.PUT_LINE('No complaints required auto-escalation.');
    ELSE
        DBMS_OUTPUT.PUT_LINE(v_count || ' complaint(s) auto-escalated.');
    END IF;

    COMMIT;
END prc_auto_escalate;
/

-- =====================================================================
-- PROCEDURE 2: Print a status-wise complaint report for a department
-- using an explicit cursor.
-- =====================================================================
CREATE OR REPLACE PROCEDURE prc_department_report (
    p_department_id IN Department.DepartmentID%TYPE
)
IS
    CURSOR c_status_counts IS
        SELECT Status, COUNT(*) AS cnt
        FROM   Complaint
        WHERE  DepartmentID = p_department_id
        GROUP BY Status
        ORDER BY Status;

    v_dept_name Department.Dept_Name%TYPE;
    v_total     NUMBER;
BEGIN
    SELECT Dept_Name INTO v_dept_name
    FROM   Department
    WHERE  DepartmentID = p_department_id;

    v_total := fn_dept_complaint_count(p_department_id);

    DBMS_OUTPUT.PUT_LINE('===== Report for Department: ' || v_dept_name || ' =====');
    DBMS_OUTPUT.PUT_LINE('Total Complaints: ' || v_total);
    DBMS_OUTPUT.PUT_LINE('-----------------------------------------');

    FOR rec IN c_status_counts LOOP
        DBMS_OUTPUT.PUT_LINE(RPAD(rec.Status, 15) || ': ' || rec.cnt);
    END LOOP;

    DBMS_OUTPUT.PUT_LINE('=========================================');
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('No department found with ID ' || p_department_id);
END prc_department_report;
/

PROMPT ===== PL/SQL objects compiled successfully =====

-- =====================================================================
-- DEMO CALLS (uncomment / run individually to test in SQL*Plus)
-- =====================================================================
-- EXEC prc_department_report(1);
-- EXEC prc_auto_escalate(5);
-- SELECT fn_days_open(3) FROM DUAL;
-- SELECT fn_dept_complaint_count(2) FROM DUAL;
