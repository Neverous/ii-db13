-- Bieńkowski,Paluch,Stachowiak,Sysło
SELECT STRING_AGG(DISTINCT nazwisko, ',' ORDER BY nazwisko ASC)
FROM        uzytkownik
    JOIN    grupa               USING(kod_uz)
    JOIN    przedmiot_semestr   USING(kod_przed_sem)
    JOIN    przedmiot           USING(kod_przed)
    JOIN    semestr             USING(semestr_id)
WHERE   semestr.nazwa   = 'Semestr zimowy 2010/2011'
    AND przedmiot.nazwa = 'Matematyka dyskretna (M)';
