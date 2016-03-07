-- 4
SELECT COUNT(DISTINCT kod_grupy)
FROM        grupa
    JOIN    przedmiot_semestr   USING(kod_przed_sem)
    JOIN    przedmiot           USING(kod_przed)
    JOIN    uzytkownik          USING(kod_uz)
WHERE   uzytkownik.nazwisko = 'Kanarek'
    AND grupa.rodzaj_zajec  = 'r';
