import os
from dotenv import load_dotenv
load_dotenv()                                       # NAČTENÍ .ENV SOUBORU
#from tabulate import tabulate                       # NAČTENÍ KNIHOVNY PRO TABULKOVÝ VÝSTUP
import mysql.connector                              # IMPORT KNIHOVY MY SQL, KTERÁ UMOŽŃUJE KOMUNIKACI PYTHONA S MYSQL
from mysql.connector import Error                   # IMPORT ERROR
#from datetime import date                           # IMPORT DATE
#datum_vytvoreni = date.today()                         NENÍ POTŘEBA, NEBOT SE DATUM VKLÁDÁ DO SQL AUTOMATICKY.

#FUNKCE PRO PŘIPOJENÍ DO DB:
def pripojeni_db():                                 # FUNKCE PRO PŘIPOJENÍ K DB
    try:                                            # ZKUS PROVÉST NÁSLEDUJÍCÍ, A POKUD NASTANE CHYBY, PŘEJDI DO EXCEPT
        spojeni = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        if spojeni.is_connected():                  # FUNKCE IS.CONNECTED VRACÍ TRUE, POKUD JE SPOJENÍ AKTIVNÍ
            return spojeni, None
    except Error as chyba:                          # POKUD NASTANE JAKÁKOLI CHYBA PŘI PŘIPOJENÍ, SKOČ SEM
        return None, chyba                             # POKUD SE PŘIPOJENÍ NEZDAŘÍ, FUNKCE VRÁTÍ NONE = TEDY NIC



# FUNKCE PRO VYTVOŘENÍ TABULKY V DB:
def vytvoreni_tabulky_db(spojeni):
    try:
        cursor = spojeni.cursor()
        cursor.execute("""                                                      
            CREATE TABLE IF NOT EXISTS ukoly(
                id INT AUTO_INCREMENT PRIMARY KEY,                                  
                nazev TEXT NOT NULL,
                popis TEXT NOT NULL,
                stav VARCHAR(20) NOT NULL DEFAULT 'nezahájeno',
                datum_vytvoreni DATE NOT NULL DEFAULT (CURDATE())
            );
        """)
        spojeni.commit()
        return True, None
    except Error as chyba:
        return False, chyba
    finally:
        cursor.close()                                                                                   


#FUNKCE PRO PŘIDÁNÍ ÚKOLU: 
def pridat_ukol_db(spojeni, nazev, popis, stav="nezahájeno"):
    if not nazev.strip() or not popis.strip():
        return False, "Název a popis nesmí být prázdné hodnoty."
    try:
        cursor = spojeni.cursor()
        cursor.execute("""
            INSERT INTO ukoly (nazev, popis, stav)        
            VALUES (%s, %s, %s);                                        
        """, (nazev, popis, stav))                             
        spojeni.commit()                                               
        return True, None
    except Error as chyba:
        print(f"chyba v pridat ukol: {chyba}")
        return False, chyba
    finally:
        cursor.close()                                                     


#FUNKCE PRO ZOBRAZNÍ ÚKOLŮ:
def zobrazit_ukoly_db(spojeni):
    try: 
        cursor = spojeni.cursor()
        cursor.execute("SELECT * FROM ukoly WHERE stav IN ('nezahájeno','probíhá') ORDER BY datum_vytvoreni DESC")        
        vysledek = cursor.fetchall()               #Vezme všechny řádky, které mi databáze poslala, a vloží je jako do seznamu        
        return vysledek, None
    except Error as chyba:
        return None, chyba
    finally:
        cursor.close()


#FUNKCE PRO AKTUALIZOVÁNÍ ÚKOLŮ:
def aktualizovat_ukol_db(spojeni, id_ukolu, novy_stav):
    cursor = None   
    try:
        cursor = spojeni.cursor()
        cursor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", (novy_stav, id_ukolu))
        spojeni.commit()
        if cursor.rowcount == 0:
            return False, "Úkol s tímto ID neexistuje"
        return True, None
    except Error as chyba:
        return False, chyba
    finally:
        if cursor:
            cursor.close()
    
 

#FUNKCE PRO ZOBRAZENÍ VŠECH ID ÚKOLŮ:
def seznam_id_ukolu_db(spojeni):
    try:
        cursor = spojeni.cursor()
        cursor.execute("SELECT id FROM ukoly")
        vysledek = cursor.fetchall()
        seznam_id = []
        for i in vysledek:
            seznam_id.append(i[0])
        return seznam_id, None
    except Error as chyba:
        return None, chyba
    finally:
        cursor.close()



#FUNKCE PRO ODSTRANĚNÍ ÚKOLŮ:
def odstranit_ukol_db(spojeni, id_ukolu):
    try:
        cursor = spojeni.cursor()
        cursor.execute("DELETE FROM ukoly WHERE id = %s", (id_ukolu,))    
        spojeni.commit()
        if cursor.rowcount > 0:
            return True, None
        else:
            return False, "Úkol s tímto ID neexistuje"
    except Error as chyba:
        return None, chyba
    finally:
        cursor.close()
    
    

#FUNKCE PRO UKONČENÍ SPOJENI:
def ukonceni_spojeni_db(spojeni):
    if spojeni and spojeni.is_connected():
        spojeni.close()
