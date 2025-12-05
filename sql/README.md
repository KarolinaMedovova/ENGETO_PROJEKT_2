## Nastavení databáze

Projekt používá MySQL databázi. V repozitáři najdete složku 'sql/' se dvěma soubory:
- projekt2.sql → ostrá databáze
- projekt2_test.sql → testovací databáze pro pytest testy


Obě databáze obsahují tabulku 'ukoly' se sloupci:
- id – primární klíč, AUTO_INCREMENT
- nazev – název úkolu (VARCHAR)
- popis – popis úkolu (TEXT)
- stav – stav úkolu (nezahájeno, probíhá, hotovo)
- datum_vytvoreni – datum vytvoření (automaticky dnešní)


## Spuštění:
Spusťte skripty v MySQL Workbench nebo přes terminál:

'''bash
# vytvoření ostré databáze
mysql -u USER -p < projekt2.sql

# vytvoření testovací databáze
mysql -u USER -p < projekt2_test.sql
