CREATE TABLE urls (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255),
    last_check VARCHAR(15),
    response_code INTEGER,
);

CREATE TABLE url (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    response_code INTEGER,
    title VARCHAR(255),
    description TEXT,
    creation_date VARCHAR(15),
);