CREATE DATABASE bulat_test
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

-- Table: public.student

-- DROP TABLE public.student;

CREATE TABLE public.student
(
    full_name text COLLATE pg_catalog."default" NOT NULL UNIQUE,
    id        bigint                            NOT NULL,
    vk_url    text COLLATE pg_catalog."default" NOT NULL UNIQUE,
    email     text COLLATE pg_catalog."default" NOT NULL UNIQUE,
    CONSTRAINT student_pkey PRIMARY KEY (id)
)
    WITH (
        OIDS = FALSE
    )
    TABLESPACE pg_default;

ALTER TABLE public.student
    OWNER to postgres;

-- Table: public.curator

-- DROP TABLE public.curator;

CREATE TABLE public.curator
(
    id   bigint                            NOT NULL,
    name text COLLATE pg_catalog."default" NOT NULL UNIQUE,
    CONSTRAINT curator_pkey PRIMARY KEY (id)
)
    WITH (
        OIDS = FALSE
    )
    TABLESPACE pg_default;

ALTER TABLE public.curator
    OWNER to postgres;

CREATE TABLE public.manager
(
    id   bigint                            NOT NULL,
    name text COLLATE pg_catalog."default" NOT NULL UNIQUE,
    CONSTRAINT manager_pkey PRIMARY KEY (id)
)
    WITH (
        OIDS = FALSE
    )
    TABLESPACE pg_default;

ALTER TABLE public.manager
    OWNER to postgres;

CREATE TABLE public.status
(
    id   bigint                            NOT NULL,
    name text COLLATE pg_catalog."default" NOT NULL UNIQUE,
    CONSTRAINT status_pkey PRIMARY KEY (id)
);

CREATE TABLE public.group
(
    id   bigint                            NOT NULL,
    name text COLLATE pg_catalog."default" NOT NULL UNIQUE,
    CONSTRAINT status_pkey PRIMARY KEY (id)
);

CREATE TABLE public.records
(
    id               bigint NOT NULL,
    manager_id       bigint NOT NULL,
    CONSTRAINT fk_manager FOREIGN KEY (manager_id) REFERENCES manager (id),
    curator_id       bigint NOT NULL,
    CONSTRAINT fk_curator FOREIGN KEY (curator_id) REFERENCES curator (id),
    student_id       bigint NOT NULL,
    CONSTRAINT fk_student FOREIGN KEY (student_id) REFERENCES student (id),
    status_id        bigint NOT NULL,
    CONSTRAINT fk_status FOREIGN KEY (status_id) REFERENCES status (id),
    begin_date       date   NOT NULL,
    last_bought_date date   NOT NULL,
    CONSTRAINT records_pkey PRIMARY KEY (id)
);

