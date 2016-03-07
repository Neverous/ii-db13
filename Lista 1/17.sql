-- 34
SELECT COUNT(*)
FROM
(
    SELECT uzytkownik.kod_uz
    FROM        uzytkownik
        JOIN    wybor               USING(kod_uz)
        JOIN    grupa               USING(kod_grupy)
        JOIN    przedmiot_semestr   USING(kod_przed_sem)
        JOIN    przedmiot           USING(kod_przed)
    WHERE przedmiot.nazwa = 'Bazy danych'
    GROUP BY uzytkownik.kod_uz
    HAVING COUNT(DISTINCT semestr_id) >= 2
) _;
