WITH
    uczestnicy_jfizo AS
    (
        SELECT DISTINCT uzytkownik.kod_uz, imie, nazwisko, semestr_id
        FROM        uzytkownik
            JOIN    wybor               USING(kod_uz)
            JOIN    grupa               USING(kod_grupy)
            JOIN    przedmiot_semestr   USING(kod_przed_sem)
            JOIN    przedmiot           USING(kod_przed)
        WHERE przedmiot.nazwa = 'Języki formalne i złożoność obliczeniowa'
    )
SELECT kod_uz, imie, nazwisko
FROM uczestnicy_jfizo
GROUP BY kod_uz, imie, nazwisko
HAVING COUNT(DISTINCT semestr_id) > 2;
