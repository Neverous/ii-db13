/*********************************    4     **********************************/

-- 1.
CREATE DOMAIN rodzaje_zajec AS char(1)
CHECK ( VALUE IS NOT NULL
    AND VALUE IN (  'w', 'W',
                    'c', 'C',
                    'e', 'E',
                    'p', 'P',
                    'r', 'R',
                    's', 'S' )
);

-- 2.
ALTER TABLE grupa
ALTER COLUMN rodzaj_zajec TYPE rodzaje_zajec;

-- 3.
CREATE VIEW obsada_zajec_view (prac_kod, prac_nazwisko, przed_kod, przed_nazwa, rodzaj_zajec, liczba_grup, liczba_studentow)
AS SELECT pracownik.kod_uz, pracownik.nazwisko, przedmiot.kod_przed, przedmiot.nazwa, grupa.rodzaj_zajec, COUNT(DISTINCT grupa.kod_grupy), COUNT(DISTINCT student.kod_uz)
FROM        grupa
    JOIN    uzytkownik AS pracownik ON grupa.kod_uz = pracownik.kod_uz
    JOIN    przedmiot_semestr   USING(kod_przed_sem)
    JOIN    przedmiot           USING(kod_przed)
    JOIN    wybor               USING(kod_grupy)
    JOIN    uzytkownik AS student ON wybor.kod_uz = student.kod_uz
GROUP BY pracownik.kod_uz, pracownik.nazwisko, przedmiot.kod_przed, przedmiot.nazwa, grupa.rodzaj_zajec;

-- 4.
CREATE TABLE obsada_zajec_tab
(
    prac_kod            INTEGER NOT NULL,
    prac_nazwisko       VARCHAR(30) NOT NULL,
    przed_kod           INTEGER NOT NULL,
    przed_nazwa         TEXT,
    rodzaj_zajec        rodzaje_zajec,
    liczba_grup         INTEGER,
    liczba_studentow    INTEGER
);

INSERT INTO obsada_zajec_tab
SELECT * FROM obsada_zajec_view;

-- 5.
SELECT DISTINCT max_studentow.przed_kod, przed_nazwa, prac_kod, prac_nazwisko, max_studentow.liczba_studentow
FROM
(
    SELECT przed_kod, MAX(liczba_studentow) AS liczba_studentow
    FROM        obsada_zajec_view
        JOIN    przedmiot ON przedmiot.kod_przed = przed_kod
    WHERE (przedmiot.rodzaj = 'o' OR przedmiot.rodzaj = 'p')
    GROUP BY przed_kod
) AS        max_studentow
    JOIN    obsada_zajec_view ON max_studentow.przed_kod = obsada_zajec_view.przed_kod AND max_studentow.liczba_studentow = obsada_zajec_view.liczba_studentow
ORDER BY max_studentow.liczba_studentow, przed_nazwa, prac_nazwisko;
-- > ~1900ms

SELECT DISTINCT max_studentow.przed_kod, przed_nazwa, prac_kod, prac_nazwisko, max_studentow.liczba_studentow
FROM
(
    SELECT przed_kod, MAX(liczba_studentow) AS liczba_studentow
    FROM        obsada_zajec_tab
        JOIN    przedmiot ON przedmiot.kod_przed = przed_kod
    WHERE (przedmiot.rodzaj = 'o' OR przedmiot.rodzaj = 'p')
    GROUP BY przed_kod
) AS        max_studentow
    JOIN    obsada_zajec_tab ON max_studentow.przed_kod = obsada_zajec_tab.przed_kod AND max_studentow.liczba_studentow = obsada_zajec_tab.liczba_studentow
ORDER BY max_studentow.liczba_studentow, przed_nazwa, prac_nazwisko;

-- > ~3ms
