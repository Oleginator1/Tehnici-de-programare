## Laborator 6 — Informatii invizibile: forensics si steganography

### Lucrarea A — decoderul universal
- **Trebuie de rulat partea A cu "python arsenal/forensics/decode.py probe/mesaj.txt --fisier"
- **Trebuie de rulat test_decode.py cu "python -m pytest -v"
- **Mesajul cu straturi (`probe/mesaj.txt`):** ascundea `FLAG{straturi_de_encoding}`, sub trei straturi: base64 → base64 → hex.
- **XOR (`probe/xor.bin`):** cheia găsită este 128 (0x80); textul clar este `Un singur octet tine tot secretul... gaseste-l! FLAG{xor_un_octet}`.
- **Hash-uri (`probe/hashuri.txt`, MD5, dicționar `wordlist.txt`):** password, dragon, qwerty, letmein, monkey.

### Lucrarea B — forensics pe fisiere si LSB
- **Tipul real:** `probe/foto.jpg` este jpeg (`ff d8 ff`); `probe/ascuns.png` este png (`89 50 4e 47`).
- **Metadate EXIF (`foto.jpg`):** Make = Apple, Model = iPhone 13, DateTime = 2026:09:14 10:30:00.
- **GPS:** 47° 1′ 0″ N, 28° 51′ 27″ E, adică 47.0167, 28.8575 (Chișinău).
- **Arhiva ascunsă:** în `ascuns.png`, după octetul 782, se află un ZIP care conține `secret.txt` = `FLAG{ascuns_prin_carving}`.
- **Mesaj LSB:** în `stego.png` am ascuns și apoi am dezvăluit `FLAG{ascuns_in_pixeli}` (cu un octet 0 ca marcaj de final).
