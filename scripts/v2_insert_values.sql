CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

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
INSERT INTO degree_type (type)
VALUES ('BS, MS, PhD');

INSERT INTO visa_type (type)
VALUES ('yes');
INSERT INTO visa_type (type)
VALUES ('no');
INSERT INTO visa_type (type)
VALUES ('maybe');

INSERT INTO college (id, name, address, city, zipcode, website, state)
VALUES (uuid_generate_v4(), 'University of Illinois at Chicago', '1200 W Harrison St', 'Chicago', '60607', 'www.uic.edu', 'IL');

INSERT INTO careerfair(
	id, organization_id, name, description, date, start_time, end_time, location, address, city, zipcode)
	VALUES (
	uuid_generate_v4(),
	(select id from college where city = 'Chicago' limit 1),
	'test careerfair',
	'test careerfair description',
	now(),
	now(),
	now(),
	'test location',
	'test address',
	'test city',
	'123');

INSERT INTO public.user (id, first_name, last_name, personal_email, profile_img, registered_on)
VALUES (uuid_generate_v4(), 'Seho', 'Lim', 'seho@gmail.com', 'default_profile.png', now() at time zone 'utc');

INSERT INTO connection (id, user_id, public_id, token, os)
VALUES(uuid_generate_v4(), (select id from public.user where first_name = 'Seho'), 'DFWERN15', 'WERQGFVADFGEWRY123124ADF', 'Android');

INSERT INTO public.user (id, first_name, last_name, personal_email, profile_img, registered_on)
VALUES (uuid_generate_v4(), 'recruiter', 'Kim', 'recruiter1@gmail.com', 'default_profile.png', now() at time zone 'utc');

INSERT INTO connection (id, user_id, public_id, token, os)
VALUES(uuid_generate_v4(), (select id from public.user where first_name = 'recruiter'), 'DFsadfWERN15', 'WERQqwerGwetvadfFVADFGEWRY123124ADF', 'iOS');

INSERT INTO employer (id, name, found_year, hq_city, company_url, logo_url)
VALUES (uuid_generate_v4(), 'Google', '1998', 'Menlo Park', 'google.com', 'default_employer.png');

INSERT INTO employer (id, name, found_year, hq_city, company_url, logo_url)
VALUES (uuid_generate_v4(), 'Apple', '1976', 'Cupertino', 'apple.com', 'default_employer.png');

INSERT INTO employer (id, name, found_year, hq_city, company_url, logo_url)
VALUES (uuid_generate_v4(), 'Facebook', '2004', 'Cambridge', 'facebook.com', 'default_employer.png');

INSERT INTO employer (id, name, found_year, hq_city, company_url, logo_url)
VALUES (uuid_generate_v4(), 'Microsoft', '1975', 'Albuquerque', 'microsoft.com', 'default_employer.png');

INSERT INTO student (id, college_id, looking_hiring_type, degree, graduating_date, available_date, school_email, user_id)
VALUES (
    uuid_generate_v4(),
    (select id from college where city = 'Chicago' limit 1),
    (select id from hiring_type where type = 'INT, FT' limit 1),
    (select id from degree_type where type = 'MS' limit 1),
    '2019-05-23',
    '2019-06-01',
    'slim@uic.edu',
    (select id from public.user where first_name= 'Seho')
    );

