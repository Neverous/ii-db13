SELECT DISTINCT uzytkownik1.kod_uz, imie, nazwisko
FROM        uzytkownik AS uzytkownik1
    JOIN    wybor               USING(kod_uz)
    JOIN    grupa               USING(kod_grupy)
    JOIN    przedmiot_semestr   USING(kod_przed_sem)
    JOIN    przedmiot           USING(kod_przed)
WHERE   grupa.rodzaj_zajec = 'w'
    AND przedmiot.rodzaj = 'o'
    AND NOT EXISTS
    (
        SELECT *
        FROM        uzytkownik
            JOIN    wybor               USING(kod_uz)
            JOIN    grupa               USING(kod_grupy)
            JOIN    przedmiot_semestr   USING(kod_przed_sem)
            JOIN    przedmiot           USING(kod_przed)
        WHERE   uzytkownik.kod_uz = uzytkownik1.kod_uz
            AND przedmiot.rodzaj = 'k'
    )
ORDER BY nazwisko DESC;
