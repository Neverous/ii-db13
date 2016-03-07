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
