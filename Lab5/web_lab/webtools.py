# Laborator: funcții, metode și importuri pe web
# Student: <Nastas Oleg>

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde


import requests
import time
from datetime import datetime, UTC
import csv
from urllib.parse import urlparse, urljoin
import socket
import ssl
import re
import json


# Exercițiul 47. Constante de modul. 
# Adăugați constanta DEFAULT_HEADERS = {"User-Agent": "WebLab-<numele vostru>"} în webtools.py #
# și folosiți-o în fetch(). În main.py, importați constanta și afișați-o.

DEFAULT_HEADERS = {"User-Agent": "WebLab-Nastas Oleg"}

# Exercițiul 44. Crearea unui modul. Mutați fetch, get_status, 
# get_title și security_headers într-un fișier nou, webtools.py. 
# În main.py, scrieți import webtools și apelați webtools.get_title(webtools.fetch(BASE_URL).text).

def fetch(url: str, timeout: int = 10) -> requests.Response:
    """Efectuează o cerere HTTP GET utilizând antetele implicite transmise în aplicație.

    Args:
        url (str): URL-ul destinație.
        timeout (int): Timpul maxim de așteptare în secunde. Implicit este 10.

    Returns:
        requests.Response: Obiectul răspuns HTTP primit de la server.
    """
    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    return response


def get_status(url: str) -> int:
    """Obține codul de stare HTTP pentru un anumit URL.

    Args:
        url (str): URL-ul complet care va fi interogat.

    Returns:
        int: Codul de stare HTTP (ex: 200, 404).
    """
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code


def get_title(html: str) -> str:
    """Returnează titlul unei pagini HTML din <title>

    Args:
        html(str): textul unei pagini HTML

    Returns:
        str: textul din interiorul <title>
    """
    start = html.find("<title>")
    if start == -1:
        return ""
    start += len("<title>")
    end = html.find("</title>", start)
    return html[start:end].strip()


headers = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
]


def security_headers(url: str) -> dict:
    """Verifică existența a 5 antete HTTP esențiale pentru securitate pe un URL specificat.

    Args:
        url (str): URL-ul site-ului analizat.

    Returns:
        dict: Un dicționar cu numele antetelor drept chei și valori booleene (True/False) pentru prezența lor.
    """
    response = requests.get(url, timeout=TIMEOUT)
    results = {}
    for header in headers:
        results[header] = header in response.headers
    return results


def score_headers(results: dict) -> str:
    """Calculează un scor fracționar bazat pe numărul de antete de securitate găsite.

    Args:
        results (dict): Dicționarul cu rezultate obținut din funcția `security_headers`.

    Returns:
        str: Un șir de caractere reprezentat sub formă de scor (ex: "3/5").
    """
    count = 0
    for header in results:
        if results[header] == True:
            count += 1
    return f"{count}/{len(results)}"


def check_paths(base: str, paths: list) -> dict:
    """Verifică o listă de căi relative atașate la un URL de bază și colectează codurile lor de stare.

    Args:
        base (str): URL-ul de bază al site-ului.
        paths (list): O listă de string-uri reprezentând căile relative de verificat.

    Returns:
        dict: Un dicționar care mapează fiecare cale la codul ei status HTTP (sau None în caz de eroare).
    """
    results = {}
    for e in paths:
        try:
            results[e] = get_status(base + e)
        except requests.RequestException:
            results[e] = None
        time.sleep(1)
    return results


def resolve(hostname: str) -> str:
    """Efectuează o interogare DNS pentru a obține adresa IPv4 asociată unui nume de domeniu.

    Args:
        hostname (str): Numele de domeniu (ex: 'cybercor.org').

    Returns:
        str: Adresa IP în format string (ex: '192.168.1.1').
    """
    return socket.gethostbyname(hostname)


def redirect_chain(url: str) -> list:
    """Urmărește și colectează istoricul de redirecționări HTTP (redirection chain) parcurs de un URL.

    Args:
        url (str): URL-ul inițial de la care pornește verificarea.

    Returns:
        list: O listă de tupluri, unde fiecare tuplu conține codul de stare al redirecționării și locația (URL-ul intermediar).
    """
    response = fetch(url)
    return [
        (step.status_code, step.headers.get("Location", step.url))
        for step in response.history
    ]


def fetch_robots(base: str) -> str:
    """Descarcă conținutul text al fișierului robots.txt de pe un domeniu de bază.

    Args:
        base (str): URL-ul de bază al site-ului (fără / final).

    Returns:
        str: Conținutul brut al fișierului robots.txt, sau None în caz de eroare/lipsă.
    """
    try:
        response = requests.get(base + "/robots.txt", timeout=TIMEOUT)
    except requests.RequestException:
        return None
    if response.status_code != 200:
        return None

    return response.text


def disallowed_paths(robots_text: str) -> list:
    """Analizează conținutul unui fișier robots.txt și extrage toate căile interzise (Disallow).

    Args:
        robots_text (str): Textul brut extras din robots.txt (sau None).

    Returns:
        list: O listă de string-uri cu toate rutele restricționate găsite. Returnează [] dacă input-ul este None.
    """
    if robots_text is None:
        return []
    paths = []
    for line in robots_text.splitlines():
        if line.lower().startswith("disallow:"):
            parts = line.split(":", 1)
            if len(parts) > 1:
                value = parts[1].strip()
                if value:
                    paths.append(value)
    return paths


def extract_links(html: str) -> list:
    """Extrage toate legăturile (href) dintr-un șir de caractere HTML, eliminând duplicatele din rezultat.

    Args:
        html (str): Textul sursă HTML al paginii.

    Returns:
        list: O listă de string-uri conținând legăturile unice găsite.
    """
    links = re.findall(r'href="([^"]+)"', html)
    return list(dict.fromkeys(links))


def split_links(links: list, domain: str) -> tuple:
    """Clasifică o listă de legături în interne (aparțin aceluiași domeniu) și externe (trimit către alte site-uri).

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



# Exercițiul 49. Un raport CSV. Folosiți modulul csv pentru a salva 
# rezultatul funcției check_paths() în report.csv, cu coloanele path, status și checked_at.
# Pentru oră, folosiți datetime.now().isoformat().

def save_csv(results: dict, filename:str = "report.csv") -> None:
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["path", "status", "checked_at"])
        for path, status in results.items():
            writer.writerow([path, status, datetime.now().isoformat()])



# Exercițiul 50. Proiect final: raportul site-ului. 
# Scrieți site_report(url) în webtools.py. 
# Funcția trebuie să folosească funcțiile voastre pentru a colecta
# toate informațiile de mai jos, să le afișeze și să le salveze în report.json:
#1.	Codul de stare și URL-ul final
#2.	Titlul paginii
#3.	Adresa IP
#4.	Lanțul de redirecționări pornind de la http://
#5.	Scorul antetelor de securitate, de exemplu 3/5
#6.	Zilele rămase până la expirarea certificatului
#7.	Numărul de legături interne și externe
#8.	Căile interzise din robots.txt



def safe(func: str, *args):
    try:
        return func(*args)
    except Exception:
        return None

    
def site_report(url: str, filename:str = "report.json") -> dict:
    parsed = urlparse(url)
    host = parsed.netloc

    response = fetch(url)
    html = response.text
    title = get_title(html)
    ip = safe(resolve, host)
    time.sleep(1)

    chain = safe(redirect_chain, "https://" + host)
    time.sleep(1)

    sec = safe(security_headers, url)
    score = score_headers(sec) if sec else None
    days = safe(cert_days_left, host)
    internal, external = split_links(extract_links(html), host)
    time.sleep(1)
    disallowed = disallowed_paths(safe(fetch_robots, url.rstrip("/")))

    report = {
        "url": url,
        "status": response.status_code,
        "final_url": response.url,
        "title": title,
        "ip": ip,
        "redirects": [{"status": s, "url": u} for s, u in (chain or [])],
        "security_score": score,
        "security_headers": sec,
        "cert_days_left": days,
        "internal_links": len(internal),
        "external_links": len(external),
        "disallowed_paths": disallowed,
        "checked_at": datetime.now().isoformat(),
    }


    redirects_text = " | ".join(f"{s} -> {u}" for s, u in (chain or [])) or "fără"
    print(f"=== Raport site: {url} ===")
    print(f"Cod de stare: {report['status']} (URL final: {report['final_url']})")
    print(f"Titlu: {title or 'lipsește'}")
    print(f"Adresă IP: {ip or 'necunoscută'}")
    print(f"Redirecționări: {redirects_text}")
    print(f"Scor securitate: {score or 'necunoscut'}")
    print(f"Certificat: {days} de zile rămase" if days is not None
          else "Certificat: necunoscut")
    print(f"Legături: {len(internal)} interne, {len(external)} externe")
    print(f"Căi interzise: {', '.join(disallowed) or 'niciuna'}")

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)
    print(f"Salvat în {filename}")
    return report


# Ex 46:
if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))
# Când rulăm python webtools.py, Python setează __name__ == "__main__",
# deci blocul se executa. Cand main.py face import webtools,
# __name__ este "webtools", condiția e falsă si autotestul nu ruleaza
# altfel fiecare import ar trimite o cerere web nedorita.