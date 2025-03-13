import json
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

def normalize_json(data):
    authors = (data.get("authors") or {}).get("author", [])
    if isinstance(authors, str):
        authors = [authors]
    elif not isinstance(authors, list):
        authors = []
    return {
        "load_date": data.get("load-date"),
        "links": [{"ref": link["@ref"], "href": link["@href"]} for link in data.get("link", [])],
        "identifier": data.get("dc:identifier"),
        "url": data.get("prism:url"),
        "title": data.get("dc:title"),
        "creator": data.get("dc:creator"),
        "publication_name": data.get("prism:publicationName"),
        "volume": data.get("prism:volume"),
        "cover_date": data.get("prism:coverDate"),
        "starting_page": data.get("prism:startingPage"),
        "doi": data.get("prism:doi"),
        "openaccess": data.get("openaccess"),
        "pii": data.get("pii"),
        "authors": [author["$"] if isinstance(author, dict) and "$" in author else str(author) for author in authors]
    }


with open('data.json', 'r') as file:
    data = json.load(file)

print(len(data))


normalized_json_list = [normalize_json(item) for item in data[:10000]]



years = [item["cover_date"][:4] for item in normalized_json_list if item["cover_date"]]
year_counts = Counter(years)

df = pd.DataFrame(year_counts.items(), columns=["Year", "Number of Articles"])
df = df.sort_values("Year")

plt.figure(figsize=(10, 5))
plt.bar(df["Year"], df["Number of Articles"], color="skyblue")
plt.xlabel("Year")
plt.ylabel("Number of Articles")
plt.title("Number of Published Articles by Year")
plt.xticks(rotation=45)
plt.savefig("articles_by_year.png")

df_journals = pd.DataFrame(normalized_json_list)

journal_counts = Counter(df_journals["publication_name"].dropna())
top_journals = journal_counts.most_common(10)
journals, counts = zip(*top_journals)

plt.figure(figsize=(10, 5))
plt.barh(journals, counts, color="skyblue")
plt.xlabel("Number of Publications")
plt.ylabel("Journals")
plt.title("Top 10 Most Popular Journals")
plt.gca().invert_yaxis()
plt.savefig("top_journals.png")

