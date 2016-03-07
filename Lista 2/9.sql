SELECT nazwisko --, COUNT(DISTINCT kod_przed)
FROM        uzytkownik
    JOIN    grupa               USING(kod_uz)
    JOIN    przedmiot_semestr   USING(kod_przed_sem)
WHERE grupa.rodzaj_zajec = 'w'
GROUP BY nazwisko
HAVING COUNT(DISTINCT kod_przed) =
    (
        SELECT MAX(count)
        FROM
        (
            SELECT COUNT(DISTINCT kod_przed) AS count
            FROM uzytkownik
                JOIN    grupa               USING(kod_uz)
                JOIN    przedmiot_semestr   USING(kod_przed_sem)
            WHERE grupa.rodzaj_zajec = 'w'
            GROUP BY nazwisko
        ) AS cnt
    );
