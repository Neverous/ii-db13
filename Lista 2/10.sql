WITH
    semestr_osoba AS
    (
        SELECT nazwa, semestr_id, imie, nazwisko, MAX(data) - MIN(data) AS czas
        FROM        semestr
            JOIN    przedmiot_semestr   USING(semestr_id)
            JOIN    grupa               USING(kod_przed_sem)
            JOIN    wybor               USING(kod_grupy)
            JOIN    uzytkownik          ON uzytkownik.kod_uz = wybor.kod_uz
        GROUP BY nazwa, uzytkownik.kod_uz, nazwisko, semestr_id
    ),

    semestr_zapis AS
    (
        SELECT nazwa, semestr_id, MIN(czas) AS czas
        FROM semestr_osoba
        GROUP BY nazwa, semestr_id
    )
SELECT nazwa, imie, nazwisko
FROM        semestr_osoba
    JOIN    semestr_zapis USING(nazwa, czas, semestr_id)
GROUP BY nazwa, imie, nazwisko, semestr_id
ORDER BY semestr_id, nazwisko
