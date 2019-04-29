CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

INSERT INTO hiring_type (type, uuid)
VALUES ('INT', uuid_generate_v4());

INSERT INTO hiring_type (type, uuid)
VALUES ('FT', uuid_generate_v4());

INSERT INTO hiring_type (type, uuid)
VALUES ('INT, FT', uuid_generate_v4());

INSERT INTO degree_type (type, uuid)
VALUES ('BS', uuid_generate_v4());
INSERT INTO degree_type (type, uuid)
VALUES ('MS', uuid_generate_v4());
INSERT INTO degree_type (type, uuid)
VALUES ('PhD', uuid_generate_v4());
INSERT INTO degree_type (type, uuid)
VALUES ('BS, MS', uuid_generate_v4());
INSERT INTO degree_type (type, uuid)
VALUES ('BS, PhD', uuid_generate_v4());
INSERT INTO degree_type (type, uuid)
VALUES ('MS, PhD', uuid_generate_v4());
INSERT INTO degree_type (type, uuid)
VALUES ('BS, MS, PhD', uuid_generate_v4());

INSERT INTO visa_type (type, uuid)
VALUES ('yes', uuid_generate_v4());
INSERT INTO visa_type (type, uuid)
VALUES ('no', uuid_generate_v4());
INSERT INTO visa_type (type, uuid)
VALUES ('maybe', uuid_generate_v4());

INSERT INTO college (name, address, city, zipcode, website, state, uuid)
VALUES ('University of Illinois at Chicago', '1200 W Harrison St', 'Chicago', '60607', 'www.uic.edu', 'IL', uuid_generate_v4());

INSERT INTO public.user (first_name, last_name, personal_email, uuid, profile_img, registered_on)
VALUES ('Seho', 'Lim', 'seho@gmail.com', uuid_generate_v4(), 'default_profile.png', now() at time zone 'utc');

INSERT INTO public.user (first_name, last_name, personal_email, uuid, profile_img, registered_on)
VALUES ('recruiter', 'Kim', 'recruiter1@gmail.com', uuid_generate_v4(), 'default_profile.png', now() at time zone 'utc');

INSERT INTO connection (user_id, public_id, token, os, uuid)
VALUES(1, 'DFWERN15', 'WERQGFVADFGEWRY123124ADF', 'Android', uuid_generate_v4());

INSERT INTO connection (user_id, public_id, token, os, uuid)
VALUES(2, 'DFsadfWERN15', 'WERQqwerGwetvadfFVADFGEWRY123124ADF', 'iOS', uuid_generate_v4());

INSERT INTO employer (name, found_year, hq_city, company_url, uuid, logo_url)
VALUES ('Google', '1998', 'Menlo Park', 'google.com', uuid_generate_v4(), 'default_employer.png');

INSERT INTO employer (name, found_year, hq_city, company_url, uuid, logo_url)
VALUES ('Apple', '1976', 'Cupertino', 'apple.com', uuid_generate_v4(), 'default_employer.png');

INSERT INTO employer (name, found_year, hq_city, company_url, uuid, logo_url)
VALUES ('Facebook', '2004', 'Cambridge', 'facebook.com', uuid_generate_v4(), 'default_employer.png');

INSERT INTO employer (name, found_year, hq_city, company_url, uuid, logo_url)
VALUES ('Microsoft', '1975', 'Albuquerque', 'microsoft.com', uuid_generate_v4(), 'default_employer.png');

INSERT INTO student (college_id, looking_hiring_type, degree, graduating_date, available_date, school_email, user_id, uuid)
VALUES (1, 2, 1, '2019-05-23', '2019-06-01', 'slim@uic.edu', 1, uuid_generate_v4());

INSERT INTO recruiter (first_name, last_name, employer_id, work_email, work_phone, uuid)
VALUES ('Recruiter1', 'Gerlach', 2, 'work_email@gmail.com', '223-112-1942', uuid_generate_v4());

INSERT INTO recruiter (first_name, last_name, employer_id, work_email, work_phone, uuid)
VALUES ('Recruiter2', 'Lim', 2, 'work_email2@gmail.com', '223-312-1342', uuid_generate_v4());

INSERT INTO careerfair (organization_id, name, date, start_time, end_time, location, address, city, zipcode, uuid)
VALUES (1, 'D-1 UIC Computer Science Career Fair', '2018-09-18', '2018-09-18 18:00:00', '2018-09-18 22:00:00', 'Isadore and Sadie Dorin Forum', '725 West Roosevelt Road', 'Chicago', '60608', uuid_generate_v4());

INSERT INTO careerfair (organization_id, name, date, start_time, end_time, location, address, city, zipcode, uuid)
VALUES (1, 'D-2 UIC Engineering Career Fair', '2018-09-19', '2018-09-19 18:00:00', '2018-09-19 22:00:00', 'Isadore and Sadie Dorin Forum', '725 West Roosevelt Road', 'Chicago', '60608', uuid_generate_v4());

INSERT INTO careerfair_employer
(employer_id, degree_type_id, hiring_type_id, visa_type_id, careerfair_id, recruiter_id, hiring_majors, tables, uuid)
VALUES (1, 7, 3, 1, 1, 1, 'CS, CSE', '21, 22', uuid_generate_v4());

INSERT INTO careerfair_employer
(employer_id, degree_type_id, hiring_type_id, visa_type_id, careerfair_id, recruiter_id, hiring_majors, tables, uuid)
VALUES (2, 6, 2, 2, 1, 1, 'CS, CSE', '10, 11, 12', uuid_generate_v4());

INSERT INTO careerfair_employer
(employer_id, degree_type_id, hiring_type_id, visa_type_id, careerfair_id, recruiter_id, hiring_majors, tables, uuid)
VALUES (1, 7, 1, 3, 2, 2, 'ECE, CSE', '30, 31', uuid_generate_v4());

INSERT INTO careerfair_employer
(employer_id, degree_type_id, hiring_type_id, visa_type_id, careerfair_id, recruiter_id, hiring_majors, tables, uuid)
VALUES (2, 7, 3, 1, 2, 2, 'ECE, CSE', '21', uuid_generate_v4());
