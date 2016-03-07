UPDATE zadanie
SET aktywne = false
WHERE zadanie.kod_sez NOT IN
(
    SELECT kod_sez
    FROM sezon
    ORDER BY kod_sez DESC
    LIMIT 2
);
