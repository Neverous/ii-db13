(
    SELECT DISTINCT kod, nick AS nazwa
    FROM
    (
        SELECT kod_uz AS kod, nick, kod_sez
        FROM uz, sezon
        WHERE imie IS NULL AND nazwisko IS NULL
        EXCEPT
        (
            SELECT kod_uz as kod, nick, zadanie.kod_sez AS sezon
            FROM        uz
                JOIN    zgloszenie USING(kod_uz)
                JOIN    zadanie USING(kod_zad)
        )
    ) AS X
)
UNION
(
    SELECT DISTINCT kod, imie || ' ' || nazwisko AS nazwa
    FROM
    (
        SELECT kod_uz AS kod, imie, nazwisko, kod_sez
        FROM uz, sezon
        WHERE imie IS NOT NULL AND nazwisko IS NOT NULL
        EXCEPT
        (
            SELECT kod_uz as kod, imie, nazwisko, zadanie.kod_sez AS sezon
            FROM        uz
                JOIN    zadanie ON zadanie.autor = uz.kod_uz
        )

    ) AS Y
)
