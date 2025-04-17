--
-- PostgreSQL database dump
--

-- Dumped from database version 14.17 (Homebrew)
-- Dumped by pg_dump version 14.17 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: applicationstatus; Type: TYPE; Schema: public; Owner: archana
--

CREATE TYPE public.applicationstatus AS ENUM (
    'APPLIED',
    'REVIEWING',
    'INTERVIEW',
    'OFFER',
    'REJECTED',
    'WITHDRAWN'
);


ALTER TYPE public.applicationstatus OWNER TO archana;

--
-- Name: experiencelevel; Type: TYPE; Schema: public; Owner: archana
--

CREATE TYPE public.experiencelevel AS ENUM (
    'ENTRY',
    'JUNIOR',
    'MID',
    'SENIOR',
    'LEAD',
    'EXECUTIVE'
);


ALTER TYPE public.experiencelevel OWNER TO archana;

--
-- Name: jobtype; Type: TYPE; Schema: public; Owner: archana
--

CREATE TYPE public.jobtype AS ENUM (
    'FULL_TIME',
    'PART_TIME',
    'CONTRACT',
    'FREELANCE',
    'INTERNSHIP'
);


ALTER TYPE public.jobtype OWNER TO archana;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: categories; Type: TABLE; Schema: public; Owner: archana
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description character varying(200),
    icon_class character varying(100),
    is_active boolean DEFAULT true
);


ALTER TABLE public.categories OWNER TO archana;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: archana
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.categories_id_seq OWNER TO archana;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: archana
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: companies; Type: TABLE; Schema: public; Owner: archana
--

CREATE TABLE public.companies (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    website character varying(200),
    logo_url character varying(255),
    location character varying(100),
    created_at timestamp without time zone,
    owner_id integer
);


ALTER TABLE public.companies OWNER TO archana;

--
-- Name: companies_id_seq; Type: SEQUENCE; Schema: public; Owner: archana
--

CREATE SEQUENCE public.companies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.companies_id_seq OWNER TO archana;

--
-- Name: companies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: archana
--

ALTER SEQUENCE public.companies_id_seq OWNED BY public.companies.id;


--
-- Name: job_applications; Type: TABLE; Schema: public; Owner: archana
--

CREATE TABLE public.job_applications (
    id integer NOT NULL,
    user_id integer NOT NULL,
    job_id integer NOT NULL,
    resume_url character varying(255),
    cover_letter text,
    status public.applicationstatus,
    applied_at timestamp without time zone,
    updated_at timestamp without time zone,
    is_withdraw boolean DEFAULT true
);


ALTER TABLE public.job_applications OWNER TO archana;

--
-- Name: job_applications_id_seq; Type: SEQUENCE; Schema: public; Owner: archana
--

CREATE SEQUENCE public.job_applications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.job_applications_id_seq OWNER TO archana;

--
-- Name: job_applications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: archana
--

ALTER SEQUENCE public.job_applications_id_seq OWNED BY public.job_applications.id;


--
-- Name: job_skills; Type: TABLE; Schema: public; Owner: archana
--

CREATE TABLE public.job_skills (
    job_id integer NOT NULL,
    skill_id integer NOT NULL,
    is_required boolean
);


ALTER TABLE public.job_skills OWNER TO archana;

--
-- Name: jobs; Type: TABLE; Schema: public; Owner: archana
--

CREATE TABLE public.jobs (
    id integer NOT NULL,
    title character varying(100) NOT NULL,
    description text NOT NULL,
    location character varying(100),
    salary_min integer,
    salary_max integer,
    job_type public.jobtype NOT NULL,
    experience_level public.experiencelevel,
    created_at timestamp without time zone,
    expires_at timestamp without time zone,
    is_active boolean,
    company_id integer NOT NULL,
    category_id integer NOT NULL,
    user_id integer NOT NULL,
    is_deleted boolean DEFAULT false NOT NULL
);


ALTER TABLE public.jobs OWNER TO archana;

--
-- Name: jobs_id_seq; Type: SEQUENCE; Schema: public; Owner: archana
--

CREATE SEQUENCE public.jobs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.jobs_id_seq OWNER TO archana;

--
-- Name: jobs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: archana
--

ALTER SEQUENCE public.jobs_id_seq OWNED BY public.jobs.id;


--
-- Name: skills; Type: TABLE; Schema: public; Owner: archana
--

CREATE TABLE public.skills (
    id integer NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.skills OWNER TO archana;

--
-- Name: skills_id_seq; Type: SEQUENCE; Schema: public; Owner: archana
--

CREATE SEQUENCE public.skills_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.skills_id_seq OWNER TO archana;

--
-- Name: skills_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: archana
--

ALTER SEQUENCE public.skills_id_seq OWNED BY public.skills.id;


--
-- Name: user_skills; Type: TABLE; Schema: public; Owner: archana
--

CREATE TABLE public.user_skills (
    user_id integer NOT NULL,
    skill_id integer NOT NULL
);


ALTER TABLE public.user_skills OWNER TO archana;

--
-- Name: users; Type: TABLE; Schema: public; Owner: archana
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(100),
    phone_number character varying(20),
    email character varying(120) NOT NULL,
    password_hash character varying(200) NOT NULL,
    created_at timestamp without time zone,
    otp character varying(6),
    otp_created_at timestamp without time zone,
    is_verified boolean,
    is_employer boolean,
    full_name character varying(100),
    bio text,
    resume_path character varying(255),
    role character varying(20) DEFAULT 'viewer'::character varying NOT NULL
);


ALTER TABLE public.users OWNER TO archana;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: archana
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO archana;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: archana
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: companies id; Type: DEFAULT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.companies ALTER COLUMN id SET DEFAULT nextval('public.companies_id_seq'::regclass);


--
-- Name: job_applications id; Type: DEFAULT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.job_applications ALTER COLUMN id SET DEFAULT nextval('public.job_applications_id_seq'::regclass);


--
-- Name: jobs id; Type: DEFAULT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.jobs ALTER COLUMN id SET DEFAULT nextval('public.jobs_id_seq'::regclass);


--
-- Name: skills id; Type: DEFAULT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.skills ALTER COLUMN id SET DEFAULT nextval('public.skills_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: archana
--

COPY public.categories (id, name, description, icon_class, is_active) FROM stdin;
3	Design	UI/UX and graphic design	fa-paint-brush	t
6	Sales	Sales and business development	fa-handshake	t
2	Marketing	Digital marketing and brand management	fa-bullhorn	t
4	Data Science	Data analysis and machine learning	fa-chart-bar	t
5	Product Management	Product strategy and development	fa-tasks	t
1	Software Development	Software engineering and development roles	fa-code	t
\.


--
-- Data for Name: companies; Type: TABLE DATA; Schema: public; Owner: archana
--

COPY public.companies (id, name, description, website, logo_url, location, created_at, owner_id) FROM stdin;
1	TechCorp Solutions	Leading software development company	https://www.techcorpsolutions.com	\N	\N	2025-04-14 04:24:39.549995	\N
2	BrandGrowth Inc	Digital marketing agency	https://www.brandgrowthinc.com	\N	\N	2025-04-14 04:24:39.552983	\N
3	DesignHub	Creative design studio	https://www.designhub.com	\N	\N	2025-04-14 04:24:39.553646	\N
4	DataMinds Analytics	Data science consulting firm	https://www.datamindsanalytics.com	\N	\N	2025-04-14 04:24:39.554253	\N
5	InnovatePro	Product development company	https://www.innovatepro.com	\N	\N	2025-04-14 04:24:39.55484	\N
6	CloudTech Systems	Cloud infrastructure provider	https://www.cloudtechsystems.com	\N	\N	2025-04-14 04:24:39.555671	\N
\.


--
-- Data for Name: job_applications; Type: TABLE DATA; Schema: public; Owner: archana
--

COPY public.job_applications (id, user_id, job_id, resume_url, cover_letter, status, applied_at, updated_at, is_withdraw) FROM stdin;
2	1	1	1_1_8836769472642184_25032025_P03222545255100_070451.pdf	test	APPLIED	2025-04-17 08:29:58.049539	2025-04-17 08:47:40.54894	t
1	1	6	1_6_8836769472642184_25032025_P03222545255100_070451.pdf		APPLIED	2025-04-15 07:20:25.310218	2025-04-17 08:47:43.634786	t
\.


--
-- Data for Name: job_skills; Type: TABLE DATA; Schema: public; Owner: archana
--

COPY public.job_skills (job_id, skill_id, is_required) FROM stdin;
\.


--
-- Data for Name: jobs; Type: TABLE DATA; Schema: public; Owner: archana
--

COPY public.jobs (id, title, description, location, salary_min, salary_max, job_type, experience_level, created_at, expires_at, is_active, company_id, category_id, user_id, is_deleted) FROM stdin;
1	Senior Software Engineer	Looking for an experienced software engineer to lead development projects.	San Francisco, CA	120000	180000	FULL_TIME	SENIOR	2025-04-08 09:54:39.557437	\N	t	1	1	1	f
2	Marketing Manager	Lead digital marketing campaigns and brand strategy.	New York, NY	80000	120000	FULL_TIME	MID	2025-04-08 09:54:39.563927	\N	t	2	2	1	f
3	UX/UI Designer	Create beautiful and intuitive user interfaces.	Remote	70000	100000	CONTRACT	MID	2025-04-08 09:54:39.565113	\N	t	3	3	1	f
4	Junior Data Scientist	Help analyze data and build machine learning models.	Boston, MA	70000	90000	FULL_TIME	ENTRY	2025-04-08 09:54:39.566183	\N	t	4	4	1	f
6	DevOps Engineer	Manage cloud infrastructure and CI/CD pipelines.	Seattle, WA	100000	150000	PART_TIME	MID	2025-04-08 09:54:39.569748	\N	t	6	1	1	f
5	Product Manager	Drive product strategy and development.	Austin, TX	110000	160000	FULL_TIME	SENIOR	2025-04-08 09:54:39.567228	\N	t	5	5	1	f
\.


--
-- Data for Name: skills; Type: TABLE DATA; Schema: public; Owner: archana
--

COPY public.skills (id, name) FROM stdin;
1	Python
2	Azure Data Factory
\.


--
-- Data for Name: user_skills; Type: TABLE DATA; Schema: public; Owner: archana
--

COPY public.user_skills (user_id, skill_id) FROM stdin;
1	1
1	2
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: archana
--

COPY public.users (id, username, phone_number, email, password_hash, created_at, otp, otp_created_at, is_verified, is_employer, full_name, bio, resume_path, role) FROM stdin;
1	\N	\N	shashidasari2000@gmail.com	scrypt:32768:8:1$orUV5CkDMZgdA1sC$89d7e68094887b44a6bfb04bef52024f2ce72b51118e7cae9453e6ebb474f8daefaeb4b4e55ab5748afba82732a4153bbfa4585cd9c4525eac71bd0dceab4a17	2025-04-11 15:36:38.356508	973683	2025-04-11 15:36:38.365054	f	f	SHASHIDAR S DASARI		1_pan_card_letter.pdf	admin
\.


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: archana
--

SELECT pg_catalog.setval('public.categories_id_seq', 6, true);


--
-- Name: companies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: archana
--

SELECT pg_catalog.setval('public.companies_id_seq', 6, true);


--
-- Name: job_applications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: archana
--

SELECT pg_catalog.setval('public.job_applications_id_seq', 2, true);


--
-- Name: jobs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: archana
--

SELECT pg_catalog.setval('public.jobs_id_seq', 6, true);


--
-- Name: skills_id_seq; Type: SEQUENCE SET; Schema: public; Owner: archana
--

SELECT pg_catalog.setval('public.skills_id_seq', 2, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: archana
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);


--
-- Name: categories categories_name_key; Type: CONSTRAINT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_name_key UNIQUE (name);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: companies companies_pkey; Type: CONSTRAINT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (id);


--
-- Name: job_applications job_applications_pkey; Type: CONSTRAINT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.job_applications
    ADD CONSTRAINT job_applications_pkey PRIMARY KEY (id);


--
-- Name: job_skills job_skills_pkey; Type: CONSTRAINT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.job_skills
    ADD CONSTRAINT job_skills_pkey PRIMARY KEY (job_id, skill_id);


--
-- Name: jobs jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_pkey PRIMARY KEY (id);


--
-- Name: skills skills_name_key; Type: CONSTRAINT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.skills
    ADD CONSTRAINT skills_name_key UNIQUE (name);


--
-- Name: skills skills_pkey; Type: CONSTRAINT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.skills
    ADD CONSTRAINT skills_pkey PRIMARY KEY (id);


--
-- Name: user_skills user_skills_pkey; Type: CONSTRAINT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.user_skills
    ADD CONSTRAINT user_skills_pkey PRIMARY KEY (user_id, skill_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_phone_number_key; Type: CONSTRAINT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_phone_number_key UNIQUE (phone_number);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: companies companies_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(id);


--
-- Name: job_applications job_applications_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.job_applications
    ADD CONSTRAINT job_applications_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(id);


--
-- Name: job_applications job_applications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.job_applications
    ADD CONSTRAINT job_applications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: job_skills job_skills_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.job_skills
    ADD CONSTRAINT job_skills_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(id);


--
-- Name: job_skills job_skills_skill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.job_skills
    ADD CONSTRAINT job_skills_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES public.skills(id);


--
-- Name: jobs jobs_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- Name: jobs jobs_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: jobs jobs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_skills user_skills_skill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.user_skills
    ADD CONSTRAINT user_skills_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES public.skills(id);


--
-- Name: user_skills user_skills_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: archana
--

ALTER TABLE ONLY public.user_skills
    ADD CONSTRAINT user_skills_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

