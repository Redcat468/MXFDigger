#!/usr/bin/env python3
import sys
import requests
from requests.auth import HTTPBasicAuth

# ───── CONFIG ───────────────
BASE_URL        = "http://AD02:8000/rest/v1"
USER            = "admin"
PASS            = "aJx`lHDRqL;)L]e}'u"
CLIENT          = "localhost"
ARCHIVE_PLAN_ID = "10011"             # NJ_MONTAGE
FILE_LIST       = sys.argv[1]         # ex. "files.txt"

# Corrigé : chemin valide et correctement échappé
RELOCATE_PATH   = r"M:\DESARCHIVAGE"  
# ───────────────────────────────

def read_names(path):
    with open(path, encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]

def build_searches(names):
    """
    Construit la liste des filtres P5 pour retrouver chaque fichier
    par un match “contains” sur le nom.
    """
    searches = []
    for name in names:
        # On passe à '*=' pour matcher le début/une portion du nom
        expr = f"{{name *= '{name}'}}"
        searches.append({
            "archivePlan": ARCHIVE_PLAN_ID,
            "expression":  expr
        })
    return searches

def launch_restore(searches):
    url = f"{BASE_URL}/restore/restoreselections"
    headers = {
        "client":       CLIENT,
        "relocate":     RELOCATE_PATH,        # on indique le dossier cible
        "time":         "now",
        "Content-Type": "application/json",
        "Accept":       "application/json"
    }
    resp = requests.post(
        url,
        auth=HTTPBasicAuth(USER, PASS),
        headers=headers,
        json={"searches": searches}           # P5 recherche et restaure vos fichiers :contentReference[oaicite:0]{index=0}&#8203;:contentReference[oaicite:1]{index=1}
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
        sys.exit(1)

    print("✅ Restore lancé :", result)

if __name__ == "__main__":
    main()
