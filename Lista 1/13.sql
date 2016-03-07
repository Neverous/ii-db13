-- 2009-09-25,2010-01-19
SELECT cast(MIN(data) AS DATE) || ',' || cast(MAX(data) AS DATE)
FROM        wybor
    JOIN    grupa               USING(kod_grupy)
    JOIN    przedmiot_semestr   USING(kod_przed_sem)
    JOIN    semestr             USING(semestr_id)
WHERE semestr.nazwa = 'Semestr zimowy 2009/2010';
