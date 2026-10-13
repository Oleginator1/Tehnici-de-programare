# Laborator: funcții, metode și importuri pe web
# Student: <Nastas Oleg>

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import re
import hashlib
import json
import socket
import ssl
import time
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
import requests
from datetime import datetime, UTC


# Exercițiul 35. Descompunerea unui URL. Folosiți urllib.parse.urlparse()
# pe https://cybercor.org/path?x=1#top. Afișați .scheme, .netloc, .path, .query și .fragment.

def parse_demo() -> None:
    """Descompune un URL demonstrativ în componentele sale structurale și le afișează."""
    parts = urlparse(BASE_URL + "/path?x=1#top")
    print(f"Scheme: {parts.scheme}")
    print(f"Netloc: {parts.netloc}")
    print(f"Path {parts.path}")
    print(f"Query {parts.query}")
    print(f"Fragment: {parts.fragment}")


print("Ex 35:")
parse_demo()


# Exercițiul 36. Compunerea URL-urilor. Folosiți urllib.parse.urljoin()
# pentru a transforma legăturile relative /about, contact.html și ../index.html în URL-uri complete, pornind de la BASE_URL.
print("Ex 36:")


def join_demo() -> None:
    """Transformă o listă predefinită de legături relative în URL-uri absolute,

    folosind URL-ul de bază al aplicației.
    """
    for link in ["/about", "contact.html", "../index.html"]:
        print(link, "->", urljoin(BASE_URL, link))


join_demo()


# Exercițiul 37. Extragerea legăturilor.
# Folosiți re.findall(r'href="([^"]+)"', html) pentru a obține toate legăturile de pe pagina principală.
# Puneți codul într-o funcție extract_links(html), care returnează legăturile fără duplicate.


def extract_links(html: str) -> list:
    """Extrage toate legăturile (href) dintr-un șir de caractere HTML,

    eliminând duplicatele din rezultat.

    Args:
        html (str): Textul sursă HTML al paginii.

    Returns:
        list: O listă de string-uri conținând legăturile unice găsite.
    """
    links = re.findall(r'href="([^"]+)"', html)
    return list(dict.fromkeys(links))


import requests

response = requests.get(BASE_URL, timeout=TIMEOUT)
links = extract_links(response.text)
print(f"Ex 37: Legaturi unice: {links}")


# Exercițiul 38. Interne sau externe? Scrieți split_links(links, domain),
# care returnează două liste: legăturile de pe același domeniu și legăturile către alte site-uri.
# Folosiți mai întâi urljoin(), apoi urlparse().netloc.


def split_links(links: list, domain: str) -> tuple:
    """Clasifică o listă de legături în interne (aparțin aceluiași domeniu)

    și externe (trimit către alte site-uri).

    Args:
        links (list): Lista de legături relative sau absolute.
        domain (str): Domeniul de referință (ex: 'cybercor.org').

    Returns:
        tuple: Două liste de string-uri sub forma (internal_links, external_links).
    """
    internal, external = [], []

    if not domain.startswith(("http://", "https://")):
        base_url = "https://" + domain
    else:
        base_url = domain

    for link in links:
        full_link = urljoin(base_url, link)
        parsed = urlparse(full_link)
        if parsed.netloc.lower() == domain.lower():
            internal.append(full_link)
        else:
            external.append(full_link)
    return internal, external


internal, external = split_links(links, "cybercor.org")
print(f"Ex 38: interne - {internal}, externe - {external}")


# Exercițiul 39. Propriile metode.
# Creați o clasă care moștenește html.parser.HTMLParser și suprascrieți metoda handle_starttag(),
# pentru a colecta atributul src al fiecărui tag <img>.


class ImageFinder(HTMLParser):
    """Un parser HTML personalizat conceput pentru a identifica și colecta

    atributele 'src' din toate etichetele <img> întâlnite în document.
    """

    def __init__(self):
        """Inițializează parserul și configurează o listă vidă pentru stocarea legăturilor imaginilor."""
        super().__init__()
        self.images = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        """Metodă callback apelată automat la întâlnirea fiecărui tag de deschidere.

        Filtrează tag-urile 'img' și salvează valoarea atributului 'src'.

        Args:
            tag (str): Numele tag-ului curent convertit în litere mici.
            attrs (list): O listă de tupluri (nume_atribut, valoare).
        """
        if tag == "img":
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)


test_html = """
<html><body>
  <img src="/logo.png" alt="Logo">
  <IMG SRC="poza.jpg">
  <img alt="imagine fără src">
  <img src="https://cdn.example.com/banner.webp" />
  <a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""
print("Ex 39:")
finder = ImageFinder()
finder.feed(test_html)
print(finder.images)

assert finder.images == [
    "/logo.png",  # imagine obișnuită
    "poza.jpg",  # tag scris cu majuscule
    "https://cdn.example.com/banner.webp",  # tag care se închide singur
], "Parserul nu a găsit exact imaginile așteptate"
print("Testul a trecut!")


response = requests.get(BASE_URL, timeout=TIMEOUT)
finder = ImageFinder()
finder.feed(response.text)
print(len(finder.images), "imagini găsite")
for src in finder.images:
    print(src)
time.sleep(1)


# Exercițiul 40. Amprenta paginii. Scrieți page_fingerprint(url),
# care returnează hashlib.sha256(response.content).hexdigest().
# Rulați-o de două ori și comparați rezultatele. Când ar fi diferite?


def page_fingerprint(url: str) -> str:
    """Generează o amprentă unică SHA-256 (hash) bazată pe conținutul binar

    brut al paginii web solicitate.

    Args:
        url (str): URL-ul paginii web de verificat.

    Returns:
        str: Reprezentarea în hexazecimal a hash-ului generat.
    """
    response = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(response.content).hexdigest()


a = page_fingerprint(BASE_URL)
time.sleep(1)
b = page_fingerprint(BASE_URL)
print("Ex 40:")
print(a == b, a, b)
time.sleep(1)


# Exercițiul 41. Salvarea în JSON. Salvați antetele paginii principale în headers.json
# cu json.dump(dict(response.headers), file, indent=2).
# Apoi încărcați fișierul înapoi cu json.load() și afișați un antet din el.


def save_headers_json(url: str, filename: str = "headers.json") -> None:
    """Descarcă antetele HTTP ale unui URL, le salvează structurat într-un fișier JSON,

    iar apoi le reîncarcă pentru a valida operațiunea.

    Args:
        url (str): URL-ul de unde se preiau antetele.
        filename (str): Numele fișierului JSON generat. Implicit este 'headers.json'.
    """
    response = requests.get(url, timeout=TIMEOUT)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(dict(response.headers), file, indent=2)
    with open(filename, encoding="utf-8") as file:
        data = json.load(file)
    print("Content-Type:", data.get("Content-Type", "None"))


print("Ex 41:")
save_headers_json(BASE_URL)


# Exercițiul 42. Interogare DNS. Scrieți resolve(hostname),
# care returnează socket.gethostbyname(hostname). Afișați adresa IP a domeniului cybercor.org.


def resolve(hostname: str) -> str:
    """Efectuează o interogare DNS pentru a obține adresa IPv4 asociată unui nume de domeniu.

    Args:
        hostname (str): Numele de domeniu (ex: 'cybercor.org').

    Returns:
        str: Adresa IP în format string (ex: '192.168.1.1').
    """
    return socket.gethostbyname(hostname)

print("Ex 42:")
print(f"Ip: {resolve("cybercor.org")}")


# Exercițiul 43. Expirarea certificatului. Scrieți cert_days_left(hostname),
# care se conectează la portul 443, citește certificatul și returnează câte zile mai sunt până la expirarea lui.

# Am folosit get_server_certificate, deoarece pe calculatorul meu magazinul de certificate Windows conține un certificat expirat și conexiunea verificată eșuează
def cert_days_left(hostname: str) -> int:
    """Se conectează securizat la un server și calculează numărul de zile

        rămase până la expirarea certificatului său SSL/TLS.

        Args:
            hostname (str): Numele de domeniu al serverului verificat.

        Returns:
            int: Numărul de zile întregi rămase până la expirare.
    """
    # 1. Descărcăm certificatul text (PEM) fără validare
    pem_cert = ssl.get_server_certificate((hostname, 443), timeout=TIMEOUT)
    
    # 2. Îl convertim în format binar (DER)
    der_cert = ssl.PEM_cert_to_DER_cert(pem_cert)
    
    # 3. Decodificăm ca 'latin-1' pentru a evita erorile de octeți nuli
    cert_text = der_cert.decode('latin-1')
    
    # 4. Găsim toate structurile de timp UTC (YYMMDDHHMMSSZ sau YYYYMMDDHHMMSSZ)
    matches = re.findall(r'(\d{12,14}Z)', cert_text)
    
    if not matches:
        raise ValueError("Nu s-a putut găsi data de expirare în certificat.")
        
    # În structura ASN.1, a doua dată din listă este întotdeauna 'notAfter' (data expirării)
    expiration_raw = matches[1] if len(matches) > 1 else matches[0]
    
    # 5. Parsăm string-ul folosind formatul corect de timp și îi setăm fusul orar UTC
    if len(expiration_raw) == 13:      # Format: YYMMDDHHMMSSZ
        expires_date = datetime.strptime(expiration_raw, "%y%m%d%H%M%SZ").replace(tzinfo=UTC)
    else:                              # Format: YYYYMMDDHHMMSSZ
        expires_date = datetime.strptime(expiration_raw, "%Y%m%d%H%M%SZ").replace(tzinfo=UTC)
    
    # 6. Calculăm zilele rămase față de momentul actual folosind obiecte aware de timezone
    now = datetime.now(UTC)
    delta = expires_date - now
    
    return delta.days



print("Ex 43:", cert_days_left("cybercor.org"), "zile ramase")