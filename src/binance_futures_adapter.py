"""
Binance Futures API Adapter

Lightweight wrappers for Binance USD-M Futures API endpoints.
"""
from typing import Optional, Dict, Any, List
import requests

BASE = "https://fapi.binance.com"  # USD-M Futures

def _get(path: str, params: Optional[Dict[str, Any]] = None, timeout: int = 10):
    url = f"{BASE}{path}"
    r = requests.get(url, params=params, timeout=timeout)
    r.raise_for_status()
    return r.json()

def exchange_info() -> Dict[str, Any]:
    """GET /fapi/v1/exchangeInfo"""
    return _get("/fapi/v1/exchangeInfo")

def premium_index(symbol: Optional[str] = None):
    """
    GET /fapi/v1/premiumIndex
    If symbol is None, returns all; else returns single-symbol dict.
    """
    params = {"symbol": symbol} if symbol else None
    return _get("/fapi/v1/premiumIndex", params=params)

def funding_rate_history(symbol: str, limit: int = 200):
    """GET /fapi/v1/fundingRate (most recent 'limit' entries)"""
    return _get("/fapi/v1/fundingRate", params={"symbol": symbol, "limit": limit})
