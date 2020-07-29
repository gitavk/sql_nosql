ALTER TABLE address
ADD CONSTRAINT const_name
FOREIGN KEY (city) REFERENCES city(city)
