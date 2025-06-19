import requests
import yaml
import os

# Token diretamente no script — use apenas localmente
ADS_TOKEN = "ynygJ9vdhawN3I1RwvcLuKzMkE7yYMDNZHbGH0SY"
headers = {"Authorization": f"Bearer {ADS_TOKEN}"}

# Consulta ADS com nomes comuns
query = 'author:("EVANGELISTA-SANTANA, M." OR "Evangelista Santana, Marçal")'

params = {
    "q": query,
    "fl": "title,bibcode,author,pubdate,property,aff",
    "rows": 100,
    "sort": "pubdate desc",
    "format": "json"
}

response = requests.get("https://api.adsabs.harvard.edu/v1/search/query", headers=headers, params=params)
docs = response.json().get("response", {}).get("docs", [])

print(f"{len(docs)} documentos retornados.")

# Palavras-chave para verificar afiliação (inclusive redundantes)
afil_keywords = [
    "observatório nacional", "on", "csic", "granada", "andalucía",
    "iaa", "iaa-csic", "instituto de astrofísica"
]

# Lista de publicações filtradas
publications = []
for doc in docs:
    title = doc.get("title", [""])[0]
    authors = doc.get("author", [])
    affs = [a.lower() for a in doc.get("aff", [])]
    bibcode = doc.get("bibcode")
    props = doc.get("property", [])
    year = doc.get("pubdate", "")[:4]

    # Apenas artigos referenciados
    if "REFEREED" not in props:
        continue

    # Pelo menos uma afiliação relevante OU o nome completo como autor
    author_match = any("evangelista-santana" in a.lower() or "marçal" in a.lower() for a in authors)
    affil_match = any(any(k in aff for k in afil_keywords) for aff in affs)

    if author_match or affil_match:
        publications.append({
            "title": title,
            "authors": ", ".join(authors),
            "year": year,
            "url": f"https://ui.adsabs.harvard.edu/abs/{bibcode}"
        })
    else:
        print(f"🔎 Ignorado: {title[:40]}...")

# Salvar no formato YAML
with open("_data/publications.yml", "w") as f:
    yaml.dump(publications, f, allow_unicode=True)

print(f"{len(publications)} publicações atualizadas.")

