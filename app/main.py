from fastapi import FastAPI
import pandas as pd
import os

app = FastAPI()

# Excel dosyasının yolu
EXCEL_FILE = os.path.join("data", "Dosya.xlsx")

# Ortak fonksiyon -> excel oku
def read_excel(sheet_name: str):
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name)
        return {"status": "ok", "data": df.to_dict(orient="records")}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 1. Sayfa -> Fiyatlar
@app.get("/prices")
def get_prices():
    return read_excel("Sayfa1")

# 2. Sayfa -> Mobil Uygulama & Şirket
@app.get("/apps")
def get_apps():
    return read_excel("Sayfa2")

# 3. Sayfa -> Kampanyalar
@app.get("/campaigns")
def get_campaigns():
    return read_excel("Sayfa3")

# Root endpoint (test için)
@app.get("/")
def root():
    return {"message": "Charge Prices API aktif! Kullanılabilir endpointler: /prices, /apps, /campaigns"}
