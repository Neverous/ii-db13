-- 19
SELECT COUNT(DISTINCT kod_przed)
FROM        przedmiot
    JOIN    przedmiot_semestr   USING(kod_przed)
    JOIN    grupa               USING(kod_przed_sem)
WHERE   przedmiot.rodzaj    = 'o'
    AND grupa.rodzaj_zajec  = 'e';
