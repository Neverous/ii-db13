-- Zadanie 1
SELECT autor.nazwisko, autor.kod_uz, uzytkownik.kod_uz, uzytkownik.nick
FROM        uz AS autor
    JOIN    zadanie ON (zadanie.autor = autor.kod_uz)
    JOIN    zgloszenie ON (zadanie.kod_zad = zgloszenie.kod_zad)
    JOIN    uz AS uzytkownik ON (zgloszenie.kod_uz = uzytkownik.kod_uz)
WHERE zgloszenie.wynik = 100 AND zgloszenie.czas_zgl >= (
    SELECT MAX(zgloszenie.czas_zgl)
    FROM        uz
        JOIN    zadanie ON (zadanie.autor = uz.kod_uz)
        JOIN    zgloszenie ON (zadanie.kod_zad = zgloszenie.kod_zad)
    WHERE zgloszenie.wynik = 100 AND uz.kod_uz = autor.kod_uz)
ORDER BY autor.kod_uz ASC, autor.nazwisko ASC, uzytkownik.kod_uz ASC, uzytkownik.nick ASC;

-- Zadanie 2
SELECT nazwa, kod_sez, COUNT(DISTINCT zgloszenie.kod_uz) AS count
FROM        sezon
    JOIN    zadanie USING (kod_sez)
    JOIN    zgloszenie USING (kod_zad)
WHERE zgloszenie.czas_zgl > sezon.data_stop OR zgloszenie.czas_zgl < sezon.data_start
GROUP BY nazwa, kod_sez
ORDER BY count DESC;

-- Zadanie 3
SELECT DISTINCT uzytkownik.kod_uz, uzytkownik.nick, zadanie1.kod_zad
FROM        uz AS uzytkownik
    JOIN    zgloszenie          ON (zgloszenie.kod_uz = uzytkownik.kod_uz)
    JOIN    zadanie             ON (zadanie.kod_zad = zgloszenie.kod_zad)
    JOIN    sezon               ON (sezon.kod_sez = zadanie.kod_sez)
    JOIN    konkurs             ON (konkurs.kod_kon = zadanie.kod_kon),
            zadanie AS zadanie1
    JOIN    konkurs AS konkurs1 ON (konkurs1.kod_kon = zadanie1.kod_kon)
    JOIN    sezon AS sezon1     ON (sezon1.kod_sez = zadanie1.kod_sez)
WHERE   sezon.nazwa     = 'Sezon letni 2010'
    AND konkurs.nazwa   = 'Bazy danych'
    AND sezon1.nazwa    = 'Sezon letni 2010'
    AND konkurs1.nazwa  = 'Bazy danych'
    AND NOT EXISTS (
        SELECT *
        FROM zgloszenie
        WHERE   zgloszenie.kod_zad = zadanie1.kod_zad
            AND zgloszenie.kod_uz = uzytkownik.kod_uz);

-- Zadanie 4
---- (a)
CREATE TABLE aktywnosc_w_dniach
(
    data            DATE,
    liczba_zgloszen BIGINT
);

INSERT INTO aktywnosc_w_dniach
SELECT zgloszenie.czas_zgl::DATE AS data, COUNT(*)
FROM    zgloszenie
GROUP BY data;

-- SELECT * FROM aktywnosc_w_dniach ORDER BY liczba_zgloszen DESC;
---- (b)
CREATE FUNCTION zablokuj_zmiane() RETURNS TRIGGER AS $$
    BEGIN
        IF (OLD.czas_zgl IS DISTINCT FROM NEW.czas_zgl) THEN
            RETURN OLD;
        END IF;

        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER zablokuj_zmiane_czasu BEFORE UPDATE ON zgloszenie
FOR EACH ROW
EXECUTE PROCEDURE zablokuj_zmiane();

CREATE FUNCTION zaktualizuj() RETURNS TRIGGER AS $$
    BEGIN
        IF (EXISTS (SELECT * FROM aktywnosc_w_dniach WHERE data = NEW.czas_zgl::DATE)) THEN
            UPDATE aktywnosc_w_dniach
                SET liczba_zgloszen = liczba_zgloszen + 1
            WHERE data = NEW.czas_zgl::DATE;

        ELSE
            INSERT INTO aktywnosc_w_dniach VALUES (NEW.czas_zgl::DATE, 1);
        END IF;

        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER zaktualizuj_statystyki AFTER INSERT ON zgloszenie
FOR EACH ROW
EXECUTE PROCEDURE zaktualizuj();

-- Zadanie 5
---- (a)
CREATE OR REPLACE VIEW kategorie_zadan (nazwa, liczba_zadan) AS
SELECT zadanie.kategoria AS nazwa, COUNT(DISTINCT kod_zad)
FROM    zadanie
GROUP BY zadanie.kategoria;

---- (b)
CREATE OR REPLACE RULE wstaw_kategorie AS ON INSERT
TO kategorie_zadan
DO INSTEAD INSERT INTO zadanie VALUES (
    (SELECT MAX(kod_zad) + 1 FROM zadanie),
    (SELECT MAX(kod_kon) FROM konkurs),
    (SELECT MAX(kod_sez) FROM sezon),
    NULL,
    NEW.nazwa,
    0,
    0);

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

-- Zadanie 7
CREATE OR REPLACE FUNCTION ranking(kod_zad INTEGER) RETURNS TABLE(uz INTEGER, wynik INTEGER, czas_zgl TIMESTAMP, uz_max INTEGER, wynik_max INTEGER) AS $$
    SELECT DISTINCT uz, X.wynik, czas_zgl, Y.uz_max, wynik_max
    FROM (
        SELECT zgloszenie.kod_uz AS uz, zgloszenie.wynik AS wynik, zgloszenie.czas_zgl AS czas_zgl, MAX(zgloszenie1.wynik) AS wynik_max
        FROM    zgloszenie, zgloszenie AS zgloszenie1
        WHERE   zgloszenie.kod_zad = $1
            AND zgloszenie1.kod_zad = $1
            AND zgloszenie1.czas_zgl <= zgloszenie.czas_zgl
        GROUP BY zgloszenie.kod_uz, zgloszenie.wynik, zgloszenie.czas_zgl
    ) AS X
    JOIN
    (
        SELECT zgloszenie1.kod_uz AS uz_max, zgloszenie1.wynik AS wynik
        FROM    zgloszenie, zgloszenie AS zgloszenie1
        WHERE   zgloszenie.kod_zad = $1
            AND zgloszenie1.kod_zad = $1
            AND zgloszenie1.czas_zgl <= zgloszenie.czas_zgl
    ) AS Y ON (X.wynik_max = Y.wynik)
    ORDER BY wynik DESC;
$$ LANGUAGE SQL;

--SELECT * FROM ranking(4703);
