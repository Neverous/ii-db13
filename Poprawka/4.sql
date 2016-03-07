-- Zadanie 4
---- (a)
CREATE TABLE aktywnosc_w_dniach
(
    data            DATE,
    liczba_zgloszen BIGINT
);

INSERT INTO aktywnosc_w_dniach
SELECT zgloszenie.czas_zgl::DATE AS data, COUNT(*)
FROM    zgloszenie
GROUP BY data;

-- SELECT * FROM aktywnosc_w_dniach ORDER BY liczba_zgloszen DESC;
---- (b)
CREATE FUNCTION zablokuj_zmiane() RETURNS TRIGGER AS $$
    BEGIN
        IF (OLD.czas_zgl IS DISTINCT FROM NEW.czas_zgl) THEN
            RETURN OLD;
        END IF;

        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER zablokuj_zmiane_czasu BEFORE UPDATE ON zgloszenie
FOR EACH ROW
EXECUTE PROCEDURE zablokuj_zmiane();

CREATE FUNCTION zaktualizuj() RETURNS TRIGGER AS $$
    BEGIN
        IF (EXISTS (SELECT * FROM aktywnosc_w_dniach WHERE data = NEW.czas_zgl::DATE)) THEN
            UPDATE aktywnosc_w_dniach
                SET liczba_zgloszen = liczba_zgloszen + 1
            WHERE data = NEW.czas_zgl::DATE;

        ELSE
            INSERT INTO aktywnosc_w_dniach VALUES (NEW.czas_zgl::DATE, 1);
        END IF;

        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER zaktualizuj_statystyki AFTER INSERT ON zgloszenie
FOR EACH ROW
EXECUTE PROCEDURE zaktualizuj();
