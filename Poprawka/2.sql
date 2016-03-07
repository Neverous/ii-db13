-- Zadanie 2
SELECT nazwa, kod_sez, COUNT(DISTINCT zgloszenie.kod_uz) AS count
FROM        sezon
    JOIN    zadanie USING (kod_sez)
    JOIN    zgloszenie USING (kod_zad)
WHERE zgloszenie.czas_zgl > sezon.data_stop OR zgloszenie.czas_zgl < sezon.data_start
GROUP BY nazwa, kod_sez
ORDER BY count DESC;
