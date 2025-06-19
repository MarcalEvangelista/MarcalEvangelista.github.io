import requests
import yaml
import os

ADS_TOKEN = os.environ["ADS_TOKEN"]
headers = {"Authorization": f"Bearer {ADS_TOKEN}"}

query = 'author:("EVANGELISTA-SANTANA, M." OR "Evangelista Santana, Marçal")'
params = {
    "q": query,
    "fl": "title,bibcode,author,pubdate",
    "rows": 50,
    "sort": "pubdate desc",
    "format": "json"
}

response = requests.get("https://api.adsabs.harvard.edu/v1/search/query", headers=headers, params=params)
docs = response.json().get("response", {}).get("docs", [])

publications = []
for doc in docs:
    publications.append({
        "title": doc["title"][0],
        "authors": ", ".join(doc["author"]),
        "year": doc["pubdate"][:4],
        "url": f"https://ui.adsabs.harvard.edu/abs/{doc['bibcode']}"
    })

with open("_data/publications.yml", "w") as f:
    yaml.dump(publications, f, allow_unicode=True)



