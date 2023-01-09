import requests
from bs4 import BeautifulSoup


def ekstraksi_data():

    """
    Tanggal : 30 Desember 2022
    Waktu :  19:10:47 WIB
    Magnitudo : 5.4
    Kedalaman : 10 km
    Lokasi : 8.24 LS - 129.07 BT
    Pusat Gempa : 142 km Tenggara MALUKUBRTDAYA
    Potensi : tidak berpotensi TSUNAMI
    """

    try:
        content = requests.get("https://bmkg.go.id")
    except Exception:
        return None

    if content.status_code == 200:
        soup = BeautifulSoup(content.text, "html.parser")

        result = soup.find("span", {"class": "waktu"})
        result = result.text.split(",")
        Tanggal = result [0]
        Waktu = result[1]

        result = soup.find("ul", {"class": "list-unstyled"})
        result = result.findChildren("li")
        i = 0
        Magnitudo = None
        LS = None
        BT = None
        Kedalaman = None
        Lokasi = None
        Dirasakan = None


        for res in result:

            if i == 1:
                Magnitudo = res.text
            elif i == 2:
                Kedalaman = res.text
            elif i == 3:
                Koordinat = res.text.split(" - ")
                LS = Koordinat[0]
                BT = Koordinat[1]
            elif i == 4:
                Lokasi = res.text
            elif i == 5:
                Dirasakan = res.text
            i = i + 1


        hasil = dict()
        hasil["Tanggal"] = Tanggal
        hasil["Waktu"] = Waktu
        hasil["Magnitudo"] = Magnitudo
        hasil["Kedalaman"] = Kedalaman
        hasil["Koordinat"] = {"LS": LS, "BT": BT}
        hasil["Lokasi"] = Lokasi
        hasil["Dirasakan"] = Dirasakan

        return hasil
    else:
        return None

def tampilkan_data(result):
    print("Gempa terakhir berdasarkan BMKG")
    print(f"Tanggal {result['Tanggal']}")
    print(f"Waktu {result['Waktu']}")
    print(f"Magnitudo {result['Magnitudo']}")
    print(f"Kedalaman {result['Kedalaman']}")
    print(f"Koordinat : LS = {result['Koordinat']['LS']}, BT = {result['Koordinat']['BT']}")
    print(f"Lokasi {result['Lokasi']}")
    print(f"Dirasakan {result['Dirasakan']}")

if __name__ == "__main__":
    result = ekstraksi_data()
    tampilkan_data(result)