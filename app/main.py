# NAČTENÍ KNIHOVNY PRO TABULKOVÝ VÝSTUP:
from tabulate import tabulate
# 1) IMPORTY FUNKCÍ Z DB:
from db import ( pripojeni_db, vytvoreni_tabulky_db, pridat_ukol_db, zobrazit_ukoly_db, aktualizovat_ukol_db, seznam_id_ukolu_db, odstranit_ukol_db, ukonceni_spojeni_db)

# 2) FUNKCE PRO PŘIPOJENÍ K DB:
spojeni, chyba = pripojeni_db()
if chyba:
    print(f"❌ Nelze se připojit k databázi: {chyba}")
print("Připojení k databázi proběhlo úspěšně!")


# 3) FUNKCE PRO VYTVOŘENÍ TABULKY:
ok, chyba = vytvoreni_tabulky_db(pripojeni_db)
if chyba:
    print(f"Při vytvoření tabulky došlo k chybě: {chyba}")
else:
    print("Tabulka byla vytvořena a je připravena.")


# 4) FUNKCE HLAVNÍ MENU:
def hlavni_menu(spojeni):
   while True:
        print("\n📋 HLAVNÍ MENU :\n1. Přidat úkol\n2. Zobrazit úkoly\n3. Aktualizovat úkol\n4. Odstranit úkol\n5. Ukončit program\n--------------------------")
        option = input("Vyberte možnost (1 - 5): ")
        # volba 1, přidání úkolu
        if option == "1":
            nazev = input("Zadejte název úkolu: ")
            #když je název prázný nebo uživatel zadá omylem Enter:
            while nazev.isspace() or nazev == "":
                print("Byl zadán prázdný vstup. Zadejte název úkolu.\n")
                nazev = input("Zadejte název úkolu: ")

            popis = input("Zadejte popis úkolu: ")
            #když je popis prázný nebo uživatel zadá omylem Enter:
            while popis.isspace() or popis == "":
                print("Byl zadán prázdný vstup. Zadejte popis úkolu.\n")
                popis = input("Zadejte popis úkolu: ")

            pridat_ukol_db(spojeni, nazev, popis)
            print(f"Úkol {nazev} byl úspěšně přidán do databáze 'projekt2'.")

        # volba 2, zobrazení úkolů:
        elif option == "2":
            vysledek = zobrazit_ukoly_db(spojeni)            
            if vysledek:
                nazvy_sloupcu = ["ID", "Název", "Popis", "Stav", "Datum vytvoření"]
                # capitalize převádí první písmeno na velké
                vysledek_format = []
                for id, nazev, popis, stav, datum in vysledek:
                    vysledek_format.append((id, nazev, popis, stav.capitalize(), datum))
                # tabulate vezme seznam řádků a názvy sloupců a vypíše je jako tabulku ve zvoleném stylu grid.
                print(tabulate(vysledek_format, headers=nazvy_sloupcu, tablefmt="grid"))
            else:
                print("⚠️ Tabulka 'ukoly' je prázdná. Zvolte jinou možnost v hlavním menu.")

        # volba 3, aktualizování úkolu: 
        elif option == "3":
            vysledek, chyba = zobrazit_ukoly_db(spojeni)
            if chyba is not None:
                print(f"Došlo k chybě: {chyba}.")
                continue
            
            if vysledek :
                nazvy_sloupcu = ["ID", "Název", "Stav"]
                seznam_hodnot = []
                for id, nazev, popis, stav, datum in vysledek:
                    seznam_hodnot.append((id, nazev, stav.capitalize(),))
                print(tabulate(seznam_hodnot, headers=nazvy_sloupcu, tablefmt="grid"))

            list_id = []
            for radek in seznam_hodnot:                         # projdeme každý řádek v seznamu
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

            print("✅ Úkol byl aktualizován.")

        # volba 4, odstranění úkolu:
        elif option == "4":
            vysledek, chyba = zobrazit_ukoly_db(spojeni)
            if chyba is not None:
                print(f"Došlo k chybě: {chyba}.")
                continue
            if vysledek:
                nazvy_sloupcu = ["ID", "Název", "Popis", "Stav", "Datum vytvoření"]
                seznam_hodnot = []
                for id, nazev, popis, stav, datum_vytvoreni in vysledek:
                    seznam_hodnot.append((id, nazev, popis, stav.capitalize(), datum_vytvoreni,))
                print(tabulate(seznam_hodnot, headers=nazvy_sloupcu, tablefmt="grid"))

                seznam_id = []
                for i in vysledek:
                    seznam_id.append(i[0])

                while True:
                    id_delete = input("Zadejte ID číslo úkolu, který chcete odstranit. (Pro návrat do hlavního menu zadejte 'x'.): ")
                    if id_delete.lower() == "x":
                        return
                    elif id_delete.isspace() or id_delete == "":
                        print("❌ Nebylo zadáno žádné ID číslo úkolu!")
                        continue                                      # nechá smyčku běžet dál, uživatel může zkusit znovu


                    # seznam_id = [1, 2, 3, 5, 8, 9, 10]
                    # vysledek = [(1. nazev1, popis1, hotov, 1.1.2026), (2. nazev2, popis2, hotovo, 3.2.2025,)]
                    try:
                        id_delete_int = int(id_delete)
                        if id_delete_int in seznam_id:

                            seznam_id.


                    except Error as e:
                        print("❌ Zadané ID neexistuje. Zadejte platné ID z tabulky 'ukoly': ")
        

                        

                    elif task_delete in seznam_id:

                        print(f"Úkol s ID č. {task_delete} byl odstraněn.")
                        print("\nAktualizovaný seznam : \n")
                        update_list = []
                        for id, nazev, popis, stav.capitalize(), datum_vytvoreni in vysledek:
                            print(tabulate)
                        for i in update_list:
                            print(f"ID {i[0]}. Název úkolu: {i[1]} - Popis úkolu: {i[2]} - Stav: {i[3].capitalize()} - Datum vytvoření: {i[4]}\n")
                    else:
                        print("❌ Zadané ID neexistuje. Zadejte platné ID z tabulky 'ukoly': ")

        
        elif option == "5":
            ukonceni_spojeni_db(spojeni)
            break                                     # UKONČUJE NEJBLIŽŠÍ SMYČKU (WHILE, FOR). JAKO CELEK UKONČUJE RETURN!
        else:
            print("" "\n❌ Byla zadána neplatná volba. Prosím, zvolte možnost 1, 2, 3, 4 nebo 5.")
    


# FUNKCE PRO PŘIDÁNÍ ÚKOLU:
def pridat_ukol_ui(spojeni):
    nazev_ukolu = input("Zadejte název úkolu: ")
    popis_ukolu = input("Zadejte popis úkolu: ")
    pridat_ukol_db(spojeni, nazev_ukolu, popis_ukolu)
    print(f"=Ukol '{nazev_ukolu}' byl vložen do databáze.")

#___________________________________________________________________________________________

def zobrazit_ukoly_ui(spojeni):
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



def aktualizovat_ukol_ui(spojeni):
    if spojeni is None:
        print("❌ Chyba při připojení k databázi!")
        return
    else:
        print("\n✅ Připojení k databázi PROJEKT2 proběhlo úspěšně. Nyní můžete aktualizovat úkoly:")
        
    zobrazit_ukoly_ui()

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


def seznam_id_ukolu_ui():
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


def odstranit_ukol_ui(spojeni):
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


def ukoncit_program_ui(spojeni):
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
            pridat_ukol_ui(spojeni)
        elif option == "2":
            zobrazit_ukoly_ui(spojeni)
        elif option == "3":
            aktualizovat_ukol_ui(spojeni)
        elif option == "4":
            odstranit_ukol_ui(spojeni)
        elif option == "5":
            ukoncit_program_ui(spojeni)
            break                                     # UKONČUJE NEJBLIŽŠÍ SMYČKU (WHILE, FOR). JAKO CELEK UKONČUJE RETURN!
        else:
            print("" "\n❌ Byla zadána neplatná volba. Prosím, zvolte možnost 1, 2, 3, 4 nebo 5.")


if __name__ == "__main__":                          # aby se hlavní menu nespouštělo v rámci automatizovaných testů
    hlavni_menu()

if __name__ == "__main__":
    vytvoreni_tabulky_db()