import requests
import xml.etree.ElementTree as ET
import csv
 
# URL du sitemap
XML_URL = "https://www.speedy.fr/sitemaps/products.xml"
# CSV à la racine du repo
CSV_PATH = "products.csv"
 
try:
    # Télécharger le XML
    response = requests.get(XML_URL)
    response.raise_for_status()
except requests.RequestException as e:
    print("Erreur lors du téléchargement du XML :", e)
    exit(1)
 
try:
    # Parser le XML
    root = ET.fromstring(response.content)
except ET.ParseError as e:
    print("Erreur lors du parsing XML :", e)
    exit(1)
 
# Namespace du sitemap
ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
 
# Récupérer tous les tags <url>
urls = root.findall("sm:url", ns)
 
rows = []
 
for u in urls:
    loc = u.find("sm:loc", ns)
    changefreq = u.find("sm:changefreq", ns)
    priority = u.find("sm:priority", ns)

    rows.append({
        "loc": loc.text if loc is not None else "",
        "changefreq": changefreq.text if changefreq is not None else "",
        "priority": priority.text if priority is not None else ""
    })
 
if not rows:
    print("Aucune URL trouvée dans le sitemap.")
    exit(1)
 
# Écriture du CSV à la racine
try:
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["loc", "changefreq", "priority"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"CSV généré avec succès : {CSV_PATH} ({len(rows)} lignes)")
except Exception as e:
    print("Erreur lors de l'écriture du CSV :", e)
    exit(1)
