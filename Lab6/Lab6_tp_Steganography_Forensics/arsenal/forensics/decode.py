import re
import base64
from urllib.parse import unquote
import os
import hashlib
import argparse, json


#A2. Recunoști stratul după formă   
def ghici_strat(s):
    if "%" in s or re.search(r'%[0-9A-Fa-f]{2}', s):
        return "url"
    elif re.fullmatch(r'[0-9a-fA-F]+', s) and len(s) % 2 == 0:
        return "hex"
    elif re.fullmatch(r'[A-Za-z0-9+/=]+', s):
        return "base64"
    return "necunoscut"



#A3. Desfaci stratul recunoscut   
#Acum chiar decodează, în funcție de ce a zis A2. Întoarce și tipul, și rezultatul.
def desfa(s):
    strat = ghici_strat(s)
    try:
        if strat == "base64":
            rezultat = base64.b64decode(s, validate=True)
        elif strat == "hex":
            rezultat = bytes.fromhex(s)
        elif strat == "url":
            rezultat = unquote(s).encode()
        else:
            rezultat = s.encode()
    except Exception:
        strat = "necunoscut"
        rezultat = s.encode()
        
    return strat, rezultat

#A4
def citibil(b):    
    return all(32 <= c < 127 for c in b)

def main():  
    #A1 Text și octeți: încălzirea
    print("A1:")
    s = "Salut"
    b = s.encode()          # bytes
    print(b, b[0])          # b"Salut" 83
    print("Hex:", b.hex())
    print("Reconstructie:", bytes.fromhex(b.hex()))


    #A2
    print("A2")
    print(ghici_strat("%2Fetc"))   # url
    print(ghici_strat("48656c6c6f"))  # hex

    #A3
    print("A3:")
    print(desfa("abc123"))


    # A4. Straturi multiple, într-o buclă   
    # Un rezultat poate fi tot o codare. Decodează în buclă până iese text citibil 
    # (sau te oprești după câteva încercări, ca să nu intri în buclă infinită).
    print("A4:")    
    val = "NTM1OTU3NTk="
    for _ in range(8):
        strat, b = desfa(val)
        if strat == "necunoscut" or not citibil(b):
            break
        val = b.decode()
    print("Rezultat:", val)



    # A5. Spargi un XOR cu cheie de un octet
    # Citește probe/xor.bin (octeți), încearcă toate cele 256 de chei și păstrează rezultatul care arată a text.
    print("A5:")    

    date_xor = open("probe/xor.bin", "rb").read()
    for k in range(256):
            clar = bytes(bx ^ k for bx in date_xor)
            if citibil(clar):
                print(f"XOR - Cheie găsită: {k} -> {clar.decode(errors='ignore')}")


    # A6. Spargi un hash prin dicționar  
    # Din probe/hashuri.txt ia un hash. Identifică algoritmul după lungime, apoi caută parola într-o wordlist.
    print("A6:")
    wordlist = open("probe/wordlist.txt", encoding="latin1").read().split()
    for tinta in open("probe/hashuri.txt").read().split():
        algo = {32: "md5", 40: "sha1", 64: "sha256"}[len(tinta)]
        for cuv in wordlist:
            if hashlib.new(algo, cuv.encode()).hexdigest() == tinta:
                print(tinta, algo, "->", cuv)
                break




    # A7. argparse, fișa JSON și un test
    # Leagă totul într-o unealtă comandată din afară, salvează rezultatul ca fișă, și scrie un test.
    print("A7:")
    p = argparse.ArgumentParser()
    p.add_argument("intrare", nargs="?", default="NTM1OTU3NTk=", help="șir sau cale")
    p.add_argument("--fisier", action="store_true")
    a = p.parse_args()

    if a.fisier:
        val = open(a.intrare, "rb").read().decode("latin1").strip()
    else:
        val = a.intrare

    straturi = []
    for _ in range(8):
        strat, b = desfa(val)
        if strat == "necunoscut" or not citibil(b):
            break
        straturi.append(strat)
        val = b.decode()

    fisa = {"strat": straturi, "rezultat": val}
    print(fisa)
    os.makedirs("arsenal/forensics", exist_ok=True)
    with open("arsenal/forensics/fisa.json", "w", encoding="utf-8") as f:
        json.dump(fisa, f, indent=4)

if __name__ == "__main__":
    main()