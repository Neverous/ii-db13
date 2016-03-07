-- 43
SELECT COUNT(DISTINCT kod_przed)
FROM            przedmiot
    LEFT JOIN   przedmiot_semestr   USING(kod_przed)
WHERE   przedmiot.rodzaj = 'k'
    AND kod_przed_sem IS NULL;
