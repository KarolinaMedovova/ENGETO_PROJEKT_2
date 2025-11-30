import os
import pytest
import mysql.connector
from dotenv import load_dotenv
load_dotenv
from mysql.connector import Error
from app.mysql import pridat_ukol

# fixtura pro připojení do testovací databáze
def test_pridat_ukol(connection_test_db):
    cursor = connection_test_db.cursor()
    cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", ("Název č.1", "Popis č.1",))
    connection_test_db.commit()
    cursor.execute("SELECT * FROM ukoly WHERE nazesv = %s", ("Název č.1",))
    vysledek = cursor.fetchone()
    assert vysledek is not None
    cursor.execute("DELETE FROM ukoly WHERE nazev = %s", ("Název č.1",))
    connection_test_db.commit()
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

        #pozitvní test fce pridat ukol()
def pridat_ukol_test_db():
    spojeni = pripojeni_test_db
    nazev_ukolu = "Úkol č.1"
    popis_ukoli = "Popis č.1"
    
    nazev_ukolu, popis_ukolu, stav="nezahájeno"



    def test_pridat_ukol():
    # připojení k testo.db
    spojeni = pripojeni_test_db()
    # vložit název úkolu "Úkol č.1"
    nazev_ukolu = "Úkol č.1"
    # vložit popis úkolu "Popis č.1"
    popis_ukolu = "Popis č.2"
    pridat_ukol(nazev_ukolu, popis_ukolu, stav="nezahájeno")
    cursor = spojeni.cursor()
    cursor.execute("SELECT * FROM ukoly WHERE nazev_ukolu = %s", (nazev_ukolu,))
    vysledek = cursor.fetchone()
    assert vysledek is not None, "Test pridat_ukol neprošel"
    cursor.execute("DELETE FROM ukoly WHERE nazev_ukolu = %s", (nazev_ukolu))
    spojeni.commit()
    cursor.close()
    spojeni.close()

negativní test funkce pridat ukol()
def test_neg_pridat_ukol():
    # připojení k test. db
    spojeni = pripojeni_test_db()
    # vložit jako název úkolu "Enter"
    nazev_ukolu = ""
    # vložit "mezeru" jako popis úkolu
    popis_ukolu = " "
    pridat_ukol(nazev_ukolu, popis_ukolu, stav="nezahájeno")
    cursor = spojeni.cursor()
    cursor.execute("SELECT * FROM ukoly WHERE nazev_ukolu = %s", (nazev_ukolu,))
    vysledek = cursor.fetchone()
    assert vysledek is not None, "Test neg_pridat_ukol neprošel"
    cursor.execute("DELETE FROM ukoly WHERE nazev_ukolu = %s", (nazev_ukolu,))
    cursor.commit()
    cursor.close()
    spojeni.close()



def test_aktualizovat_ukol(id_ukolu, novy_stav):
    spojeni = pripojeni_test_db()
    cursor = spojeni.cursor()
    sql = "UPDATE ukoly SET stav = %x WHERE id = %s"
    cursor.execute(sql, (novy_stav, id_ukolu))
    spojeni.commit()
"""




