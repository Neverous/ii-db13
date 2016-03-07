-- Zadanie 6
---- (a)
CREATE TABLE uczelnia
(
    kod_ucz SERIAL PRIMARY KEY,
    nazwa   VARCHAR(256) NOT NULL UNIQUE,
    miasto  VARCHAR(256) NOT NULL UNIQUE,
    rektor  INTEGER REFERENCES uz ON DELETE SET NULL
);

---- (b)
INSERT INTO uczelnia(nazwa, miasto, rektor) VALUES
    ('Szkoła wyższa', 'Olsztyn', 187),
    ('Szkoła średnia', 'Nieszawa', 4133),
    --('Szkoła niedzielna', 'Kielce', 256);
    ('Szkoła niedzielna', 'Kielce', 2256);

---- (c)
ALTER TABLE uz
    ADD COLUMN szkola INTEGER REFERENCES uczelnia;
