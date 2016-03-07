-- 22
SELECT EXTRACT(DAY FROM '23:59:59' + MAX(data) - MIN(data))
FROM        wybor
    JOIN    grupa               USING(kod_grupy)
    JOIN    przedmiot_semestr   USING(kod_przed_sem)
    JOIN    przedmiot           USING(kod_przed)
    JOIN    semestr             USING(semestr_id)
WHERE   semestr.nazwa       = 'Semestr zimowy 2010/2011'
    AND przedmiot.nazwa     = 'Matematyka dyskretna (M)'
    AND grupa.rodzaj_zajec  = 'w';
