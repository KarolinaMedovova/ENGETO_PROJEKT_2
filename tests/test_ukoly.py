#import os
import pytest
import mysql.connector
from dotenv import load_dotenv
load_dotenv()
#from mysql.connector import Error
from app.db import pridat_ukol_db, zobrazit_ukoly_db, aktualizovat_ukol_db, odstranit_ukol_db


# Pozitivní test funkce přidat úkol:
def test_pridat_ukol_pozitivni(connection_test_db):
    pridat_ukol_db(connection_test_db,"Název č.1", "Popis č.1")
    cursor = connection_test_db.cursor()
    cursor.execute("SELECT * FROM ukoly WHERE nazev = %s", ("Název č.1",))
    vysledek = cursor.fetchone()
    #assert vysledek is not None
    assert vysledek[1] == "Název č.1"
    assert vysledek[2] == "Popis č.1"
    assert vysledek[3] == "nezahájeno"
    #cursor.fetchall()
    cursor.execute("DELETE FROM ukoly WHERE nazev = %s", ("Název č.1",))
    connection_test_db.commit()
    cursor.close()


# Negativní test funkce přidat úkol:
def test_pridat_ukol_negativni(connection_test_db):
    ok, chyba = pridat_ukol_db(connection_test_db, " ", " ")
    assert ok is False
    assert chyba is not None
    cursor = connection_test_db.cursor()
    cursor.execute("SELECT * FROM ukoly WHERE nazev = %s", (" ",))
    vysledek = cursor.fetchall()
    assert vysledek == []
    #assert len(vysledek) == 0
    cursor.close()


# Pozitivní test funkce aktualizovat úkol:
def test_aktualizovat_ukol_pozitivni(connection_test_db):
    pridat_ukol_db(connection_test_db,"Název č.2", "Popis č.2")
    cursor = connection_test_db.cursor()
    cursor.execute("SELECT * FROM ukoly WHERE nazev = %s", ("Název č.2", ))
    vysledek = cursor.fetchone()
    assert vysledek is not None
    assert vysledek[1] == "Název č.2"
    id_ukolu = vysledek[0]
    ok, chyba = aktualizovat_ukol_db(connection_test_db, id_ukolu, "hotovo")
    assert ok is True
    assert chyba is None
    cursor.execute("SELECT stav FROM ukoly WHERE id=%s", (id_ukolu,))
    novy_stav = cursor.fetchone()[0]
    assert novy_stav == "hotovo"
    cursor.execute("DELETE FROM ukoly WHERE id = %s", (id_ukolu,))
    connection_test_db.commit()
    cursor.close()


# Negativní test funkce aktualizovat úkol:
def test_aktualizovat_ukol_negativni(connection_test_db):
    pridat_ukol_db(connection_test_db, "Úklid", "Koupelna")
    cursor = connection_test_db.cursor()
    cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Úklid",))
    id_ukolu = cursor.fetchone()[0]
    neexistujici_ukol = id_ukolu + 1
    # nebo taky velmi spolehlivé je extrémně vysoké číslo, napr. neexistujici_ukol2 = 999999
    ok, chyba = aktualizovat_ukol_db(connection_test_db, neexistujici_ukol, "hotovo")
    assert ok is False
    assert chyba is not None
    cursor.execute("DELETE FROM ukoly WHERE id = %s", (id_ukolu,))
    connection_test_db.commit()
    cursor.close()


# Pozitivní test funce odstranit úkol :
def test_odstranit_ukol_pozitivni(connection_test_db):
    pridat_ukol_db(connection_test_db, "Odstranit ukol", "Odstranit pomocí id")
    cursor = connection_test_db.cursor()
    cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Odstranit ukol",))
    new_id = cursor.fetchone()[0]
    #print(f"---ID nově vloženého ukolu je: {new_id} ---")
    ok, chyba = odstranit_ukol_db(connection_test_db, new_id)
    assert ok is True
    assert chyba is None
    cursor.execute("SELECT id FROM ukoly WHERE id = %s", (new_id,))
    result = cursor.fetchone()              # pokud výsledek selectu je nic, vyhodí to None
    assert result is None
    cursor.close()


# Negativní test funce odstranit úkol :
def test_odstranit_ukol_negativni(connection_test_db):
    cursor = connection_test_db.cursor()
    cursor.execute("SELECT COUNT(*) FROM ukoly ")
    pocet_radku = cursor.fetchone()[0]
    id = 999999
    ok, chyba = odstranit_ukol_db(connection_test_db, id)
    assert ok is False
    assert chyba is not None
    cursor.execute("SELECT COUNT(*) FROM ukoly")
    radky = cursor.fetchone()[0]
    assert pocet_radku == radky
    cursor.close()


# NEPOVINNÉ TESTY
# Pozitivní test pro připojední do testovací DB:
def test_pripojeni_test_db_pozitivni(connection_test_db):
    assert connection_test_db is not None, "Nepodařilo se navázat spojení!"
    assert connection_test_db.is_connected, "Spojení není aktivní!"


# Pozitivní test pro funkci zobrazit úkoly:
def test_zobrazit_ukoly_pozitivni(connection_test_db):
    cursor = connection_test_db.cursor()
    pridat_ukol_db(connection_test_db, "Zobrazení názvu", "Zobrazení popisu")
    connection_test_db.commit()
    vysledek, chyba = zobrazit_ukoly_db(connection_test_db)
    assert len(vysledek) > 0
    assert chyba is None
    assert any(
        radek[1] == "Zobrazení názvu" and radek[2] == "Zobrazení popisu"
        for radek in vysledek
    )
    cursor.close()


# Negativní test pro funkci zobrazit úkoly:
def test_zobrazit_ukoly_negativni(connection_test_db):
    cursor = connection_test_db.cursor()
    cursor.execute("RENAME TABLE ukoly to ukoly_negtest")
    connection_test_db.commit()
    vysledek, chyba = zobrazit_ukoly_db(connection_test_db)
    assert vysledek is None
    assert chyba is not None
    cursor.execute("RENAME TABLE ukoly_negtest to ukoly")
    connection_test_db.commit()
    cursor.close()