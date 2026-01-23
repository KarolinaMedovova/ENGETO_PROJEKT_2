import os
from dotenv import load_dotenv
load_dotenv()
import pytest
import mysql.connector
from mysql.connector import Error

# fixtura pro pripojení do testovací DB
@pytest.fixture(scope="function")
def connection_test_db():
    try:
        spojeni = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME_TEST")
        )
        if spojeni.is_connected():
            yield spojeni
    except Error as chyba:
        print(f"❌ Chyba při připojení: {chyba}")
        yield None
    finally:
        if spojeni and spojeni.is_connected():
            spojeni.close()
        else:
            print("⚠️ Spojení není aktivní nebo nevzniklo — není co zavírat.")


# fixtura pro pripojení do ostré DB
@pytest.fixture(scope="function")
def connection_prod_db():
    try:
        spojeni = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        if spojeni.is_connected():
            yield spojeni
    except Error as chyba:
        print(f"❌ Chyba při připojení: {chyba}")
        yield None
    finally:
        if spojeni and spojeni.is_connected():
            spojeni.close()
        else:
            print("⚠️ Spojení není aktivní nebo nevzniklo — není co zavírat.")


# fixtura pro automatické vyčištění testovací DB před a po testu :
@pytest.fixture(autouse=True)                           # autouse=True = pytest spustí automaticky sám u každého testu!
def clean_db(connection_test_db):
    cursor = connection_test_db.cursor()
    cursor.execute("TRUNCATE ukoly")
    connection_test_db.commit()
    # konec příprav, spusť test
    yield                                              
    cursor.execute("TRUNCATE ukoly")
    connection_test_db.commit()
    cursor.close()