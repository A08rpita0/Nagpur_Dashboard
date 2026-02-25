import pandas as pd
import numpy as np
import re

# Load dataset
df = pd.read_csv("nagpur_dataset.csv")

# Normalize column names (VERY IMPORTANT to avoid KeyError)
df.columns = df.columns.str.strip().str.lower()

# ------------------------------
# 1️⃣ CLEAN CURRENT PRICE COLUMN
# ------------------------------

def clean_price(value):
    if pd.isna(value):
        return np.nan
    
    value = str(value)
    value = value.replace("â‚¹", "")
    value = value.replace("₹", "")
    value = value.replace("/ sq.ft", "")
    value = value.replace(",", "")
    
    numbers = re.findall(r"\d+\.?\d*", value)
    
    return float(numbers[0]) if numbers else np.nan


# ✅ Use current_price_raw instead of avg_price
df["current_price_raw"] = df["current_price_raw"].apply(clean_price)


# ------------------------------
# 2️⃣ CLEAN price_1y, price_3y, price_5y
# ------------------------------

for col in ["price_1y", "price_3y", "price_5y"]:
    if col in df.columns:
        df[col] = df[col].apply(clean_price)


# ------------------------------
# 3️⃣ HANDLE MISSING VALUES
# ------------------------------

for col in ["price_1y", "price_3y"]:
    if col in df.columns:
        df[col] = df[col].replace(0, np.nan)

# Drop rows where current price is missing
df = df.dropna(subset=["current_price_raw"])


# ------------------------------
# 4️⃣ CALCULATE GROWTH %
# ------------------------------

df["growth_1y"] = (
    (df["current_price_raw"] - df["price_1y"]) / df["price_1y"]
) * 100

df["growth_3y"] = (
    (df["current_price_raw"] - df["price_3y"]) / df["price_3y"]
) * 100


# ------------------------------
# 5️⃣ ROUND VALUES
# ------------------------------

df["growth_1y"] = df["growth_1y"].round(2)
df["growth_3y"] = df["growth_3y"].round(2)


# ------------------------------
# 6️⃣ DROP 5Y COLUMN (INSUFFICIENT DATA)
# ------------------------------

if "price_5y" in df.columns:
    df = df.drop(columns=["price_5y"])

if "growth_5y" in df.columns:
    df = df.drop(columns=["growth_5y"])


# ------------------------------
# 7️⃣ DROP ROWS WHERE GROWTH CANNOT BE CALCULATED
# ------------------------------

df = df.dropna(subset=["growth_1y", "growth_3y"])

# Investment Score (weighted growth)
df["investment_score"] = (
    0.6 * df["growth_1y"] +
    0.4 * df["growth_3y"]
)

# Ranking based on score
df["rank"] = df["investment_score"].rank(ascending=False)

def recommendation(score):
    if score > 15:
        return "Strong Buy"
    elif score > 5:
        return "Moderate Buy"
    else:
        return "Watch / Hold"

df["recommendation"] = df["investment_score"].apply(recommendation)

# ------------------------------
# ADD VOLATILITY COLUMN
# ------------------------------

df["volatility"] = df[["growth_1y", "growth_3y"]].std(axis=1)
df["volatility"] = df["volatility"].round(2)
# ------------------------------
# 8️⃣ SAVE CLEAN DATASET
# ------------------------------

df.to_csv("nagpur_cleaned_dataset.csv", index=False)

print("✅ Dataset cleaned successfully!")