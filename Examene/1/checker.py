import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    if not host.startswith("https://") and not host.startswith("http://"):
        host = f"https://{host}"
    
    host = host.rstrip("/")
    path = path.lstrip("/")
    
    return f"{host}/{path}"


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.startswith("https://")


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    try:
        response = requests.get(url, timeout=5)
        content_type = response.headers.get("Content-Type", "unknown")
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {content_type}")
    except requests.RequestException as e:
        print(f"Cererea a eșuat: {e}")


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        response = requests.get(url, timeout=5)
    
        raw_content_type = response.headers.get("Content-Type", "")
        content_type = raw_content_type.split(";")[0].strip() if raw_content_type else "unknown"
        
        length = response.headers.get("Content-Length")
        if length is not None:
            length = int(length)
        else:
            length = len(response.content)
            
        server = response.headers.get("Server", "unknown")
        
        return {
            "status": response.status_code,
            "content_type": content_type,
            "length": length,
            "server": server
        }
    except requests.Timeout:
        return {"status": None, "error": "timeout"}
    except requests.RequestException:
        return {"status": None, "error": "connection_error"}


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    successful_sites = []
    success_count = 0
    fail_count = 0
    
    for url in SITES:
        res = check_site(url)
        if res.get("status") == 200:
            success_count += 1
            successful_sites.append((url, res["length"]))
        else:
            fail_count += 1
            
    successful_sites.sort(key=lambda x: x[1], reverse=True)
    
    for url, length in successful_sites:
        print(f"{url} -> 200, {length} octeți")
        
    print(f"\nReușite: {success_count} | Eșuate: {fail_count}")


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        response = requests.get(url, timeout=5)
    
        received_headers_lower = {k.lower(): v for k, v in response.headers.items()}
        
        present = []
        missing = []
        
        for header in SECURITY_HEADERS:
            if header.lower() in received_headers_lower:
                present.append(header)
            else:
                missing.append(header)
                
        score = int((len(present) / len(SECURITY_HEADERS)) * 100)
        
        return {
            "present": present,
            "missing": missing,
            "score": score
        }
    except requests.Timeout:
        return {"status": None, "error": "timeout"}
    except requests.RequestException:
        return {"status": None, "error": "connection_error"}


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    current_attempt = 0
    last_status = None
    
    while current_attempt < attempts:
        current_attempt += 1
        try:
            response = requests.get(url, timeout=5)
            last_status = response.status_code
            if last_status < 500:
                return {"status": last_status, "attempts": current_attempt}
                
        except (requests.Timeout, requests.RequestException):
            last_status = None
            
    if last_status is None:
        return {"status": None, "error": "failed_after_retry", "attempts": current_attempt}
        
    return {"status": last_status, "attempts": current_attempt}
