import mysql.connector                              # IMPORT KNIHOVY MY SQL, KTERÁ UMOŽŃUJE KOMUNIKACI PYTHONA S MYSQL
from mysql.connector import Error                   # IMPORT ERROR
from datetime import date                           # IMPORT DATE

list_id = []

def pripojeni_db():                                 # FUNKCE PRO PŘIPOJENÍ K DB
    try:                                            # ZKUS PROVÉST NÁSLEDUJÍCÍ, A POKUD NASTANE CHYBY, PŘEJDI DO EXCEPT
        spojeni = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="1111",
            database="projekt2"
        )
        if spojeni.is_connected():                  # FUNKCE IS.CONNECTED VRACÍ TRUE, POKUD JE SPOJENÍ AKTIVNÍ
            print("✅ Připojení k databázi bylo úspěšné.")
            return spojeni
    except Error as chyba:                          # POKUD NASTANE JAKÁKOLI HCBA PŘI PŘIPOJENÍ, SKOČ SEM
        print(f"❌ Chyba při připojení: {chyba}")
        return None                                 # POKUD SE PŘIPOJENÍ NEZDAŘÍ, FUNKCE VRÁTÍ NONE = TEDY NIC
    
pripojeni_db()

def vytvoreni_tabulky():
    spojeni = pripojeni_db()
    if spojeni is None:
        print("❌ Nelze vytvořit tabulku, protože připojení selhalo.")
        return

    try:
        kurzor = spojeni.cursor()
        kurzor.execute("""                                          # provede dotaz do SQL
            CREATE TABLE IF NOT EXISTS ukoly(
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev TEXT NOT NULL,
                popis TEXT NOT NULL,
                stav VARCHAR(20) NOT NULL DEFAULT "Nezahájeno",
                datum_vytvoreni DATE NOT NULL);
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
        print("Připojení k databázi proběhlo úspěšně. Nyní můžete přidávat úkoly.")

    nazev_ukolu = input("Zadejte název úkolu: ")
    #když je název prázný nebo uživatel zadá omylem Enter:
    while nazev_ukolu.isspace() or nazev_ukolu == "":
        print("Byl zadán prázdný vstup. Zadejte název úkolu.\n" "")
        nazev_ukolu = input("Zadejte název úkolu: ")
        
    popis_ukolu = input("Zadejte popis úkolu: ")
    #když je název prázný nebo uživatel zadá omylem Enter:
    while popis_ukolu.isspace() or popis_ukolu == "":
        print("Byl zadán prázdný vstup. Zadejte popis úkolu.\n" "")
        popis_ukolu = input("Zadejte popis úkolu: ")

    stav = "Nezahájeno"
    datum_vytvoreni = date.today()
    kurzor = spojeni.cursor()
    kurzor.execute("""
        INSERT INTO ukoly (nazev, popis, stav, datum_vytvoreni)         # do kterých sloupců chci vložit data
        VALUES (%s, %s, %s, %s);                                        # říká, že dodám 4 hodnoty
    """, (nazev_ukolu, popis_ukolu, stav, datum_vytvoreni))             # čtveřice hodnot, která se dosadí do těch %s
    spojeni.commit()                                                    # uloží všechny změny do DB, keré jsem provedla
    kurzor.close()                                                      # konec změn v DB
    spojeni.close()                                                     # konec spojení mezi Pythonem a DB
    print("✅ Úkol byl úspěšně přidán do databáze.")


def zobrazit_ukoly():
    spojeni = pripojeni_db()
    if spojeni is None:                                                 # POKUD SE PŘIPOJENÍ NEZDAŘÍ, FUNKCE VRÁTÍ NONE = TEDY NIC
        print("❌ Chyba při připojení k databázi!")
        return
    else:
        print("Připojení k databázi proběhlo úspěšně. Nyní můžete zobrazovat úkoly.")
        
    kurzor = spojeni.cursor()
    kurzor.execute("SELECT * FROM ukoly")
    vysledek = kurzor.fetchall()                                         #NAČTE VŠECHNY ŘÁDKY Z TABULKY UKOLY

    if vysledek:
        print("\n📋 Seznam úkolu: ")
        for ukol in vysledek:
            print(f"{ukol[0]} {ukol[1]} {ukol[2]} {ukol[3]} {ukol[4]}")
    else:
        print("⚠️ Tabulka s úkoly je prázdná. Zvolte jinou možnost v hlavním menu.")
    kurzor.close()                                                       # ukončení spojení mezi Pythonem a DB
    spojeni.close()


def aktualizovat_ukol():
    spojeni = pripojeni_db()
    if spojeni is None:
        print("❌ Chyba při připojení k databázi!")
        return
    else:
        print("Připojení k databázi proběhlo úspěšně. Nyní můžete aktualizovat úkoly.")
        
    zobrazit_ukoly()

    id_ukolu = input("Zadejte ID číslo úkolu, který chcete aktualizovat. (Pro návrat do hlavního menu zadejte 'x'.) ")
    if id_ukolu.lower() == "x":
        return
    id_ukolu = int(id_ukolu)

    kurzor = spojeni.cursor()
    kurzor.execute("SELECT id FROM ukoly")
    selected_id = kurzor.fetchall()

    list_id = []
    for radek in selected_id:                                     # projdeme každý řádek v seznamu
        list_id.append(radek[0])                                  # vezmeme první číslo z n-tice a přidáme ho do list_id

    novy_stav = input("Zadej nový stav úkolu : Vyber z následujících možností: Nezahájeno/Probíhá/Hotovo.")
    kurzor.execute("UPDATE ukoly SET stav = %s where id = %s", (novy_stav, id_ukolu))
    
    spojeni.commit()

while True:
        id_ukolu >= 1 and id_ukolu <= 




def odstranit_ukol(): 
    print("Funce odstranit úkol - zatím ve fázi vývoje.")

def ukoncit_program():
    print("\nKONEC PROGRAMU! - zatím ve fázi vývoje.")

hlavni_menu()


def hlavni_menu():
    print("\n📋 HLAVNÍ MENU :\n1. Přidat úkol\n2. Zobrazit úkoly\n3. Aktualizovat úkol\n4. Odstranit úkol\n5. Ukončit program")
    while True:
        option = int(input("Vyberte možnost (1 - 5): "))
        if option == 1:
            pridat_ukol()
        elif option == 2:
            zobrazit_ukoly()
        elif option == 3:
            aktualizovat_ukol()
        elif option == 4:
            odstranit_ukol()
        elif option == 5:
            ukoncit_program()
            break                    # UKONČUJE NEJBLIŽŠÍ SMYČKU (WHILE, FOR). JAKO CELEK UKONČUJE RETURN!
        else:
            print("" "\n❌ Byla zadána neplatná volba. Prosím, zvolte možnost 1, 2, 3, 4 nebo 5.")