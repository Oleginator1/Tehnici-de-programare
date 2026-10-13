from checker import build_url, is_https, show_response, check_site, scan_sites, check_headers, retry_check


print("Partea 1:")
print(build_url("example.com", "login"))
print(build_url("example.com", "/login"))
print(is_https("https://example.com"))
print(is_https("http://example.com"))


print("Partea 2:")
show_response("https://example.com")


print("Partea 3:")
print(check_site("https://example.com"))
print(check_site("http://this-site-does-not-exist.invalid"))


print("Partea 4:")
scan_sites()


print("Partea 5:")
print(check_headers("https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff"))
print(check_headers("http://this-site-does-not-exist.invalid"))
print()

print("Partea 6:")
print(retry_check("https://httpbin.org/status/200"))
print(retry_check("https://httpbin.org/status/404"))
print(retry_check("https://httpbin.org/status/500", attempts=3))
print(retry_check("http://this-site-does-not-exist.invalid", attempts=2))
