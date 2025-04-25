import os
import re
import configparser
from flask import Flask, render_template_string, request, flash, redirect, url_for
import requests
from requests.auth import HTTPBasicAuth

# Chargement de la configuration depuis settings.conf
config = configparser.ConfigParser()
config.read('settings.conf')

# ────── RESTORE CONFIGURATION ──────
BASE_URL        = config.get('RESTORE', 'base_url')
USER            = config.get('RESTORE', 'user')
PASSWD          = config.get('RESTORE', 'password')
CLIENT          = config.get('RESTORE', 'client')
ARCHIVE_PLAN_ID = config.get('RESTORE', 'archive_plan_id')
RELOCATE_PATH   = config.get('RESTORE', 'relocate_path')
TXT_FILENAME    = config.get('RESTORE', 'txt_filename')
# ───────────────────────────────────

# ────── FLASK CONFIGURATION ────────
FLASK_SECRET_KEY = config.get('FLASK', 'secret_key')
HOST             = config.get('FLASK', 'host')
PORT             = config.getint('FLASK', 'port')
DEBUG            = config.getboolean('FLASK', 'debug')
# ───────────────────────────────────

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

# Template HTML
template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MXFDigger - Extraction MXF et Désarchivage</title>
    <link rel="icon" type="image/x-icon" href="{{ url_for('static', filename='images/logo.ico') }}">
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; color: #333; }
        .container { margin: 20px auto; padding: 20px; max-width: 1000px; background: #fff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        .flash-message { padding: 10px; margin-bottom: 20px; border-radius: 5px; font-weight: bold; }
        .flash-error { background-color: #ffebee; color: #c62828; }
        .flash-success { background-color: #e8f5e9; color: #2e7d32; }
        .flash-warning { background-color: #fff3e0; color: #ef6c00; }
        .btn { display: inline-block; padding: 10px 20px; font-size: 16px; color: #fff; background-color: #651a8b; border: none; border-radius: 15px; cursor: pointer; box-shadow: 0 2px 2px rgba(0,0,0,0.3); transition: background-color 0.2s ease, transform 0.2s ease; }
        .btn:hover { background-color: #5a167a; transform: translateY(-2px); }
        .file-input-container { display: flex; justify-content: center; margin-top: 20px; }
        .file-input { padding: 10px; border: 2px dashed #ccc; border-radius: 5px; background-color: #f9f9f9; cursor: pointer; transition: background-color 0.3s ease; }
        .file-input:hover { background-color: #e0e0e0; }
        .volume { text-align: center; font-weight: bold; color: #2e7d32; margin-top: 20px; }
    </style>
</head>
<body>
<div class="logo-container" style="display: flex; justify-content: center; margin-top: 20px;">
    <img src="{{ url_for('static', filename='images/banner.svg') }}" alt="MxfDigger Logo" style="width: 40%; height: auto;">
</div>
<div class="container">
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <div class="flash-message">
                {% for category, message in messages %}
                    <span class="flash-{{ category }}">{{ message }}</span><br>
                {% endfor %}
            </div>
        {% endif %}
    {% endwith %}

    <form method="POST" enctype="multipart/form-data">
        <div class="file-input-container">
            <input type="file" name="log_file" class="file-input" accept=".txt" required>
        </div>
        <div style="text-align: center; margin-top: 10px;">
            <button type="submit" class="btn">Extraire .mxf</button>
        </div>
    </form>

    {% if count is defined %}
        <div class="volume">Nombre de fichiers MXF extraits : {{ count }}</div>
        {% if count > 0 %}
            <form method="POST" action="{{ url_for('restore') }}" style="text-align: center; margin-top: 20px;">
                <button type="submit" class="btn">Lancer le désarchivage</button>
            </form>
        {% endif %}
    {% endif %}
</div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded = request.files.get('log_file')
        if not uploaded or uploaded.filename == '':
            flash('Aucun fichier sélectionné.', 'error')
            return redirect(request.url)
        try:
            text = uploaded.stream.read().decode('utf-8', errors='ignore')
            pattern = re.compile(r'[\w\-.]+\.mxf', re.IGNORECASE)
            filenames = sorted(set(pattern.findall(text)))
            if not filenames:
                flash('Aucun fichier .mxf trouvé dans le log.', 'warning')
                return redirect(request.url)
            with open(TXT_FILENAME, 'w', encoding='utf-8') as f:
                f.write('\n'.join(filenames))
            return render_template_string(template, count=len(filenames))
        except Exception as e:
            flash(f'Erreur lors du traitement : {e}', 'error')
            return redirect(request.url)
    return render_template_string(template)

@app.route('/restore', methods=['POST'])
def restore():
    if not os.path.exists(TXT_FILENAME):
        flash("Le fichier d'extraction n'existe pas.", 'error')
        return redirect(url_for('index'))
    with open(TXT_FILENAME, encoding='utf-8') as f:
        names = [l.strip() for l in f if l.strip()]
    if not names:
        flash('Aucun nom à restaurer.', 'warning')
        return redirect(url_for('index'))
    searches = []
    for name in names:
        searches.append({
            'archivePlan': ARCHIVE_PLAN_ID,
            'expression': f"{{name *= '{name}'}}"
        })
    try:
        url = f"{BASE_URL}/restore/restoreselections"
        headers = {
            'client': CLIENT,
            'relocate': RELOCATE_PATH,
            'time': 'now',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        resp = requests.post(
            url,
            auth=HTTPBasicAuth(USER, PASSWD),
            headers=headers,
            json={'searches': searches}
        )
        resp.raise_for_status()
        result = resp.json()
        flash(f"✅ Restore lancé : {result}", 'success')
    except Exception as e:
        flash(f"❌ Erreur RESTORE : {e}", 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
