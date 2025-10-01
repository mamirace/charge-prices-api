from fastapi import FastAPI, Query
from typing import Optional, List, Dict, Any
import pandas as pd
import os, re, unicodedata

app = FastAPI(title="Charge Prices API")

EXCEL_PATH = os.path.join("data", "Dosya.xlsx")

# --- Yardımcılar -------------------------------------------------------------

def _read(sheet: str) -> pd.DataFrame:
    # Excel her istekte tekrar okunur (dosyayı güncellersen anında yansısın diye)
    return pd.read_excel(EXCEL_PATH, sheet_name=sheet, engine="openpyxl")

_norm_re = re.compile(r"[\s\-.()/_,]+")
def _norm(s: Any) -> str:
    """Türkçe duyarlı, boşluk-tire-noktalama ayıklayan normalizasyon."""
    if s is None or (isinstance(s, float) and pd.isna(s)):
        return ""
    s = str(s).casefold()
    # diakritikleri kaldır (İ/ı vb. için daha toleranslı)
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    s = _norm_re.sub("", s)
    return s

def _filter_by_station(df: pd.DataFrame, station: Optional[str]) -> pd.DataFrame:
    if not station:
        return df
    q = _norm(station)
    # Hem "İstasyon" hem "ChatGPT Kanonik İsim" üzerinde yakın eşleşme
    mask = df["İstasyon"].apply(_norm).str.contains(q) | df["ChatGPT Kanonik İsim"].apply(_norm).str.contains(q)
    return df[mask]

def _ok(data: List[Dict]) -> Dict[str, Any]:
    return {"status": "ok", "count": len(data), "data": data}

def _err(msg: str) -> Dict[str, Any]:
    return {"status": "error", "message": msg}

# --- Endpointler -------------------------------------------------------------

@app.get("/", tags=["health"])
def root():
    return {"message": "Charge Prices API aktif", "endpoints": ["/prices", "/apps", "/campaigns"]}

@app.get("/prices", tags=["prices"])
def get_prices(
    station: Optional[str] = Query(None, description="İstasyon adı (örn. ZES, Trugo, Shell Recharge)"),
    socket_type: Optional[str] = Query(
        None,
        description='Şarj tipi: "Yavaş Şarj (AC)" | "Hızlı Şarj (DC)" | "AC Detay" | "DC Detay"',
    ),
):
    try:
        df = _read("Sayfa1")
        # Beklenen kolonlar
        needed = {"ChatGPT Kanonik İsim", "İstasyon", "Fiyat Tipi", "Fiyat"}
        if not needed.issubset(df.columns):
            return _err("Sayfa1 kolonları beklenen formatta değil.")
        # İstasyon filtreleme
        df = _filter_by_station(df, station)
        # Tip filtreleme
        if socket_type:
            df = df[df["Fiyat Tipi"].astype(str).str.casefold() == socket_type.casefold()]
        # Çıktı
        out = df[["ChatGPT Kanonik İsim", "İstasyon", "Fiyat Tipi", "Fiyat"]].to_dict(orient="records")
        return _ok(out)
    except Exception as e:
        return _err(str(e))

@app.get("/apps", tags=["apps"])
def get_apps(
    station: Optional[str] = Query(None, description="İstasyon adı (örn. ZES, Shell Recharge, Trugo)")
):
    try:
        df = _read("Sayfa2")
        needed = {
            "ChatGPT Kanonik İsim",
            "İstasyon",
            "Mobil Uygulama",
            "Diğer Mobil Uygulamalar",
            "Grup/Şirket Bilgisi",
        }
        if not needed.issubset(df.columns):
            return _err("Sayfa2 kolonları beklenen formatta değil.")
        df = _filter_by_station(df, station)
        out = df[
            ["ChatGPT Kanonik İsim", "İstasyon", "Mobil Uygulama", "Diğer Mobil Uygulamalar", "Grup/Şirket Bilgisi"]
        ].to_dict(orient="records")
        return _ok(out)
    except Exception as e:
        return _err(str(e))

@app.get("/campaigns", tags=["campaigns"])
def get_campaigns(
    station: Optional[str] = Query(None, description="İstasyon adı (örn. ZES, Shell Recharge, Trugo)")
):
    try:
        df = _read("Sayfa3")
        needed = {"ChatGPT Kanonik İsim", "İstasyon", "KAMPANYA 1", "KAMPANYA 2"}
        if not needed.issubset(df.columns):
            return _err("Sayfa3 kolonları beklenen formatta değil.")
        df = _filter_by_station(df, station)
        out = df[["ChatGPT Kanonik İsim", "İstasyon", "KAMPANYA 1", "KAMPANYA 2"]].to_dict(orient="records")
        return _ok(out)
    except Exception as e:
        return _err(str(e))
