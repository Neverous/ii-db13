-- 107
SELECT COUNT(*)
FROM (
    SELECT DISTINCT uzytkownik.kod_uz
    FROM        uzytkownik
        JOIN    wybor               USING(kod_uz)
        JOIN    grupa               USING(kod_grupy)
        JOIN    przedmiot_semestr   USING(kod_przed_sem)
        JOIN    przedmiot           USING(kod_przed)
    WHERE   przedmiot.nazwa = 'Algorytmy i struktury danych (M)'
    GROUP BY uzytkownik.kod_uz
    HAVING COUNT(DISTINCT semestr_id) > 1
) _;
