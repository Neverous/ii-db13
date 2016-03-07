SELECT imie, nazwisko
FROM autorzy_wg_kategorii
WHERE   katA + katB > 10
    AND katC + katD + katE + katF + katInne < 20
ORDER BY nazwisko, imie
