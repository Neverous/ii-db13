-- 9
SELECT COUNT(kod_grupy)
FROM        grupa
    JOIN    przedmiot_semestr   USING(kod_przed_sem)
    JOIN    przedmiot           USING(kod_przed)
    JOIN    semestr             USING(semestr_id)
WHERE   przedmiot.nazwa     = 'Logika dla informatyków'
    AND semestr.nazwa       = 'Semestr zimowy 2010/2011'
    AND (grupa.rodzaj_zajec  = 'c' OR grupa.rodzaj_zajec = 'C');
