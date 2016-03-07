SELECT nazwa, COUNT(DISTINCT kod_uz)
FROM            przedmiot
    LEFT JOIN   przedmiot_semestr   USING(kod_przed)
    LEFT JOIN   grupa               USING(kod_przed_sem)
GROUP BY kod_przed
--HAVING COUNT(DISTINCT kod_uz) = 0
ORDER BY count DESC;
