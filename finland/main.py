"""Clean the Finnish route log, rebuild the network, rank towns by degree."""
import unicodedata

import pandas as pd

# Swedish (and one misspelled) names -> the Finnish name used elsewhere in the log.
SWEDISH = {
    "abo": "turku", "alavo": "alavus", "birkala": "pirkkala", "bjorneborg": "pori",
    "borga": "porvoo", "brahestad": "raahe", "esbo": "espoo", "fredrikshamn": "hamina",
    "grankulla": "kauniainen", "hango": "hanko", "helsingfors": "helsinki", "hogfors": "karkkila",
    "hyvinge": "hyvinkaa", "idensalmi": "iisalmi", "ikalis": "ikaalinen", "ilmola": "ilmajoki",
    "inga": "inkoo", "jakobstad": "pietarsaari", "kajana": "kajaani", "karleby": "kokkola",
    "kasko": "kaskinen", "kervo": "kerava", "keuru": "keuruu", "kimitoon": "kemionsaari",
    "korsholm": "mustasaari", "kristinestad": "kristiinankaupunki", "kronoby": "kruunupyy",
    "kumo": "kokemaki", "kyrkslatt": "kirkkonummi", "lahtis": "lahti", "lappo": "lapua",
    "larsmo": "luoto", "lojo": "lohja", "lovisa": "loviisa", "lundo": "lieto", "malax": "maalahti",
    "nadendal": "naantali", "narpes": "narpio", "nykarleby": "uusikaarlepyy", "nystad": "uusikaupunki",
    "pargas": "parainen", "raseborg": "raasepori", "raumo": "rauma", "reso": "raisio",
    "s:t karins": "kaarina", "s:t michel": "mikkeli", "sibbo": "sipoo", "sjundea": "siuntio",
    "tammerfors": "tampere", "tavastehus": "hameenlinna", "tornea": "tornio", "traskanda": "jarvenpaa",
    "tusby": "tuusula", "uleaborg": "oulu", "ulvsby": "ulvila", "vanda": "vantaa", "vasa": "vaasa", "vichtis": "vihti",
    "villmanstrand": "lappeenranta", "virmo": "mynamaki", "vora": "voyri",
}


def clean(name: str) -> str:
    s = name.strip().rstrip(".").strip().casefold()                      # spaces, dots, case
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))  # ä/ö/å
    return SWEDISH.get(s, s)                                              # Swedish -> Finnish


d = pd.read_csv("routes.csv")
a, b = d["from_town"].map(clean), d["to_town"].map(clean)
edges = {tuple(sorted(p)) for p in zip(a, b) if p[0] != p[1]}            # undirected, once each
towns = set(a) | set(b)

deg = pd.Series([t for e in edges for t in e]).value_counts()
print(f"raw: {len(d)} log rows, {pd.concat([d.from_town, d.to_town]).nunique()} raw town spellings")
print(f"clean: {len(towns)} towns, {len(edges)} connections (self-check: 116 / 448)\n")
print("busiest towns:")
print(deg.head(10).to_string())
word = "".join(t[0] for t in deg.index[:7]).upper()
print(f"\nSIGMOID_{word}")
