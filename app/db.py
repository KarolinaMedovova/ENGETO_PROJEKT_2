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
            #print("✅ Připojení k databázi 'projekt2' bylo úspěšné.")
            return spojeni 
    except Error as chyba:                          # POKUD NASTANE JAKÁKOLI CHYBA PŘI PŘIPOJENÍ, SKOČ SEM
        print(f"❌ Chyba při připojení: {chyba}")
        return None                                 # POKUD SE PŘIPOJENÍ NEZDAŘÍ, FUNKCE VRÁTÍ NONE = TEDY NIC



# FUNKCE PRO VYTVOŘENÍ TABULKY V DB:
def vytvoreni_tabulky():
    spojeni = pripojeni_db()
    if spojeni is None:
        print("❌ Nelze vytvořit tabulku, protože připojení selhalo.")
        return

    try:
        cursor = spojeni.cursor()
        cursor.execute("""                                                      
            CREATE TABLE IF NOT EXISTS ukoly(
                id INT AUTO_INCREMENT PRIMARY KEY,                                  
                nazev TEXT NOT NULL,
                popis TEXT NOT NULL,
                stav VARCHAR(20) NOT NULL DEFAULT 'nezahájeno',
                datum_vytvoreni DATE NOT NULL DEFAULT (CURDATE));
        """)
        spojeni.commit()
        cursor.execute("SELECT COUNT(*) FROM ukoly")
        pocet_radku = cursor.fetchone()[0]
        if not pocet_radku:
            print(f"Tabulka 'ukoly' v databázi 'projekt2' je připravena, ale je prázdná.")
        else:
            print(f"Tabulka 'ukoly' v databázi 'projekt2' je připravena a obsahuje {pocet_radku} řádků.")
    except Error as chyba:
        print("❌ Chyba při vytváření tabulky:", chyba)
    finally:
        cursor.close()                                              # konec změn v DB
        spojeni.close()                                             # konec spojení mezi Pythonem a DB
        #datum_vytvoreni = date.today()                         NENÍ POTŘEBA, NEBOT SE DATUM VKLÁDÁ DO SQL AUTOMATICKY.


#FUNKCE PRO PŘIDÁNÍ ÚKOLU: 
def pridat_ukol_db(spojeni, nazev, popis, stav="nezahájeno"):
    try:
        cursor = spojeni.cursor()
        cursor.execute("""
            INSERT INTO ukoly (nazev, popis, stav)        
            VALUES (%s, %s, %s);                                        
        """, (nazev, popis, stav))                             
        spojeni.commit()                                               
        print(f"✅ Úkol '{nazev}' byl uložen do databáze.")
    except Error as chyba:
        print(f"❌ Chyba při přidávání úkolu: {chyba}")
    finally:
        cursor.close()                                                     

# ---------------------------------------------------------------------------------------------------------

#FUNKCE PRO ZOBRAZNÍ ÚKOLŮ:
def zobrazit_ukoly(spojeni):
    if spojeni is None:                                                 # POKUD SE PŘIPOJENÍ NEZDAŘÍ, FUNKCE VRÁTÍ NONE = TEDY NIC
        print("❌ Chyba při připojení k databázi!")
        return
    #else:
    #    print("\n✅ Připojení k databázi proběhlo úspěšně. Nyní můžete zobrazovat úkoly:")
        
    cursor = spojeni.cursor()
    cursor.execute("SELECT * FROM ukoly WHERE stav = 'nezahájeno' or stav = 'probíhá'")         #NAČTE VŠECHNY ŘÁDKY Z TABULKY UKOLY, KDE STAV JE NEZAHÁJENO NEBO PROBÍHÁ
    vysledek = cursor.fetchall()           #Vezme všechny řádky, které mi databáze poslala, a vloží je jako do seznamu        
    cursor.close()                                                       # ukončení spojení mezi Pythonem a DB
    spojeni.close()
     
    if vysledek:
        nazvy_sloupcu = ["ID", "Název", "Popis", "Stav", "Datum vytvoření"]
        # převedeme stav na hezký formát s velkým písmenem
        vysledek_format = [(id, nazev, popis, stav.capitalize(), datum) for id, nazev, popis, stav, datum in vysledek]
        print(tabulate(vysledek_format, headers=nazvy_sloupcu, tablefmt="grid"))
    else:
        print("⚠️ Tabulka 'ukoly' je prázdná. Zvolte jinou možnost v hlavním menu.")

    return vysledek



def aktualizovat_ukol(spojeni):
    if spojeni is None:
        print("❌ Chyba při připojení k databázi!")
        return
    else:
        print("\n✅ Připojení k databázi PROJEKT2 proběhlo úspěšně. Nyní můžete aktualizovat úkoly:")
        
    zobrazit_ukoly()

    cursor = spojeni.cursor()
    cursor.execute("SELECT id FROM ukoly")
    selected_id = cursor.fetchall()

    list_id = []
    for radek in selected_id:                                     # projdeme každý řádek v seznamu
        list_id.append(radek[0])                                  # vezmeme první číslo z n-tice a přidáme ho do list_id

    while True:
        id_ukolu = input("Zadejte ID číslo úkolu, který chcete aktualizovat. (Pro návrat do hlavního menu zadejte 'x'.) ")
        if id_ukolu.lower() == "x":
            return
        elif id_ukolu.isspace() or id_ukolu == "":
            print("❌ Nebylo zadáno žádné ID číslo úkolu!")
        else:
            try:
                id_ukolu = int(id_ukolu)
                if id_ukolu in list_id:
                    break
                else:
                    print("❌ Zadané ID neexistuje. Zadejte platné ID z tabulky 'ukoly'.")
            except ValueError:
                print("❌ ID musí být číslo!")


    while True:
        novy_stav = input("Zadejte nový stav úkolu. Vyberte z následujících možností: nezahájeno/probíhá/hotovo: ")
        novy_stav = novy_stav.lower()
        if novy_stav == "nezahájeno" or novy_stav == "probíhá" or novy_stav == "hotovo":
            break
        else:
            print("Nový stav úkolu byl zadán špatně. Prosím, zadejte přesný název nového stavu - nezahájeno/probíhá/hotovo: ")

    cursor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", (novy_stav, id_ukolu))
    spojeni.commit()
    cursor.close()
    spojeni.close()
    print("✅ Úkol byl aktualizován.")


def seznam_id_ukolu():
    spojeni = pripojeni_db()
    if spojeni is None:
        print("❌ Chyba při připojení k databázi!")
        return
    cursor = spojeni.cursor()
    cursor.execute("SELECT id FROM ukoly")
    vysledek = cursor.fetchall()
    seznam_id = []
    for i in vysledek:
        seznam_id.append(i[0])
    #print(seznam_id)
    cursor.close()
    spojeni.close()
    return seznam_id                    # uloží výsledek funkce do budoucna, kdy jej lze jednoduše použít uložením 
                                        # do proměnné, např. ids = seznam_id_ukolu()


def odstranit_ukol(spojeni):
    if spojeni is None:
        print("❌ Chyba při připojení k databázi!")
        return
    else:
        print("\n✅ Připojení k databázi 'projekt2' proběhlo úspěšně. Nyní můžete odstraňovat úkoly:\n")
   
    cursor = spojeni.cursor()
    cursor.execute("SELECT * FROM ukoly")                               #NAČTE VŠECHNY ŘÁDKY Z TABULKY UKOLY
    vysledek = cursor.fetchall()           #Vezme všechny řádky, které mi databáze poslala, a vloží je jako do seznamu             
    
    nazvy_sloupcu = ["ID", "Název", "Popis", "Stav", "Datum vytvoření"]
    # převedeme stav na hezký formát s velkým písmenem
    vysledek_format = [(id, nazev, popis, stav.capitalize(), datum) for id, nazev, popis, stav, datum in vysledek]
    print(tabulate(vysledek_format, headers=nazvy_sloupcu, tablefmt="grid"))
    cursor.close()

    task_id = []
    for i in vysledek:
        task_id.append(i[0])

    while True:
        task_delete = input("Zadejte ID číslo úkolu, který chcete odstranit. (Pro návrat do hlavního menu zadejte 'x'.): ")
        if task_delete.lower() == "x":
            spojeni.close()
            return
        elif task_delete.isspace() or task_delete == "":
            print("❌ Nebylo zadáno žádné ID číslo úkolu!")
            continue                                        # nechá smyčku běžet dál, uživatel může zkusit znovu
        elif int(task_delete) in task_id:
            cursor = spojeni.cursor()
            cursor.execute("DELETE FROM ukoly WHERE id = %s", (task_delete,))
            spojeni.commit()
            print(f"Úkol s ID č. {task_delete} byl odstraněn.")
            cursor.execute("SELECT * FROM ukoly")
            update_list = cursor.fetchall()
            print("\nAktualizovaný seznam : \n")
            for i in update_list:
                print(f"ID {i[0]}. Název úkolu: {i[1]} - Popis úkolu: {i[2]} - Stav: {i[3].capitalize()} - Datum vytvoření: {i[4]}\n")
            cursor.close()
        else:
            print("❌ Zadané ID neexistuje. Zadejte platné ID z tabulky 'ukoly': ")


def ukoncit_program(spojeni):
    if spojeni and spojeni.is_connected():
        spojeni.close()
        print("Spojení s databází 'projekt2' bylo ukončeno!")
    print("\nKONEC PROGRAMU!\n")


def hlavni_menu():
    spojeni = pripojeni_db()
    while True:
        print("\n📋 HLAVNÍ MENU :\n1. Přidat úkol\n2. Zobrazit úkoly\n3. Aktualizovat úkol\n4. Odstranit úkol\n5. Ukončit program\n--------------------------")
        option = input("Vyberte možnost (1 - 5): ")
        if option == "1":
            pridat_ukol(spojeni)
        elif option == "2":
            zobrazit_ukoly(spojeni)
        elif option == "3":
            aktualizovat_ukol(spojeni)
        elif option == "4":
            odstranit_ukol(spojeni)
        elif option == "5":
            ukoncit_program(spojeni)
            break                                     # UKONČUJE NEJBLIŽŠÍ SMYČKU (WHILE, FOR). JAKO CELEK UKONČUJE RETURN!
        else:
            print("" "\n❌ Byla zadána neplatná volba. Prosím, zvolte možnost 1, 2, 3, 4 nebo 5.")


if __name__ == "__main__":                          # aby se hlavní menu nespouštělo v rámci automatizovaných testů
    hlavni_menu()

if __name__ == "__main__":
    vytvoreni_tabulky()