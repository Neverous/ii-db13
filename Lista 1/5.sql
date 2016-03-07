-- 30
SELECT COUNT(DISTINCT kod_uz)
FROM        uzytkownik
    JOIN    grupa               USING(kod_uz)
    JOIN    przedmiot_semestr   USING(kod_przed_sem)
    JOIN    przedmiot           USING(kod_przed)
    JOIN    semestr             USING(semestr_id)
WHERE   przedmiot.rodzaj = 'o'
    AND semestr.nazwa LIKE '%zimowy%';
