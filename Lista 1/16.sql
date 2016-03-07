-- 6
SELECT COUNT(DISTINCT kod_grupy)
FROM        grupa
    JOIN    przedmiot_semestr   USING(kod_przed_sem)
    JOIN    przedmiot           USING(kod_przed)
    JOIN    uzytkownik          USING(kod_uz)
WHERE   przedmiot.nazwa     LIKE 'Logika dla informatyków'
    AND uzytkownik.nazwisko = 'Charatonik';
