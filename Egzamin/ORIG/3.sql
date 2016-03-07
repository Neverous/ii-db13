-- Źle
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
