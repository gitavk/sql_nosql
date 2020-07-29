CREATE ROLE librarian WITH LOGIN SUPERUSER PASSWORD 'librarian';
ALTER DATABASE library OWNER TO librarian;

CREATE TABLE person (
    id              SERIAL      PRIMARY KEY,
    first_name      VARCHAR(64),
    last_name       VARCHAR(64),
    date_of_birth   DATE,
    hometown        VARCHAR(64)
);

CREATE TYPE phone_type AS ENUM ('work', 'home', 'personal');
CREATE TABLE phone (
    id          SERIAL      PRIMARY KEY,
    number      VARCHAR(64),
    type        phone_type,
    person_id   INT,
    FOREIGN KEY (person_id) REFERENCES  person(id)
);

CREATE TYPE address_type AS ENUM ('work', 'home', 'summerhouse');
CREATE TABLE address (
    id          SERIAL      PRIMARY KEY,
    address     VARCHAR(64),
    city        VARCHAR(64),
    type        address_type,
    person_id   INT,
    FOREIGN KEY (person_id) REFERENCES  person(id)
);
