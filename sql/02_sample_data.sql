-- =====================================================================
-- Digital Public Grievance Redressal System
-- 02_sample_data.sql : Sample records
-- =====================================================================

SET DEFINE OFF;

-- =====================================================================
-- DEPARTMENT
-- =====================================================================

INSERT INTO Department (Dept_Name, Contact_No)
VALUES ('Water Supply', '9800000001');

INSERT INTO Department (Dept_Name, Contact_No)
VALUES ('Electricity', '9800000002');

INSERT INTO Department (Dept_Name, Contact_No)
VALUES ('Roads & Infrastructure', '9800000003');

INSERT INTO Department (Dept_Name, Contact_No)
VALUES ('Sanitation', '9800000004');

INSERT INTO Department (Dept_Name, Contact_No)
VALUES ('Public Health', '9800000005');

INSERT INTO Department (Dept_Name, Contact_No)
VALUES ('Education', '9800000006');

INSERT INTO Department (Dept_Name, Contact_No)
VALUES ('Police', '9800000007');

INSERT INTO Department (Dept_Name, Contact_No)
VALUES ('Public Transport', '9800000008');

INSERT INTO Department (Dept_Name, Contact_No)
VALUES ('Municipal Tax', '9800000009');

INSERT INTO Department (Dept_Name, Contact_No)
VALUES ('Parks & Recreation', '9800000010');


-- =====================================================================
-- CITIZEN
-- =====================================================================

INSERT INTO Citizen
    (First_Name, Last_Name, Phone_Number, Email, Password)
VALUES
    ('Arjun', 'Menon', '9847012345',
     'arjun.menon@example.com', 'changeme123');

INSERT INTO Citizen
    (First_Name, Last_Name, Phone_Number, Email, Password)
VALUES
    ('Divya', 'Nair', '9847012346',
     'divya.nair@example.com', 'changeme123');

INSERT INTO Citizen
    (First_Name, Last_Name, Phone_Number, Email, Password)
VALUES
    ('Rahul', 'Pillai', '9847012347',
     'rahul.pillai@example.com', 'changeme123');

INSERT INTO Citizen
    (First_Name, Last_Name, Phone_Number, Email, Password)
VALUES
    ('Sneha', 'Varma', '9847012348',
     'sneha.varma@example.com', 'changeme123');

INSERT INTO Citizen
    (First_Name, Last_Name, Phone_Number, Email, Password)
VALUES
    ('Kiran', 'Das', '9847012349',
     'kiran.das@example.com', 'changeme123');

INSERT INTO Citizen
    (First_Name, Last_Name, Phone_Number, Email, Password)
VALUES
    ('Anjali', 'Krishnan', '9847012350',
     'anjali.k@example.com', 'changeme123');

INSERT INTO Citizen
    (First_Name, Last_Name, Phone_Number, Email, Password)
VALUES
    ('Vishnu', 'Prasad', '9847012351',
     'vishnu.prasad@example.com', 'changeme123');

INSERT INTO Citizen
    (First_Name, Last_Name, Phone_Number, Email, Password)
VALUES
    ('Meera', 'Suresh', '9847012352',
     'meera.suresh@example.com', 'changeme123');

INSERT INTO Citizen
    (First_Name, Last_Name, Phone_Number, Email, Password)
VALUES
    ('Nikhil', 'Thomas', '9847012353',
     'nikhil.thomas@example.com', 'changeme123');

INSERT INTO Citizen
    (First_Name, Last_Name, Phone_Number, Email, Password)
VALUES
    ('Fathima', 'Rasheed', '9847012354',
     'fathima.rasheed@example.com', 'changeme123');

INSERT INTO Citizen
    (First_Name, Last_Name, Phone_Number, Email, Password)
VALUES
    ('Sanjay', 'Kumar', '9847012355',
     'sanjay.kumar@example.com', 'changeme123');

INSERT INTO Citizen
    (First_Name, Last_Name, Phone_Number, Email, Password)
VALUES
    ('Lakshmi', 'Iyer', '9847012356',
     'lakshmi.iyer@example.com', 'changeme123');


-- =====================================================================
-- COMPLAINT
-- =====================================================================

INSERT INTO Complaint
    (Complaint_Title, Complaint_Date, Status, Priority,
     Description, Citizen_ID, DepartmentID)
VALUES
    ('No water supply for 3 days',
     DATE '2026-08-20',
     'Closed',
     'High',
     'No piped water in Ward 4 since Monday.',
     1,
     1);

INSERT INTO Complaint
    (Complaint_Title, Complaint_Date, Status, Priority,
     Description, Citizen_ID, DepartmentID)
VALUES
    ('Frequent power outages',
     DATE '2026-08-22',
     'Escalated',
     'High',
     'Power cuts every evening for a week.',
     2,
     2);

INSERT INTO Complaint
    (Complaint_Title, Complaint_Date, Status, Priority,
     Description, Citizen_ID, DepartmentID)
VALUES
    ('Pothole causing accidents',
     DATE '2026-08-25',
     'In Progress',
     'High',
     'Large pothole near the bus stop on MG Road.',
     3,
     3);

INSERT INTO Complaint
    (Complaint_Title, Complaint_Date, Status, Priority,
     Description, Citizen_ID, DepartmentID)
VALUES
    ('Garbage not collected',
     DATE '2026-08-10',
     'Closed',
     'Medium',
     'Garbage piling up for over a week.',
     4,
     4);

INSERT INTO Complaint
    (Complaint_Title, Complaint_Date, Status, Priority,
     Description, Citizen_ID, DepartmentID)
VALUES
    ('Mosquito breeding in drain',
     DATE '2026-08-15',
     'Closed',
     'Medium',
     'Stagnant water breeding mosquitoes.',
     5,
     5);

INSERT INTO Complaint
    (Complaint_Title, Complaint_Date, Status, Priority,
     Description, Citizen_ID, DepartmentID)
VALUES
    ('School building leaking roof',
     DATE '2026-08-28',
     'Open',
     'Medium',
     'Classroom roof leaks during rain.',
     6,
     6);

INSERT INTO Complaint
    (Complaint_Title, Complaint_Date, Status, Priority,
     Description, Citizen_ID, DepartmentID)
VALUES
    ('Streetlight not working',
     DATE '2026-08-30',
     'Open',
     'Low',
     'Streetlight outside house #24 is off.',
     7,
     2);

INSERT INTO Complaint
    (Complaint_Title, Complaint_Date, Status, Priority,
     Description, Citizen_ID, DepartmentID)
VALUES
    ('Illegal parking blocking road',
     DATE '2026-08-18',
     'Escalated',
     'Medium',
     'Vehicles parked illegally block the lane daily.',
     8,
     7);

INSERT INTO Complaint
    (Complaint_Title, Complaint_Date, Status, Priority,
     Description, Citizen_ID, DepartmentID)
VALUES
    ('Bus service delays',
     DATE '2026-08-12',
     'Closed',
     'Low',
     'Route 14 buses consistently 30 min late.',
     9,
     8);

INSERT INTO Complaint
    (Complaint_Title, Complaint_Date, Status, Priority,
     Description, Citizen_ID, DepartmentID)
VALUES
    ('Incorrect property tax bill',
     DATE '2026-08-05',
     'Closed',
     'Medium',
     'Tax amount charged is higher than assessed.',
     10,
     9);

INSERT INTO Complaint
    (Complaint_Title, Complaint_Date, Status, Priority,
     Description, Citizen_ID, DepartmentID)
VALUES
    ('Park equipment damaged',
     DATE '2026-08-27',
     'Open',
     'Low',
     'Swing set broken in the community park.',
     11,
     10);

INSERT INTO Complaint
    (Complaint_Title, Complaint_Date, Status, Priority,
     Description, Citizen_ID, DepartmentID)
VALUES
    ('Water leakage flooding street',
     DATE '2026-08-29',
     'In Progress',
     'High',
     'Burst pipe flooding the main road.',
     12,
     1);

INSERT INTO Complaint
    (Complaint_Title, Complaint_Date, Status, Priority,
     Description, Citizen_ID, DepartmentID)
VALUES
    ('Transformer sparking',
     DATE '2026-08-31',
     'Escalated',
     'High',
     'Sparks seen from the transformer near school.',
     1,
     2);

INSERT INTO Complaint
    (Complaint_Title, Complaint_Date, Status, Priority,
     Description, Citizen_ID, DepartmentID)
VALUES
    ('Broken footpath tiles',
     DATE '2026-08-14',
     'Closed',
     'Low',
     'Loose tiles on the footpath, tripping hazard.',
     3,
     3);

INSERT INTO Complaint
    (Complaint_Title, Complaint_Date, Status, Priority,
     Description, Citizen_ID, DepartmentID)
VALUES
    ('Overflowing public toilet',
     DATE '2026-09-01',
     'Open',
     'Medium',
     'Public toilet near the market is overflowing.',
     5,
     4);


-- =====================================================================
-- ESCALATION
-- =====================================================================

INSERT INTO Escalation
    (Escalated_To, Escalation_Date, Reason, Complaint_ID)
VALUES
    ('District Electricity Officer',
     DATE '2026-08-27',
     'Not resolved within SLA of 3 days.',
     2);

INSERT INTO Escalation
    (Escalated_To, Escalation_Date, Reason, Complaint_ID)
VALUES
    ('Traffic Control Unit Head',
     DATE '2026-08-23',
     'Recurring complaint, no action taken.',
     8);

INSERT INTO Escalation
    (Escalated_To, Escalation_Date, Reason, Complaint_ID)
VALUES
    ('Chief Electrical Engineer',
     DATE '2026-09-01',
     'Safety hazard - urgent attention required.',
     13);

INSERT INTO Escalation
    (Escalated_To, Escalation_Date, Reason, Complaint_ID)
VALUES
    ('Municipal Commissioner',
     DATE '2026-08-30',
     'Pothole complaint pending over 5 days.',
     3);

INSERT INTO Escalation
    (Escalated_To, Escalation_Date, Reason, Complaint_ID)
VALUES
    ('Regional Water Board Head',
     DATE '2026-09-02',
     'Flooding risk to nearby homes.',
     12);


-- =====================================================================
-- CLOSURE
-- =====================================================================

INSERT INTO Closure
    (Closure_Date, Resolution, Feedback, Complaint_ID)
VALUES
    (DATE '2026-08-23',
     'Pipeline repaired and supply restored.',
     'Satisfied with quick response.',
     1);

INSERT INTO Closure
    (Closure_Date, Resolution, Feedback, Complaint_ID)
VALUES
    (DATE '2026-08-13',
     'Garbage cleared and collection schedule fixed.',
     'Good, but took a while.',
     4);

INSERT INTO Closure
    (Closure_Date, Resolution, Feedback, Complaint_ID)
VALUES
    (DATE '2026-08-18',
     'Drain cleaned and fogging done.',
     'Issue resolved satisfactorily.',
     5);

INSERT INTO Closure
    (Closure_Date, Resolution, Feedback, Complaint_ID)
VALUES
    (DATE '2026-08-15',
     'Additional bus deployed on route.',
     'Service has improved.',
     9);

INSERT INTO Closure
    (Closure_Date, Resolution, Feedback, Complaint_ID)
VALUES
    (DATE '2026-08-09',
     'Tax bill corrected and reissued.',
     'Thank you for the quick fix.',
     10);

INSERT INTO Closure
    (Closure_Date, Resolution, Feedback, Complaint_ID)
VALUES
    (DATE '2026-08-17',
     'Footpath tiles relaid.',
     'Looks good now.',
     14);

INSERT INTO Closure
    (Closure_Date, Resolution, Feedback, Complaint_ID)
VALUES
    (DATE '2026-08-24',
     'Illegal parking fine issued; signage added.',
     NULL,
     8);


-- =====================================================================
-- COMMIT
-- =====================================================================

COMMIT;

SET DEFINE ON;

PROMPT ===== Sample data inserted successfully =====