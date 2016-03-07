/*********************************    3     **********************************/

-- 1.
CREATE TABLE pracownik
(
    kod_uz      INTEGER NOT NULL PRIMARY KEY,
    imie        VARCHAR(15) NOT NULL,
    nazwisko    VARCHAR(30) NOT NULL
);

CREATE TABLE student
(
    kod_uz      INTEGER NOT NULL PRIMARY KEY,
    imie        VARCHAR(15) NOT NULL,
    nazwisko    VARCHAR(30) NOT NULL,
    semestr     SMALLINT
);

-- 2.
INSERT INTO pracownik
SELECT DISTINCT kod_uz, imie, nazwisko
FROM        grupa
    JOIN    uzytkownik USING(kod_uz);

-- 3.
INSERT INTO student
SELECT DISTINCT kod_uz, imie, nazwisko, semestr
FROM        wybor
    JOIN    uzytkownik USING(kod_uz);

-- 4.
ALTER TABLE grupa
DROP CONSTRAINT fk_grupa_uz,
ADD CONSTRAINT fk_grupa_uz FOREIGN KEY(kod_uz) REFERENCES pracownik;

ALTER TABLE wybor
DROP CONSTRAINT fk_wybor_uz,
ADD CONSTRAINT fk_wybor_uz FOREIGN KEY(kod_uz) REFERENCES student;

DROP TABLE uzytkownik;
