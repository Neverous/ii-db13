(
    SELECT DISTINCT uzytkownik.kod_uz, imie, nazwisko
    FROM        uzytkownik
        JOIN    wybor               USING(kod_uz)
        JOIN    grupa               USING(kod_grupy)
        JOIN    przedmiot_semestr   USING(kod_przed_sem)
        JOIN    przedmiot           USING(kod_przed)
    WHERE   grupa.rodzaj_zajec = 'w'
        AND przedmiot.rodzaj = 'o'
)
EXCEPT
(
    SELECT uzytkownik.kod_uz, imie, nazwisko
    FROM        uzytkownik
        JOIN    wybor               USING(kod_uz)
        JOIN    grupa               USING(kod_grupy)
        JOIN    przedmiot_semestr   USING(kod_przed_sem)
        JOIN    przedmiot           USING(kod_przed)
    WHERE przedmiot.rodzaj = 'k'
)
ORDER BY nazwisko;
