import re
from PIL import Image
from PIL.ExifTags import TAGS
import zipfile

# B1. Magic bytes: tipul real, nu extensia
# Deschide un fișier în mod binar și citește-i primii octeți. Compară-i cu semnăturile cunoscute.
print("B1:")
def tip_real(cale):
    with open(cale, "rb") as f:
        cap = f.read(8)
    if cap.startswith(b"%PDF"):
        return "pdf"
    elif cap.startswith(b"\x89PNG"):
        return "png"
    elif cap.startswith(b"\xff\xd8"):
        return "jpeg"
    elif cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return cap.hex()
print(tip_real("probe/foto.jpg"))
print(tip_real("probe/ascuns.png"))



# B2. strings: textul citibil dintr-un binar
# Scoate secvențele de caractere imprimabile dintr-un fișier, cu un regex pe octeți.
print("B2:")
with open("probe/ascuns.png", "rb") as f:
    date = f.read()
for m in re.findall(rb"[ -~]{4,}", date):
    print(m.decode())


# B3. Metadate EXIF și GPS din poză 
# Citește blocul EXIF din probe/foto.jpg și scoate coordonatele GPS. Convertește-le în grade zecimale.
print("B3:")
exif = Image.open("probe/foto.jpg")._getexif() or {}
for id, val in exif.items():
    print(TAGS.get(id, id), "=", val)
date_gps = exif.get(34853)

if date_gps is not None:
    lat = date_gps.get(1)
    lat_coord = date_gps.get(2)
    lon = date_gps.get(3)
    lon_coord = date_gps.get(4)

    lat_zecimala = float(lat_coord[0]) + float(lat_coord[1] / 60.0) + float(lat_coord[2] / 3600.0)
    if lat == "S":
        lat_zecimala = -lat_zecimala

    lon_zecimala = float(lon_coord[0]) + float(lon_coord[1] / 60.0) + float(lon_coord[2] / 3600.0)
    if lon == "W":
        lon_zecimala = -lon_zecimala

    print(f"Latitudine GPS: {lat_zecimala:.4f}")
    print(f"Longitudine GPS: {lon_zecimala:.4f}")
else:
    print("Nu s-au gasit date GPS in aceasta poza")



# B4. File carving: scoți fișierul ascuns
# probe/ascuns.png are o arhivă ZIP lipită la coadă. Găsește-i semnătura și salveaz-o separat.
print("B4:")
with open("probe/ascuns.png", "rb") as f:
    date = f.read()
i = date.find(b"PK\x03\x04")
if i != -1:
    with open("gasit.zip", "wb") as f:
        f.write(date[i:]) 
    print("arhiva extrasa la octetul", i)

    with zipfile.ZipFile("gasit.zip", "r") as z:
        print("Fisiere in arhiva:", z.namelist())
        for nume in z.namelist():
            print(nume, "->", z.read(nume).decode().strip())
        z.extractall("extras")
else:
    print("Semnatura ZIP (PK\\x03\\x04) nu a fost gasita în fisier")




