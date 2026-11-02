import argparse, json, os


#A1. Scheletul și prima listă
def citeste_linii(cale):
    with open(cale, encoding="utf-8") as f:
        lines = [ln.strip() for ln in f]
    return [ln for ln in lines if ln and not ln.startswith("#")]       
 
cai = citeste_linii("arsenal/privesc/start/suid.txt")
print("linii SUID:", len(cai))


# A2. Nume unice: de la listă la mulțime
def nume(cale):
    return cale.rsplit("/", 1)[-1]
     
nume_unice = {nume(c) for c in cai}    # set comprehension
print("SUID distincte:", len(nume_unice))


# A3. Constatările SUID: listă de dicționare  
GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash",
        "less", "awk", "python3", "perl"}
 
def suid_constatari(cale):
    cai = citeste_linii(cale)
    return [{"cale": c, "nume": nume(c),
             "risc": "mare" if nume(c) in GTFO else "normal"}
              for c in sorted(set(cai))]    
 
suid = suid_constatari("arsenal/privesc/start/suid.txt")
mari = [c for c in suid if c["risc"] == "mare"]
print(len(suid), "SUID,", len(mari), "cu risc mare")
print(sorted(c["nume"] for c in mari))


# A4. sudo și cron: tuplul și gruparea
def sudo_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        user, drept = ln.split(" : ", 1)   # despachetare in tuplu
        
        out.append({"user": user.strip(), "drept": drept.strip(),
                "risc": "mare" if "NOPASSWD" in drept else "normal"})
    
    return out
 
def cron_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        campuri = ln.split()
        user = campuri[5]
        comanda = " ".join(campuri[6:])
        out.append({"user": user, "comanda": comanda})
    return out
    

def enumereaza(d):
    return {
        "suid": suid_constatari(os.path.join(d, "suid.txt")),
        "sudo": sudo_constatari(os.path.join(d, "sudo.txt")),
        "cron": cron_constatari(os.path.join(d, "crontab.txt")),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    raport = enumereaza(a.capturi)
    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False)); return
    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print(f"{categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")
    users_sudo = {c["user"] for c in raport["sudo"]}
    users_cron = {c["user"] for c in raport["cron"]}
    print("utilizatori implicati:", ", ".join(sorted(users_sudo | users_cron)))    
    with open("enum.json", "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)
    print("Raport salvat in enum.json")
 
if __name__ == "__main__":
    main()

