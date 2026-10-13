# Laborator: funcții, metode și importuri pe web
# Student: <Nastas Oleg>

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import requests
import time

# Exercițiul 9. Elementele de bază ale răspunsului. 
# Descărcați pagina principală și afișați response.status_code, response.ok, response.url și response.encoding. 
# Lângă fiecare linie, scrieți un comentariu care spune dacă este un atribut sau o metodă.
response = requests.get(BASE_URL, timeout=TIMEOUT)
print("Ex 9: ")
print(response.status_code) #atribut
print(response.ok) #atribut
print(response.url) #
print(response.encoding) 
time.sleep(1)


# Exercițiul 10. Tratarea erorilor cu o metodă. Apelați response.raise_for_status() pe pagina principală. 
# Apoi trimiteți o cerere către BASE_URL + "/this-page-does-not-exist" și prindeți excepția requests.HTTPError.
# Afișați un mesaj prietenos în loc să lăsați programul să se oprească cu eroare.

print("Ex 10")
response.raise_for_status()
try:
    bad_res = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    bad_res.raise_for_status()
except requests.HTTPError as err:
    print(f"Pagina cautata nu exista: {err}")



# Exercițiul 11. Toate antetele. Parcurgeți response.headers.items() și afișați fiecare antet în forma Nume: valoare.
print("Ex 11")
for name, value in response.headers.items():
    print(f"{name}: {value}")



# Exercițiul 12. Metode de dicționar. Folosiți response.headers.get() pentru a afișa antetele Server 
# și Content-Type, cu "lipsește" ca valoare implicită. Apoi încercați response.headers.get("content-type"), cu litere mici. 
# Ce observați?
print("Ex 12:")
print("Server:", response.headers.get("Server", "lipsește"))
print("Content-Type:", response.headers.get("Content-Type", "lipsește"))
print("content-type:", response.headers.get("content-type", "lipsește"))

# headers.get() este o functie case insensitive deci poate ruleaza la fel indiferent daca primeste parametrul cu majustule sau minuscule


# Exercițiul 13. Înlănțuirea metodelor de șir. Numărați de câte ori apare cuvântul cyber pe pagina principală, 
# cu response.text.lower().count("cyber"). Într-un comentariu, explicați de ce puteți înlănțui .lower() și .count().
print("Ex 13:")
print(f"Cyber apare de {response.text.lower().count("cyber")} ori")
# Putem inlantui .lower() si .count() pentru ca lower returneaza un string nou si apoi functia count este executata
# asupra stringului, deoarece toate stringurile au functia count()


# Exercițiul 14. Găsirea titlului. Folosiți .find() și felierea (slicing) 
# pe response.text pentru a extrage textul dintre <title> și </title>. Curățați-l cu .strip() și afișați-l.
# Indiciu: start = html.find("<title>") + len("<title>")

html = response.text
start = html.find("<title>")
if start == -1:
    print("Ex 14: Nu exista title")
else:
    start += len("<title>")
    end = html.find("</title>", start)
    title = html[start:end].strip()
    print(f"Ex 14: {title}")


# Exercițiul 15. Numărarea liniilor.
# Împărțiți codul HTML în linii cu .splitlines(). 
# Afișați câte linii sunt și lungimea celei mai lungi linii, folosind max(lines, key=len).

lines = html.splitlines()
print("Ex 15:")
print(f"Total linii: {len(lines)}")
print(f"Cea mai lunga linie: {len(max(lines, key=len))}")


# Exercițiul 16. Verificarea HTTPS. Folosiți .startswith() 
# pentru a verifica dacă response.url începe cu https://. 
# Afișați Conexiune securizată sau Conexiune nesecurizată.
print("Ex 16:")
if response.url.startswith("https://"):
    print("Conexiune securizata")
else:
    print("Conexiune nesecurizata")



# Exercițiul 17. Urmărirea redirecționărilor. Trimiteți o cerere către http://cybercor.org (HTTP simplu, fără S).
# Parcurgeți response.history și afișați codul de stare și URL-ul fiecărei redirecționări, apoi URL-ul final.

print("Ex 17:")
response = requests.get("http://cybercor.org", timeout=TIMEOUT)
for r in response.history:
    print(f"Cod: {r.status_code} -> {r.url}")
print(response.url)
time.sleep(1)




# Exercițiul 18. HEAD versus GET. Trimiteți o cerere către pagina principală cu requests.head() și una cu requests.get().
# Comparați len(response.content) pentru ambele și explicați diferența într-un comentariu.
print("Ex 18:")
response = requests.head(BASE_URL, timeout=TIMEOUT)
print("Head:", len(response.content))
time.sleep(1)

response = requests.get(BASE_URL, timeout=TIMEOUT)
print("Get:", len(response.content))
time.sleep(1)

# HEAD cere doar antetele (status + headers), fara corp, deci
# len(head.content) este 0. GET aduce si corpul paginii (HTML-ul).
# HEAD e util pentru a verifica rapid o pagina fara a o descarca.



# Exercițiul 19. Cookie-uri. Parcurgeți response.cookies și afișați, 
# pentru fiecare cookie, atributele .name și .secure. Dacă nu există cookie-uri, afișați Niciun cookie setat.
print("Ex 19:")
if len(response.cookies) == 0:
    print("Niciun cookie setat")
else:
    for cookie in response.cookies:
        print("Name:", cookie.name, "Secure:", cookie.secure)



# Exercițiul 20. Sesiuni. Creați un obiect requests.Session() 
# și setați un User-Agent personalizat cu session.headers.update({"User-Agent": "WebLab-<numele vostru>"}).
# Trimiteți o cerere către ECHO_URL + "/headers" și confirmați în rezultat că antetul a fost trimis.

print("Ex 20:")
session = requests.Session()
session.headers.update({"User-Agent": "WebLab-Nastas Oleg"})
time.sleep(1)
response = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
print(response.json())
sent = response.json()["headers"].get("User-Agent")
print(sent)




# Verificați-vă: atât response.text, cât și response.json() vă dau corpul răspunsului. De ce unul are paranteze, iar celălalt nu?
# pentru ca json() e o metoda care poate primi argumente, iar .text este un atribut care este o valaoare gata de citit