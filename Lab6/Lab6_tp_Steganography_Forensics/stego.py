from PIL import Image

# B5. Ascunzi un mesaj prin LSB
# Scrie un mesaj în ultimii biți ai pixelilor dintr-o poză gazdă. Rezultatul arată identic cu originalul.
print("B5:")
img = Image.open("probe/foto.jpg").convert("RGB")
px = list(img.get_flattened_data())
mesaj = b"FLAG{ascuns_in_pixeli}"
biti = "".join(f"{x:08b}" for x in mesaj + b"\x00")
if len(biti) > len(px) * 3:
    print("Eroare, imaginea este prea mica pentru acest mesaj")
else:
    px_nou = []
    index_bit = 0
    numar_total_biti = len(biti)

    for pixel in px:
        r, g, b = pixel

        if index_bit < numar_total_biti:
            bit_curent = int(biti[index_bit])
            r = (r & ~1) | bit_curent
            index_bit += 1

        if index_bit < numar_total_biti:
            bit_curent = int(biti[index_bit])
            g = (g & ~1) | bit_curent
            index_bit += 1

        if index_bit < numar_total_biti:
            bit_curent = int(biti[index_bit])
            b = (b & ~1) | bit_curent
            index_bit += 1

        px_nou.append((r, g, b))
    
    img.putdata(px_nou)
    img.save("stego.png")
    print("Mesajul a fost ascuns in 'stego.png'")



# B6. Dezvălui mesajul înapoi   
# Citește ultimii biți ai pixelilor din stego.png, regrupează-i câte 8 și reconstituie mesajul.
print("B6:")
px = list(Image.open("stego.png").convert("RGB").get_flattened_data())
biti = ""
for (r, g, b) in px:
    biti += str(r&1) + str(g&1) + str(b&1)

mesaj_text = ""
for i in range(0, len(biti), 8):
    octet_biti = biti[i:i+8]
    if len(octet_biti) < 8:
        break

    valoare_octet = int(octet_biti, 2)
    if valoare_octet == 0:
        break

    mesaj_text += chr(valoare_octet)
print("Mesajul ascuns:", mesaj_text)


