SELECT AVG(count)
FROM
(
    SELECT COUNT(DISTINCT kod_grupy) as count
    FROM        semestr
        JOIN    przedmiot_semestr   USING(semestr_id)
        JOIN    grupa               USING(kod_przed_sem)
    WHERE grupa.rodzaj_zajec = 'w'
    GROUP BY semestr_id
) AS CNT;
