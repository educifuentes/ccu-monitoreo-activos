import pandas as pd

def format_date_spanish(dt):
    if pd.isna(dt) or str(dt).lower() in ["nan", "nat", ""]:
        return "N/A"
        
    if isinstance(dt, str):
        try:
            dt = pd.to_datetime(dt)
        except Exception:
            return str(dt)

    try:
        months = ["enero", "febrero", "marzo", "abril", "mayo", "junio", 
                  "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        return f"{months[dt.month - 1]} {dt.year}"
    except Exception:
        return str(dt)
