-- Analiza matematyczna
SELECT STRING_AGG(DISTINCT nazwa, ',' ORDER BY nazwa ASC)
FROM        przedmiot
    JOIN    przedmiot_semestr   USING(kod_przed)
    JOIN    grupa               USING(kod_przed_sem)
    JOIN    uzytkownik          USING(kod_uz)
WHERE uzytkownik.nazwisko = 'Urban';
