BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 4f6cc5ab2006

CREATE TABLE items (
    id SERIAL NOT NULL, 
    name VARCHAR(150), 
    description VARCHAR(300), 
    PRIMARY KEY (id)
);

CREATE TABLE users (
    id SERIAL NOT NULL, 
    name VARCHAR(50), 
    email VARCHAR(100), 
    PRIMARY KEY (id), 
    UNIQUE (email)
);

INSERT INTO alembic_version (version_num) VALUES ('4f6cc5ab2006') RETURNING alembic_version.version_num;

-- Running upgrade 4f6cc5ab2006 -> 95b9df28fe94

ALTER TABLE items ADD COLUMN price FLOAT;

UPDATE alembic_version SET version_num='95b9df28fe94' WHERE alembic_version.version_num = '4f6cc5ab2006';

-- Running upgrade 95b9df28fe94 -> 21b96f98d5c3

ALTER TABLE items ADD COLUMN stock INTEGER;

UPDATE alembic_version SET version_num='21b96f98d5c3' WHERE alembic_version.version_num = '95b9df28fe94';

-- Running upgrade 21b96f98d5c3 -> a01a0539b1f8

ALTER TABLE items DROP COLUMN stock;

UPDATE alembic_version SET version_num='a01a0539b1f8' WHERE alembic_version.version_num = '21b96f98d5c3';

COMMIT;

