SELECT DISTINCT kod_uz, imie, nazwisko
FROM        uzytkownik AS uzytkownik1
    JOIN    grupa                                       USING(kod_uz)
    JOIN    przedmiot_semestr AS przedmiot_semestr1     USING(kod_przed_sem)
    JOIN    przedmiot                                   USING(kod_przed)
WHERE   przedmiot.nazwa LIKE 'Logika%'
    AND EXISTS
    (
        SELECT *
        FROM        uzytkownik
            JOIN    grupa               USING(kod_uz)
            JOIN    przedmiot_semestr   USING(kod_przed_sem)
            JOIN    przedmiot           USING(kod_przed)
        WHERE   przedmiot.nazwa LIKE 'Algorytmy%'
            AND semestr_id > przedmiot_semestr1.semestr_id
            AND kod_uz = uzytkownik1.kod_uz
    );
