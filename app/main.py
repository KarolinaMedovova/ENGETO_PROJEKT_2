from tabulate import tabulate
from db import pripojeni_db, vytvoreni_tabulky_db, pridat_ukol_db, zobrazit_ukoly_db, aktualizovat_ukol_db, seznam_id_ukolu_db, odstranit_ukol_db, ukonceni_spojeni_db



# funkce přidat úkol:
def pridat_ukol(spojeni):
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
        
    ok, chyba = pridat_ukol_db(spojeni, nazev, popis)
    if ok:
        print(f"Úkol '{nazev}' byl úspěšně přidán do databáze 'projekt2'.")
    else:
        print(f"❌ Úkol se nepodařilo přidat: {chyba}")

# funkce zobrazení úkolů:
def zobrazit_ukoly(spojeni):
    vysledek, chyba = zobrazit_ukoly_db(spojeni)
    if chyba:
        print(f"Došlo k chybě: {chyba}")
        return
           
    if vysledek:
        nazvy_sloupcu = ["ID", "Název", "Popis", "Stav", "Datum vytvoření"]
        vysledek_format = []
        for id, nazev, popis, stav, datum in vysledek:
            vysledek_format.append((id, nazev, popis, stav.capitalize(), datum))
        print(tabulate(vysledek_format, headers=nazvy_sloupcu, tablefmt="grid"))
    else:
        print("⚠️ Tabulka 'ukoly' je prázdná. Zvolte jinou možnost v hlavním menu.")


# funkce aktualizovat úkol: 
def aktualizovat_ukol(spojeni):
    vysledek, chyba = zobrazit_ukoly_db(spojeni)
    if chyba is not None:
        print(f"Došlo k chybě: {chyba}.")
        return
            
    if vysledek :
        nazvy_sloupcu = ["ID", "Název", "Stav"]
        seznam_hodnot = []
        for id, nazev, popis, stav, datum in vysledek:
            seznam_hodnot.append((id, nazev, stav.capitalize(),))
        print(tabulate(seznam_hodnot, headers=nazvy_sloupcu, tablefmt="grid"))

    list_id = []
    for radek in seznam_hodnot:                       
        list_id.append(radek[0])                                

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
          
    ok, chyba = aktualizovat_ukol_db(spojeni, id_ukolu, novy_stav)
    if ok:
        print("✅ Úkol byl aktualizován.")
    else:
        print(f"❌ Úkol se nepodařilo aktualizovat: {chyba}")


#funkce odstranit úkol:
def odstranit_ukol(spojeni):
    vysledek, chyba = zobrazit_ukoly_db(spojeni)
    if chyba is not None:
        print(f"Došlo k chybě: {chyba}.")
        return
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
            continue

        try:
            id_delete_int = int(id_delete)
            if id_delete_int in seznam_id:
                ok, chyba = odstranit_ukol_db(spojeni, id_delete_int)
                if ok is True:
                    print(f"Úkol s ID č. {id_delete_int} byl odstraněn.")
                    break
                elif ok is False:
                    print(f"Úkol s tímto ID v databázi neexistuje; {chyba}")
                    continue
                elif ok is None:
                    print(f"CHYBA: {chyba}!")
                    return
            else:
                print("❌ Zadané ID neexistuje. Zadejte platné ID z tabulky 'ukoly': ")

        except ValueError:
            print("❌ Byla zadána neplatná volba. Prosím, zvolte správné číslo ID úkolu")
            continue


# funkce ukončení programu:
def konec_programu(spojeni):
    print("Ukončuji program... Na shledanou.")
    ukonceni_spojeni_db(spojeni)
    return                         
        

# funkce pro hlavní menu:   
def hlavni_menu():
    # FUNKCE PRO PŘIPOJENÍ K DB:
    spojeni, chyba = pripojeni_db()
    if chyba:
        print(f"❌ Nelze se připojit k databázi: {chyba}")
    print("Připojení k databázi proběhlo úspěšně!")

    # FUNKCE PRO VYTVOŘENÍ TABULKY:
    ok, chyba = vytvoreni_tabulky_db(spojeni)
    if chyba:
        print(f"Při vytvoření tabulky došlo k chybě: {chyba}")
    else:
        print("Tabulka byla vytvořena a je připravena.")

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
            konec_programu(spojeni)
            break                                   
        else:
            print("" "\n❌ Byla zadána neplatná volba. Prosím, zvolte možnost 1, 2, 3, 4 nebo 5.")



if __name__ == "__main__":                        
    hlavni_menu()