CREATE TABLE ukoly (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazev TEXT NOT NULL,
    popis TEXT NOT NULL,
    datum_vytvoreni DATE,
    hotovo BOOLEAN DEFAULT FALSE
);
INSERT INTO ukoly(nazev, popis, datum_vytvoreni, hotovo)
VALUES ("Úkol č.1", "Popis č.1", "2025-10-17", FALSE);
SELECT * FROM ukoly;
INSERT INTO ukoly(nazev, popis, datum_vytvoreni, hotovo)
VALUES ("Úkol č.2", "Popis č.2", "2025-10-17", TRUE);
SELECT * FROM ukoly WHERE hotovo=FALSE;
SELECT * FROM ukoly WHERE hotovo=TRUE;
SELECT COUNT(*) FROM ukoly;

UPDATE ukoly
SET hotovo = TRUE
WHERE id = 2;
DELETE FROM ukoly WHERE id = 3;
SELECT COUNT(*) FROM ukoly WHERE hotovo = FALSE;
INSERT INTO ukoly(nazev, popis, datum_vytvoreni, hotovo)
VALUES ("Úkol č.3", "Popis č.3", "2025-10-17", TRUE);
