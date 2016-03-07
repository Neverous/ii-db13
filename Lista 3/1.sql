/*********************************    1     **********************************/

-- 1.
CREATE DOMAIN semestry AS varchar(8)
CHECK ( VALUE IN ('zimowy', 'letni')
    AND VALUE IS NOT NULL);


-- 2.
CREATE SEQUENCE numer_semestru;
SELECT setval('numer_semestru', MAX(semestr_id))
FROM semestr;


-- 3. / 6.
ALTER TABLE semestr
ADD COLUMN semestr semestry DEFAULT
CASE
    WHEN    1 <= EXTRACT(MONTH FROM NOW())
        AND EXTRACT(MONTH FROM NOW()) <= 6
        THEN 'letni'
    ELSE 'zimowy'
END,
ADD COLUMN rok char(9) DEFAULT
CASE
    WHEN    1 <= EXTRACT(MONTH FROM NOW())
        AND EXTRACT(MONTH FROM NOW()) <= 6
        THEN EXTRACT(YEAR FROM NOW()) - 1 || '/' || EXTRACT(YEAR FROM NOW())
    ELSE EXTRACT(YEAR FROM NOW()) || '/' || EXTRACT(YEAR FROM NOW()) + 1
END;

-- 4.
UPDATE semestr
SET
    semestr = split_part(semestr.nazwa, ' ', 2),
    rok     = split_part(semestr.nazwa, ' ', 3);

-- 5.
ALTER TABLE semestr
DROP COLUMN nazwa;

/*
INSERT INTO semestr VALUES(90);

SELECT * FROM semestr ORDER BY semestr_id DESC LIMIT 10;
*/
