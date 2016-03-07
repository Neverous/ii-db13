SELECT DISTINCT kod_uz, imie, nazwisko
FROM        uzytkownik
    JOIN    grupa                                   USING(kod_uz)
    JOIN    przedmiot_semestr AS przedmiot_semestr1 USING(kod_przed_sem)
    JOIN    przedmiot                               USING(kod_przed)
WHERE   przedmiot.nazwa LIKE 'Logika%'
    AND kod_uz IN
    (
        SELECT kod_uz
        FROM        uzytkownik
            JOIN    grupa               USING(kod_uz)
            JOIN    przedmiot_semestr   USING(kod_przed_sem)
            JOIN    przedmiot           USING(kod_przed)
        WHERE   przedmiot.nazwa LIKE 'Algorytmy%'
            AND semestr_id > przedmiot_semestr1.semestr_id
    )
ORDER BY imie;
