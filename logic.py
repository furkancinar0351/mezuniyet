import sqlite3

def create_tables():
    try:
        conn = sqlite3.connect("destek.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS destek_mesajlari (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici TEXT,
                mesaj TEXT,
                zaman TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        print("Veritabanı oluşturulurken hata oluştu:", e)
    finally:
        conn.close()

def mesaj_kaydet(kullanici, mesaj):
    if not kullanici or not mesaj:
        print("Boş kullanıcı veya mesaj verisi.")
        return
    try:
        conn = sqlite3.connect("destek.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO destek_mesajlari (kullanici, mesaj) VALUES (?, ?)", (kullanici, mesaj))
        conn.commit()
    except sqlite3.Error as e:
        print("Mesaj kaydedilirken hata oluştu:", e)
    finally:
        conn.close()

def mesajlari_listele():
    try:
        conn = sqlite3.connect("destek.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, kullanici, mesaj, zaman FROM destek_mesajlari ORDER BY zaman DESC")
        veriler = cursor.fetchall()
        return veriler
    except sqlite3.Error as e:
        print("Mesajlar listelenirken hata oluştu:", e)
        return []
    finally:
        conn.close()