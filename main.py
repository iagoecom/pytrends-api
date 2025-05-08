from fastapi import FastAPI
from pytrends.request import TrendReq
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/trends")
def get_trends(keyword: str = "camiseta térmica feminina"):
    pytrends = TrendReq(hl='pt-BR', tz=0)
    pytrends.build_payload([keyword], cat=0, timeframe='today 12-m', geo='BR')
    data = pytrends.interest_over_time()
    if data.empty:
        return {"erro": "Sem dados para esse termo."}
    timeline = data[keyword].reset_index().to_dict(orient="records")
    insights = {
        "media": float(data[keyword].mean()),
        "pico": int(data[keyword].max()),
        "inicio": int(data[keyword].iloc[0]),
        "fim": int(data[keyword].iloc[-1]),
        "crescimento": int(data[keyword].iloc[-1] - data[keyword].iloc[0])
    }
    return {
        "keyword": keyword,
        "dados": timeline,
        "insights": insights
    }
