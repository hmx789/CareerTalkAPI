CREATE TABLE public.careerfair_table
(
    id SERIAL,
    company_id integer REFERENCES company,
    fair_id integer REFERENCES fair,
    table_number integer
);
