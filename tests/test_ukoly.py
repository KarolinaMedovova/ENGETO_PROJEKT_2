#import os
import pytest
import mysql.connector
from dotenv import load_dotenv
load_dotenv()
from mysql.connector import Error
from app.db import zobrazit_ukoly_db


def test_pridat_ukol_pozitivni(connection_test_db):
    cursor = connection_test_db.cursor()
    cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", ("Název č.1", "Popis č.1",))
    connection_test_db.commit()
    cursor.execute("SELECT * FROM ukoly WHERE nazev = %s", ("Název č.1",))
    vysledek = cursor.fetchone()
    assert vysledek is not None
    cursor.fetchall()
    cursor.execute("DELETE FROM ukoly WHERE nazev = %s", ("Název č.1",))
    connection_test_db.commit()
    cursor.close()


def test_pridat_ukol_negativni(connection_test_db):
    cursor = connection_test_db.cursor()
    with pytest.raises(mysql.connector.errors.IntegrityError):
        cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", (None, None,))
    cursor.close()


def test_aktualizovat_ukol_pozitivni(connection_test_db):
    cursor = connection_test_db.cursor()
    cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", ("Vaření", "Polévka,"))
    connection_test_db.commit()
    cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Vaření",))
    vysledek = cursor.fetchone()
    id_ukolu = vysledek[0]
    # lze zkrátit jako id_ukolu = cursor.fetchone()[0]. ale pro případný print je lepší varianta se dvěma řádky!
    cursor.execute("UPDATE ukoly SET stav = 'probíhá' WHERE id =%s", (id_ukolu,))
    connection_test_db.commit()
    cursor.execute("SELECT stav FROM ukoly WHERE id=%s", (id_ukolu,))
    stav = cursor.fetchone()[0]
    assert stav == "probíhá"
    cursor.execute("DELETE FROM ukoly WHERE id = %s", (id_ukolu,))
    connection_test_db.commit()
    cursor.close()


def test_aktualizovat_ukol_negativni(connection_test_db):
    cursor = connection_test_db.cursor()
    cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", ("Úklid", "Kuchyň",))
    connection_test_db.commit()
    cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Úklid",))
    id_ukolu = cursor.fetchone()[0]
    print(f"ID posledního ukolu je: {id_ukolu}")
    cursor.execute("UPDATE ukoly SET stav='hovovo' WHERE id=%s", (id_ukolu+1,))
    connection_test_db.commit()
    assert cursor.rowcount == 0
    cursor.execute("DELETE FROM ukoly WHERE id = %s", (id_ukolu,))
    connection_test_db.commit()
    cursor.close()



def test_odstranit_ukol_pozitivni(connection_test_db):
    cursor = connection_test_db.cursor()
    cursor.execute("SELECT * FROM ukoly")
    original_ids = cursor.fetchall()
    cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", ("Odstranit ukol", "Odstranit pomocí id",))
    connection_test_db.commit()
    new_id = cursor.lastrowid
    print(f"---ID nově vloženého ukolu je a bylo {new_id} ---")
    cursor.execute("SELECT * FROM ukoly")
    next_ids = cursor.fetchall()
    cursor.execute("DELETE FROM ukoly WHERE id = %s", (new_id,))
    connection_test_db.commit()
    cursor.execute("SELECT * FROM ukoly")
    finally_ids = cursor.fetchall()
    assert original_ids == finally_ids
    cursor.close()


def test_odstranit_ukol_negativni(connection_test_db):
    cursor = connection_test_db.cursor()
    cursor.execute("SELECT * FROM ukoly")
    rows_before = cursor.fetchall()
    ids = []
    for i in rows_before:
        ids.append(i[0])
    #print(f"Seznam všech id = {ids}.")
    cursor.execute("DELETE FROM ukoly WHERE id = %s", (19,))
    connection_test_db.commit()
    assert cursor.rowcount == 0
    cursor.execute("SELECT * FROM ukoly")
    rows_after = cursor.fetchall()
    assert rows_before == rows_after
    cursor.close()



# není potřeba, nebylo v zadání :
def test_pripojeni_test_db(connection_test_db):
    assert connection_test_db is not None, "Nepodařilo se navázat spojení!"
    assert connection_test_db.is_connected, "Spojení není aktivní!"


def test_zobrazit_ukoly_pozitivni(connection_test_db):
    cursor = connection_test_db.cursor()
    cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", ("Název č.10", "Popis č.10",))
    cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", ("Název č.20", "Popis č.20",))
    connection_test_db.commit()
    cursor.execute("SELECT * FROM ukoly WHERE stav = 'nezahájeno' or stav = 'probíhá'")
    vysledek = cursor.fetchall()
    assert vysledek
    cursor.close()

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