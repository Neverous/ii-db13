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
