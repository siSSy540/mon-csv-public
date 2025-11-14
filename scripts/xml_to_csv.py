import requests
import xml.etree.ElementTree as ET
import csv

XML_URL = "https://www.speedy.fr/sitemaps/products.xml"
CSV_PATH = "products.csv"

# Télécharger le XML
response = requests.get(XML_URL)
response.raise_for_status()

root = ET.fromstring(response.content)

# Récupération des tags <url>
urls = root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url")

rows = []

for u in urls:
    loc = u.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
    lastmod = u.find("{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod")

    rows.append({
        "url": loc.text if loc is not None else "",
        "lastmod": lastmod.text if lastmod is not None else ""
    })

# Écriture CSV
with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["url", "lastmod"])
    writer.writeheader()
    writer.writerows(rows)

print("CSV généré avec succès :", CSV_PATH)
