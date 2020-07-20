CREATE TYPE city_type
AS ENUM ('megapolis', 'town', 'village');

CREATE TABLE city (
city VARCHAR(64) PRIMARY KEY,
type city_type
);
