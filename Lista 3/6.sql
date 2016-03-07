/*********************************    6     **********************************/
\i 3.sql

-- 1.
CREATE VIEW plan_zajec(student_kod, student_nazwisko, semestr_id, przedmiot_kod, przedmiot_nazwa, zajecia_sala, prowadzacy_kod, prowadzacy_nazwisko, termin)
AS
(
    SELECT student.kod_uz, student.nazwisko, przedmiot_semestr.semestr_id, przedmiot.kod_przed, przedmiot.nazwa, grupa.sala, grupa.kod_uz, pracownik.nazwisko, grupa.termin
    FROM        student
        JOIN    wybor               ON student.kod_uz   = wybor.kod_uz
        JOIN    grupa               ON wybor.kod_grupy  = grupa.kod_grupy
        JOIN    pracownik           ON grupa.kod_uz     = pracownik.kod_uz
        JOIN    przedmiot_semestr   USING(kod_przed_sem)
        JOIN    przedmiot           USING(kod_przed)
    ORDER BY grupa.termin
);

-- 2.
SELECT *
FROM plan_zajec
WHERE   student_kod = 2884
    AND semestr_id  = 28
ORDER BY termin;

-- 3.
SELECT DISTINCT semestr_id, przedmiot_kod, przedmiot_nazwa, zajecia_sala, prowadzacy_kod, prowadzacy_nazwisko, termin
FROM plan_zajec
WHERE   prowadzacy_kod  = 166
    AND semestr_id      = 28
ORDER BY termin;

-- 4.
SELECT DISTINCT semestr_id, przedmiot_kod, przedmiot_nazwa, zajecia_sala, prowadzacy_kod, prowadzacy_nazwisko, termin
FROM plan_zajec
WHERE   zajecia_sala    = '119'
    AND semestr_id      = 28
ORDER BY termin;
