CREATE TABLE IF NOT EXISTS urls (
    id BIGINT  PRIMARY KEY GENERATED by default AS IDENTITY,
    name VARCHAR(255) UNIQUE,
    created_at VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS url (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id BIGINT REFERENCES urls (id),
    status_code INTEGER,
    h1 VARCHAR(255),
    title VARCHAR(255),
    description text,
    created_at VARCHAR(10)
);