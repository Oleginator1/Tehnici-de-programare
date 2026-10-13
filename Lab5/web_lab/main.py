# Laborator: funcții, metode și importuri pe web
# Student: <Nastas Oleg>

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import time
import webtools #44
from webtools import get_title, security_headers #45
from webtools import DEFAULT_HEADERS #47
import argparse


# Exercițiul 48. Argumente din linia de comandă.
# Folosiți argparse în main.py, astfel încât programul să ruleze ca python main.py https://cybercor.org.
# Transmiteți argumentul URL funcțiilor voastre, în loc să folosiți url.

parser = argparse.ArgumentParser(description="Raport despre un site web")
parser.add_argument("url", help="ex:. https://cybercor.org")
args = parser.parse_args()
url = args.url.rstrip("/")

print("Ex 44: Titlul:",webtools.get_title(webtools.fetch(url).text))
time.sleep(1)


# Exercițiul 45. Importarea anumitor nume. În main.py, treceți la 
# from webtools import get_title, security_headers.
# Într-un comentariu, explicați ce s-ar întâmpla dacă main.py ar avea și o funcție proprie numită get_title.

print("Ex 45: titlu =", get_title(webtools.fetch(url).text))
time.sleep(1)
print("Ex 45: antete securitate =", security_headers(url))
time.sleep(1)

# Daca main.py ar defini si el o funcție get_title(), definitia
# locală ar înlocui numele importat. Apelurile get_title() din
# main.py ar rula codul din main.py, nu cel din webtools merge dupa ultima
# atribuire a numelui). Cu import webtools nu apare problema, fiindca
# functia se apeleaza prin prefix: webtools.get_title().

#Ex 47
print("Ex 47: DEFAULT_HEADERS =", DEFAULT_HEADERS)


#Ex 49
webtools.save_csv(webtools.check_paths(url, ["/", "/robots.txt", "/sitemap.xml"]))
print("Salvat in report.csv")
time.sleep(1)


webtools.site_report(url)
