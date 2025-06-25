import json

def sss_cevap_bul(mesaj_metni):
    try:
        with open("sss.json", "r", encoding="utf-8") as f:
            sorular = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return "SSS verisi yüklenemedi. Lütfen yöneticinize başvurun."

    mesaj = mesaj_metni.lower()

    for sss in sorular:
        if sss["soru"] in mesaj:
            return sss["cevap"]

    return None