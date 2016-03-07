/*********************************    2     **********************************/

\i 1.sql

-- 0.
INSERT INTO semestr
VALUES
    (nextval('numer_semestru'), 'zimowy', '2013/2014'),
    (nextval('numer_semestru'), 'letni', '2013/2014');

-- 1.
CREATE SEQUENCE numer_przedmiot_semestr;
SELECT setval('numer_przedmiot_semestr', MAX(kod_przed_sem))
FROM przedmiot_semestr;

CREATE SEQUENCE numer_grupy;
SELECT setval('numer_grupy', MAX(kod_grupy))
FROM grupa;

-- 2.
INSERT INTO przedmiot_semestr
SELECT nextval('numer_przedmiot_semestr'), semestr_id, kod_przed
FROM przedmiot, semestr
WHERE   (semestr.semestr = 'zimowy' OR semestr.semestr = 'letni')
    AND semestr.rok     = '2013/2014'
    AND (przedmiot.rodzaj = 'o' OR przedmiot.rodzaj = 'p');

-- 3.
ALTER TABLE grupa
ALTER kod_uz DROP NOT NULL;

INSERT INTO grupa
SELECT nextval('numer_grupy'), kod_przed_sem, NULL, 100, 'w', NULL, NULL
FROM        semestr
    JOIN    przedmiot_semestr   USING(semestr_id)
    JOIN    przedmiot           USING(kod_przed)
WHERE   (semestr.semestr = 'zimowy' OR semestr.semestr = 'letni')
    AND semestr.rok     = '2013/2014'
    AND (przedmiot.rodzaj = 'o' OR przedmiot.rodzaj = 'p');

-- 4.
SELECT *
FROM        grupa
    JOIN    przedmiot_semestr   USING(kod_przed_sem)
    JOIN    przedmiot           USING(kod_przed)
    JOIN    semestr             USING(semestr_id)
WHERE   (semestr.semestr = 'zimowy' OR semestr.semestr = 'letni')
    AND semestr.rok     = '2013/2014';
