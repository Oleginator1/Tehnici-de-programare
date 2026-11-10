from dataclasses import dataclass, asdict
import json
 
# A1. Clasa Proces, un tipar de date
@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str
    
    # A2
    def e_suspect(self):
            return any(c in self.cale for c in CAI_SUSPECTE)
 
p = Proces(3120, "update.exe", "ana", r"C:\Users\ana\AppData\Local\Temp\update.exe")
print(p.pid, p.nume)
print(p)


# A2. Metoda e_suspect pe Proces 
CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")
 
print(p.e_suspect())   # True (update.exe din Temp)


# A3. Clasa Eveniment și ID-urile Windows 
SUSPECTE_ID = {4625, 1102, 7045}
 
@dataclass
class Eveniment:
    id: int
    nivel: str
    sursa: str
    cont: str
    mesaj: str
    def e_suspect(self):
        return self.id in SUSPECTE_ID or self.nivel == "critical"


# A4. Le încarci din JSON
def procese_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Proces(**d) for d in json.load(f)]

def evenimente_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Eveniment(**d) for d in json.load(f)]
       
 
procese = procese_din_json("windows/start/procese.json")
print("procese:", len(procese))
print("suspecte:", sum(1 for p in procese if p.e_suspect()))


# B1. Inventar, o clasă-container
@dataclass
class Inventar:
    procese: list
    @classmethod
    def din_json(cls, cale):
        with open(cale, encoding="utf-8") as f:
            return cls([Proces(**d) for d in json.load(f)])
    def __len__(self):
        return len(self.procese)
    
    # B2. Metodele de interogare   
    def suspecte(self):
        return [p for p in procese if p.e_suspect()]
       
    def pe_user(self):
        grupuri = {}
        for p in self.procese:
            grupuri.setdefault(p.user, []).append(p.nume)
        return grupuri

 
inv = Inventar.din_json("windows/start/procese.json")
print("procese:", len(inv))

# B2
for p in inv.suspecte():
    print(f"  [{p.pid}] {p.nume}  {p.cale}")
print(inv.pe_user())


# B3. Raportul JSON, din obiecte   

 
def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    inv = Inventar.din_json(a.capturi + "/procese.json")
    ev = evenimente_din_json(a.capturi + "/evenimente.json")
    alarma = [e for e in ev if e.e_suspect()]
    suspecte = inv.suspecte()
    
    if a.json:
        raport = {
            "procese": len(inv),
            "evenimente": len(ev),
            "procese_suspecte": [asdict(p) for p in suspecte],
            "evenimente_alarma": [asdict(e) for e in alarma],
        }
        print(json.dumps(raport, indent=2, ensure_ascii=False))
    else:
        print(f"Procese: {len(inv)} | suspecte: {len(suspecte)}")
        for p in suspecte:
            print(f"  [{p.pid}] {p.nume} ({p.user}) {p.cale}")
        print(f"Evenimente: {len(ev)} | alarma: {len(alarma)}")
        for e in alarma:
            print(f"  {e.id} [{e.nivel}] {e.cont}: {e.mesaj}")
    
    
if __name__ == "__main__":
    main()
