from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# Excel dosyasının yolu
EXCEL_PATH = "data/Dosya.xlsx"

@app.get("/prices")
def get_prices():
    try:
        # Sayfa1'den fiyatları oku
        df = pd.read_excel(EXCEL_PATH, sheet_name="Sayfa1")
        prices = df.to_dict(orient="records")
        return {"status": "ok", "data": prices}
    except Exception as e:
        return {"status": "error", "message": str(e)}
