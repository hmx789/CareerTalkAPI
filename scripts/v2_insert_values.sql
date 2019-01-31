INSERT INTO hiring_type (type)
VALUES ('INT');

INSERT INTO hiring_type (type)
VALUES ('FT');

INSERT INTO hiring_type (type)
VALUES ('INT, FT');

INSERT INTO degree_type (type)
VALUES ('BS');
INSERT INTO degree_type (type)
VALUES ('MS');
INSERT INTO degree_type (type)
VALUES ('PhD');
INSERT INTO degree_type (type)
VALUES ('BS, MS');
INSERT INTO degree_type (type)
VALUES ('BS, PhD');
INSERT INTO degree_type (type)
VALUES ('MS, PhD');

INSERT INTO visa_type (type)
VALUES ('yes');
INSERT INTO visa_type (type)
VALUES ('no');
INSERT INTO visa_type (type)
VALUES ('maybe');


INSERT INTO college (name, address, city, zipcode, website, state)
VALUES ('University of Illinois at Chicago', '1200 W Harrison St', 'Chicago', '60607', 'www.uic.edu', 'IL');


INSERT INTO user (first_name, last_name, personal_email)
VALUES ('Seho', 'Lim', 'seho@gmail.com');

INSERT INTO user (first_name, last_name, personal_email)
VALUES ('recruiter', 'Kim', 'recruiter1@gmail.com');

INSERT INTO connection (user_id, public_id, token, os)
VALUES(1, 'DFWERN15', 'WERQGFVADFGEWRY123124ADF', 'Android');

INSERT INTO connection (user_id, public_id, token, os)
VALUES(2, 'DFsadfWERN15', 'WERQqwerGwetvadfFVADFGEWRY123124ADF', 'iOS');


INSERT INTO student (college_id, looking_hiring_type, degree, graduating_date, available_date, school_email, user_id)
VALUES (1, 2, 1, '2019-05-23', '2019-06-01', 'slim@uic.edu', 1);

INSERT INTO recruiter (first_name, last_name, employer_id, work_email, work_phone)
VALUES ('Recruiter1', 'Gerlach', 2, 'work_email@gmail.com', '223-112-1942');

INSERT INTO careerfair (organization_id, name, date, start_time, end_time, location, address, city, zipcode)
VALUES (1, 'D-1 UIC Computer Science Career Fair', '2018-09-18', '2018-09-18 18:00:00', '2018-09-18 22:00:00', 'Isadore and Sadie Dorin Forum', '725 West Roosevelt Road', 'Chicago', '60608');

INSERT INTO careerfair (organization_id, name, date, start_time, end_time, location, address, city, zipcode)
VALUES (1, 'D-2 UIC Engineering Career Fair', '2018-09-19', '2018-09-19 18:00:00', '2018-09-19 22:00:00', 'Isadore and Sadie Dorin Forum', '725 West Roosevelt Road', 'Chicago', '60608');

INSERT INTO employer (name, found_year, hq_city, company_url)
VALUES ('Google', '1998', 'Menlo Park', 'google.com');

INSERT INTO employer (name, found_year, hq_city, company_url)
VALUES ('Apple', '1976', 'Cupertino', 'apple.com');

INSERT INTO employer (name, found_year, hq_city, company_url)
VALUES ('Facebook', '2004', 'Cambridge', 'facebook.com');

INSERT INTO employer (name, found_year, hq_city, company_url)
VALUES ('Microsoft', '1975', 'Albuquerque', 'microsoft.com');


INSERT INTO careerfair_employer
(employer_id, degree_type_id, hiring_type_id, visa_type_id, careerfair_id, recruiter_id, hiring_majors, tables)
VALUES (1, 7, 3, 1, 1, 1, 'CS, CSE', '21, 22');

INSERT INTO careerfair_employer
(employer_id, degree_type_id, hiring_type_id, visa_type_id, careerfair_id, recruiter_id, hiring_majors, tables)
VALUES (2, 6, 2, 2, 1, 1, 'CS, CSE', '10, 11, 12');

INSERT INTO careerfair_employer
(employer_id, degree_type_id, hiring_type_id, visa_type_id, careerfair_id, recruiter_id, hiring_majors, tables)
VALUES (1, 7, 1, 3, 2, 2, 'ECE, CSE', '30, 31');

INSERT INTO careerfair_employer
(employer_id, degree_type_id, hiring_type_id, visa_type_id, careerfair_id, recruiter_id, hiring_majors, tables)
VALUES (2, 7, 3, 1, 2, 2, 'ECE, CSE', '21');


