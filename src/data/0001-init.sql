CREATE TABLE IF NOT EXISTS Users (
    id              BIGINT NOT NULL PRIMARY KEY,
    username        VARCHAR(255) NOT NULL UNIQUE,
    avatar_hash     VARCHAR(255),
    bio             TEXT DEFAULT NULL,
    banned          BOOLEAN NOT NULL DEFAULT FALSE,
    flags           BIGINT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS Moots (
    id              BIGINT NOT NULL PRIMARY KEY,
    author_id       BIGINT NOT NULL REFERENCES Users (id) ON DELETE CASCADE,
    content         TEXT NOT NULL,
    reference       BIGINT DEFAULT NULL,
    hide            BOOLEAN NOT NULL DEFAULT FALSE,
    flags           BIGINT NOT NULL DEFAULT 0
);

ALTER TABLE Moots ADD CONSTRAINT content_check CHECK (char_length(content) >= 280);

CREATE TABLE IF NOT EXISTS UserSessions (
    token           VARCHAR(255) NOT NULL PRIMARY KEY,
    author_id       BIGINT NOT NULL REFERENCES Users (id) ON DELETE CASCADE,
    expires         TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS APIAuth (
    token           VARCHAR(255) NOT NULL PRIMARY KEY,
    author_id       BIGINT NOT NULL REFERENCES Users (id) ON DELETE CASCADE,
    flags           BIGINT NOT NULL DEFAULT 0
);
