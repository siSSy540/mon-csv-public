import requests
import xml.etree.ElementTree as ET
import csv

XML_URL = "https://www.speedy.fr/download/flux_speedy_google.xml"
CSV_PATH = "products.csv"

try:
    response = requests.get(XML_URL)
    response.raise_for_status()
except requests.RequestException as e:
    print("Erreur lors du téléchargement du XML :", e)
    exit(1)

try:
    root = ET.fromstring(response.content)
except ET.ParseError as e:
    print("Erreur lors du parsing XML :", e)
    exit(1)

ns = {
    "g": "http://base.google.com/ns/1.0"
}

items = root.findall(".//item")

if not items:
    print("Aucun item trouvé dans le flux.")
    exit(1)

rows = []
all_fields = set()

for item in items:
    row = {}
    for child in item:
        tag = child.tag
        if "}" in tag:
            tag = tag.split("}", 1)[1]
        row[tag] = child.text.strip() if child.text else ""
        all_fields.add(tag)
    rows.append(row)

all_fields = sorted(all_fields)

try:
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"CSV généré avec succès : {CSV_PATH} ({len(rows)} lignes, {len(all_fields)} colonnes)")
except Exception as e:
    print("Erreur lors de l'écriture du CSV :", e)
    exit(1)
