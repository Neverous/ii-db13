-- 1
SELECT X.kod, X.nazwa, Y.sezon
FROM
(
    SELECT kod, nazwa, MAX(wynik) AS wynik
    FROM
    (
        SELECT konkurs.kod_kon AS kod, konkurs.nazwa AS nazwa, AVG(wynik) AS wynik
        FROM        konkurs
            JOIN    zadanie     ON zadanie.kod_kon = konkurs.kod_kon
            JOIN    zgloszenie  USING(kod_zad)
        GROUP BY konkurs.kod_kon, konkurs.nazwa, zadanie.kod_sez
    ) AS _
    GROUP BY kod, nazwa
) AS X
JOIN
(
    SELECT konkurs.kod_kon AS kod, konkurs.nazwa AS nazwa, zadanie.kod_sez AS sezon, AVG(wynik) AS wynik
    FROM        konkurs
        JOIN    zadanie     ON zadanie.kod_kon = konkurs.kod_kon
        JOIN    zgloszenie  USING(kod_zad)
    GROUP BY konkurs.kod_kon, konkurs.nazwa, zadanie.kod_sez
) AS Y ON Y.wynik = X.wynik AND Y.kod = X.kod
ORDER BY X.nazwa, X.kod;

-- 2
(
    SELECT DISTINCT kod, nick AS nazwa
    FROM
    (
        SELECT kod_uz AS kod, nick, kod_sez
        FROM uz, sezon
        WHERE imie IS NULL AND nazwisko IS NULL
        EXCEPT
        (
            SELECT kod_uz as kod, nick, zadanie.kod_sez AS sezon
            FROM        uz
                JOIN    zgloszenie USING(kod_uz)
                JOIN    zadanie USING(kod_zad)
        )
    ) AS X
)
UNION
(
    SELECT DISTINCT kod, imie || ' ' || nazwisko AS nazwa
    FROM
    (
        SELECT kod_uz AS kod, imie, nazwisko, kod_sez
        FROM uz, sezon
        WHERE imie IS NOT NULL AND nazwisko IS NOT NULL
        EXCEPT
        (
            SELECT kod_uz as kod, imie, nazwisko, zadanie.kod_sez AS sezon
            FROM        uz
                JOIN    zadanie ON zadanie.autor = uz.kod_uz
        )

    ) AS Y
)

-- 3
-- //Źle
SELECT kod_kon, nazwa
FROM konkurs
WHERE
EXISTS
(
    SELECT kod_uz
    FROM        uz
        JOIN    zadanie AS zadanie1 ON zadanie1.autor = uz.kod_uz
    WHERE (zadanie1.kategoria = 'A' OR zadanie1.kategoria = 'B')
    AND NOT EXISTS
    (
        SELECT kod_zad
        FROM zadanie
        WHERE zadanie.autor = zadanie1.autor AND zadanie.kod_kon = konkurs.kod_kon AND zadanie.kod_zad = zadanie1.kod_zad AND zadanie.kod_sez < zadanie1.kod_sez
    )
)

-- 4b
SELECT imie, nazwisko
FROM autorzy_wg_kategorii
WHERE   katA + katB > 10
    AND katC + katD + katE + katF + katInne < 20
ORDER BY nazwisko, imie

-- 5a
CREATE TABLE kontakt
(
    kod_nad INTEGER REFERENCES uz ON DELETE CASCADE,
    kod_odb INTEGER REFERENCES uz ON DELETE SET NULL,
    tresc   TEXT NOT NULL,
    czas    TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (kod_nad, czas)
);

-- 5b
ALTER TABLE kontakt
    ADD COLUMN kod_kontaktu SERIAL PRIMARY KEY,
    DROP CONSTRAINT kontakt_pkey;

-- 6a
ALTER TABLE zadanie
    ADD COLUMN aktywne BOOLEAN DEFAULT true;

-- 6b
UPDATE zadanie
SET aktywne = false
WHERE zadanie.kod_sez NOT IN
(
    SELECT kod_sez
    FROM sezon
    ORDER BY kod_sez DESC
    LIMIT 2
);
