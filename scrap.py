import json
import pandas as pd

with open("nagpur_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

records = []

for segment in data["tuples"]:
    segment_name = segment["title"]

    for loc in segment["tuples"]:
        price_dict = loc.get("propYearWisePrice", {})

        records.append({
            "segment": segment_name,
            "locality": loc.get("localityName"),
            "current_price_raw": loc.get("pricePerSqFt"),
            "price_1Y": price_dict.get("1"),
            "price_3Y": price_dict.get("3"),
            "price_5Y": price_dict.get("4"),
            "rating": loc.get("rating"),
            "lat": loc.get("longLat", {}).get("y"),
            "lon": loc.get("longLat", {}).get("x"),
        })

df = pd.DataFrame(records)

print(df.head())
df.to_csv("nagpur_dataset.csv", index=False)