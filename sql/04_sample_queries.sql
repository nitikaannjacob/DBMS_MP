-- =====================================================================
-- Digital Public Grievance Redressal System
-- 04_sample_queries.sql : Demonstration SQL queries
-- =====================================================================

SET LINESIZE 150
SET PAGESIZE 50

-- 1. List all complaints with citizen name and department name (JOIN)
SELECT c.Complaint_ID, c.Complaint_Title, ci.Name AS Citizen, d.Dept_Name,
       c.Status, c.Priority, c.Complaint_Date
FROM   Complaint c
JOIN   Citizen ci ON ci.Citizen_ID = c.Citizen_ID
JOIN   Department d ON d.DepartmentID = c.DepartmentID
ORDER BY c.Complaint_Date;

-- 2. Count of complaints by status (Aggregation + GROUP BY)
SELECT Status, COUNT(*) AS Total
FROM   Complaint
GROUP BY Status
ORDER BY Total DESC;

-- 3. Count of complaints handled by each department (JOIN + GROUP BY)
SELECT d.Dept_Name, COUNT(c.Complaint_ID) AS Total_Complaints
FROM   Department d
LEFT JOIN Complaint c ON c.DepartmentID = d.DepartmentID
GROUP BY d.Dept_Name
ORDER BY Total_Complaints DESC;

-- 4. All escalated complaints with escalation details (JOIN)
SELECT c.Complaint_ID, c.Complaint_Title, e.Escalated_To, e.Escalation_Date, e.Reason
FROM   Complaint c
JOIN   Escalation e ON e.Complaint_ID = c.Complaint_ID
ORDER BY e.Escalation_Date;

-- 5. All closed complaints with resolution & feedback (JOIN)
SELECT c.Complaint_ID, c.Complaint_Title, cl.Closure_Date, cl.Resolution, cl.Feedback
FROM   Complaint c
JOIN   Closure cl ON cl.Complaint_ID = c.Complaint_ID
ORDER BY cl.Closure_Date;

-- 6. Citizens who have never submitted a complaint (Subquery / NOT IN)
SELECT Citizen_ID, Name
FROM   Citizen
WHERE  Citizen_ID NOT IN (SELECT Citizen_ID FROM Complaint);

-- 7. Complaints still open beyond 5 days (correlated with SYSDATE)
SELECT Complaint_ID, Complaint_Title, Complaint_Date,
       (SYSDATE - Complaint_Date) AS Days_Open, Status
FROM   Complaint
WHERE  Status NOT IN ('Closed')
AND    (SYSDATE - Complaint_Date) > 5
ORDER BY Days_Open DESC;

-- 8. Departments with more than 1 escalated complaint (JOIN + HAVING)
SELECT d.Dept_Name, COUNT(e.Escalation_ID) AS Escalation_Count
FROM   Department d
JOIN   Complaint c  ON c.DepartmentID = d.DepartmentID
JOIN   Escalation e ON e.Complaint_ID = c.Complaint_ID
GROUP BY d.Dept_Name
HAVING COUNT(e.Escalation_ID) > 1;

-- 9. High priority complaints that are NOT yet closed
SELECT Complaint_ID, Complaint_Title, Priority, Status, Complaint_Date
FROM   Complaint
WHERE  Priority = 'High'
AND    Status <> 'Closed'
ORDER BY Complaint_Date;

-- 10. View: a consolidated complaint status view for quick reporting
CREATE OR REPLACE VIEW vw_complaint_overview AS
SELECT c.Complaint_ID, c.Complaint_Title, ci.Name AS Citizen_Name,
       d.Dept_Name, c.Status, c.Priority, c.Complaint_Date,
       e.Escalated_To, cl.Closure_Date, cl.Resolution
FROM   Complaint c
JOIN   Citizen ci ON ci.Citizen_ID = c.Citizen_ID
JOIN   Department d ON d.DepartmentID = c.DepartmentID
LEFT JOIN Escalation e ON e.Complaint_ID = c.Complaint_ID
LEFT JOIN Closure cl   ON cl.Complaint_ID = c.Complaint_ID;

-- Usage:
-- SELECT * FROM vw_complaint_overview ORDER BY Complaint_ID;
