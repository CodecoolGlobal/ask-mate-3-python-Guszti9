DROP TABLE IF EXISTS public.users;
CREATE TABLE users (
    id serial NOT NULL,
    username text,
    password CHAR(60),
    reputation integer,
    registration_date timestamp without time zone
);


ALTER TABLE ONLY users
    ADD CONSTRAINT pk_user_id PRIMARY KEY (id);

INSERT INTO users (id, username, password, reputation, registration_date)
VALUES (-1, 'Admin', 'Admin', 0, CURRENT_TIMESTAMP);

ALTER TABLE answer
ADD user_id integer NOT NULL DEFAULT -1;

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id);

ALTER TABLE question
ADD user_id integer NOT NULL DEFAULT -1;

ALTER TABLE ONLY question
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id);

ALTER TABLE comment
ADD user_id integer NOT NULL DEFAULT -1;

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id);

ALTER TABLE answer
ADD accepted integer DEFAULT 0;

