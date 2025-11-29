--
-- PostgreSQL database dump
--

\restrict JBLryXC2MHN687PUFsZFlfel8pUo74RYGX5bdZ75igf074fgSAWI98whNfzBbri

-- Dumped from database version 16.10 (Ubuntu 16.10-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.10 (Ubuntu 16.10-0ubuntu0.24.04.1)

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

ALTER TABLE IF EXISTS ONLY public.website_servicepage DROP CONSTRAINT IF EXISTS website_servicepage_seo_block_id_2d51e33f_fk_website_s;
ALTER TABLE IF EXISTS ONLY public.website_serviceblock DROP CONSTRAINT IF EXISTS website_serviceblock_service_page_id_7c804e96_fk_website_s;
ALTER TABLE IF EXISTS ONLY public.website_mainpage DROP CONSTRAINT IF EXISTS website_mainpage_seo_block_id_34fd0e90_fk_website_seoblock_id;
ALTER TABLE IF EXISTS ONLY public.website_mainpage DROP CONSTRAINT IF EXISTS website_mainpage_gallery_id_3719118e_fk_website_gallery_id;
ALTER TABLE IF EXISTS ONLY public.website_mainblock DROP CONSTRAINT IF EXISTS website_mainblock_main_page_id_0e298da7_fk_website_mainpage_id;
ALTER TABLE IF EXISTS ONLY public.website_image DROP CONSTRAINT IF EXISTS website_image_gallery_id_91dc697f_fk_website_gallery_id;
ALTER TABLE IF EXISTS ONLY public.website_contactpage DROP CONSTRAINT IF EXISTS website_contactpage_seo_block_id_04e9db16_fk_website_s;
ALTER TABLE IF EXISTS ONLY public.website_aboutuspage DROP CONSTRAINT IF EXISTS website_aboutuspage_seo_block_id_bdbc184e_fk_website_s;
ALTER TABLE IF EXISTS ONLY public.website_aboutuspage DROP CONSTRAINT IF EXISTS website_aboutuspage_gallery2_id_e27f968c_fk_website_gallery_id;
ALTER TABLE IF EXISTS ONLY public.website_aboutuspage DROP CONSTRAINT IF EXISTS website_aboutuspage_gallery1_id_233a01d1_fk_website_gallery_id;
ALTER TABLE IF EXISTS ONLY public.users_user_user_permissions DROP CONSTRAINT IF EXISTS users_user_user_permissions_user_id_20aca447_fk_users_user_id;
ALTER TABLE IF EXISTS ONLY public.users_user_user_permissions DROP CONSTRAINT IF EXISTS users_user_user_perm_permission_id_0b93982e_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.users_user DROP CONSTRAINT IF EXISTS users_user_role_id_854f2687_fk_users_role_id;
ALTER TABLE IF EXISTS ONLY public.users_user_groups DROP CONSTRAINT IF EXISTS users_user_groups_user_id_5f6f5a90_fk_users_user_id;
ALTER TABLE IF EXISTS ONLY public.users_user_groups DROP CONSTRAINT IF EXISTS users_user_groups_group_id_9afc8d0e_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.users_ticket DROP CONSTRAINT IF EXISTS users_ticket_user_id_50aca908_fk_users_user_id;
ALTER TABLE IF EXISTS ONLY public.users_ticket DROP CONSTRAINT IF EXISTS users_ticket_role_id_e89e09d1_fk_users_role_id;
ALTER TABLE IF EXISTS ONLY public.users_ticket DROP CONSTRAINT IF EXISTS users_ticket_master_id_04be4ae4_fk_users_user_id;
ALTER TABLE IF EXISTS ONLY public.users_ticket DROP CONSTRAINT IF EXISTS users_ticket_apartment_id_ca19f243_fk_building_apartment_id;
ALTER TABLE IF EXISTS ONLY public.users_messagerecipient DROP CONSTRAINT IF EXISTS users_messagerecipient_user_id_e1db9bc9_fk_users_user_id;
ALTER TABLE IF EXISTS ONLY public.users_messagerecipient DROP CONSTRAINT IF EXISTS users_messagerecipient_message_id_98132c5f_fk_users_message_id;
ALTER TABLE IF EXISTS ONLY public.users_message DROP CONSTRAINT IF EXISTS users_message_sender_id_d1e3d44e_fk_users_user_id;
ALTER TABLE IF EXISTS ONLY public.finance_tariffservice DROP CONSTRAINT IF EXISTS finance_tariffservice_tariff_id_6f2b7432_fk_finance_tariff_id;
ALTER TABLE IF EXISTS ONLY public.finance_tariffservice DROP CONSTRAINT IF EXISTS finance_tariffservice_service_id_bd302fc4_fk_finance_service_id;
ALTER TABLE IF EXISTS ONLY public.finance_tariffservice DROP CONSTRAINT IF EXISTS finance_tariffservic_currency_id_9311c6b8_fk_finance_c;
ALTER TABLE IF EXISTS ONLY public.finance_service DROP CONSTRAINT IF EXISTS finance_service_unit_id_184196ca_fk_finance_unit_id;
ALTER TABLE IF EXISTS ONLY public.finance_receiptitem DROP CONSTRAINT IF EXISTS finance_receiptitem_service_id_8491373a_fk_finance_service_id;
ALTER TABLE IF EXISTS ONLY public.finance_receiptitem DROP CONSTRAINT IF EXISTS finance_receiptitem_receipt_id_aba49f36_fk_finance_receipt_id;
ALTER TABLE IF EXISTS ONLY public.finance_receipt DROP CONSTRAINT IF EXISTS finance_receipt_tariff_id_65d84927_fk_finance_tariff_id;
ALTER TABLE IF EXISTS ONLY public.finance_receipt DROP CONSTRAINT IF EXISTS finance_receipt_apartment_id_40aba459_fk_building_apartment_id;
ALTER TABLE IF EXISTS ONLY public.finance_counterreading DROP CONSTRAINT IF EXISTS finance_counterreadi_counter_id_934b9b88_fk_finance_c;
ALTER TABLE IF EXISTS ONLY public.finance_counter DROP CONSTRAINT IF EXISTS finance_counter_service_id_c7d84c00_fk_finance_service_id;
ALTER TABLE IF EXISTS ONLY public.finance_counter DROP CONSTRAINT IF EXISTS finance_counter_apartment_id_43501d44_fk_building_apartment_id;
ALTER TABLE IF EXISTS ONLY public.finance_cashbox DROP CONSTRAINT IF EXISTS finance_cashbox_receipt_id_443b2685_fk_finance_receipt_id;
ALTER TABLE IF EXISTS ONLY public.finance_cashbox DROP CONSTRAINT IF EXISTS finance_cashbox_personal_account_id_0488b286_fk_building_;
ALTER TABLE IF EXISTS ONLY public.finance_cashbox DROP CONSTRAINT IF EXISTS finance_cashbox_manager_id_67d9219a_fk_users_user_id;
ALTER TABLE IF EXISTS ONLY public.finance_cashbox DROP CONSTRAINT IF EXISTS finance_cashbox_article_id_2e15dc33_fk_finance_article_id;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_user_id_c564eba6_fk_users_user_id;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_content_type_id_c4bce8eb_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.building_section DROP CONSTRAINT IF EXISTS building_section_house_id_f9f4e052_fk_building_house_id;
ALTER TABLE IF EXISTS ONLY public.building_housestaff DROP CONSTRAINT IF EXISTS building_housestaff_user_id_02c2ed2e_fk_users_user_id;
ALTER TABLE IF EXISTS ONLY public.building_housestaff DROP CONSTRAINT IF EXISTS building_housestaff_house_id_53aa17fe_fk_building_house_id;
ALTER TABLE IF EXISTS ONLY public.building_floor DROP CONSTRAINT IF EXISTS building_floor_house_id_e77b8ffa_fk_building_house_id;
ALTER TABLE IF EXISTS ONLY public.building_apartment DROP CONSTRAINT IF EXISTS building_apartment_tariff_id_69fa4c41_fk_finance_tariff_id;
ALTER TABLE IF EXISTS ONLY public.building_apartment DROP CONSTRAINT IF EXISTS building_apartment_section_id_614a9436_fk_building_section_id;
ALTER TABLE IF EXISTS ONLY public.building_apartment DROP CONSTRAINT IF EXISTS building_apartment_personal_account_id_7c217087_fk_building_;
ALTER TABLE IF EXISTS ONLY public.building_apartment DROP CONSTRAINT IF EXISTS building_apartment_owner_id_d23a066e_fk_users_user_id;
ALTER TABLE IF EXISTS ONLY public.building_apartment DROP CONSTRAINT IF EXISTS building_apartment_house_id_9fe67ca5_fk_building_house_id;
ALTER TABLE IF EXISTS ONLY public.building_apartment DROP CONSTRAINT IF EXISTS building_apartment_floor_id_baa4625c_fk_building_floor_id;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
DROP INDEX IF EXISTS public.website_serviceblock_service_page_id_7c804e96;
DROP INDEX IF EXISTS public.website_mainblock_main_page_id_0e298da7;
DROP INDEX IF EXISTS public.website_image_gallery_id_91dc697f;
DROP INDEX IF EXISTS public.users_user_username_06e46fe6_like;
DROP INDEX IF EXISTS public.users_user_user_permissions_user_id_20aca447;
DROP INDEX IF EXISTS public.users_user_user_permissions_permission_id_0b93982e;
DROP INDEX IF EXISTS public.users_user_user_id_4120b7b9_like;
DROP INDEX IF EXISTS public.users_user_role_id_854f2687;
DROP INDEX IF EXISTS public.users_user_groups_user_id_5f6f5a90;
DROP INDEX IF EXISTS public.users_user_groups_group_id_9afc8d0e;
DROP INDEX IF EXISTS public.users_ticket_user_id_50aca908;
DROP INDEX IF EXISTS public.users_ticket_role_id_e89e09d1;
DROP INDEX IF EXISTS public.users_ticket_master_id_04be4ae4;
DROP INDEX IF EXISTS public.users_ticket_apartment_id_ca19f243;
DROP INDEX IF EXISTS public.users_role_name_86bbd537_like;
DROP INDEX IF EXISTS public.users_messagerecipient_user_id_e1db9bc9;
DROP INDEX IF EXISTS public.users_messagerecipient_message_id_98132c5f;
DROP INDEX IF EXISTS public.users_message_sender_id_d1e3d44e;
DROP INDEX IF EXISTS public.finance_unit_name_bc741357_like;
DROP INDEX IF EXISTS public.finance_tariffservice_tariff_id_6f2b7432;
DROP INDEX IF EXISTS public.finance_tariffservice_service_id_bd302fc4;
DROP INDEX IF EXISTS public.finance_tariffservice_currency_id_9311c6b8;
DROP INDEX IF EXISTS public.finance_service_unit_id_184196ca;
DROP INDEX IF EXISTS public.finance_service_name_bd3324db_like;
DROP INDEX IF EXISTS public.finance_receiptitem_service_id_8491373a;
DROP INDEX IF EXISTS public.finance_receiptitem_receipt_id_aba49f36;
DROP INDEX IF EXISTS public.finance_receipt_tariff_id_65d84927;
DROP INDEX IF EXISTS public.finance_receipt_number_a405a4aa_like;
DROP INDEX IF EXISTS public.finance_receipt_apartment_id_40aba459;
DROP INDEX IF EXISTS public.finance_currency_name_24513ba4_like;
DROP INDEX IF EXISTS public.finance_counterreading_number_6b1ff325_like;
DROP INDEX IF EXISTS public.finance_counterreading_counter_id_934b9b88;
DROP INDEX IF EXISTS public.finance_counter_service_id_c7d84c00;
DROP INDEX IF EXISTS public.finance_counter_serial_number_11126ce8_like;
DROP INDEX IF EXISTS public.finance_counter_apartment_id_43501d44;
DROP INDEX IF EXISTS public.finance_cashbox_receipt_id_443b2685;
DROP INDEX IF EXISTS public.finance_cashbox_personal_account_id_0488b286;
DROP INDEX IF EXISTS public.finance_cashbox_number_b310d11d_like;
DROP INDEX IF EXISTS public.finance_cashbox_manager_id_67d9219a;
DROP INDEX IF EXISTS public.finance_cashbox_article_id_2e15dc33;
DROP INDEX IF EXISTS public.django_session_session_key_c0390e0f_like;
DROP INDEX IF EXISTS public.django_session_expire_date_a5c62663;
DROP INDEX IF EXISTS public.django_admin_log_user_id_c564eba6;
DROP INDEX IF EXISTS public.django_admin_log_content_type_id_c4bce8eb;
DROP INDEX IF EXISTS public.captcha_captchastore_hashkey_cbe8d15a_like;
DROP INDEX IF EXISTS public.building_section_house_id_f9f4e052;
DROP INDEX IF EXISTS public.building_personalaccount_number_0a041963_like;
DROP INDEX IF EXISTS public.building_housestaff_user_id_02c2ed2e;
DROP INDEX IF EXISTS public.building_housestaff_house_id_53aa17fe;
DROP INDEX IF EXISTS public.building_floor_house_id_e77b8ffa;
DROP INDEX IF EXISTS public.building_apartment_tariff_id_69fa4c41;
DROP INDEX IF EXISTS public.building_apartment_section_id_614a9436;
DROP INDEX IF EXISTS public.building_apartment_owner_id_d23a066e;
DROP INDEX IF EXISTS public.building_apartment_house_id_9fe67ca5;
DROP INDEX IF EXISTS public.building_apartment_floor_id_baa4625c;
DROP INDEX IF EXISTS public.auth_permission_content_type_id_2f476e4b;
DROP INDEX IF EXISTS public.auth_group_permissions_permission_id_84c5c92e;
DROP INDEX IF EXISTS public.auth_group_permissions_group_id_b120cbf9;
DROP INDEX IF EXISTS public.auth_group_name_a6ea08ec_like;
ALTER TABLE IF EXISTS ONLY public.website_servicepage DROP CONSTRAINT IF EXISTS website_servicepage_seo_block_id_key;
ALTER TABLE IF EXISTS ONLY public.website_servicepage DROP CONSTRAINT IF EXISTS website_servicepage_pkey;
ALTER TABLE IF EXISTS ONLY public.website_serviceblock DROP CONSTRAINT IF EXISTS website_serviceblock_pkey;
ALTER TABLE IF EXISTS ONLY public.website_seoblock DROP CONSTRAINT IF EXISTS website_seoblock_pkey;
ALTER TABLE IF EXISTS ONLY public.website_mainpage DROP CONSTRAINT IF EXISTS website_mainpage_seo_block_id_key;
ALTER TABLE IF EXISTS ONLY public.website_mainpage DROP CONSTRAINT IF EXISTS website_mainpage_pkey;
ALTER TABLE IF EXISTS ONLY public.website_mainpage DROP CONSTRAINT IF EXISTS website_mainpage_gallery_id_key;
ALTER TABLE IF EXISTS ONLY public.website_mainblock DROP CONSTRAINT IF EXISTS website_mainblock_pkey;
ALTER TABLE IF EXISTS ONLY public.website_image DROP CONSTRAINT IF EXISTS website_image_pkey;
ALTER TABLE IF EXISTS ONLY public.website_gallery DROP CONSTRAINT IF EXISTS website_gallery_pkey;
ALTER TABLE IF EXISTS ONLY public.website_document DROP CONSTRAINT IF EXISTS website_document_pkey;
ALTER TABLE IF EXISTS ONLY public.website_contactpage DROP CONSTRAINT IF EXISTS website_contactpage_seo_block_id_key;
ALTER TABLE IF EXISTS ONLY public.website_contactpage DROP CONSTRAINT IF EXISTS website_contactpage_pkey;
ALTER TABLE IF EXISTS ONLY public.website_aboutuspage DROP CONSTRAINT IF EXISTS website_aboutuspage_seo_block_id_key;
ALTER TABLE IF EXISTS ONLY public.website_aboutuspage DROP CONSTRAINT IF EXISTS website_aboutuspage_pkey;
ALTER TABLE IF EXISTS ONLY public.website_aboutuspage DROP CONSTRAINT IF EXISTS website_aboutuspage_gallery2_id_key;
ALTER TABLE IF EXISTS ONLY public.website_aboutuspage DROP CONSTRAINT IF EXISTS website_aboutuspage_gallery1_id_key;
ALTER TABLE IF EXISTS ONLY public.users_user DROP CONSTRAINT IF EXISTS users_user_username_key;
ALTER TABLE IF EXISTS ONLY public.users_user_user_permissions DROP CONSTRAINT IF EXISTS users_user_user_permissions_user_id_permission_id_43338c45_uniq;
ALTER TABLE IF EXISTS ONLY public.users_user_user_permissions DROP CONSTRAINT IF EXISTS users_user_user_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.users_user DROP CONSTRAINT IF EXISTS users_user_user_id_key;
ALTER TABLE IF EXISTS ONLY public.users_user DROP CONSTRAINT IF EXISTS users_user_pkey;
ALTER TABLE IF EXISTS ONLY public.users_user_groups DROP CONSTRAINT IF EXISTS users_user_groups_user_id_group_id_b88eab82_uniq;
ALTER TABLE IF EXISTS ONLY public.users_user_groups DROP CONSTRAINT IF EXISTS users_user_groups_pkey;
ALTER TABLE IF EXISTS ONLY public.users_ticket DROP CONSTRAINT IF EXISTS users_ticket_pkey;
ALTER TABLE IF EXISTS ONLY public.users_role DROP CONSTRAINT IF EXISTS users_role_pkey;
ALTER TABLE IF EXISTS ONLY public.users_role DROP CONSTRAINT IF EXISTS users_role_name_key;
ALTER TABLE IF EXISTS ONLY public.users_messagerecipient DROP CONSTRAINT IF EXISTS users_messagerecipient_pkey;
ALTER TABLE IF EXISTS ONLY public.users_messagerecipient DROP CONSTRAINT IF EXISTS users_messagerecipient_message_id_user_id_86016272_uniq;
ALTER TABLE IF EXISTS ONLY public.users_message DROP CONSTRAINT IF EXISTS users_message_pkey;
ALTER TABLE IF EXISTS ONLY public.finance_unit DROP CONSTRAINT IF EXISTS finance_unit_pkey;
ALTER TABLE IF EXISTS ONLY public.finance_unit DROP CONSTRAINT IF EXISTS finance_unit_name_key;
ALTER TABLE IF EXISTS ONLY public.finance_tariffservice DROP CONSTRAINT IF EXISTS finance_tariffservice_tariff_id_service_id_8c28b4c6_uniq;
ALTER TABLE IF EXISTS ONLY public.finance_tariffservice DROP CONSTRAINT IF EXISTS finance_tariffservice_pkey;
ALTER TABLE IF EXISTS ONLY public.finance_tariff DROP CONSTRAINT IF EXISTS finance_tariff_pkey;
ALTER TABLE IF EXISTS ONLY public.finance_service DROP CONSTRAINT IF EXISTS finance_service_pkey;
ALTER TABLE IF EXISTS ONLY public.finance_service DROP CONSTRAINT IF EXISTS finance_service_name_key;
ALTER TABLE IF EXISTS ONLY public.finance_receiptitem DROP CONSTRAINT IF EXISTS finance_receiptitem_receipt_id_service_id_31717ab0_uniq;
ALTER TABLE IF EXISTS ONLY public.finance_receiptitem DROP CONSTRAINT IF EXISTS finance_receiptitem_pkey;
ALTER TABLE IF EXISTS ONLY public.finance_receipt DROP CONSTRAINT IF EXISTS finance_receipt_pkey;
ALTER TABLE IF EXISTS ONLY public.finance_receipt DROP CONSTRAINT IF EXISTS finance_receipt_number_key;
ALTER TABLE IF EXISTS ONLY public.finance_printtemplate DROP CONSTRAINT IF EXISTS finance_printtemplate_pkey;
ALTER TABLE IF EXISTS ONLY public.finance_paymentdetails DROP CONSTRAINT IF EXISTS finance_paymentdetails_pkey;
ALTER TABLE IF EXISTS ONLY public.finance_currency DROP CONSTRAINT IF EXISTS finance_currency_pkey;
ALTER TABLE IF EXISTS ONLY public.finance_currency DROP CONSTRAINT IF EXISTS finance_currency_name_key;
ALTER TABLE IF EXISTS ONLY public.finance_counterreading DROP CONSTRAINT IF EXISTS finance_counterreading_pkey;
ALTER TABLE IF EXISTS ONLY public.finance_counterreading DROP CONSTRAINT IF EXISTS finance_counterreading_number_key;
ALTER TABLE IF EXISTS ONLY public.finance_counter DROP CONSTRAINT IF EXISTS finance_counter_serial_number_key;
ALTER TABLE IF EXISTS ONLY public.finance_counter DROP CONSTRAINT IF EXISTS finance_counter_pkey;
ALTER TABLE IF EXISTS ONLY public.finance_cashbox DROP CONSTRAINT IF EXISTS finance_cashbox_pkey;
ALTER TABLE IF EXISTS ONLY public.finance_cashbox DROP CONSTRAINT IF EXISTS finance_cashbox_number_b310d11d_uniq;
ALTER TABLE IF EXISTS ONLY public.finance_article DROP CONSTRAINT IF EXISTS finance_article_pkey;
ALTER TABLE IF EXISTS ONLY public.django_session DROP CONSTRAINT IF EXISTS django_session_pkey;
ALTER TABLE IF EXISTS ONLY public.django_migrations DROP CONSTRAINT IF EXISTS django_migrations_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_pkey;
ALTER TABLE IF EXISTS ONLY public.captcha_captchastore DROP CONSTRAINT IF EXISTS captcha_captchastore_pkey;
ALTER TABLE IF EXISTS ONLY public.captcha_captchastore DROP CONSTRAINT IF EXISTS captcha_captchastore_hashkey_key;
ALTER TABLE IF EXISTS ONLY public.building_section DROP CONSTRAINT IF EXISTS building_section_pkey;
ALTER TABLE IF EXISTS ONLY public.building_personalaccount DROP CONSTRAINT IF EXISTS building_personalaccount_pkey;
ALTER TABLE IF EXISTS ONLY public.building_personalaccount DROP CONSTRAINT IF EXISTS building_personalaccount_number_key;
ALTER TABLE IF EXISTS ONLY public.building_housestaff DROP CONSTRAINT IF EXISTS building_housestaff_pkey;
ALTER TABLE IF EXISTS ONLY public.building_housestaff DROP CONSTRAINT IF EXISTS building_housestaff_house_id_user_id_e3a3d5dc_uniq;
ALTER TABLE IF EXISTS ONLY public.building_house DROP CONSTRAINT IF EXISTS building_house_pkey;
ALTER TABLE IF EXISTS ONLY public.building_floor DROP CONSTRAINT IF EXISTS building_floor_pkey;
ALTER TABLE IF EXISTS ONLY public.building_apartment DROP CONSTRAINT IF EXISTS building_apartment_pkey;
ALTER TABLE IF EXISTS ONLY public.building_apartment DROP CONSTRAINT IF EXISTS building_apartment_personal_account_id_key;
ALTER TABLE IF EXISTS ONLY public.building_apartment DROP CONSTRAINT IF EXISTS building_apartment_house_id_number_3b6d449e_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_codename_01ab375a_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_name_key;
DROP TABLE IF EXISTS public.website_servicepage;
DROP TABLE IF EXISTS public.website_serviceblock;
DROP TABLE IF EXISTS public.website_seoblock;
DROP TABLE IF EXISTS public.website_mainpage;
DROP TABLE IF EXISTS public.website_mainblock;
DROP TABLE IF EXISTS public.website_image;
DROP TABLE IF EXISTS public.website_gallery;
DROP TABLE IF EXISTS public.website_document;
DROP TABLE IF EXISTS public.website_contactpage;
DROP TABLE IF EXISTS public.website_aboutuspage;
DROP TABLE IF EXISTS public.users_user_user_permissions;
DROP TABLE IF EXISTS public.users_user_groups;
DROP TABLE IF EXISTS public.users_user;
DROP TABLE IF EXISTS public.users_ticket;
DROP TABLE IF EXISTS public.users_role;
DROP TABLE IF EXISTS public.users_messagerecipient;
DROP TABLE IF EXISTS public.users_message;
DROP TABLE IF EXISTS public.finance_unit;
DROP TABLE IF EXISTS public.finance_tariffservice;
DROP TABLE IF EXISTS public.finance_tariff;
DROP TABLE IF EXISTS public.finance_service;
DROP TABLE IF EXISTS public.finance_receiptitem;
DROP TABLE IF EXISTS public.finance_receipt;
DROP TABLE IF EXISTS public.finance_printtemplate;
DROP TABLE IF EXISTS public.finance_paymentdetails;
DROP TABLE IF EXISTS public.finance_currency;
DROP TABLE IF EXISTS public.finance_counterreading;
DROP TABLE IF EXISTS public.finance_counter;
DROP TABLE IF EXISTS public.finance_cashbox;
DROP TABLE IF EXISTS public.finance_article;
DROP TABLE IF EXISTS public.django_session;
DROP TABLE IF EXISTS public.django_migrations;
DROP TABLE IF EXISTS public.django_content_type;
DROP TABLE IF EXISTS public.django_admin_log;
DROP TABLE IF EXISTS public.captcha_captchastore;
DROP TABLE IF EXISTS public.building_section;
DROP TABLE IF EXISTS public.building_personalaccount;
DROP TABLE IF EXISTS public.building_housestaff;
DROP TABLE IF EXISTS public.building_house;
DROP TABLE IF EXISTS public.building_floor;
DROP TABLE IF EXISTS public.building_apartment;
DROP TABLE IF EXISTS public.auth_permission;
DROP TABLE IF EXISTS public.auth_group_permissions;
DROP TABLE IF EXISTS public.auth_group;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO admin;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO admin;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO admin;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: building_apartment; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.building_apartment (
    id bigint NOT NULL,
    number character varying(10) NOT NULL,
    area double precision,
    owner_id bigint,
    tariff_id bigint,
    floor_id bigint,
    house_id bigint NOT NULL,
    personal_account_id bigint,
    section_id bigint
);


ALTER TABLE public.building_apartment OWNER TO admin;

--
-- Name: building_apartment_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.building_apartment ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.building_apartment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: building_floor; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.building_floor (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    house_id bigint NOT NULL
);


ALTER TABLE public.building_floor OWNER TO admin;

--
-- Name: building_floor_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.building_floor ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.building_floor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: building_house; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.building_house (
    id bigint NOT NULL,
    title character varying(255) NOT NULL,
    address text NOT NULL,
    image1 character varying(100),
    image2 character varying(100),
    image3 character varying(100),
    image4 character varying(100),
    image5 character varying(100)
);


ALTER TABLE public.building_house OWNER TO admin;

--
-- Name: building_house_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.building_house ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.building_house_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: building_housestaff; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.building_housestaff (
    id bigint NOT NULL,
    role_in_house character varying(100) NOT NULL,
    house_id bigint NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.building_housestaff OWNER TO admin;

--
-- Name: building_housestaff_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.building_housestaff ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.building_housestaff_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: building_personalaccount; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.building_personalaccount (
    id bigint NOT NULL,
    number character varying(20) NOT NULL,
    status character varying(20) NOT NULL,
    balance numeric(10,2) NOT NULL
);


ALTER TABLE public.building_personalaccount OWNER TO admin;

--
-- Name: building_personalaccount_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.building_personalaccount ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.building_personalaccount_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: building_section; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.building_section (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    house_id bigint NOT NULL
);


ALTER TABLE public.building_section OWNER TO admin;

--
-- Name: building_section_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.building_section ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.building_section_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: captcha_captchastore; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.captcha_captchastore (
    id integer NOT NULL,
    challenge character varying(32) NOT NULL,
    response character varying(32) NOT NULL,
    hashkey character varying(40) NOT NULL,
    expiration timestamp with time zone NOT NULL
);


ALTER TABLE public.captcha_captchastore OWNER TO admin;

--
-- Name: captcha_captchastore_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.captcha_captchastore ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.captcha_captchastore_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO admin;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO admin;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO admin;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO admin;

--
-- Name: finance_article; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.finance_article (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    type character varying(10) NOT NULL
);


ALTER TABLE public.finance_article OWNER TO admin;

--
-- Name: finance_article_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.finance_article ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.finance_article_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: finance_cashbox; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.finance_cashbox (
    id bigint NOT NULL,
    amount numeric(10,2) NOT NULL,
    date date NOT NULL,
    comment text NOT NULL,
    article_id bigint NOT NULL,
    personal_account_id bigint,
    receipt_id bigint,
    is_posted boolean NOT NULL,
    manager_id bigint,
    number character varying(50) NOT NULL
);


ALTER TABLE public.finance_cashbox OWNER TO admin;

--
-- Name: finance_cashbox_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.finance_cashbox ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.finance_cashbox_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: finance_counter; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.finance_counter (
    id bigint NOT NULL,
    serial_number character varying(100) NOT NULL,
    is_active boolean NOT NULL,
    apartment_id bigint NOT NULL,
    service_id bigint NOT NULL
);


ALTER TABLE public.finance_counter OWNER TO admin;

--
-- Name: finance_counter_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.finance_counter ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.finance_counter_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: finance_counterreading; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.finance_counterreading (
    id bigint NOT NULL,
    number character varying(20) NOT NULL,
    date date NOT NULL,
    value numeric(12,3) NOT NULL,
    status character varying(20) NOT NULL,
    counter_id bigint NOT NULL
);


ALTER TABLE public.finance_counterreading OWNER TO admin;

--
-- Name: finance_counterreading_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.finance_counterreading ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.finance_counterreading_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: finance_currency; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.finance_currency (
    id bigint NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.finance_currency OWNER TO admin;

--
-- Name: finance_currency_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.finance_currency ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.finance_currency_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: finance_paymentdetails; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.finance_paymentdetails (
    id bigint NOT NULL,
    company_name character varying(255) NOT NULL,
    info text NOT NULL
);


ALTER TABLE public.finance_paymentdetails OWNER TO admin;

--
-- Name: finance_paymentdetails_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.finance_paymentdetails ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.finance_paymentdetails_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: finance_printtemplate; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.finance_printtemplate (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    template_file character varying(100) NOT NULL,
    is_default boolean NOT NULL
);


ALTER TABLE public.finance_printtemplate OWNER TO admin;

--
-- Name: finance_printtemplate_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.finance_printtemplate ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.finance_printtemplate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: finance_receipt; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.finance_receipt (
    id bigint NOT NULL,
    number character varying(50) NOT NULL,
    date date NOT NULL,
    is_posted boolean NOT NULL,
    period_start date,
    period_end date,
    status character varying(20) NOT NULL,
    total_amount numeric(10,2) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    apartment_id bigint NOT NULL,
    tariff_id bigint
);


ALTER TABLE public.finance_receipt OWNER TO admin;

--
-- Name: finance_receipt_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.finance_receipt ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.finance_receipt_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: finance_receiptitem; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.finance_receiptitem (
    id bigint NOT NULL,
    amount numeric(10,2) NOT NULL,
    consumption numeric(10,3),
    price_per_unit numeric(10,2),
    receipt_id bigint NOT NULL,
    service_id bigint NOT NULL
);


ALTER TABLE public.finance_receiptitem OWNER TO admin;

--
-- Name: finance_receiptitem_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.finance_receiptitem ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.finance_receiptitem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: finance_service; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.finance_service (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    show_in_counters boolean NOT NULL,
    unit_id bigint NOT NULL
);


ALTER TABLE public.finance_service OWNER TO admin;

--
-- Name: finance_service_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.finance_service ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.finance_service_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: finance_tariff; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.finance_tariff (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    description text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.finance_tariff OWNER TO admin;

--
-- Name: finance_tariff_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.finance_tariff ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.finance_tariff_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: finance_tariffservice; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.finance_tariffservice (
    id bigint NOT NULL,
    price numeric(10,2) NOT NULL,
    currency_id bigint NOT NULL,
    service_id bigint NOT NULL,
    tariff_id bigint NOT NULL
);


ALTER TABLE public.finance_tariffservice OWNER TO admin;

--
-- Name: finance_tariffservice_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.finance_tariffservice ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.finance_tariffservice_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: finance_unit; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.finance_unit (
    id bigint NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.finance_unit OWNER TO admin;

--
-- Name: finance_unit_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.finance_unit ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.finance_unit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_message; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.users_message (
    id bigint NOT NULL,
    title character varying(255) NOT NULL,
    text text NOT NULL,
    date timestamp with time zone NOT NULL,
    sender_id bigint
);


ALTER TABLE public.users_message OWNER TO admin;

--
-- Name: users_message_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.users_message ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_messagerecipient; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.users_messagerecipient (
    id bigint NOT NULL,
    message_id bigint NOT NULL,
    user_id bigint NOT NULL,
    is_read boolean NOT NULL,
    is_hidden boolean NOT NULL
);


ALTER TABLE public.users_messagerecipient OWNER TO admin;

--
-- Name: users_messagerecipient_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.users_messagerecipient ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_messagerecipient_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_role; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.users_role (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    has_statistics boolean NOT NULL,
    has_cashbox boolean NOT NULL,
    has_receipt boolean NOT NULL,
    has_personal_account boolean NOT NULL,
    has_apartment boolean NOT NULL,
    has_owner boolean NOT NULL,
    has_house boolean NOT NULL,
    has_message boolean NOT NULL,
    has_ticket boolean NOT NULL,
    has_counters boolean NOT NULL,
    has_management boolean NOT NULL,
    has_service boolean NOT NULL,
    has_tariff boolean NOT NULL,
    has_role boolean NOT NULL,
    has_user boolean NOT NULL,
    has_payment_details boolean NOT NULL,
    has_article boolean NOT NULL
);


ALTER TABLE public.users_role OWNER TO admin;

--
-- Name: users_role_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.users_role ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_ticket; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.users_ticket (
    id bigint NOT NULL,
    status character varying(20) NOT NULL,
    phone character varying(20) NOT NULL,
    description text NOT NULL,
    date date NOT NULL,
    "time" time without time zone NOT NULL,
    apartment_id bigint NOT NULL,
    role_id bigint,
    user_id bigint NOT NULL,
    comment text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    master_id bigint
);


ALTER TABLE public.users_ticket OWNER TO admin;

--
-- Name: users_ticket_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.users_ticket ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_ticket_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_user; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.users_user (
    id bigint NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    user_id character varying(20),
    middle_name character varying(150) NOT NULL,
    user_type character varying(10) NOT NULL,
    status character varying(10) NOT NULL,
    avatar character varying(100),
    birthday date,
    description text NOT NULL,
    phone character varying(20) NOT NULL,
    viber character varying(20) NOT NULL,
    telegram character varying(50) NOT NULL,
    role_id bigint
);


ALTER TABLE public.users_user OWNER TO admin;

--
-- Name: users_user_groups; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.users_user_groups (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.users_user_groups OWNER TO admin;

--
-- Name: users_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.users_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.users_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_user_user_permissions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.users_user_user_permissions (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.users_user_user_permissions OWNER TO admin;

--
-- Name: users_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.users_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: website_aboutuspage; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.website_aboutuspage (
    id bigint NOT NULL,
    title1 character varying(200) NOT NULL,
    description1 text NOT NULL,
    image character varying(100),
    title2 character varying(200) NOT NULL,
    description2 text NOT NULL,
    gallery1_id bigint,
    gallery2_id bigint,
    seo_block_id bigint NOT NULL
);


ALTER TABLE public.website_aboutuspage OWNER TO admin;

--
-- Name: website_aboutuspage_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.website_aboutuspage ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.website_aboutuspage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: website_contactpage; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.website_contactpage (
    id bigint NOT NULL,
    title character varying(200) NOT NULL,
    description text NOT NULL,
    url character varying(200) NOT NULL,
    fullname character varying(255) NOT NULL,
    location character varying(255) NOT NULL,
    address character varying(255) NOT NULL,
    phone character varying(50) NOT NULL,
    email character varying(254) NOT NULL,
    map text NOT NULL,
    seo_block_id bigint NOT NULL
);


ALTER TABLE public.website_contactpage OWNER TO admin;

--
-- Name: website_contactpage_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.website_contactpage ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.website_contactpage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: website_document; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.website_document (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    document character varying(100) NOT NULL
);


ALTER TABLE public.website_document OWNER TO admin;

--
-- Name: website_document_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.website_document ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.website_document_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: website_gallery; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.website_gallery (
    id bigint NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.website_gallery OWNER TO admin;

--
-- Name: website_gallery_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.website_gallery ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.website_gallery_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: website_image; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.website_image (
    id bigint NOT NULL,
    image character varying(100) NOT NULL,
    gallery_id bigint NOT NULL
);


ALTER TABLE public.website_image OWNER TO admin;

--
-- Name: website_image_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.website_image ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.website_image_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: website_mainblock; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.website_mainblock (
    id bigint NOT NULL,
    image character varying(100) NOT NULL,
    title character varying(150) NOT NULL,
    description text NOT NULL,
    main_page_id bigint NOT NULL
);


ALTER TABLE public.website_mainblock OWNER TO admin;

--
-- Name: website_mainblock_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.website_mainblock ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.website_mainblock_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: website_mainpage; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.website_mainpage (
    id bigint NOT NULL,
    title character varying(200) NOT NULL,
    description text NOT NULL,
    is_show_apps boolean NOT NULL,
    gallery_id bigint,
    seo_block_id bigint NOT NULL
);


ALTER TABLE public.website_mainpage OWNER TO admin;

--
-- Name: website_mainpage_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.website_mainpage ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.website_mainpage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: website_seoblock; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.website_seoblock (
    id bigint NOT NULL,
    title character varying(255) NOT NULL,
    description text NOT NULL,
    keywords character varying(255) NOT NULL
);


ALTER TABLE public.website_seoblock OWNER TO admin;

--
-- Name: website_seoblock_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.website_seoblock ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.website_seoblock_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: website_serviceblock; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.website_serviceblock (
    id bigint NOT NULL,
    image character varying(100) NOT NULL,
    title character varying(150) NOT NULL,
    description text NOT NULL,
    service_page_id bigint NOT NULL
);


ALTER TABLE public.website_serviceblock OWNER TO admin;

--
-- Name: website_serviceblock_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.website_serviceblock ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.website_serviceblock_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: website_servicepage; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.website_servicepage (
    id bigint NOT NULL,
    seo_block_id bigint NOT NULL
);


ALTER TABLE public.website_servicepage OWNER TO admin;

--
-- Name: website_servicepage_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

ALTER TABLE public.website_servicepage ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.website_servicepage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_group (id, name) FROM stdin;
1	Директор
2	Управляющий
3	Электрик
4	Сантехник
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
1	1	131
2	1	134
3	1	136
4	1	142
5	1	144
6	1	146
7	1	148
8	1	21
9	1	150
10	1	22
11	1	152
12	1	24
13	1	23
14	1	30
15	1	32
16	1	33
17	1	34
18	1	35
19	1	36
20	1	37
21	1	38
22	1	39
23	1	40
24	1	45
25	1	46
26	1	47
27	1	48
28	1	49
29	1	50
30	1	51
31	1	52
32	1	69
33	1	70
34	1	71
35	1	72
36	1	77
37	1	78
38	1	79
39	1	80
40	1	85
41	1	86
42	1	87
43	1	88
44	1	94
45	1	96
46	1	97
47	1	98
48	1	99
49	1	100
50	1	101
51	1	102
52	1	103
53	1	104
54	1	105
55	1	106
56	1	107
57	1	108
58	1	113
59	1	114
60	1	115
61	1	116
62	1	119
63	2	69
64	2	70
65	2	71
66	2	72
67	2	40
68	2	37
69	2	38
70	2	39
71	2	85
72	2	53
73	2	54
74	2	56
75	2	86
76	2	87
77	2	88
78	3	105
79	3	106
80	3	107
81	3	108
82	3	113
83	3	114
84	3	115
85	3	116
86	4	105
87	4	106
88	4	107
89	4	108
90	4	113
91	4	114
92	4	115
93	4	116
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add Revenue/expense item	6	add_article
22	Can change Revenue/expense item	6	change_article
23	Can delete Revenue/expense item	6	delete_article
24	Can view Revenue/expense item	6	view_article
25	Can add Currency	7	add_currency
26	Can change Currency	7	change_currency
27	Can delete Currency	7	delete_currency
28	Can view Currency	7	view_currency
29	Can add Платежные реквизиты	8	add_paymentdetails
30	Can change Платежные реквизиты	8	change_paymentdetails
31	Can delete Платежные реквизиты	8	delete_paymentdetails
32	Can view Платежные реквизиты	8	view_paymentdetails
33	Can add Service	9	add_service
34	Can change Service	9	change_service
35	Can delete Service	9	delete_service
36	Can view Service	9	view_service
37	Can add Tariff	10	add_tariff
38	Can change Tariff	10	change_tariff
39	Can delete Tariff	10	delete_tariff
40	Can view Tariff	10	view_tariff
41	Can add Unit	11	add_unit
42	Can change Unit	11	change_unit
43	Can delete Unit	11	delete_unit
44	Can view Unit	11	view_unit
45	Can add Счетчик	12	add_counter
46	Can change Счетчик	12	change_counter
47	Can delete Счетчик	12	delete_counter
48	Can view Счетчик	12	view_counter
49	Can add Показание счетчика	13	add_counterreading
50	Can change Показание счетчика	13	change_counterreading
51	Can delete Показание счетчика	13	delete_counterreading
52	Can view Показание счетчика	13	view_counterreading
53	Can add Квитанция	14	add_receipt
54	Can change Квитанция	14	change_receipt
55	Can delete Квитанция	14	delete_receipt
56	Can view Квитанция	14	view_receipt
57	Can add Cash transaction	15	add_cashbox
58	Can change Cash transaction	15	change_cashbox
59	Can delete Cash transaction	15	delete_cashbox
60	Can view Cash transaction	15	view_cashbox
61	Can add Receipt line	16	add_receiptitem
62	Can change Receipt line	16	change_receiptitem
63	Can delete Receipt line	16	delete_receiptitem
64	Can view Receipt line	16	view_receiptitem
65	Can add Service included in the tariff	17	add_tariffservice
66	Can change Service included in the tariff	17	change_tariffservice
67	Can delete Service included in the tariff	17	delete_tariffservice
68	Can view Service included in the tariff	17	view_tariffservice
69	Can add Apartment	18	add_apartment
70	Can change Apartment	18	change_apartment
71	Can delete Apartment	18	delete_apartment
72	Can view Apartment	18	view_apartment
73	Can add Floor	19	add_floor
74	Can change Floor	19	change_floor
75	Can delete Floor	19	delete_floor
76	Can view Floor	19	view_floor
77	Can add House	20	add_house
78	Can change House	20	change_house
79	Can delete House	20	delete_house
80	Can view House	20	view_house
81	Can add House staff	21	add_housestaff
82	Can change House staff	21	change_housestaff
83	Can delete House staff	21	delete_housestaff
84	Can view House staff	21	view_housestaff
85	Can add Personal account	22	add_personalaccount
86	Can change Personal account	22	change_personalaccount
87	Can delete Personal account	22	delete_personalaccount
88	Can view Personal account	22	view_personalaccount
89	Can add Section	23	add_section
90	Can change Section	23	change_section
91	Can delete Section	23	delete_section
92	Can view Section	23	view_section
93	Can add Role	24	add_role
94	Can change Role	24	change_role
95	Can delete Role	24	delete_role
96	Can view Role	24	view_role
97	Can add user	25	add_user
98	Can change user	25	change_user
99	Can delete user	25	delete_user
100	Can view user	25	view_user
101	Can add Владелец	26	add_owner
102	Can change Владелец	26	change_owner
103	Can delete Владелец	26	delete_owner
104	Can view Владелец	26	view_owner
105	Can add Message	27	add_message
106	Can change Message	27	change_message
107	Can delete Message	27	delete_message
108	Can view Message	27	view_message
109	Can add Message recipient	28	add_messagerecipient
110	Can change Message recipient	28	change_messagerecipient
111	Can delete Message recipient	28	delete_messagerecipient
112	Can view Message recipient	28	view_messagerecipient
113	Can add Application	29	add_ticket
114	Can change Application	29	change_ticket
115	Can delete Application	29	delete_ticket
116	Can view Application	29	view_ticket
117	Can add Name of Document	30	add_document
118	Can change Name of Document	30	change_document
119	Can delete Name of Document	30	delete_document
120	Can view Name of Document	30	view_document
121	Can add Gallery	31	add_gallery
122	Can change Gallery	31	change_gallery
123	Can delete Gallery	31	delete_gallery
124	Can view Gallery	31	view_gallery
125	Can add Seo Block	32	add_seoblock
126	Can change Seo Block	32	change_seoblock
127	Can delete Seo Block	32	delete_seoblock
128	Can view Seo Block	32	view_seoblock
129	Can add Image	33	add_image
130	Can change Image	33	change_image
131	Can delete Image	33	delete_image
132	Can view Image	33	view_image
133	Can add home page	34	add_mainpage
134	Can change home page	34	change_mainpage
135	Can delete home page	34	delete_mainpage
136	Can view home page	34	view_mainpage
137	Can add Main block	35	add_mainblock
138	Can change Main block	35	change_mainblock
139	Can delete Main block	35	delete_mainblock
140	Can view Main block	35	view_mainblock
141	Can add Contact page	36	add_contactpage
142	Can change Contact page	36	change_contactpage
143	Can delete Contact page	36	delete_contactpage
144	Can view Contact page	36	view_contactpage
145	Can add About us page	37	add_aboutuspage
146	Can change About us page	37	change_aboutuspage
147	Can delete About us page	37	delete_aboutuspage
148	Can view About us page	37	view_aboutuspage
149	Can add Service page	38	add_servicepage
150	Can change Service page	38	change_servicepage
151	Can delete Service page	38	delete_servicepage
152	Can view Service page	38	view_servicepage
153	Can add Service	39	add_serviceblock
154	Can change Service	39	change_serviceblock
155	Can delete Service	39	delete_serviceblock
156	Can view Service	39	view_serviceblock
157	Can add Шаблон для печати	40	add_printtemplate
158	Can change Шаблон для печати	40	change_printtemplate
159	Can delete Шаблон для печати	40	delete_printtemplate
160	Can view Шаблон для печати	40	view_printtemplate
161	Can add captcha store	41	add_captchastore
162	Can change captcha store	41	change_captchastore
163	Can delete captcha store	41	delete_captchastore
164	Can view captcha store	41	view_captchastore
\.


--
-- Data for Name: building_apartment; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.building_apartment (id, number, area, owner_id, tariff_id, floor_id, house_id, personal_account_id, section_id) FROM stdin;
3	1	10	4	2	2	2	3	3
4	999	10	4	2	2	2	4	3
6	777	7	3	2	2	2	6	3
5	555	5	3	2	2	2	5	3
7	123	123	3	3	3	3	8	4
2	2	10	3	2	1	1	2	1
1	1	10	3	2	1	1	1	1
\.


--
-- Data for Name: building_floor; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.building_floor (id, name, house_id) FROM stdin;
1	Этаж 1	1
2	Этаж 1	2
3	Этаж 1	3
\.


--
-- Data for Name: building_house; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.building_house (id, title, address, image1, image2, image3, image4, image5) FROM stdin;
1	ЖК 1	ЖК 1	houses/glide_c2trJPA.png
2	ЖК 2	ЖК 2	houses/glide_006_pQCv5om.png
3	ЖК 3	123	houses/glide_002.png
\.


--
-- Data for Name: building_housestaff; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.building_housestaff (id, role_in_house, house_id, user_id) FROM stdin;
1	Директор	1	1
2	Управляющий	2	2
3	Директор	3	1
\.


--
-- Data for Name: building_personalaccount; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.building_personalaccount (id, number, status, balance) FROM stdin;
4	2222	inactive	0.00
5	2221	active	0.00
6	2323	active	0.00
7	4444	inactive	0.00
1	1111	active	6547.00
8	7777777	active	1606.00
2	1112	active	5000.00
3	1113	active	555555.00
\.


--
-- Data for Name: building_section; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.building_section (id, name, house_id) FROM stdin;
1	Секция 1	1
2	Секция 2	1
3	Секция 1	2
4	Секция 1	3
\.


--
-- Data for Name: captcha_captchastore; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.captcha_captchastore (id, challenge, response, hashkey, expiration) FROM stdin;
1	ELTY	elty	0768d98bebe6a8575e4c40d9ea457c5802dbc5fd	2025-11-18 20:48:18.511552+03
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	finance	article
7	finance	currency
8	finance	paymentdetails
9	finance	service
10	finance	tariff
11	finance	unit
12	finance	counter
13	finance	counterreading
14	finance	receipt
15	finance	cashbox
16	finance	receiptitem
17	finance	tariffservice
18	building	apartment
19	building	floor
20	building	house
21	building	housestaff
22	building	personalaccount
23	building	section
24	users	role
25	users	user
26	users	owner
27	users	message
28	users	messagerecipient
29	users	ticket
30	website	document
31	website	gallery
32	website	seoblock
33	website	image
34	website	mainpage
35	website	mainblock
36	website	contactpage
37	website	aboutuspage
38	website	servicepage
39	website	serviceblock
40	finance	printtemplate
41	captcha	captchastore
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	building	0001_initial	2025-11-12 16:14:04.920206+03
2	contenttypes	0001_initial	2025-11-12 16:14:04.93856+03
3	contenttypes	0002_remove_content_type_name	2025-11-12 16:14:04.949109+03
4	auth	0001_initial	2025-11-12 16:14:05.023379+03
5	auth	0002_alter_permission_name_max_length	2025-11-12 16:14:05.029001+03
6	auth	0003_alter_user_email_max_length	2025-11-12 16:14:05.036169+03
7	auth	0004_alter_user_username_opts	2025-11-12 16:14:05.042304+03
8	auth	0005_alter_user_last_login_null	2025-11-12 16:14:05.049611+03
9	auth	0006_require_contenttypes_0002	2025-11-12 16:14:05.051706+03
10	auth	0007_alter_validators_add_error_messages	2025-11-12 16:14:05.058947+03
11	auth	0008_alter_user_username_max_length	2025-11-12 16:14:05.065093+03
12	auth	0009_alter_user_last_name_max_length	2025-11-12 16:14:05.072156+03
13	auth	0010_alter_group_name_max_length	2025-11-12 16:14:05.078865+03
14	auth	0011_update_proxy_permissions	2025-11-12 16:14:05.090496+03
15	auth	0012_alter_user_first_name_max_length	2025-11-12 16:14:05.098095+03
16	users	0001_initial	2025-11-12 16:14:05.31695+03
17	admin	0001_initial	2025-11-12 16:14:05.358696+03
18	admin	0002_logentry_remove_auto_add	2025-11-12 16:14:05.37074+03
19	admin	0003_logentry_add_action_flag_choices	2025-11-12 16:14:05.384051+03
20	finance	0001_initial	2025-11-12 16:14:05.810783+03
21	building	0002_initial	2025-11-12 16:14:06.147739+03
22	sessions	0001_initial	2025-11-12 16:14:06.173594+03
23	website	0001_initial	2025-11-12 16:14:06.36647+03
24	finance	0002_receipt_tariff	2025-11-12 17:56:16.57346+03
25	finance	0003_alter_receipt_total_amount	2025-11-12 19:02:52.767636+03
26	finance	0004_alter_tariffservice_service	2025-11-12 20:25:57.931455+03
27	users	0002_alter_message_date	2025-11-13 15:41:21.095688+03
28	users	0003_messagerecipient_is_read	2025-11-13 17:14:09.463602+03
29	users	0004_messagerecipient_is_hidden	2025-11-14 14:07:50.47193+03
30	finance	0005_printtemplate	2025-11-17 14:02:12.571301+03
31	captcha	0001_initial	2025-11-18 20:37:50.192676+03
32	captcha	0002_alter_captchastore_id	2025-11-18 20:37:50.20018+03
35	finance	0006_alter_receipt_period_start	2025-11-21 23:25:18.716766+03
36	users	0005_alter_ticket_options_ticket_comment_and_more	2025-11-21 23:25:18.885022+03
37	finance	0007_alter_cashbox_options_cashbox_is_posted_and_more	2025-11-25 18:19:25.263423+03
38	finance	0008_alter_cashbox_number	2025-11-25 18:22:31.762967+03
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
hdhd926vxyp2ba08obvn6y4i1ke5p2mk	e30:1vLifb:jZAbwshkr2Lxqadxd6Rej6ZkHc-NJNEf4glxHjBXEKM	2025-12-03 16:56:27.913418+03
1haz01n4e2948iq4zmwmhyegjcaq73zt	e30:1vLifx:HZI6GcssPwf8n4P1o2JCtHTGKeRkqG2yD5rd20IKXdA	2025-12-03 16:56:49.954002+03
rwz4m09i85e93ehlnarpn7rtmnl9brb6	e30:1vLih0:WK3ywIa5XRJWcYIQDU4wFlDK15IgA6TFp8GhgSwahl0	2025-12-03 16:57:54.512751+03
uiy4havyiuc9a0yxq4k0ruwj99sbxhga	e30:1vLihw:QA7ZQW43g9t1CPL4C9Etuh5BQdkJN_b9tkI46LpQylY	2025-12-03 16:58:52.432911+03
flrn6yp2lrbjc1hlhoxrqejf6mv3ia43	e30:1vLiiQ:OSxtUjbMBVUXx5evWUG6EvB2MioFONGzj0XVwbe9w5s	2025-12-03 16:59:22.403499+03
m4gd7watod576nmf4tdp3zw5cc3dm6w2	.eJxVi0EOwiAQRe8ya0MKU2hxqQchMzANxqhJp6yMd5cmXWj-7v333pCobTU1lTXdCpzBwumXMeW7PPdD12x2pOZgaq5Nt9fjcih_XSWtPYqhSF92GIWCsHc-TOzGMuOM0VuMwYbF0dCNccEsHtkXmTIPjogFPl_PUzUe:1vJYBe:N-bwJUXU4iaDhCYKANHdnB03TfHSfxK1qy48tSDEfQ4	2025-11-27 17:20:34.353101+03
l2l0fyv4jgj0500xksoa3sc0u1w2ld8k	.eJxVi0EOwiAQRe8ya0MKU2hxqQchMzANxqhJp6yMd5cmXWj-7v333pCobTU1lTXdCpzBwumXMeW7PPdD12x2pOZgaq5Nt9fjcih_XSWtPYqhSF92GIWCsHc-TOzGMuOM0VuMwYbF0dCNccEsHtkXmTIPjogFPl_PUzUe:1vJrfL:kQYN07URTJVIc6mlbGg4fL1emfyIbLtiwXWozUCR2ig	2025-11-28 14:08:31.618497+03
04i6wc2hb39fse6keiwhykie7xe1r74i	.eJxVi0EOwiAQRe8ya0MKU2hxqQchMzANxqhJp6yMd5cmXWj-7v333pCobTU1lTXdCpzBwumXMeW7PPdD12x2pOZgaq5Nt9fjcih_XSWtPYqhSF92GIWCsHc-TOzGMuOM0VuMwYbF0dCNccEsHtkXmTIPjogFPl_PUzUe:1vJruw:awrppqeWJQ5pZjFclIKn3eiMb5kl4un7nxH7uy-8HFc	2025-11-28 14:24:38.117362+03
y35zzb0f3vr9rn52tc3wb0uf507ujjgt	.eJxVi0EOwiAQRe8ya0MKU2hxqQchMzANxqhJp6yMd5cmXWj-7v333pCobTU1lTXdCpzBwumXMeW7PPdD12x2pOZgaq5Nt9fjcih_XSWtPYqhSF92GIWCsHc-TOzGMuOM0VuMwYbF0dCNccEsHtkXmTIPjogFPl_PUzUe:1vOd7W:Kmt09yk0ayWJC3DcC1s-mehDyX7WRvV1-tydbbBWx8Y	2025-12-11 17:37:18.672072+03
84wcju6ag495yu05crxcv6viu4sft5e2	.eJxVi0EOwiAQRe8ya0MKU2hxqQchMzANxqhJp6yMd5cmXWj-7v333pCobTU1lTXdCpzBwumXMeW7PPdD12x2pOZgaq5Nt9fjcih_XSWtPYqhSF92GIWCsHc-TOzGMuOM0VuMwYbF0dCNccEsHtkXmTIPjogFPl_PUzUe:1vKYj8:sdzSDeibwifNyOEEGe0wpViUuqwZXgQdnBu989SGuiI	2025-11-30 12:07:18.479161+03
ten0c43axu1j46cs6syokq8pl82r1f95	.eJxVi0EOwiAQRe8ya0MKU2hxqQchMzANxqhJp6yMd5cmXWj-7v333pCobTU1lTXdCpzBwumXMeW7PPdD12x2pOZgaq5Nt9fjcih_XSWtPYqhSF92GIWCsHc-TOzGMuOM0VuMwYbF0dCNccEsHtkXmTIPjogFPl_PUzUe:1vKYsl:AXmOb_mg8u4BXzFgK0y4ijw_J60JAIM5frBYHZfNgzg	2025-11-30 12:17:15.390812+03
l5ps3607vavw93u7cg80jc5ev4tv773r	.eJxVi0EOwiAQRe8ya0MKU2hxqQchMzANxqhJp6yMd5cmXWj-7v333pCobTU1lTXdCpzBwumXMeW7PPdD12x2pOZgaq5Nt9fjcih_XSWtPYqhSF92GIWCsHc-TOzGMuOM0VuMwYbF0dCNccEsHtkXmTIPjogFPl_PUzUe:1vKZEH:IzGl8FAkpqhRRZEFbNKwNy0UhV-dHwRD1OveWNOl-mw	2025-11-30 12:39:29.828093+03
7qq6i59ecp9cz9uci9k5bhht6tg3wjld	.eJxVi0EOwiAQRe8ya0MKU2hxqQchMzANxqhJp6yMd5cmXWj-7v333pCobTU1lTXdCpzBwumXMeW7PPdD12x2pOZgaq5Nt9fjcih_XSWtPYqhSF92GIWCsHc-TOzGMuOM0VuMwYbF0dCNccEsHtkXmTIPjogFPl_PUzUe:1vKZwM:pfVVSMSozaw1_Rur_1b-LUmnYOugbgZU8k8MiaJoC38	2025-11-30 13:25:02.47115+03
denoehn92ul8znxc9qtuaikwl9wkn8ju	.eJxVi0EOwiAQRe8ya0MKU2hxqQchMzANxqhJp6yMd5cmXWj-7v333pCobTU1lTXdCpzBwumXMeW7PPdD12x2pOZgaq5Nt9fjcih_XSWtPYqhSF92GIWCsHc-TOzGMuOM0VuMwYbF0dCNccEsHtkXmTIPjogFPl_PUzUe:1vNbkc:0Y4gbAfeoHnKfmxVQXQUo5H0l0FdTjuPOUjE9p_p-bA	2025-12-08 21:57:26.996205+03
r5akccqt3q1880en78typgz1k406ymoj	.eJxVi0sOwiAQQO_C2pChyAAu7UEIDEMwRk06ZWW8u23ShW7f561SHmtPQ3hJt6ouCtXpl5VMd37uQhbSOxJ9MNHzkPX1uB7J39ez9G0iai5TtL4hOM_Rgzm3YqKxWEMOU-XqNtkqQORQYSIkLs0WC2iRnfp8AdU2NQE:1vOJ6O:IG_F8DC1S7k8KLUwgHoro2WocOfjtmyqnX7bWTtSNfY	2025-12-10 20:14:48.588611+03
\.


--
-- Data for Name: finance_article; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.finance_article (id, name, type) FROM stdin;
1	вода	income
2	вода	expense
3	123	expense
12	Оплата квитанции	income
13	тест	income
\.


--
-- Data for Name: finance_cashbox; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.finance_cashbox (id, amount, date, comment, article_id, personal_account_id, receipt_id, is_posted, manager_id, number) FROM stdin;
8	5000.00	2025-11-25		2	\N	\N	t	1	0000000007
9	5000.00	2025-11-25	555	1	1	\N	t	1	0000000009
10	777.00	2025-11-25		1	1	\N	t	1	0000000010
11	770.00	2025-11-26	Онлайн-оплата квитанции №1241	12	1	15	t	\N	PAY-1241-1764163192
12	1606.00	2025-11-26	Онлайн-оплата квитанции №1240	12	8	14	t	\N	0000000012
13	5000.00	2025-11-26	555	13	2	\N	t	1	0000000013
14	10000.00	2025-11-26	11	2	\N	\N	t	1	0000000014
15	555555.00	2025-11-26		12	3	\N	t	1	0000000015
\.


--
-- Data for Name: finance_counter; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.finance_counter (id, serial_number, is_active, apartment_id, service_id) FROM stdin;
1	auto-1-1	t	1	1
2	auto-2-1	t	2	1
3	auto-2-2	t	2	2
4	auto-1-4	t	1	4
5	auto-2-3	t	2	3
6	auto-7-3	t	7	3
7	auto-2-4	t	2	4
8	auto-1-3	t	1	3
\.


--
-- Data for Name: finance_counterreading; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.finance_counterreading (id, number, date, value, status, counter_id) FROM stdin;
6	13132	2025-11-21	123.000	new	6
1	1111	2025-11-12	77.000	considered	1
4	132	2025-11-12	80.000	considered	2
2	1112	2025-11-12	20.000	considered	2
3	1113	2025-11-12	7777.000	new	7
5	5555	2025-11-12	132.000	new	4
7	13133	2025-11-27	111111111.000	new	8
\.


--
-- Data for Name: finance_currency; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.finance_currency (id, name) FROM stdin;
1	грн
\.


--
-- Data for Name: finance_paymentdetails; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.finance_paymentdetails (id, company_name, info) FROM stdin;
1	MyHouse24	MyHouse24MyHouse24
\.


--
-- Data for Name: finance_printtemplate; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.finance_printtemplate (id, name, template_file, is_default) FROM stdin;
1	test	receipt_templates/tpl-111.xlsx	f
5	шаблон	receipt_templates/1111.xlsx	t
\.


--
-- Data for Name: finance_receipt; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.finance_receipt (id, number, date, is_posted, period_start, period_end, status, total_amount, created_at, apartment_id, tariff_id) FROM stdin;
8	1113	2025-11-13	t	2025-11-13	2025-11-14	unpaid	726.00	2025-11-13 14:07:48.781882+03	2	2
10	1237	2025-11-16	t	2025-11-01	2025-11-16	unpaid	330.00	2025-11-16 15:35:57.452875+03	4	2
11	1238	2025-11-16	t	2025-11-01	2025-11-16	unpaid	0.00	2025-11-16 15:37:42.882287+03	6	2
13	1239	2025-11-19	f	2025-11-11	2025-11-11	unpaid	3516.00	2025-11-19 19:55:34.274569+03	5	2
9	1236	2025-11-13	t	2025-11-13	2025-11-14	unpaid	20.00	2025-11-13 14:18:00.589144+03	2	2
15	1241	2025-11-24	t	2025-11-24	2025-11-24	paid	770.00	2025-11-25 00:16:15.126364+03	1	2
14	1240	2025-11-21	f	2025-11-21	2025-11-22	paid	1606.00	2025-11-21 20:03:55.511051+03	7	3
16	1242	2025-11-26	f	\N	\N	unpaid	121.00	2025-11-26 20:20:38.577867+03	1	2
\.


--
-- Data for Name: finance_receiptitem; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.finance_receiptitem (id, amount, consumption, price_per_unit, receipt_id, service_id) FROM stdin;
9	605.00	55.000	11.00	8	4
12	121.00	11.000	11.00	8	2
13	110.00	11.000	10.00	10	1
14	110.00	11.000	10.00	10	2
15	110.00	11.000	10.00	10	3
16	0.00	11.000	\N	11	3
21	1230.00	123.000	10.00	13	1
22	2130.00	213.000	10.00	13	2
23	120.00	12.000	10.00	13	3
24	36.00	3.000	12.00	13	4
25	1353.00	11.000	123.00	14	1
26	253.00	11.000	23.00	14	4
27	770.00	77.000	10.00	15	1
33	20.00	20.000	1.00	9	1
35	121.00	11.000	11.00	16	1
\.


--
-- Data for Name: finance_service; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.finance_service (id, name, show_in_counters, unit_id) FROM stdin;
1	Вода	t	1
2	Электричество	t	2
3	UNIT	t	3
4	test	t	4
\.


--
-- Data for Name: finance_tariff; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.finance_tariff (id, name, description, created_at, updated_at) FROM stdin;
2	Стандарт	Стандарт	2025-11-12 16:40:51.803129+03	2025-11-12 16:40:51.80314+03
3	123	123	2025-11-18 16:03:07.312665+03	2025-11-18 16:03:18.695739+03
\.


--
-- Data for Name: finance_tariffservice; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.finance_tariffservice (id, price, currency_id, service_id, tariff_id) FROM stdin;
1	10.00	1	1	2
2	10.00	1	2	2
3	10.00	1	3	2
4	123.00	1	1	3
5	23.00	1	4	3
\.


--
-- Data for Name: finance_unit; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.finance_unit (id, name) FROM stdin;
1	m³
2	кВт.ч
3	UNIT
4	test
\.


--
-- Data for Name: users_message; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users_message (id, title, text, date, sender_id) FROM stdin;
5	121	<p>123</p>	2025-11-14 14:08:59.783146+03	1
6	123	<p>123</p>	2025-11-14 14:25:11.716389+03	1
7	вапвапавп	<p>вавпкувап</p>	2025-11-19 19:56:14.742117+03	1
8	всем	<p>всем</p>	2025-11-24 23:26:58.337927+03	1
9	Новое сообщение	<h1>Новое сообщение</h1>	2025-11-25 12:39:17.775862+03	1
10	222222	<p>22222222</p>	2025-11-26 20:17:36.590132+03	1
11	dctv	<p>dctv</p>	2025-11-26 20:18:09.124483+03	1
12	2131232	<p>213213</p>	2025-11-26 20:48:03.469292+03	1
\.


--
-- Data for Name: users_messagerecipient; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users_messagerecipient (id, message_id, user_id, is_read, is_hidden) FROM stdin;
5	5	3	t	t
7	7	3	t	t
6	6	3	t	t
8	8	8	f	f
10	8	4	f	f
9	8	3	t	f
11	9	4	f	f
13	11	8	f	f
15	11	4	f	f
14	11	3	t	f
16	12	3	t	f
12	10	3	t	f
\.


--
-- Data for Name: users_role; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users_role (id, name, has_statistics, has_cashbox, has_receipt, has_personal_account, has_apartment, has_owner, has_house, has_message, has_ticket, has_counters, has_management, has_service, has_tariff, has_role, has_user, has_payment_details, has_article) FROM stdin;
1	Директор	t	t	t	t	t	t	t	t	t	t	t	t	t	t	t	t	t
4	Электрик	f	f	f	f	f	f	f	t	t	f	f	f	f	f	f	f	f
5	Сантехник	f	f	f	f	f	f	f	t	t	f	f	f	f	f	f	f	f
2	Управляющий	f	f	t	t	t	f	f	t	t	f	f	f	t	f	f	f	f
3	Бухгалтер	f	f	f	f	f	f	f	t	t	f	f	f	f	f	f	f	f
\.


--
-- Data for Name: users_ticket; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users_ticket (id, status, phone, description, date, "time", apartment_id, role_id, user_id, comment, created_at, master_id) FROM stdin;
3	new	owner1	465	2025-11-22	18:21:00	1	2	3	<p>456</p>	2025-11-22 19:22:02.164514+03	2
4	new	owner1	1233	2025-11-22	18:55:00	1	5	3	<p>1233</p>	2025-11-22 19:28:49.075552+03	6
5	new		user2	2025-11-22	19:03:00	1	2	3		2025-11-22 20:04:19.43114+03	\N
6	new	owner1	333	2025-11-22	19:18:00	1	5	3	<p>33</p>	2025-11-22 20:18:52.382786+03	6
7	new	owner2	132	2025-11-26	14:29:00	4	5	4	<p>123</p>	2025-11-26 15:30:06.239028+03	6
8	in_progress	owner2	123	2025-11-26	14:31:00	3	4	4	<p>123</p>	2025-11-26 15:30:42.515642+03	7
9	new	owner1	1111111111111111111	2025-11-26	19:13:00	1	5	3	<p>1111111111111111</p>	2025-11-26 20:14:27.484744+03	6
\.


--
-- Data for Name: users_user; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, user_id, middle_name, user_type, status, avatar, birthday, description, phone, viber, telegram, role_id) FROM stdin;
8	pbkdf2_sha256$1000000$gHhb6nT5rl9jjF6EntU3TH$Up6+s65BGYBmowFiKU4dgh2UMymp1UEwspxnjiUrxH0=	\N	f	owner3@owner3.com	owner3	owner3	owner3@owner3.com	f	t	2025-11-19 16:46:44.039522+03	owner3	owner3	owner	new	avatars/glide_005.png	2025-11-11	owner3	owner3	owner3	owner3	\N
3	pbkdf2_sha256$1000000$enjsLlH7BjgncdUqEkdQZC$YBlH0cxGw+Y9OY3X78+bUVJzzsLR7iZhTxSq5ny3lmc=	2025-11-27 17:35:58.846865+03	f	owner1@owner1.com	owner1	owner1	owner1@owner1.com	f	t	2025-11-12 16:31:11.480762+03	owner1	owner1	owner	active	avatars/glide_c8874BU.png	2025-11-11	owner1owner1	owner1	owner1	owner1	\N
1	pbkdf2_sha256$1000000$fLRRNi7pg0T1x08q8N7LNq$KXrVIqM6mN0tZs3E9WugLAuoKAE+XfnVHjLGYjaC3WE=	2025-11-27 17:37:18.660551+03	t	admin	admin	admin	admin@admin.com	t	t	2025-11-12 16:14:43.87725+03	\N		employee	new		\N		admin			1
6	pbkdf2_sha256$1000000$LfJWtIkwggAQovjm0rF8fq$rXOqZVj2ZJPx8DBbDCi5tDArlWBwffsVSpYJ0atTXAI=	2025-11-26 20:14:48.579675+03	f	user2@user2.com	user2	user2	user2@user2.com	t	t	2025-11-18 20:28:21.093442+03	\N		employee	new		\N		user2			5
2	pbkdf2_sha256$1000000$iturlbbcptP2n7RkX3IgUs$fukiK3NRP4gufG1ONWSkqZHM4Cu0iDo4YquPnlfDWxE=	2025-11-22 20:10:29.929587+03	f	user1@user1.com	user1	user1	user1@user1.com	t	t	2025-11-12 16:29:50.344135+03	\N		employee	new		\N		user1			2
4	pbkdf2_sha256$1000000$ahSwTtgx2UQJj3VMbRUy48$3MtpjKqlsrwhjaRBvdzKaicPXJrW0arX9+FZfmJg92Y=	2025-11-26 20:18:37.284019+03	f	owner2@owner2.com	owner2	owner2	owner2@owner2.com	f	t	2025-11-12 16:31:35.363612+03	owner2	owner2	owner	new		2025-11-06	owner2	owner2	owner2	owner2	\N
7	pbkdf2_sha256$1000000$STnR19c2HSt5s8ll6yxXja$pc9R8yK2LyE1MiivIPwsUNlvxAz5LSgFPjSD9VOGscI=	2025-11-26 15:31:06.462474+03	f	user3@user3.com	user3	user3	user3@user3.com	t	t	2025-11-18 21:47:43.273609+03	\N		employee	new		\N		user3			4
\.


--
-- Data for Name: users_user_groups; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users_user_groups (id, user_id, group_id) FROM stdin;
1	1	1
2	2	2
4	6	4
5	7	3
\.


--
-- Data for Name: users_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: website_aboutuspage; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.website_aboutuspage (id, title1, description1, image, title2, description2, gallery1_id, gallery2_id, seo_block_id) FROM stdin;
1	О нас	<h3 class="card-title">О нас</h3>\r\n<h3 class="card-title">О нас</h3>\r\n<h3 class="card-title">О нас</h3>		О нас	<h3 class="card-title">О нас</h3>	4	5	6
\.


--
-- Data for Name: website_contactpage; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.website_contactpage (id, title, description, url, fullname, location, address, phone, email, map, seo_block_id) FROM stdin;
1	Contacts	Contacts	https://avada-media.ua/moydom24/	Contacts	Contacts	Contacts	Contacts	Contacts@Contacts.com	<div style="width: 100%"><iframe width="100%" height="600" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.com/maps?width=100%25&amp;height=600&amp;hl=en&amp;q=Odessa%20Ukraine%20Avada%20Media+(My%20Business%20Name)&amp;t=&amp;z=14&amp;ie=UTF8&amp;iwloc=B&amp;output=embed"><a href="https://www.maps.ie/distance-area-calculator.html">measure acres/hectares on map</a></iframe></div>	8
\.


--
-- Data for Name: website_document; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.website_document (id, name, document) FROM stdin;
1	Document	documents/glide_P4T0Cd3.png
\.


--
-- Data for Name: website_gallery; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.website_gallery (id, name) FROM stdin;
1	Home Page Slider
2	Home Page Slider
3	Home Page Slider
4	Gallery 1 'About us'
5	Gallery 2 'About us'
6	Home Page Slider
7	Home Page Slider
8	Home Page Slider
9	Home Page Slider
10	Home Page Slider
11	Home Page Slider
12	Home Page Slider
13	Home Page Slider
14	Home Page Slider
15	Home Page Slider
16	Home Page Slider
17	Home Page Slider
18	Home Page Slider
19	Home Page Slider
20	Home Page Slider
21	Home Page Slider
22	Home Page Slider
23	Home Page Slider
24	Home Page Slider
25	Home Page Slider
26	Home Page Slider
27	Home Page Slider
28	Home Page Slider
29	Home Page Slider
\.


--
-- Data for Name: website_image; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.website_image (id, image, gallery_id) FROM stdin;
3		1
1	gallery_images/glide_Qp8LE5a.png	1
2	gallery_images/glide_009_Idoi9D1.png	1
4	gallery_images/glide_008.png	4
5	gallery_images/glide_009_PZiuDZ3.png	4
6	gallery_images/glide_008_HcPOzIf.png	5
7	gallery_images/glide_009_WQMV14G.png	5
\.


--
-- Data for Name: website_mainblock; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.website_mainblock (id, image, title, description, main_page_id) FROM stdin;
4		Block 4		1
5		Block 5		1
6		Block 6		1
1	main_page/blocks/glide_008_Ciw7fmZ.png	Block 1	<p>123</p>	1
2	main_page/blocks/glide_003.png	Block 2	<p>123</p>	1
3	main_page/blocks/glide_006.png	Block 3		1
\.


--
-- Data for Name: website_mainpage; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.website_mainpage (id, title, description, is_show_apps, gallery_id, seo_block_id) FROM stdin;
1	Default Title	<p>Default description</p>	t	1	2
\.


--
-- Data for Name: website_seoblock; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.website_seoblock (id, title, description, keywords) FROM stdin;
1	Услуги
3	Услуги
4	Home Page
5	Home Page
7	Услуги
9	About us
10	Home Page
11	Home Page
12	Home Page
13	About us
14	Услуги
15	Contacts
16	Home Page
17	Home Page
18	About us
19	Услуги
20	Contacts
21	Home Page
22	Home Page
23	Home Page
24	Home Page
25	Home Page
26	Home Page
27	Home Page
28	Home Page
29	Home Page
30	Home Page
31	Home Page
32	Home Page
33	About us
34	Услуги
35	Contacts
36	Home Page
37	Home Page
38	Home Page
39	Home Page
40	Home Page
2	Home Page	Home Page	Home Page
41	Home Page
42	Home Page
43	About us
44	About us
6	About us	About us	About us
45	About us
46	Услуги
47	Contacts
48	Contacts
8	Contacts	Contacts	Contacts
49	Contacts
50	Contacts
\.


--
-- Data for Name: website_serviceblock; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.website_serviceblock (id, image, title, description, service_page_id) FROM stdin;
\.


--
-- Data for Name: website_servicepage; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.website_servicepage (id, seo_block_id) FROM stdin;
1	1
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 4, true);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 93, true);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 164, true);


--
-- Name: building_apartment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.building_apartment_id_seq', 7, true);


--
-- Name: building_floor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.building_floor_id_seq', 3, true);


--
-- Name: building_house_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.building_house_id_seq', 3, true);


--
-- Name: building_housestaff_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.building_housestaff_id_seq', 3, true);


--
-- Name: building_personalaccount_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.building_personalaccount_id_seq', 8, true);


--
-- Name: building_section_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.building_section_id_seq', 4, true);


--
-- Name: captcha_captchastore_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.captcha_captchastore_id_seq', 2, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 41, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 38, true);


--
-- Name: finance_article_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.finance_article_id_seq', 13, true);


--
-- Name: finance_cashbox_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.finance_cashbox_id_seq', 15, true);


--
-- Name: finance_counter_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.finance_counter_id_seq', 8, true);


--
-- Name: finance_counterreading_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.finance_counterreading_id_seq', 7, true);


--
-- Name: finance_currency_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.finance_currency_id_seq', 1, true);


--
-- Name: finance_paymentdetails_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.finance_paymentdetails_id_seq', 1, false);


--
-- Name: finance_printtemplate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.finance_printtemplate_id_seq', 5, true);


--
-- Name: finance_receipt_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.finance_receipt_id_seq', 16, true);


--
-- Name: finance_receiptitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.finance_receiptitem_id_seq', 35, true);


--
-- Name: finance_service_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.finance_service_id_seq', 4, true);


--
-- Name: finance_tariff_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.finance_tariff_id_seq', 5, true);


--
-- Name: finance_tariffservice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.finance_tariffservice_id_seq', 9, true);


--
-- Name: finance_unit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.finance_unit_id_seq', 4, true);


--
-- Name: users_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.users_message_id_seq', 12, true);


--
-- Name: users_messagerecipient_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.users_messagerecipient_id_seq', 16, true);


--
-- Name: users_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.users_role_id_seq', 5, true);


--
-- Name: users_ticket_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.users_ticket_id_seq', 9, true);


--
-- Name: users_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.users_user_groups_id_seq', 5, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.users_user_id_seq', 8, true);


--
-- Name: users_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.users_user_user_permissions_id_seq', 1, false);


--
-- Name: website_aboutuspage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.website_aboutuspage_id_seq', 1, false);


--
-- Name: website_contactpage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.website_contactpage_id_seq', 1, false);


--
-- Name: website_document_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.website_document_id_seq', 1, true);


--
-- Name: website_gallery_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.website_gallery_id_seq', 29, true);


--
-- Name: website_image_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.website_image_id_seq', 7, true);


--
-- Name: website_mainblock_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.website_mainblock_id_seq', 6, true);


--
-- Name: website_mainpage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.website_mainpage_id_seq', 1, false);


--
-- Name: website_seoblock_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.website_seoblock_id_seq', 50, true);


--
-- Name: website_serviceblock_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.website_serviceblock_id_seq', 1, false);


--
-- Name: website_servicepage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.website_servicepage_id_seq', 1, false);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: building_apartment building_apartment_house_id_number_3b6d449e_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.building_apartment
    ADD CONSTRAINT building_apartment_house_id_number_3b6d449e_uniq UNIQUE (house_id, number);


--
-- Name: building_apartment building_apartment_personal_account_id_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.building_apartment
    ADD CONSTRAINT building_apartment_personal_account_id_key UNIQUE (personal_account_id);


--
-- Name: building_apartment building_apartment_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.building_apartment
    ADD CONSTRAINT building_apartment_pkey PRIMARY KEY (id);


--
-- Name: building_floor building_floor_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.building_floor
    ADD CONSTRAINT building_floor_pkey PRIMARY KEY (id);


--
-- Name: building_house building_house_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.building_house
    ADD CONSTRAINT building_house_pkey PRIMARY KEY (id);


--
-- Name: building_housestaff building_housestaff_house_id_user_id_e3a3d5dc_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.building_housestaff
    ADD CONSTRAINT building_housestaff_house_id_user_id_e3a3d5dc_uniq UNIQUE (house_id, user_id);


--
-- Name: building_housestaff building_housestaff_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.building_housestaff
    ADD CONSTRAINT building_housestaff_pkey PRIMARY KEY (id);


--
-- Name: building_personalaccount building_personalaccount_number_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.building_personalaccount
    ADD CONSTRAINT building_personalaccount_number_key UNIQUE (number);


--
-- Name: building_personalaccount building_personalaccount_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.building_personalaccount
    ADD CONSTRAINT building_personalaccount_pkey PRIMARY KEY (id);


--
-- Name: building_section building_section_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.building_section
    ADD CONSTRAINT building_section_pkey PRIMARY KEY (id);


--
-- Name: captcha_captchastore captcha_captchastore_hashkey_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.captcha_captchastore
    ADD CONSTRAINT captcha_captchastore_hashkey_key UNIQUE (hashkey);


--
-- Name: captcha_captchastore captcha_captchastore_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.captcha_captchastore
    ADD CONSTRAINT captcha_captchastore_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: finance_article finance_article_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_article
    ADD CONSTRAINT finance_article_pkey PRIMARY KEY (id);


--
-- Name: finance_cashbox finance_cashbox_number_b310d11d_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_cashbox
    ADD CONSTRAINT finance_cashbox_number_b310d11d_uniq UNIQUE (number);


--
-- Name: finance_cashbox finance_cashbox_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_cashbox
    ADD CONSTRAINT finance_cashbox_pkey PRIMARY KEY (id);


--
-- Name: finance_counter finance_counter_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_counter
    ADD CONSTRAINT finance_counter_pkey PRIMARY KEY (id);


--
-- Name: finance_counter finance_counter_serial_number_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_counter
    ADD CONSTRAINT finance_counter_serial_number_key UNIQUE (serial_number);


--
-- Name: finance_counterreading finance_counterreading_number_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_counterreading
    ADD CONSTRAINT finance_counterreading_number_key UNIQUE (number);


--
-- Name: finance_counterreading finance_counterreading_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_counterreading
    ADD CONSTRAINT finance_counterreading_pkey PRIMARY KEY (id);


--
-- Name: finance_currency finance_currency_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_currency
    ADD CONSTRAINT finance_currency_name_key UNIQUE (name);


--
-- Name: finance_currency finance_currency_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_currency
    ADD CONSTRAINT finance_currency_pkey PRIMARY KEY (id);


--
-- Name: finance_paymentdetails finance_paymentdetails_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_paymentdetails
    ADD CONSTRAINT finance_paymentdetails_pkey PRIMARY KEY (id);


--
-- Name: finance_printtemplate finance_printtemplate_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_printtemplate
    ADD CONSTRAINT finance_printtemplate_pkey PRIMARY KEY (id);


--
-- Name: finance_receipt finance_receipt_number_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_receipt
    ADD CONSTRAINT finance_receipt_number_key UNIQUE (number);


--
-- Name: finance_receipt finance_receipt_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_receipt
    ADD CONSTRAINT finance_receipt_pkey PRIMARY KEY (id);


--
-- Name: finance_receiptitem finance_receiptitem_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_receiptitem
    ADD CONSTRAINT finance_receiptitem_pkey PRIMARY KEY (id);


--
-- Name: finance_receiptitem finance_receiptitem_receipt_id_service_id_31717ab0_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_receiptitem
    ADD CONSTRAINT finance_receiptitem_receipt_id_service_id_31717ab0_uniq UNIQUE (receipt_id, service_id);


--
-- Name: finance_service finance_service_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_service
    ADD CONSTRAINT finance_service_name_key UNIQUE (name);


--
-- Name: finance_service finance_service_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_service
    ADD CONSTRAINT finance_service_pkey PRIMARY KEY (id);


--
-- Name: finance_tariff finance_tariff_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_tariff
    ADD CONSTRAINT finance_tariff_pkey PRIMARY KEY (id);


--
-- Name: finance_tariffservice finance_tariffservice_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_tariffservice
    ADD CONSTRAINT finance_tariffservice_pkey PRIMARY KEY (id);


--
-- Name: finance_tariffservice finance_tariffservice_tariff_id_service_id_8c28b4c6_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_tariffservice
    ADD CONSTRAINT finance_tariffservice_tariff_id_service_id_8c28b4c6_uniq UNIQUE (tariff_id, service_id);


--
-- Name: finance_unit finance_unit_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_unit
    ADD CONSTRAINT finance_unit_name_key UNIQUE (name);


--
-- Name: finance_unit finance_unit_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_unit
    ADD CONSTRAINT finance_unit_pkey PRIMARY KEY (id);


--
-- Name: users_message users_message_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_message
    ADD CONSTRAINT users_message_pkey PRIMARY KEY (id);


--
-- Name: users_messagerecipient users_messagerecipient_message_id_user_id_86016272_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_messagerecipient
    ADD CONSTRAINT users_messagerecipient_message_id_user_id_86016272_uniq UNIQUE (message_id, user_id);


--
-- Name: users_messagerecipient users_messagerecipient_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_messagerecipient
    ADD CONSTRAINT users_messagerecipient_pkey PRIMARY KEY (id);


--
-- Name: users_role users_role_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_role
    ADD CONSTRAINT users_role_name_key UNIQUE (name);


--
-- Name: users_role users_role_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_role
    ADD CONSTRAINT users_role_pkey PRIMARY KEY (id);


--
-- Name: users_ticket users_ticket_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_ticket
    ADD CONSTRAINT users_ticket_pkey PRIMARY KEY (id);


--
-- Name: users_user_groups users_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_groups
    ADD CONSTRAINT users_user_groups_pkey PRIMARY KEY (id);


--
-- Name: users_user_groups users_user_groups_user_id_group_id_b88eab82_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_groups
    ADD CONSTRAINT users_user_groups_user_id_group_id_b88eab82_uniq UNIQUE (user_id, group_id);


--
-- Name: users_user users_user_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user
    ADD CONSTRAINT users_user_pkey PRIMARY KEY (id);


--
-- Name: users_user users_user_user_id_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user
    ADD CONSTRAINT users_user_user_id_key UNIQUE (user_id);


--
-- Name: users_user_user_permissions users_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_user_permissions
    ADD CONSTRAINT users_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: users_user_user_permissions users_user_user_permissions_user_id_permission_id_43338c45_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_user_permissions
    ADD CONSTRAINT users_user_user_permissions_user_id_permission_id_43338c45_uniq UNIQUE (user_id, permission_id);


--
-- Name: users_user users_user_username_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user
    ADD CONSTRAINT users_user_username_key UNIQUE (username);


--
-- Name: website_aboutuspage website_aboutuspage_gallery1_id_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_aboutuspage
    ADD CONSTRAINT website_aboutuspage_gallery1_id_key UNIQUE (gallery1_id);


--
-- Name: website_aboutuspage website_aboutuspage_gallery2_id_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_aboutuspage
    ADD CONSTRAINT website_aboutuspage_gallery2_id_key UNIQUE (gallery2_id);


--
-- Name: website_aboutuspage website_aboutuspage_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_aboutuspage
    ADD CONSTRAINT website_aboutuspage_pkey PRIMARY KEY (id);


--
-- Name: website_aboutuspage website_aboutuspage_seo_block_id_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_aboutuspage
    ADD CONSTRAINT website_aboutuspage_seo_block_id_key UNIQUE (seo_block_id);


--
-- Name: website_contactpage website_contactpage_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_contactpage
    ADD CONSTRAINT website_contactpage_pkey PRIMARY KEY (id);


--
-- Name: website_contactpage website_contactpage_seo_block_id_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_contactpage
    ADD CONSTRAINT website_contactpage_seo_block_id_key UNIQUE (seo_block_id);


--
-- Name: website_document website_document_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_document
    ADD CONSTRAINT website_document_pkey PRIMARY KEY (id);


--
-- Name: website_gallery website_gallery_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_gallery
    ADD CONSTRAINT website_gallery_pkey PRIMARY KEY (id);


--
-- Name: website_image website_image_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_image
    ADD CONSTRAINT website_image_pkey PRIMARY KEY (id);


--
-- Name: website_mainblock website_mainblock_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_mainblock
    ADD CONSTRAINT website_mainblock_pkey PRIMARY KEY (id);


--
-- Name: website_mainpage website_mainpage_gallery_id_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_mainpage
    ADD CONSTRAINT website_mainpage_gallery_id_key UNIQUE (gallery_id);


--
-- Name: website_mainpage website_mainpage_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_mainpage
    ADD CONSTRAINT website_mainpage_pkey PRIMARY KEY (id);


--
-- Name: website_mainpage website_mainpage_seo_block_id_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_mainpage
    ADD CONSTRAINT website_mainpage_seo_block_id_key UNIQUE (seo_block_id);


--
-- Name: website_seoblock website_seoblock_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_seoblock
    ADD CONSTRAINT website_seoblock_pkey PRIMARY KEY (id);


--
-- Name: website_serviceblock website_serviceblock_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_serviceblock
    ADD CONSTRAINT website_serviceblock_pkey PRIMARY KEY (id);


--
-- Name: website_servicepage website_servicepage_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_servicepage
    ADD CONSTRAINT website_servicepage_pkey PRIMARY KEY (id);


--
-- Name: website_servicepage website_servicepage_seo_block_id_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_servicepage
    ADD CONSTRAINT website_servicepage_seo_block_id_key UNIQUE (seo_block_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: building_apartment_floor_id_baa4625c; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX building_apartment_floor_id_baa4625c ON public.building_apartment USING btree (floor_id);


--
-- Name: building_apartment_house_id_9fe67ca5; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX building_apartment_house_id_9fe67ca5 ON public.building_apartment USING btree (house_id);


--
-- Name: building_apartment_owner_id_d23a066e; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX building_apartment_owner_id_d23a066e ON public.building_apartment USING btree (owner_id);


--
-- Name: building_apartment_section_id_614a9436; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX building_apartment_section_id_614a9436 ON public.building_apartment USING btree (section_id);


--
-- Name: building_apartment_tariff_id_69fa4c41; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX building_apartment_tariff_id_69fa4c41 ON public.building_apartment USING btree (tariff_id);


--
-- Name: building_floor_house_id_e77b8ffa; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX building_floor_house_id_e77b8ffa ON public.building_floor USING btree (house_id);


--
-- Name: building_housestaff_house_id_53aa17fe; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX building_housestaff_house_id_53aa17fe ON public.building_housestaff USING btree (house_id);


--
-- Name: building_housestaff_user_id_02c2ed2e; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX building_housestaff_user_id_02c2ed2e ON public.building_housestaff USING btree (user_id);


--
-- Name: building_personalaccount_number_0a041963_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX building_personalaccount_number_0a041963_like ON public.building_personalaccount USING btree (number varchar_pattern_ops);


--
-- Name: building_section_house_id_f9f4e052; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX building_section_house_id_f9f4e052 ON public.building_section USING btree (house_id);


--
-- Name: captcha_captchastore_hashkey_cbe8d15a_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX captcha_captchastore_hashkey_cbe8d15a_like ON public.captcha_captchastore USING btree (hashkey varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: finance_cashbox_article_id_2e15dc33; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX finance_cashbox_article_id_2e15dc33 ON public.finance_cashbox USING btree (article_id);


--
-- Name: finance_cashbox_manager_id_67d9219a; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX finance_cashbox_manager_id_67d9219a ON public.finance_cashbox USING btree (manager_id);


--
-- Name: finance_cashbox_number_b310d11d_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX finance_cashbox_number_b310d11d_like ON public.finance_cashbox USING btree (number varchar_pattern_ops);


--
-- Name: finance_cashbox_personal_account_id_0488b286; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX finance_cashbox_personal_account_id_0488b286 ON public.finance_cashbox USING btree (personal_account_id);


--
-- Name: finance_cashbox_receipt_id_443b2685; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX finance_cashbox_receipt_id_443b2685 ON public.finance_cashbox USING btree (receipt_id);


--
-- Name: finance_counter_apartment_id_43501d44; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX finance_counter_apartment_id_43501d44 ON public.finance_counter USING btree (apartment_id);


--
-- Name: finance_counter_serial_number_11126ce8_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX finance_counter_serial_number_11126ce8_like ON public.finance_counter USING btree (serial_number varchar_pattern_ops);


--
-- Name: finance_counter_service_id_c7d84c00; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX finance_counter_service_id_c7d84c00 ON public.finance_counter USING btree (service_id);


--
-- Name: finance_counterreading_counter_id_934b9b88; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX finance_counterreading_counter_id_934b9b88 ON public.finance_counterreading USING btree (counter_id);


--
-- Name: finance_counterreading_number_6b1ff325_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX finance_counterreading_number_6b1ff325_like ON public.finance_counterreading USING btree (number varchar_pattern_ops);


--
-- Name: finance_currency_name_24513ba4_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX finance_currency_name_24513ba4_like ON public.finance_currency USING btree (name varchar_pattern_ops);


--
-- Name: finance_receipt_apartment_id_40aba459; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX finance_receipt_apartment_id_40aba459 ON public.finance_receipt USING btree (apartment_id);


--
-- Name: finance_receipt_number_a405a4aa_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX finance_receipt_number_a405a4aa_like ON public.finance_receipt USING btree (number varchar_pattern_ops);


--
-- Name: finance_receipt_tariff_id_65d84927; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX finance_receipt_tariff_id_65d84927 ON public.finance_receipt USING btree (tariff_id);


--
-- Name: finance_receiptitem_receipt_id_aba49f36; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX finance_receiptitem_receipt_id_aba49f36 ON public.finance_receiptitem USING btree (receipt_id);


--
-- Name: finance_receiptitem_service_id_8491373a; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX finance_receiptitem_service_id_8491373a ON public.finance_receiptitem USING btree (service_id);


--
-- Name: finance_service_name_bd3324db_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX finance_service_name_bd3324db_like ON public.finance_service USING btree (name varchar_pattern_ops);


--
-- Name: finance_service_unit_id_184196ca; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX finance_service_unit_id_184196ca ON public.finance_service USING btree (unit_id);


--
-- Name: finance_tariffservice_currency_id_9311c6b8; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX finance_tariffservice_currency_id_9311c6b8 ON public.finance_tariffservice USING btree (currency_id);


--
-- Name: finance_tariffservice_service_id_bd302fc4; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX finance_tariffservice_service_id_bd302fc4 ON public.finance_tariffservice USING btree (service_id);


--
-- Name: finance_tariffservice_tariff_id_6f2b7432; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX finance_tariffservice_tariff_id_6f2b7432 ON public.finance_tariffservice USING btree (tariff_id);


--
-- Name: finance_unit_name_bc741357_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX finance_unit_name_bc741357_like ON public.finance_unit USING btree (name varchar_pattern_ops);


--
-- Name: users_message_sender_id_d1e3d44e; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_message_sender_id_d1e3d44e ON public.users_message USING btree (sender_id);


--
-- Name: users_messagerecipient_message_id_98132c5f; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_messagerecipient_message_id_98132c5f ON public.users_messagerecipient USING btree (message_id);


--
-- Name: users_messagerecipient_user_id_e1db9bc9; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_messagerecipient_user_id_e1db9bc9 ON public.users_messagerecipient USING btree (user_id);


--
-- Name: users_role_name_86bbd537_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_role_name_86bbd537_like ON public.users_role USING btree (name varchar_pattern_ops);


--
-- Name: users_ticket_apartment_id_ca19f243; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_ticket_apartment_id_ca19f243 ON public.users_ticket USING btree (apartment_id);


--
-- Name: users_ticket_master_id_04be4ae4; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_ticket_master_id_04be4ae4 ON public.users_ticket USING btree (master_id);


--
-- Name: users_ticket_role_id_e89e09d1; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_ticket_role_id_e89e09d1 ON public.users_ticket USING btree (role_id);


--
-- Name: users_ticket_user_id_50aca908; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_ticket_user_id_50aca908 ON public.users_ticket USING btree (user_id);


--
-- Name: users_user_groups_group_id_9afc8d0e; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_user_groups_group_id_9afc8d0e ON public.users_user_groups USING btree (group_id);


--
-- Name: users_user_groups_user_id_5f6f5a90; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_user_groups_user_id_5f6f5a90 ON public.users_user_groups USING btree (user_id);


--
-- Name: users_user_role_id_854f2687; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_user_role_id_854f2687 ON public.users_user USING btree (role_id);


--
-- Name: users_user_user_id_4120b7b9_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_user_user_id_4120b7b9_like ON public.users_user USING btree (user_id varchar_pattern_ops);


--
-- Name: users_user_user_permissions_permission_id_0b93982e; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_user_user_permissions_permission_id_0b93982e ON public.users_user_user_permissions USING btree (permission_id);


--
-- Name: users_user_user_permissions_user_id_20aca447; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_user_user_permissions_user_id_20aca447 ON public.users_user_user_permissions USING btree (user_id);


--
-- Name: users_user_username_06e46fe6_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX users_user_username_06e46fe6_like ON public.users_user USING btree (username varchar_pattern_ops);


--
-- Name: website_image_gallery_id_91dc697f; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX website_image_gallery_id_91dc697f ON public.website_image USING btree (gallery_id);


--
-- Name: website_mainblock_main_page_id_0e298da7; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX website_mainblock_main_page_id_0e298da7 ON public.website_mainblock USING btree (main_page_id);


--
-- Name: website_serviceblock_service_page_id_7c804e96; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX website_serviceblock_service_page_id_7c804e96 ON public.website_serviceblock USING btree (service_page_id);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: building_apartment building_apartment_floor_id_baa4625c_fk_building_floor_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.building_apartment
    ADD CONSTRAINT building_apartment_floor_id_baa4625c_fk_building_floor_id FOREIGN KEY (floor_id) REFERENCES public.building_floor(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: building_apartment building_apartment_house_id_9fe67ca5_fk_building_house_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.building_apartment
    ADD CONSTRAINT building_apartment_house_id_9fe67ca5_fk_building_house_id FOREIGN KEY (house_id) REFERENCES public.building_house(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: building_apartment building_apartment_owner_id_d23a066e_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.building_apartment
    ADD CONSTRAINT building_apartment_owner_id_d23a066e_fk_users_user_id FOREIGN KEY (owner_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: building_apartment building_apartment_personal_account_id_7c217087_fk_building_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.building_apartment
    ADD CONSTRAINT building_apartment_personal_account_id_7c217087_fk_building_ FOREIGN KEY (personal_account_id) REFERENCES public.building_personalaccount(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: building_apartment building_apartment_section_id_614a9436_fk_building_section_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.building_apartment
    ADD CONSTRAINT building_apartment_section_id_614a9436_fk_building_section_id FOREIGN KEY (section_id) REFERENCES public.building_section(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: building_apartment building_apartment_tariff_id_69fa4c41_fk_finance_tariff_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.building_apartment
    ADD CONSTRAINT building_apartment_tariff_id_69fa4c41_fk_finance_tariff_id FOREIGN KEY (tariff_id) REFERENCES public.finance_tariff(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: building_floor building_floor_house_id_e77b8ffa_fk_building_house_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.building_floor
    ADD CONSTRAINT building_floor_house_id_e77b8ffa_fk_building_house_id FOREIGN KEY (house_id) REFERENCES public.building_house(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: building_housestaff building_housestaff_house_id_53aa17fe_fk_building_house_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.building_housestaff
    ADD CONSTRAINT building_housestaff_house_id_53aa17fe_fk_building_house_id FOREIGN KEY (house_id) REFERENCES public.building_house(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: building_housestaff building_housestaff_user_id_02c2ed2e_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.building_housestaff
    ADD CONSTRAINT building_housestaff_user_id_02c2ed2e_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: building_section building_section_house_id_f9f4e052_fk_building_house_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.building_section
    ADD CONSTRAINT building_section_house_id_f9f4e052_fk_building_house_id FOREIGN KEY (house_id) REFERENCES public.building_house(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: finance_cashbox finance_cashbox_article_id_2e15dc33_fk_finance_article_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_cashbox
    ADD CONSTRAINT finance_cashbox_article_id_2e15dc33_fk_finance_article_id FOREIGN KEY (article_id) REFERENCES public.finance_article(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: finance_cashbox finance_cashbox_manager_id_67d9219a_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_cashbox
    ADD CONSTRAINT finance_cashbox_manager_id_67d9219a_fk_users_user_id FOREIGN KEY (manager_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: finance_cashbox finance_cashbox_personal_account_id_0488b286_fk_building_; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_cashbox
    ADD CONSTRAINT finance_cashbox_personal_account_id_0488b286_fk_building_ FOREIGN KEY (personal_account_id) REFERENCES public.building_personalaccount(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: finance_cashbox finance_cashbox_receipt_id_443b2685_fk_finance_receipt_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_cashbox
    ADD CONSTRAINT finance_cashbox_receipt_id_443b2685_fk_finance_receipt_id FOREIGN KEY (receipt_id) REFERENCES public.finance_receipt(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: finance_counter finance_counter_apartment_id_43501d44_fk_building_apartment_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_counter
    ADD CONSTRAINT finance_counter_apartment_id_43501d44_fk_building_apartment_id FOREIGN KEY (apartment_id) REFERENCES public.building_apartment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: finance_counter finance_counter_service_id_c7d84c00_fk_finance_service_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_counter
    ADD CONSTRAINT finance_counter_service_id_c7d84c00_fk_finance_service_id FOREIGN KEY (service_id) REFERENCES public.finance_service(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: finance_counterreading finance_counterreadi_counter_id_934b9b88_fk_finance_c; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_counterreading
    ADD CONSTRAINT finance_counterreadi_counter_id_934b9b88_fk_finance_c FOREIGN KEY (counter_id) REFERENCES public.finance_counter(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: finance_receipt finance_receipt_apartment_id_40aba459_fk_building_apartment_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_receipt
    ADD CONSTRAINT finance_receipt_apartment_id_40aba459_fk_building_apartment_id FOREIGN KEY (apartment_id) REFERENCES public.building_apartment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: finance_receipt finance_receipt_tariff_id_65d84927_fk_finance_tariff_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_receipt
    ADD CONSTRAINT finance_receipt_tariff_id_65d84927_fk_finance_tariff_id FOREIGN KEY (tariff_id) REFERENCES public.finance_tariff(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: finance_receiptitem finance_receiptitem_receipt_id_aba49f36_fk_finance_receipt_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_receiptitem
    ADD CONSTRAINT finance_receiptitem_receipt_id_aba49f36_fk_finance_receipt_id FOREIGN KEY (receipt_id) REFERENCES public.finance_receipt(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: finance_receiptitem finance_receiptitem_service_id_8491373a_fk_finance_service_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_receiptitem
    ADD CONSTRAINT finance_receiptitem_service_id_8491373a_fk_finance_service_id FOREIGN KEY (service_id) REFERENCES public.finance_service(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: finance_service finance_service_unit_id_184196ca_fk_finance_unit_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_service
    ADD CONSTRAINT finance_service_unit_id_184196ca_fk_finance_unit_id FOREIGN KEY (unit_id) REFERENCES public.finance_unit(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: finance_tariffservice finance_tariffservic_currency_id_9311c6b8_fk_finance_c; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_tariffservice
    ADD CONSTRAINT finance_tariffservic_currency_id_9311c6b8_fk_finance_c FOREIGN KEY (currency_id) REFERENCES public.finance_currency(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: finance_tariffservice finance_tariffservice_service_id_bd302fc4_fk_finance_service_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_tariffservice
    ADD CONSTRAINT finance_tariffservice_service_id_bd302fc4_fk_finance_service_id FOREIGN KEY (service_id) REFERENCES public.finance_service(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: finance_tariffservice finance_tariffservice_tariff_id_6f2b7432_fk_finance_tariff_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.finance_tariffservice
    ADD CONSTRAINT finance_tariffservice_tariff_id_6f2b7432_fk_finance_tariff_id FOREIGN KEY (tariff_id) REFERENCES public.finance_tariff(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_message users_message_sender_id_d1e3d44e_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_message
    ADD CONSTRAINT users_message_sender_id_d1e3d44e_fk_users_user_id FOREIGN KEY (sender_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_messagerecipient users_messagerecipient_message_id_98132c5f_fk_users_message_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_messagerecipient
    ADD CONSTRAINT users_messagerecipient_message_id_98132c5f_fk_users_message_id FOREIGN KEY (message_id) REFERENCES public.users_message(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_messagerecipient users_messagerecipient_user_id_e1db9bc9_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_messagerecipient
    ADD CONSTRAINT users_messagerecipient_user_id_e1db9bc9_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_ticket users_ticket_apartment_id_ca19f243_fk_building_apartment_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_ticket
    ADD CONSTRAINT users_ticket_apartment_id_ca19f243_fk_building_apartment_id FOREIGN KEY (apartment_id) REFERENCES public.building_apartment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_ticket users_ticket_master_id_04be4ae4_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_ticket
    ADD CONSTRAINT users_ticket_master_id_04be4ae4_fk_users_user_id FOREIGN KEY (master_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_ticket users_ticket_role_id_e89e09d1_fk_users_role_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_ticket
    ADD CONSTRAINT users_ticket_role_id_e89e09d1_fk_users_role_id FOREIGN KEY (role_id) REFERENCES public.users_role(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_ticket users_ticket_user_id_50aca908_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_ticket
    ADD CONSTRAINT users_ticket_user_id_50aca908_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_user_groups users_user_groups_group_id_9afc8d0e_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_groups
    ADD CONSTRAINT users_user_groups_group_id_9afc8d0e_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_user_groups users_user_groups_user_id_5f6f5a90_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_groups
    ADD CONSTRAINT users_user_groups_user_id_5f6f5a90_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_user users_user_role_id_854f2687_fk_users_role_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user
    ADD CONSTRAINT users_user_role_id_854f2687_fk_users_role_id FOREIGN KEY (role_id) REFERENCES public.users_role(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_user_user_permissions users_user_user_perm_permission_id_0b93982e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_user_permissions
    ADD CONSTRAINT users_user_user_perm_permission_id_0b93982e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_user_user_permissions users_user_user_permissions_user_id_20aca447_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_user_user_permissions
    ADD CONSTRAINT users_user_user_permissions_user_id_20aca447_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: website_aboutuspage website_aboutuspage_gallery1_id_233a01d1_fk_website_gallery_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_aboutuspage
    ADD CONSTRAINT website_aboutuspage_gallery1_id_233a01d1_fk_website_gallery_id FOREIGN KEY (gallery1_id) REFERENCES public.website_gallery(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: website_aboutuspage website_aboutuspage_gallery2_id_e27f968c_fk_website_gallery_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_aboutuspage
    ADD CONSTRAINT website_aboutuspage_gallery2_id_e27f968c_fk_website_gallery_id FOREIGN KEY (gallery2_id) REFERENCES public.website_gallery(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: website_aboutuspage website_aboutuspage_seo_block_id_bdbc184e_fk_website_s; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_aboutuspage
    ADD CONSTRAINT website_aboutuspage_seo_block_id_bdbc184e_fk_website_s FOREIGN KEY (seo_block_id) REFERENCES public.website_seoblock(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: website_contactpage website_contactpage_seo_block_id_04e9db16_fk_website_s; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_contactpage
    ADD CONSTRAINT website_contactpage_seo_block_id_04e9db16_fk_website_s FOREIGN KEY (seo_block_id) REFERENCES public.website_seoblock(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: website_image website_image_gallery_id_91dc697f_fk_website_gallery_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_image
    ADD CONSTRAINT website_image_gallery_id_91dc697f_fk_website_gallery_id FOREIGN KEY (gallery_id) REFERENCES public.website_gallery(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: website_mainblock website_mainblock_main_page_id_0e298da7_fk_website_mainpage_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_mainblock
    ADD CONSTRAINT website_mainblock_main_page_id_0e298da7_fk_website_mainpage_id FOREIGN KEY (main_page_id) REFERENCES public.website_mainpage(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: website_mainpage website_mainpage_gallery_id_3719118e_fk_website_gallery_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_mainpage
    ADD CONSTRAINT website_mainpage_gallery_id_3719118e_fk_website_gallery_id FOREIGN KEY (gallery_id) REFERENCES public.website_gallery(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: website_mainpage website_mainpage_seo_block_id_34fd0e90_fk_website_seoblock_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_mainpage
    ADD CONSTRAINT website_mainpage_seo_block_id_34fd0e90_fk_website_seoblock_id FOREIGN KEY (seo_block_id) REFERENCES public.website_seoblock(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: website_serviceblock website_serviceblock_service_page_id_7c804e96_fk_website_s; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_serviceblock
    ADD CONSTRAINT website_serviceblock_service_page_id_7c804e96_fk_website_s FOREIGN KEY (service_page_id) REFERENCES public.website_servicepage(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: website_servicepage website_servicepage_seo_block_id_2d51e33f_fk_website_s; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.website_servicepage
    ADD CONSTRAINT website_servicepage_seo_block_id_2d51e33f_fk_website_s FOREIGN KEY (seo_block_id) REFERENCES public.website_seoblock(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

\unrestrict JBLryXC2MHN687PUFsZFlfel8pUo74RYGX5bdZ75igf074fgSAWI98whNfzBbri
