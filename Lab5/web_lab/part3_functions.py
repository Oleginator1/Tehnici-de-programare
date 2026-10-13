# Laborator: funcții, metode și importuri pe web
# Student: <Nastas Oleg>

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import time
import requests

# Exercițiul 21. Prima funcție. Scrieți fetch(url), care returnează obiectul răspuns. 
# Apelați-o pentru BASE_URL și afișați codul de stare.

def fetch(url: str, timeout: int = 10) -> requests.Response:
    """Efectuează o cerere HTTP GET către URL-ul specificat.

    Args:
        url (str): URL-ul destinație.
        timeout (int): Timpul maxim de așteptare în secunde. Implicit este 10.

    Returns:
        requests.Response: Obiectul răspuns HTTP primit de la server.
    """
    response = requests.get(url, timeout=timeout)
    time.sleep(1)
    return response

print("Ex 21:", fetch(BASE_URL).status_code)



# Exercițiul 22. Returnarea unei singure valori. Scrieți get_status(url), care returnează doar codul de stare.
# Apelați-o pentru /, /robots.txt și /sitemap.xml, cu time.sleep(1) între apeluri.

def get_status(url: str) -> int:
    """Obține codul de stare HTTP pentru un anumit URL.

    Args:
        url (str): URL-ul complet care va fi interogat.

    Returns:
        int: Codul de stare HTTP (ex: 200, 404).
    """
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code

print("Ex 22:")
paths = ["/", "/robots.txt", "/sitemap.xml"]
for path in paths:
    print(f"Codul de stare pentru {BASE_URL + path} este {get_status(BASE_URL + path)}")
    time.sleep(1)



# Exercițiul 23. Parametri impliciți. Modificați funcția în fetch(url, timeout=10). 
# Apelați-o o dată cu valoarea implicită și o dată cu timeout=3.

print("Ex 23:")
print(f"Valoare implicita: {fetch(BASE_URL).status_code}")
print(f"Valoare timeout=3: {fetch(BASE_URL, 3).status_code}")



# Exercițiul 24. O singură sarcină pe funcție. Scrieți get_title(html), 
# care primește un șir HTML și returnează titlul paginii, refolosind logica din exercițiul 14.
# Observați că această funcție nu face nicio operație de rețea: descărcarea și analiza sunt acum separate.

def get_title(html: str) -> str:
    """Returnează titlul unei pagini HTML din tag-ul <title>.

    Args:
        html (str): Textul sursă al paginii HTML.

    Returns:
        str: Textul curățat din interiorul etichetei <title> sau un șir gol dacă lipsește.
    """
    start = html.find("<title>")
    if start == -1:
        return ""
    start += len("<title>")
    end = html.find("</title>", start)
    return html[start:end].strip()

print("Ex 24:")
print(get_title(fetch(BASE_URL).text))
time.sleep(1)


# Exercițiul 25. Docstring-uri. Adăugați un docstring funcției get_title și afișați-l cu help(get_title).
help(get_title)


# Exercițiul 26. Adnotări de tip. Adăugați adnotări de tip (type hints) funcțiilor, 
# de exemplu def get_status(url: str) -> int:.
# Apelați get_status(123) și observați ce se întâmplă. Vă opresc adnotările de tip?

try:
    get_status(123)
except Exception as err:
    print("Ex 26:", type(err).__name__, "-", err)

# Adnotările de tip nu opresc dacă introducem o valoare de tip diferit, 
# codul va rula dar va afișa o eroare deoarece librăria requests așteaptă un string pentru URL.
# Adnotările sunt doar informații despre tipul de date cerut de argument.




# Exercițiul 27. Fără opriri neașteptate. Scrieți page_exists(url), care returnează True sau False. 
# Folosiți try / except requests.RequestException, 
# astfel încât funcția să returneze False în loc să se oprească cu eroare, chiar și pentru un URL precum https://this-domain-does-not-exist.invalid.

def page_exists(url: str) -> bool:
    """Verifică dacă o pagină web există și este accesibilă cu succes.

    Args:
        url (str): URL-ul paginii verificate.

    Returns:
        bool: True dacă statusul este de succes (2xx) și False în caz de eroare/excepție de rețea.
    """
    try:
        response = requests.get(url, timeout=TIMEOUT)
        return response.ok
    except requests.RequestException:
        return False

print("Ex 27:")
print(page_exists("https://this-domain-does-not-exist.invalid"))


# Exercițiul 28. Returnarea unui dicționar. Scrieți check_paths(base, paths), 
# care primește o listă precum ["/", "/robots.txt", "/sitemap.xml"] și returnează un dicționar {path: status_code}.

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

print("Ex 28:")
print(check_paths(BASE_URL, paths))



# Exercițiul 29. Argumente cu nume. Scrieți get_header(url, name, default="lipsește"), 
# care returnează valoarea unui singur antet. Apelați-o cu argumente cu nume: get_header(BASE_URL, name="Server").

def get_header(url: str, name: str, default: str = "lipsește") -> str:
    """Extrage valoarea unui antet (header) specific din răspunsul HTTP al unui URL.

    Args:
        url (str): URL-ul țintă.
        name (str): Numele antetului HTTP căutat (ex: 'Content-Type').
        default (str): Valoarea returnată în cazul în care antetul nu există. Implicit este "lipsește".

    Returns:
        str: Valoarea antetului solicitat sau valoarea implicită.
    """
    response = requests.get(url, timeout=TIMEOUT)
    return response.headers.get(name, default)

print("Ex 29:")
print(get_header(BASE_URL, name="Server"))
time.sleep(1)




# Exercițiul 30. Antete de securitate. Scrieți security_headers(url), care verifică prezența acestor cinci antete și returnează {antet: True/False}:
#•	Strict-Transport-Security
#•	Content-Security-Policy
#•	X-Frame-Options
#•	X-Content-Type-Options
#•	Referrer-Policy

headers = ["Strict-Transport-Security",
           "Content-Security-Policy",
           "X-Frame-Options",
           "X-Content-Type-Options",
           "Referrer-Policy"]

def security_headers(url: str) -> dict:
    """Verifică existența a 5 antete HTTP esențiale pentru securitate pe un URL specificat.

    Args:
        url (str): URL-ul site-ului analizat.

    Returns:
        dict: Un dicționar cu numele antetelor drept chei și valori booleene (True/False) pentru prezența lor.
    """
    response  = requests.get(url, timeout=TIMEOUT)
    results = {}
    for header in headers:        
        results[header] = header in response.headers
    return results

print("Ex 30:")
print(security_headers(BASE_URL))
time.sleep(1)



# Exercițiul 31. Funcții care apelează funcții. Scrieți score_headers(results), 
# care primește dicționarul din exercițiul 30 și returnează un șir precum "3/5". 
# Apelați-le împreună: score_headers(security_headers(BASE_URL)).

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

print("Ex 31:")
print(score_headers(security_headers(BASE_URL)))
time.sleep(1)



# Exercițiul 32. Două funcții, o sarcină. Scrieți fetch_robots(base), 
# care returnează textul fișierului /robots.txt sau None dacă fișierul lipsește.
# Apoi scrieți disallowed_paths(robots_text), care returnează o listă cu toate valorile Disallow:.
# Asigurați-vă că funcționează și atunci când primește None.

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

text_robots = fetch_robots(BASE_URL)
print(f"Ex 32 - Cai interzise in robots.txt: {disallowed_paths(text_robots)}")
print(f"Ex 32 - Test functionare cu None: {disallowed_paths(None)}")
time.sleep(1)



# Exercițiul 33. Oricâte argumente. 
# Scrieți response_times(*urls), care returnează un dicționar {url: secunde}.
# Apelați-o cu două URL-uri.

def response_times(*urls: str) -> dict:
    """Măsoară timpul de răspuns în secunde pentru un număr variabil de URL-uri transmise.

    Args:
        *urls (str): Un număr arbitrar de argumente de tip string reprezentând URL-uri.

    Returns:
        dict: Un dicționar cu URL-urile drept chei și timpii de răspuns rotunjiți la 3 zecimale drept valori (-1 în caz de eroare).
    """
    time_s = {}
    for url in urls:
        try:
            start = time.time()
            response = requests.get(url, timeout=TIMEOUT)
            end = time.time()
            time_s[url] = round(end - start, 3)
        except requests.RequestException:
            time_s[url] = -1
            time.sleep(1)
        return time_s
    
print("Ex 33: ", response_times(BASE_URL, BASE_URL + "/robots.txt"))




# Exercițiul 34. Argumente cu nume colectate. 
# Scrieți log(message, **details), care afișează mesajul urmat de fiecare detaliu. 
# Exemplu: log("verificat", url=BASE_URL, status=200) afișează verificat | url=https://cybercor.org | status=200.

def log(message: str, **details: str) -> None:
    """Afișează un mesaj de jurnalizare formatat, combinat cu detalii adiționale sub formă de perechi cheie=valoare.
        Args:
        message (str): Mesajul principal al log-ului.
        **details (str): Argumente de tip keyword flexibile care adaugă context log-ului.
        Returns:
        None: Funcția doar printează rezultatul în consolă.
    """
    text = message
    if details:
        text += " | "
        elements = []
        for key, value in details.items():
            elements.append(f"{key}={value}")
        
        text += " | ".join(elements)
    print(text)

log("verificat", url=BASE_URL, status=200)






# Verificați-vă: care este diferența dintre a afișa o valoare cu print() în interiorul unei funcții și a o returna cu return?

# print() doar afiseaza o valoare pe ecran, funcția returnează apoi
# None și valoarea se pierde
# return trimite valoarea celui care a apelat functia, iar apoi
# o poate salva intr-o variabila, testa, combina cu alte functii sau scrie intr-un fisier.
