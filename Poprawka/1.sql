-- Zadanie 1
SELECT autor.nazwisko, autor.kod_uz, uzytkownik.kod_uz, uzytkownik.nick
FROM        uz AS autor
    JOIN    zadanie ON (zadanie.autor = autor.kod_uz)
    JOIN    zgloszenie ON (zadanie.kod_zad = zgloszenie.kod_zad)
    JOIN    uz AS uzytkownik ON (zgloszenie.kod_uz = uzytkownik.kod_uz)
WHERE zgloszenie.wynik = 100 AND zgloszenie.czas_zgl >= (
    SELECT MAX(zgloszenie.czas_zgl)
    FROM        uz
        JOIN    zadanie ON (zadanie.autor = uz.kod_uz)
        JOIN    zgloszenie ON (zadanie.kod_zad = zgloszenie.kod_zad)
    WHERE zgloszenie.wynik = 100 AND uz.kod_uz = autor.kod_uz)
ORDER BY autor.kod_uz ASC, autor.nazwisko ASC, uzytkownik.kod_uz ASC, uzytkownik.nick ASC;
