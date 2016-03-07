SELECT nazwa, nazwisko
FROM        uzytkownik
    JOIN    grupa               USING(kod_uz)
    JOIN    przedmiot_semestr   USING(kod_przed_sem)
    JOIN    semestr             USING(semestr_id)
WHERE   grupa.rodzaj_zajec = 'w'
GROUP BY semestr_id, nazwa, kod_uz
HAVING COUNT(DISTINCT kod_grupy) >= 3;
