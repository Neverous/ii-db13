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
