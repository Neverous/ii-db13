\i 5a.sql
ALTER TABLE kontakt
    ADD COLUMN kod_kontaktu SERIAL PRIMARY KEY,
    DROP CONSTRAINT kontakt_pkey;

