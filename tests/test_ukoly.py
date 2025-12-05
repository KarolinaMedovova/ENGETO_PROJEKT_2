# import os
import pytest
import mysql.connector
from dotenv import load_dotenv
load_dotenv()
from mysql.connector import Error
#from app.P2_mysql import pridat_ukol, aktualizovat_ukol, odstranit_ukol



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









"""
def pripojeni_test_db():
    try:                                            # ZKUS PROVÉST NÁSLEDUJÍCÍ, A POKUD NASTANE CHYBY, PŘEJDI DO EXCEPT
        spojeni = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME_TEST")
        )
        if spojeni.is_connected():                  # FUNKCE IS.CONNECTED VRACÍ TRUE, POKUD JE SPOJENÍ AKTIVNÍ
            #print("✅ Připojení k databázi projekt2_test bylo úspěšné.")
            return spojeni 
    except Error as chyba:                          # POKUD NASTANE JAKÁKOLI CHYBA PŘI PŘIPOJENÍ, SKOČ SEM
        print(f"❌ Chyba při připojení: {chyba}")
        return None                                 # POKUD SE PŘIPOJENÍ NEZDAŘÍ, FUNKCE VRÁTÍ NONE = TEDY NIC

            
#funkce pro připojení do produkční databáze
def pripojeni_prod_db():
    try:
        spojeni = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        if spojeni.is_connected():
            #print("Připojení k databázi 'projekt2" bylo úspěšné.")
            return spojeni
    except Error as chyba:
        print(f"❌ Chyba při připojení: {chyba}")
        return None


    
není potřeba, nebylo v zadání...
def test_zobrazit_ukoly_pozitivni(connection_test_db):
    cursor = connection_test_db.cursor()
    cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", ("Název č.10", "Popis č.10",))
    cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", ("Název č.20", "Popis č.20",))
    connection_test_db.commit()
    cursor.execute("SELECT * FROM ukoly WHERE stav = 'nezahájeno' or stav = 'probíhá'")
    vysledek = cursor.fetchall()
    assert vysledek


def test_zobrazit_ukoly_negativni(connection_test_db):
    cursos = connection_test_db.cursos()
    cursor.execute("SELECT ")

"""