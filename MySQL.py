from dotenv import load_dotenv
import os
import mysql.connector                              # IMPORT KNIHOVY MY SQL, KTERÁ UMOŽŃUJE KOMUNIKACI PYTHONA S MYSQL
from mysql.connector import Error                   # IMPORT ERROR
from datetime import date                           # IMPORT DATE
load_dotenv()                                       # NAČTENÍ .ENV SOUBORU

def pripojeni_db():                                 # FUNKCE PRO PŘIPOJENÍ K DB
    try:                                            # ZKUS PROVÉST NÁSLEDUJÍCÍ, A POKUD NASTANE CHYBY, PŘEJDI DO EXCEPT
        spojeni = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        if spojeni.is_connected():                  # FUNKCE IS.CONNECTED VRACÍ TRUE, POKUD JE SPOJENÍ AKTIVNÍ
            #print("✅ Připojení k databázi bylo úspěšné.")
            return spojeni
    except Error as chyba:                          # POKUD NASTANE JAKÁKOLI CHYBA PŘI PŘIPOJENÍ, SKOČ SEM
        print(f"❌ Chyba při připojení: {chyba}")
        return None                                 # POKUD SE PŘIPOJENÍ NEZDAŘÍ, FUNKCE VRÁTÍ NONE = TEDY NIC
    

def vytvoreni_tabulky():
    spojeni = pripojeni_db()
    if spojeni is None:
        print("❌ Nelze vytvořit tabulku, protože připojení selhalo.")
        return

    try:
        kurzor = spojeni.cursor()
        kurzor.execute("""                                          
            CREATE TABLE IF NOT EXISTS ukoly(
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev TEXT NOT NULL,
                popis TEXT NOT NULL,
                stav VARCHAR(20) NOT NULL DEFAULT "Nezahájeno",
                datum_vytvoreni DATE NOT NULL DEFAULT (CURRENT_DATE));
        """)
        spojeni.commit()                                            # uloží všechny změny do DB, keré jsem provedla
        print("Tabulka 'ukoly' je připravena.")
    except Error as e:
        print("❌ Chyba při vytváření tabulky:", e)
    finally:
        kurzor.close()                                              # konec změn v DB
        spojeni.close()                                             # konec spojení mezi Pythonem a DB

vytvoreni_tabulky()


def pridat_ukol():
    spojeni = pripojeni_db()
    if spojeni is None:                              # POKUD SE PŘIPOJENÍ NEZDAŘÍ, FUNKCE VRÁTÍ NONE = TEDY NIC
        print("❌ Chyba při připojení k databázi!")
        return
    else:
        print("\n✅ Připojení k databázi proběhlo úspěšně. Nyní můžete přidávat úkoly:\n")

    nazev_ukolu = input("Zadejte název úkolu: ")
    #když je název prázný nebo uživatel zadá omylem Enter:
    while nazev_ukolu.isspace() or nazev_ukolu == "":
        print("Byl zadán prázdný vstup. Zadejte název úkolu.\n")
        nazev_ukolu = input("Zadejte název úkolu: ")
        
    popis_ukolu = input("Zadejte popis úkolu: ")
    #když je název prázný nebo uživatel zadá omylem Enter:
    while popis_ukolu.isspace() or popis_ukolu == "":
        print("Byl zadán prázdný vstup. Zadejte popis úkolu.\n")
        popis_ukolu = input("Zadejte popis úkolu: ")

    stav = "Nezahájeno"
    datum_vytvoreni = date.today()

    kurzor = spojeni.cursor()
    kurzor.execute("""
        INSERT INTO ukoly (nazev, popis, stav)        
        VALUES (%s, %s, %s);                                        
    """, (nazev_ukolu, popis_ukolu, stav))             # čtveřice hodnot, která se dosadí do těch %s
    spojeni.commit()                                                    # uloží všechny změny do DB, keré jsem provedla
    kurzor.close()                                                      # konec změn v DB
    spojeni.close()                                                     # konec spojení mezi Pythonem a DB
    print(f"Úkol {nazev_ukolu} byl úspěšně přidán do databáze.")



def zobrazit_ukoly():
    spojeni = pripojeni_db()
    if spojeni is None:                                                 # POKUD SE PŘIPOJENÍ NEZDAŘÍ, FUNKCE VRÁTÍ NONE = TEDY NIC
        print("❌ Chyba při připojení k databázi!")
        return
    #else:
    #    print("\n✅ Připojení k databázi proběhlo úspěšně. Nyní můžete zobrazovat úkoly:")
        
    kurzor = spojeni.cursor()
    kurzor.execute("SELECT * FROM ukoly")                               #NAČTE VŠECHNY ŘÁDKY Z TABULKY UKOLY
    vysledek = kurzor.fetchall()           #Vezme všechny řádky, které mi databáze poslala, a vloží je jako do seznamu             

    if vysledek:
        print("\n📋 Seznam úkolů:\n")
        for ukol in vysledek:
            print(f"ID {ukol[0]}. Název úkolu: {ukol[1]} - Popis úkolu: {ukol[2]} - Stav: {ukol[3]} - Datum vytvoření: {ukol[4]}\n")
    else:
        print("⚠️ Tabulka 'ukoly' je prázdná. Zvolte jinou možnost v hlavním menu.")
    kurzor.close()                                                       # ukončení spojení mezi Pythonem a DB
    spojeni.close()


def aktualizovat_ukol():
    spojeni = pripojeni_db()
    if spojeni is None:
        print("❌ Chyba při připojení k databázi!")
        return
    else:
        print("\n✅ Připojení k databázi proběhlo úspěšně. Nyní můžete aktualizovat úkoly:")
        
    zobrazit_ukoly()

    kurzor = spojeni.cursor()
    kurzor.execute("SELECT id FROM ukoly")
    selected_id = kurzor.fetchall()

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

    kurzor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", (novy_stav, id_ukolu))
    spojeni.commit()
    kurzor.close()
    spojeni.close()
    print("✅ Úkol byl aktualizován.")


def seznam_id_ukolu():
    spojeni = pripojeni_db()
    if spojeni is None:
        print("❌ Chyba při připojení k databázi!")
        return
    kurzor = spojeni.cursor()
    kurzor.execute("SELECT id FROM ukoly")
    vysledek = kurzor.fetchall()
    seznam_id = []
    for i in vysledek:
        seznam_id.append(i[0])
    #print(seznam_id)
    kurzor.close()
    spojeni.close()
    return seznam_id                    # uloží výsledek funkce do budoucna, kdy jej lze jednoduše použít uložením 
                                        # do proměnné, např. ids = seznam_id_ukolu()


def odstranit_ukol():
    spojeni = pripojeni_db()
    if spojeni is None:
        print("❌ Chyba při připojení k databázi!")
        return
    else:
        print("\n✅ Připojení k databázi proběhlo úspěšně. Nyní můžete odstraňovat úkoly:\n")
   
    kurzor = spojeni.cursor()
    kurzor.execute("SELECT * FROM ukoly")                               #NAČTE VŠECHNY ŘÁDKY Z TABULKY UKOLY
    vysledek = kurzor.fetchall()           #Vezme všechny řádky, které mi databáze poslala, a vloží je jako do seznamu             
    for ukol in vysledek:
        print(f"ID {ukol[0]}. Název úkolu: {ukol[1]} - Popis úkolu: {ukol[2]} - Stav: {ukol[3]} - Datum vytvoření: {ukol[4]}\n")
    kurzor.close()

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
            kurzor = spojeni.cursor()
            kurzor.execute("DELETE FROM ukoly WHERE id = %s", (task_delete,))
            spojeni.commit()
            print(f"Úkol ID č. {task_delete} byl odstraněn.")
            kurzor.execute("SELECT id FROM ukoly")
            update_task_id = kurzor.fetchall()
            task_id = []
            for radek in update_task_id:
                task_id.append(radek[0])
            print(f"Aktuální seznam id: {task_id}")
            kurzor.close()
        else:
            print("❌ Zadané ID neexistuje. Zadejte platné ID z tabulky 'ukoly': ")


def ukoncit_program():
    print("\nKONEC PROGRAMU!\n")


def hlavni_menu():
    while True:
        print("\n📋 HLAVNÍ MENU :\n1. Přidat úkol\n2. Zobrazit úkoly\n3. Aktualizovat úkol\n4. Odstranit úkol\n5. Ukončit program\n--------------------------")
        option = input("Vyberte možnost (1 - 5): ")
        if option == "1":
            pridat_ukol()
        elif option == "2":
            zobrazit_ukoly()
        elif option == "3":
            aktualizovat_ukol()
        elif option == "4":
            odstranit_ukol()
        elif option == "5":
            ukoncit_program()
            break                                     # UKONČUJE NEJBLIŽŠÍ SMYČKU (WHILE, FOR). JAKO CELEK UKONČUJE RETURN!
        else:
            print("" "\n❌ Byla zadána neplatná volba. Prosím, zvolte možnost 1, 2, 3, 4 nebo 5.")

hlavni_menu()
