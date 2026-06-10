--
-- PostgreSQL database dump
--

\restrict 0f9NYv6aP2Ivm5x4KJMeX8Lnsnk7S8PJNqc00GWhfGDVt97BkDJGLOSBSdxmqLc

-- Dumped from database version 17.10
-- Dumped by pg_dump version 17.10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: images; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.images (
    id integer NOT NULL,
    filename character varying(100) NOT NULL,
    original_name character varying(100) NOT NULL,
    size integer NOT NULL,
    upload_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    file_type character varying(10) NOT NULL
);


ALTER TABLE public.images OWNER TO postgres;

--
-- Name: images_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.images_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.images_id_seq OWNER TO postgres;

--
-- Name: images_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.images_id_seq OWNED BY public.images.id;


--
-- Name: images id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.images ALTER COLUMN id SET DEFAULT nextval('public.images_id_seq'::regclass);


--
-- Data for Name: images; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.images (id, filename, original_name, size, upload_time, file_type) FROM stdin;
2	4cbddc6c2c9c4e839ab418da74624cb9.png	Снимок экрана 2026-05-21 204900.png	157276	2026-06-09 10:36:18.508686	png
3	279ae22379574213b352067351483962.png	Снимок экрана (6).png	430735	2026-06-09 10:36:29.262618	png
4	c76c864185a445f19d4d83ba2333fd2d.png	Снимок экрана 2026-05-22 213017.png	31584	2026-06-09 10:37:37.135589	png
5	902a8032c77141e7adb41e7888eb37f7.png	Снимок экрана 2026-05-23 180756.png	1926	2026-06-09 10:37:47.826736	png
6	b7cf17d1043149259289121f57476e94.png	Снимок экрана 2026-05-23 180822.png	63530	2026-06-09 10:37:56.615329	png
7	dd1378d70f824e61b3a76bd480d8d5f1.png	Снимок экрана 2026-05-22 213718.png	36038	2026-06-09 10:38:05.020663	png
8	1f742bf5d9644870b34bfb51418f5442.png	Снимок экрана 2026-05-24 123121.png	32688	2026-06-09 10:38:40.97909	png
9	e29e85c1120946b6962108a8e645b234.png	Снимок экрана 2026-05-24 124118.png	66253	2026-06-09 10:38:50.455196	png
10	9df888e7569145e791338ab04ee0a97f.png	Снимок экрана 2026-05-25 143549.png	56330	2026-06-09 10:39:01.956135	png
11	c6dee72265d44564ba40aba4e18fb300.png	Снимок экрана 2026-05-24 145607.png	113211	2026-06-09 10:39:35.779985	png
12	2c16f5875d934d8dbf73639eab6e3486.png	Снимок экрана 2026-05-23 180822.png	63530	2026-06-09 10:39:46.814867	png
13	70d80dbc4c3d456b8cc3f5ccbb125e0c.png	Снимок экрана (4).png	730156	2026-06-09 10:55:01.770724	png
\.


--
-- Name: images_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.images_id_seq', 13, true);


--
-- Name: images images_filename_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_filename_key UNIQUE (filename);


--
-- Name: images images_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

\unrestrict 0f9NYv6aP2Ivm5x4KJMeX8Lnsnk7S8PJNqc00GWhfGDVt97BkDJGLOSBSdxmqLc

