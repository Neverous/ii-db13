/*********************************    5     **********************************/

\i 2.sql
\i 3.sql

-- 1.
CREATE TABLE firma
(
    kod_firmy   SERIAL PRIMARY KEY,
    nazwa       VARCHAR(256) NOT NULL,
    adres       VARCHAR(256) NOT NULL,
    kontakt     VARCHAR(256) NOT NULL
);

-- 2.
INSERT INTO firma(nazwa, adres, kontakt)
VALUES
    ('SNS', 'Wrocław', 'H.Kloss'),
    ('BIT', 'Kraków', 'R.Bruner'),
    ('MIT', 'Berlin', 'J.Kos');

-- 3.
CREATE TABLE oferta_praktyki
(
    kod_oferty      SERIAL PRIMARY KEY,
    kod_firmy       INTEGER REFERENCES firma,
    semestr_id      INTEGER REFERENCES semestr,
    liczba_miejsc   INTEGER
);

-- 4.
INSERT INTO oferta_praktyki(kod_firmy, semestr_id, liczba_miejsc)
SELECT kod_firmy, semestr_id, 3
FROM firma, semestr
WHERE firma.nazwa = 'SNS' AND semestr.rok = '2013/2014' AND semestr.semestr = 'letni';

INSERT INTO oferta_praktyki(kod_firmy, semestr_id, liczba_miejsc)
SELECT kod_firmy, semestr_id, 2
FROM firma, semestr
WHERE firma.nazwa = 'MIT' AND semestr.rok = '2013/2014' AND semestr.semestr = 'letni';

-- 5.
CREATE TABLE praktyki
(
    student INTEGER REFERENCES student,
    opiekun INTEGER REFERENCES pracownik,
    oferta  INTEGER REFERENCES oferta_praktyki
);

-- 6.
-- ??

-- 7.
(
    SELECT student.*
    FROM        student
    WHERE   6 <= student.semestr AND student.semestr <= 10
)
EXCEPT
(
    SELECT student.*
    FROM        student
        JOIN    wybor               USING(kod_uz)
        JOIN    grupa               USING(kod_grupy)
        JOIN    przedmiot_semestr   USING(kod_przed_sem)
        JOIN    przedmiot           USING(kod_przed)
    WHERE   6 <= student.semestr AND student.semestr <= 10
        AND przedmiot.nazwa = 'Praktyka zawodowa'
);

-- 8.
DELETE FROM oferta_praktyki
WHERE NOT EXISTS (SELECT * FROM praktyki WHERE oferta = oferta_praktyki.kod_oferty);

DELETE FROM firma
WHERE NOT EXISTS (SELECT * FROM oferta_praktyki WHERE oferta_praktyki.kod_firmy = firma.kod_firmy);
