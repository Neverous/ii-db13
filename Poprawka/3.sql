-- Zadanie 3
SELECT DISTINCT uzytkownik.kod_uz, uzytkownik.nick, zadanie1.kod_zad
FROM        uz AS uzytkownik
    JOIN    zgloszenie          ON (zgloszenie.kod_uz = uzytkownik.kod_uz)
    JOIN    zadanie             ON (zadanie.kod_zad = zgloszenie.kod_zad)
    JOIN    sezon               ON (sezon.kod_sez = zadanie.kod_sez)
    JOIN    konkurs             ON (konkurs.kod_kon = zadanie.kod_kon),
            zadanie AS zadanie1
    JOIN    konkurs AS konkurs1 ON (konkurs1.kod_kon = zadanie1.kod_kon)
    JOIN    sezon AS sezon1     ON (sezon1.kod_sez = zadanie1.kod_sez)
WHERE   sezon.nazwa     = 'Sezon letni 2010'
    AND konkurs.nazwa   = 'Bazy danych'
    AND sezon1.nazwa    = 'Sezon letni 2010'
    AND konkurs1.nazwa  = 'Bazy danych'
    AND NOT EXISTS (
        SELECT *
        FROM zgloszenie
        WHERE   zgloszenie.kod_zad = zadanie1.kod_zad
            AND zgloszenie.kod_uz = uzytkownik.kod_uz);
