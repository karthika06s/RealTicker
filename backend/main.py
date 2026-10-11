from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
from typing import List, Dict
import random

app = FastAPI(
    title="RealTicker Backend",
    description="Backend service for stock dashboard with AI analysis",
    version="1.0.0"
)

# -------------------- CORS --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- AI MODEL --------------------
llm = pipeline("text-generation", model="distilgpt2")

# -------------------- MOCK STOCK DATA --------------------
stocks: List[Dict] = [
    {
        "ticker": "AAPL",
        "company": "Apple Inc",
        "price": 185.4,
        "change": 1.2,
        "volume": 78,
        "market_cap": 2900,
        "history": [150, 152, 155, 160, 170, 180],
    },
    {
        "ticker": "MSFT",
        "company": "Microsoft Corp",
        "price": 412.3,
        "change": 0.8,
        "volume": 45,
        "market_cap": 3100,
        "history": [350, 360, 370, 380, 395, 410],
    },
    {
        "ticker": "GOOGL",
        "company": "Alphabet Inc",
        "price": 142.1,
        "change": 1.5,
        "volume": 55,
        "market_cap": 1800,
        "history": [120, 125, 130, 135, 138, 142],
    },
    {
        "ticker": "AMZN",
        "company": "Amazon.com Inc",
        "price": 175.6,
        "change": 2.1,
        "volume": 68,
        "market_cap": 1600,
        "history": [130, 140, 150, 160, 168, 175],
    },
    {
        "ticker": "NVDA",
        "company": "NVIDIA Corp",
        "price": 720.5,
        "change": 2.8,
        "volume": 95,
        "market_cap": 2200,
        "history": [520, 560, 600, 650, 690, 720],
    },
    {
        "ticker": "META",
        "company": "Meta Platforms Inc",
        "price": 480.3,
        "change": 1.1,
        "volume": 52,
        "market_cap": 1200,
        "history": [350, 380, 410, 440, 460, 480],
    },
    {
        "ticker": "TSLA",
        "company": "Tesla Inc",
        "price": 230.8,
        "change": 3.4,
        "volume": 110,
        "market_cap": 900,
        "history": [180, 190, 200, 210, 220, 230],
    },
    {
        "ticker": "NFLX",
        "company": "Netflix Inc",
        "price": 610.2,
        "change": 1.9,
        "volume": 38,
        "market_cap": 270,
        "history": [480, 500, 520, 550, 580, 610],
    },
    {
        "ticker": "ORCL",
        "company": "Oracle Corp",
        "price": 118.7,
        "change": 0.6,
        "volume": 29,
        "market_cap": 330,
        "history": [95, 100, 105, 110, 115, 118],
    },
    {
        "ticker": "INTC",
        "company": "Intel Corp",
        "price": 43.2,
        "change": -0.4,
        "volume": 65,
        "market_cap": 180,
        "history": [30, 32, 35, 38, 40, 43],
    },
    {
        "ticker": "AMD",
        "company": "Advanced Micro Devices",
        "price": 165.4,
        "change": 2.2,
        "volume": 72,
        "market_cap": 260,
        "history": [120, 130, 140, 150, 158, 165],
    },
    {
        "ticker": "IBM",
        "company": "IBM Corp",
        "price": 191.6,
        "change": 0.3,
        "volume": 21,
        "market_cap": 175,
        "history": [170, 172, 175, 180, 185, 191],
    },
]

# -------------------- TOP 10 STOCKS --------------------
@app.get("/api/stocks/top10")
def get_top_stocks():
    """
    Returns Top 10 stocks based on:
    - Highest volume
    - Highest daily growth
    - Market cap (mocked)
    """

    for stock in stocks:
        stock["price"] = round(stock["price"] + random.uniform(-1, 1), 2)
        stock["change"] = round(random.uniform(-2, 2), 2)

    sorted_stocks = sorted(
        stocks,
        key=lambda s: (s["volume"], s["change"], s["market_cap"]),
        reverse=True
    )

    return sorted_stocks[:10]

# -------------------- STOCK HISTORY --------------------
@app.get("/api/stocks/{ticker}/history")
def get_stock_history(ticker: str) -> List[int]:
    for stock in stocks:
        if stock["ticker"] == ticker.upper():
            return stock["history"]

    raise HTTPException(status_code=404, detail="Stock not found")

# -------------------- AI ANALYSIS --------------------
@app.post("/api/stocks/{ticker}/analyze")
def analyze_stock(ticker: str) -> Dict:
    stock = next((s for s in stocks if s["ticker"] == ticker.upper()), None)

    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    prompt = f"""
    Analyze the following stock price history:
    {stock['history']}

    Explain:
    - Overall trend
    - Risk level
    - Beginner-friendly investment advice
    """

    result = llm(prompt, max_length=150)

    return {
        "ticker": stock["ticker"],
        "analysis": result[0]["generated_text"],
        "disclaimer": "AI-generated content. Not financial advice."
    }
