import os
import pytest
import mysql.connector
from dotenv import load_dotenv
load_dotenv
from mysql.connector import Error
from app.mysql import pridat_ukol

# fixtura pro připojení do testovací databáze
def test_pridat_ukol_pozitivní(connection_test_db):
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


def test_zobrazit_ukoly_pozitivni(connection_test_db):
    cursor = connection_test_db.cursor()
    cursor.execute("SELECT * FROM ukoly WHERE stav = 'nezahájeno' or stav = 'probíhá'")
    vysledek = cursor.fetchall()
    assert vysledek


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


    



def test_aktualizovat_ukol(id_ukolu, novy_stav):
    spojeni = pripojeni_test_db()
    cursor = spojeni.cursor()
    sql = "UPDATE ukoly SET stav = %x WHERE id = %s"
    cursor.execute(sql, (novy_stav, id_ukolu))
    spojeni.commit()
"""




