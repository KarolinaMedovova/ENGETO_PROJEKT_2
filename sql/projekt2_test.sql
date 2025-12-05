-- Vytvoření Databáze, pokud neexistuje
CREATE DATABASE IF NOT EXISTS projekt2_test;

-- Přepnutí od této databáze
USE projekt2_test;

-- Vytvoření tabulky, pokud neexistuje
CREATE TABLE IF NOT EXISTS ukoly (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazev TEXT NOT NULL,
    popis TEXT NOT NULL,
    stav VARCHAR(20) NOT NULL DEFAULT 'nezahájeno',
    datum_vytvoreni DATE NOT NULL DEFAULT (CURRENT_DATE)
);
