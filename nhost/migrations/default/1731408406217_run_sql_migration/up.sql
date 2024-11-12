--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2
-- Dumped by pg_dump version 16.2

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
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--



SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: assertions; Type: TABLE; Schema: public; Owner: nhost_hasura
--

CREATE TABLE public.assertions (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    text text,
    evidence_type text,
    is_fallacy boolean,
    source text,
    content_id uuid,
    date_created timestamp with time zone,
    date_last_modified timestamp with time zone,
    content_context text,
    citations jsonb,
    "timestamp" text,
    original_sentence text,
    standalone_assertion_reliability text,
    citation_content_id uuid,
    assertion_search_verify text,
    pro_evidence_aggregate_score numeric,
    against_evidence_aggregate_score numeric
);


ALTER TABLE public.assertions OWNER TO nhost_hasura;

--
-- Name: assertions_content; Type: TABLE; Schema: public; Owner: nhost_hasura
--

CREATE TABLE public.assertions_content (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    assertion_id uuid NOT NULL,
    content_id uuid NOT NULL,
    weight_conclusion numeric NOT NULL,
    date_created timestamp with time zone,
    date_last_modified timestamp with time zone,
    why_relevant text,
    why_not_relevant text,
    is_pro_content boolean,
    original_sentence text,
    video_timestamp text,
    assertion_context text
);


ALTER TABLE public.assertions_content OWNER TO nhost_hasura;

--
-- Name: content; Type: TABLE; Schema: public; Owner: nhost_hasura
--

CREATE TABLE public.content (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    content_type text,
    full_text text,
    source_url text,
    video_description text,
    video_transcript jsonb,
    date_added timestamp with time zone,
    date_last_modified timestamp with time zone,
    media_type text,
    is_parsed boolean,
    doi_number text,
    crossref_info jsonb,
    direct_download_url text,
    title text,
    summary text,
    video_id text,
    conclusion text,
    abstract text,
    science_paper_classification jsonb,
    error_message text,
    content_score numeric,
    pro_aggregate_content_score numeric,
    against_aggregate_content_score numeric
);


ALTER TABLE public.content OWNER TO nhost_hasura;

--
-- Name: content_relationship; Type: TABLE; Schema: public; Owner: nhost_hasura
--

CREATE TABLE public.content_relationship (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    child_content_id uuid,
    parent_content_id uuid,
    date_added timestamp with time zone,
    date_updated timestamp with time zone
);


ALTER TABLE public.content_relationship OWNER TO nhost_hasura;

--
-- Name: contents_assertion; Type: TABLE; Schema: public; Owner: nhost_hasura
--

CREATE TABLE public.contents_assertion (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    assertion_id uuid NOT NULL,
    content_id uuid NOT NULL,
    weight_conclusion numeric,
    date_created timestamp with time zone,
    date_last_modified timestamp with time zone,
    why_relevant text,
    why_not_relevant text,
    is_pro_assertion boolean DEFAULT true,
    is_citation_from_original_content boolean
);


ALTER TABLE public.contents_assertion OWNER TO nhost_hasura;

--
-- Name: contents_assertion assertion_citation_contents_pkey; Type: CONSTRAINT; Schema: public; Owner: nhost_hasura
--

ALTER TABLE ONLY public.contents_assertion
    ADD CONSTRAINT assertion_citation_contents_pkey PRIMARY KEY (id);


--
-- Name: assertions assertions_content_id_text_key; Type: CONSTRAINT; Schema: public; Owner: nhost_hasura
--

ALTER TABLE ONLY public.assertions
    ADD CONSTRAINT assertions_content_id_text_key UNIQUE (content_id, text);


--
-- Name: assertions_content assertions_content_pkey; Type: CONSTRAINT; Schema: public; Owner: nhost_hasura
--

ALTER TABLE ONLY public.assertions_content
    ADD CONSTRAINT assertions_content_pkey PRIMARY KEY (id);


--
-- Name: assertions assertions_pkey; Type: CONSTRAINT; Schema: public; Owner: nhost_hasura
--

ALTER TABLE ONLY public.assertions
    ADD CONSTRAINT assertions_pkey PRIMARY KEY (id);


--
-- Name: content content_pkey; Type: CONSTRAINT; Schema: public; Owner: nhost_hasura
--

ALTER TABLE ONLY public.content
    ADD CONSTRAINT content_pkey PRIMARY KEY (id);


--
-- Name: content_relationship content_relationship_child_content_id_parent_content_id_key; Type: CONSTRAINT; Schema: public; Owner: nhost_hasura
--

ALTER TABLE ONLY public.content_relationship
    ADD CONSTRAINT content_relationship_child_content_id_parent_content_id_key UNIQUE (child_content_id, parent_content_id);


--
-- Name: content_relationship content_relationship_pkey; Type: CONSTRAINT; Schema: public; Owner: nhost_hasura
--

ALTER TABLE ONLY public.content_relationship
    ADD CONSTRAINT content_relationship_pkey PRIMARY KEY (id);


--
-- Name: content content_source_url_key; Type: CONSTRAINT; Schema: public; Owner: nhost_hasura
--

ALTER TABLE ONLY public.content
    ADD CONSTRAINT content_source_url_key UNIQUE (source_url);




--
-- Name: contents_assertion assertion_citation_contents_assertion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nhost_hasura
--

ALTER TABLE ONLY public.contents_assertion
    ADD CONSTRAINT assertion_citation_contents_assertion_id_fkey FOREIGN KEY (assertion_id) REFERENCES public.assertions(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: contents_assertion assertion_citation_contents_content_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nhost_hasura
--

ALTER TABLE ONLY public.contents_assertion
    ADD CONSTRAINT assertion_citation_contents_content_id_fkey FOREIGN KEY (content_id) REFERENCES public.content(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: assertions assertions_citation_content_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nhost_hasura
--

ALTER TABLE ONLY public.assertions
    ADD CONSTRAINT assertions_citation_content_id_fkey FOREIGN KEY (citation_content_id) REFERENCES public.content(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: assertions_content assertions_content_assertion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nhost_hasura
--

ALTER TABLE ONLY public.assertions_content
    ADD CONSTRAINT assertions_content_assertion_id_fkey FOREIGN KEY (assertion_id) REFERENCES public.assertions(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: assertions_content assertions_content_content_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nhost_hasura
--

ALTER TABLE ONLY public.assertions_content
    ADD CONSTRAINT assertions_content_content_id_fkey FOREIGN KEY (content_id) REFERENCES public.content(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: assertions assertions_content_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nhost_hasura
--

ALTER TABLE ONLY public.assertions
    ADD CONSTRAINT assertions_content_id_fkey FOREIGN KEY (content_id) REFERENCES public.content(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: content_relationship content_relationship_parent_content_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nhost_hasura
--

ALTER TABLE ONLY public.content_relationship
    ADD CONSTRAINT content_relationship_parent_content_id_fkey FOREIGN KEY (parent_content_id) REFERENCES public.content(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: content_relationship content_relationship_referenced_by_content_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nhost_hasura
--

ALTER TABLE ONLY public.content_relationship
    ADD CONSTRAINT content_relationship_referenced_by_content_id_fkey FOREIGN KEY (child_content_id) REFERENCES public.content(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT USAGE ON SCHEMA public TO nhost_hasura;


--
-- PostgreSQL database dump complete
--;
