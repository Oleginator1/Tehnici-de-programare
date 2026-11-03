import re
from collections import Counter

# A1. Scheletul și funcția care întoarce o fișă
TIPAR = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\S+) port")
 
def esec(linie):
    m = TIPAR.search(linie)
    if m is None:
        return None
    else:
        return (m.group(1), m.group(2))
    


# A2. Lista de eșecuri, robustă la rânduri stricate
def citeste_esecuri(cale):
    esecuri = []
    try:
        f = open(cale, encoding="utf-8")
    except FileNotFoundError:
        print("nu gasesc", cale)
        return esecuri
    with f:
        for linie in f:
            r = esec(linie)
            if r is not None:
                esecuri.append({"user": r[0], "ip": r[1]})
    return esecuri
 


# A3. Numărarea pe IP: o funcție cu return 
def pe_ip(esecuri):
    return (Counter(e["ip"] for e in esecuri))
 



# A4. Rezumatul   
def main():
    print(esec("... Failed password for root from 203.0.113.9 port 51230 ssh2"))
    print(esec("<linie stricata fara structura>"))
    
    esecuri = citeste_esecuri("aparare/start/auth.log")
    print("esecuri:", len(esecuri))
    
    counts = pe_ip(esecuri)
    for ip, n in counts.most_common():
        print(f"  {ip}: {n}")
    return 0

if __name__ == "__main__":
    main()