#!/usr/bin/env python3
import sys
import requests
from requests.auth import HTTPBasicAuth

# ───── CONFIG ─────
BASE_URL        = "http://AD02:8000/rest/v1"
USER            = "admin"
PASS            = "aJx`lHDRqL;)L]e}'u"
CLIENT          = "localhost"
ARCHIVE_PLAN_ID = "10011"       # NJ_MONTAGE
FILE_LIST       = sys.argv[1] if len(sys.argv)>1 else "files.txt"
# ────────────────────

def read_names(path):
    with open(path, encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]

def build_searches(names):
    return [
        {
            "archivePlan": ARCHIVE_PLAN_ID,
            # on utilise '*=' pour matcher le début ou la chaîne
            "expression": f"{{name *= \"{name}\"}}"
        }
        for name in names
    ]

def launch_restore(searches):
    url = f"{BASE_URL}/restore/restoreselections"
    headers = {
        "client":       CLIENT,
        "time":         "now",
        "Content-Type": "application/json",
        "Accept":       "application/json"
    }
    resp = requests.post(
        url,
        auth=HTTPBasicAuth(USER, PASS),
        headers=headers,
        json={"searches": searches}
    )
    resp.raise_for_status()
    return resp.json()

def main():
    names = read_names(FILE_LIST)
    if not names:
        print("❌ Aucun nom dans", FILE_LIST)
        sys.exit(1)

    searches = build_searches(names)
    try:
        result = launch_restore(searches)
    except requests.HTTPError as e:
        print("❌ Erreur RESTORE :", e)
        print("💡 Vérifiez que l’ID de plan est 10011 et que vos noms sont exacts.")
        sys.exit(1)

    print("✅ Restore lancé :", result)

if __name__ == "__main__":
    main()
