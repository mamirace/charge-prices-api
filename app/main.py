from fastapi import FastAPI, Query
import pandas as pd

app = FastAPI()

# Excel dosyasını yükle
excel_path = "data/Dosya.xlsx"

# Fiyatları getir
@app.get("/prices")
def get_prices(station: str = Query(...), socket_type: str = Query(...)):
    df = pd.read_excel(excel_path, sheet_name="Sayfa1")

    # İstasyon filtreleme
    results = df[df["İstasyon"].str.contains(station, case=False, na=False)]

    # Soket tipi filtreleme
    if socket_type:
        results = results[results["Fiyat Tipi"].str.contains(socket_type, case=False, na=False)]

    data = []
    for _, row in results.iterrows():
        data.append({
            "ChatGPT Kanonik İsim": row["ChatGPT Kanonik İsim"],
            "İstasyon": row["İstasyon"],
            "Fiyat Tipi": row["Fiyat Tipi"],
            "Fiyat": row["Fiyat"]
        })
    return {"status": "ok", "data": data}


# Mobil uygulamaları getir
@app.get("/apps")
def get_apps(station: str = Query(...)):
    df = pd.read_excel(excel_path, sheet_name="Sayfa2")

    results = df[df["İstasyon"].str.contains(station, case=False, na=False)]

    data = []
    for _, row in results.iterrows():
        data.append({
            "ChatGPT Kanonik İsim": row["ChatGPT Kanonik İsim"],
            "İstasyon": row["İstasyon"],
            "Mobil Uygulama": row["Mobil Uygulama"],
            "Diğer Mobil Uygulamalar": row["Diğer Mobil Uygulamalar"],
            "Grup/Şirket Bilgisi": row["Grup/Şirket Bilgisi"]
        })
    return {"status": "ok", "data": data}


# Kampanyaları getir
@app.get("/campaigns")
def get_campaigns(station: str = Query(...)):
    df = pd.read_excel(excel_path, sheet_name="Sayfa3")

    results = df[df["İstasyon"].str.contains(station, case=False, na=False)]

    data = []
    for _, row in results.iterrows():
        data.append({
            "ChatGPT Kanonik İsim": row["ChatGPT Kanonik İsim"],
            "İstasyon": row["İstasyon"],
            "Kampanya 1": row["Kampanya 1"],
            "Kampanya 2": row["Kampanya 2"]
        })
    return {"status": "ok", "data": data}
