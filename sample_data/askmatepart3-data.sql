DROP TABLE IF EXISTS public.users;
CREATE TABLE users (
    id serial NOT NULL,
    username text,
    password CHAR(128)
);

