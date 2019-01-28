DROP TABLE IF EXISTS public.careerfair
DROP TABLE IF EXISTS public.careerfair_table;
DROP TABLE IF EXISTS public.note_on_employer;
DROP TABLE IF EXISTS public.recruiter;
DROP TABLE IF EXISTS public.state;
DROP TABLE IF EXISTS public.college;
DROP TABLE IF EXISTS public.degree;
DROP TABLE IF EXISTS public.education;
DROP TABLE IF EXISTS public.top_five_employers;
DROP TABLE IF EXISTS public.student_like_employer;
DROP TABLE IF EXISTS public.employer_fair;
DROP TABLE IF EXISTS public.user;
DROP TABLE IF EXISTS public.connection


CREATE TABLE public.careerfair (
	id SERIAL PRIMARY KEY,
	organization_id INTEGER REFERENCES college(id),
	other_organization VARCHAR(50)
	name VARCHAR(100) NOT NULL,
	description VARCHAR,
	date timestamptz NOT NULL,
	start_time timestamptz NOT NULL,
	end_time timestamptz NOT NULL,
	location VARCHAR(100) NOT NULL,
	address VARCHAR(200),
	city VARCHAR(50),
	zipcode VARCHAR(5)
);

CREATE TABLE public.employer
(
	id SERIAL PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
	found_year VARCHAR(4),
	hq_city VARCHAR(50),
	description VARCHAR,
	logo_url VARCHAR DEFAULT 'default_employer.png',
	employer_url VARCHAR
);


CREATE TABLE public.careerfair_table
(
    id SERIAL PRIMARY KEY,
    employer_id integer NOT NULL REFERENCES employer,
    fair_id integer NOT NULL REFERENCES fair,
    table_number integer
);

CREATE TABLE public.note_on_employer
(
	id SERIAL PRIMARY KEY,
	employer_fair_id integer NOT NULL REFERENCES employer,
	student_id integer NOT NULL REFERENCES student,
	date timestamptz,
	tables text,
	content text
);

CREATE TABLE public.recruiter
(
	id SERIAL PRIMARY KEY,
	first_name VARCHAR(100) NOT NULL,
	last_name VARCHAR(100) NOT NULL,
	middle_name VARCHAR(100),
	employer_id INTEGER REFERENCES employer,
	work_email VARCHAR(255) NOT NULL,
	work_phone VARCHAR(16),
);


CREATE TABLE public.state
(
	id SERIAL PRIMARY KEY,
	state_code VARCHAR(2) NOT NULL,
	state_name VARCHAR(128) NOT NULL

);


CREATE TABLE public.college
(
	id SERIAL PRIMARY KEY,
	name VARCHAR(200) NOT NULL,
	state VARCHAR(2),
	city VARCHAR(100),
	zipcode VARCHAR(5),
	established DATE,
	address VARCHAR(255),
	website VARCHAR(255),
	logo_url VARCHAR(255) DEFAULT 'default_college.png'
);

CREATE TABLE public.degree
(
	id SERIAL PRIMARY KEY,
	name VARCHAR(10) NOT NULL

);

CREATE TABLE public.education
(
	id SERIAL PRIMARY KEY,
	school_id INTEGER NOT NULL REFERENCES college,
	student_id INTEGER NOT NULL REFERENCES student,
	major VARCHAR(255) NOT NULL,
	other VARCHAR(255)
);

CREATE TABLE public.top_five_employers
(
	id SERIAL PRIMARY KEY,
	top1 INTEGER NOT NULL REFERENCES employer,
	top2 INTEGER NOT NULL REFERENCES employer,
	top3 INTEGER NOT NULL REFERENCES employer,
	top4 INTEGER NOT NULL REFERENCES employer,
	top5 INTEGER NOT NULL REFERENCES employer,
	fair_id INTEGER NOT NULL REFERENCES fair,
	date DATE NOT NULL
);

CREATE TABLE public.student_like_employer
(
	id SERIAL PRIMARY KEY,
	student_id INTEGER NOT NULL REFERENCES student,
	employer_id INTEGER NOT NULL REFERENCES employer,
	fair_id INTEGER NOT NULL REFERENCES fair,
	date DATE NOT NULL
);

CREATE TABLE public.student
(
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES user,
    major VARCHAR(50),
    college_id INTEGER REFERENCES college,
    looking_hiring_type INTEGER REFERENCES hiring_type,
    highest_degree INTEGER REFERENCES degree_type,
    graduating_date DATE,
    available_date DATE,
    github_link VARCHAR(100),
    linkedin_link VARCHAR(100),
    portfolio_link VARCHAR,
    school_email VARCHAR(100)
);

CREATE TABLE employer_fair
(
	id SERIAL PRIMARY KEY,
	employer_id INTEGER NOT NULL REFERENCES employer,
	degree_req INTEGER NOT NULL REFERENCES degree_type,
	hiring_type INTEGER NOT NULL REFERENCES hiring_type,
	visa_type INTEGER NOT NULL REFERENCES visa_type,
	fair_id INTEGER NOT NULL REFERENCES fair,
	recruiter_id INTEGER REFERENCES recruiter,
	hiring_majors VARCHAR
);

CREATE TABLE public.user
(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    personal_email VARCHAR(255) UNIQUE,
    profile_img VARCHAR DEFAULT 'default_profile.png'
    registered_on timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE public.connection
(
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES public.user,
    public_id VARCHAR(255),
    access_token VARCHAR(255),
    id_token VARCHAR(255)
    secret VARCHAR(255),
    token VARCHAR,
    os VARCHAR(10),
);