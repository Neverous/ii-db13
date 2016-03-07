-- 33
SELECT semestr_id
FROM        semestr
    JOIN    przedmiot_semestr   USING(semestr_id)
    JOIN    przedmiot           USING(kod_przed)
WHERE   przedmiot.rodzaj = 'o'
GROUP BY semestr_id
ORDER BY COUNT(DISTINCT przedmiot.kod_przed)
LIMIT 1;
