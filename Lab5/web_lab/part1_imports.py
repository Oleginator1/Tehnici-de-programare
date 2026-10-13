# Laborator: funcții, metode și importuri pe web
# Student: <Nastas Oleg>

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

# Exercițiul 1. Primul import. Scrieți import requests și afișați requests.__version__.
# Apoi scrieți import urllib.request.
# Într-un comentariu, explicați de ce requests a avut nevoie de pip install, iar urllib nu.
import requests
import urllib.request
import time
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
print("Ex1 - Versiunea requests:", requests.__version__)

# requests este un modul extern care nu vine cu Python, de aceea trebuie descărcat cu pip install requests".
# Dar urllib face parte din biblioteca standard si se instaleaza odata cu Python,


# Exercițiul 2. Două stiluri de import. Descărcați pagina BASE_URL cu requests.get() 
# și afișați codul de stare. Apoi rescrieți același script folosind from requests import get.
# Într-un comentariu, scrieți câte un avantaj al fiecărui stil.

response = requests.get(BASE_URL, timeout=TIMEOUT)
print("Ex 2 - Codul de stare prin import requsts:", response.status_code)
time.sleep(1)

from requests import get
response = get(BASE_URL, timeout=TIMEOUT)
print("Ex 2 - Codul de stare prin import get:", response.status_code)
time.sleep(1)
# Avantajul la import.requests este ca nu apar conflicte la nume daca mai este o functie get,
# este vazuta clar calea de unde vine functia si toate functiile publice din requests pot fi acesate
# Avantajula la from requests import get este ca codul este mai scurt si nu trebuie sa indicam calea

# Exercițiul 3. Alias-uri. Importați requests cu un alias: import requests as rq. 
# Descărcați pagina principală cu rq.get(). 
# Într-un comentariu, spuneți când un alias face codul mai ușor de citit și când îl face mai greu de citit.

import requests as rq
print("Ex 3 - alias cu rq", rq.get(BASE_URL, timeout=TIMEOUT).status_code)
time.sleep(1)

# Alias face mai usor de citit codul cand numele la modul este lung sau cand exista o conventii de import pentru anumite module 
# Alias face mai greu de citit codul cand acesta este greu de inteles si nu se intelege de odata ce reprezinta, este nevoie de ghicit
# si in diferite fisiere aliasul difera



# Exercițiul 4. Doar biblioteca standard. Descărcați pagina principală folosind doar urllib.request.urlopen(). 
# Afișați atributul .status al răspunsului și primele 200 de caractere din corp.
# Indiciu: .read() returnează octeți (bytes). Folosiți .decode("utf-8") ca să îi transformați într-un șir de caractere.

req = urllib.request.Request(
    BASE_URL, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)
with urllib.request.urlopen(req, timeout=TIMEOUT) as res:
    body = res.read().decode("utf-8")
    print("Ex 4 - status:", res.status)
    print(body[:200])

time.sleep(1)


# Exercițiul 5. Priviți în interiorul unui modul. Rulați print(dir(requests)). 
# Alegeți trei nume din rezultat și scrieți, într-un comentariu, dacă fiecare este o funcție, o clasă sau un modul.
print("Ex 5:", dir(requests))

# get - functie
# Session - clasa
# exceptions - modul



# Exercițiul 6. Citiți documentația. Rulați help(requests.get).
# Găsiți parametrul care setează timpul maxim de așteptare și folosiți-l într-o cerere.
print("Ex 6")
help(requests.get)
# parametrul care setează timpul maxim de așteptare se numește timeout in help este scris ca **kwargs
time.sleep(1)
response = requests.get(BASE_URL, timeout=TIMEOUT)
print("Ex 6 - cerere cu timeout =", TIMEOUT, "->", response.status_code)
time.sleep(1)


# Exercițiul 7. Cronometrarea unei cereri. Importați time și măsurați cât durează o cerere către pagina principală,
# apelând time.perf_counter() înainte și după. Comparați rezultatul cu response.elapsed.
start = time.perf_counter()
response = requests.get(BASE_URL, timeout=TIMEOUT)
end = time.perf_counter()

print(f"Ex 7 - perf_counter: {end - start:.3f}s")
print("Ex 7 - response elapsed:", response.elapsed.total_seconds(), "s")
# perf_counter masoara tot timpul masurat de noi inclusiv descarcarea
# corpului si munca din interiorul bibliotecii, pe cand response.elapsed
# masoara doar intervalul dintre trimiterea cererii si sosirea antetelor
# raspunsului, deci este de obicei putin mai mic.



# Exercițiul 8. Când un import eșuează. Scrieți un script care încearcă import bs4 într-un bloc try / except ImportError. 
# Dacă modulul lipsește, afișați: Instalați modulul cu: pip install beautifulsoup4.

try:
    import bs4
    print("Modulul a fost gasit")
except ImportError:
    print("Instalați modulul cu: pip install beautifulsoup4.")

# Verificați-vă: care este diferența dintre un modul, un pachet și o bibliotecă?
# Un modul este un singur fisier Python care conține cod (functii, clase, variabile), 
# un pachet este un director care contine mai multe module organizate, 
# o biblioteca este o colectie mai mare de pachete si module care ofera o gama larga de funcționalitati pentru un scop anume.

