"""
Futures Math Utilities

Calculations for perpetual and dated futures including basis, funding rates,
cash-and-carry strategies, and cost-of-carry pricing.
"""
import math
from typing import Iterable, Literal, Dict, Any, List, Tuple, Optional
import datetime
import numpy as np

Side = Literal["long", "short"]

def year_fraction(start_ts: float, end_ts: float) -> float:
    """ACT/365F year fraction between two POSIX timestamps (seconds)."""
    return max(1e-12, (end_ts - start_ts) / (365.0 * 24.0 * 3600.0))

def cost_of_carry_fair_price(S: float, r_annual: float, c_annual: float, T_years: float) -> float:
    """
    Classic cost-of-carry forward pricing: F = S * exp((r - c) * T)
    r_annual: risk-free rate (annualized, as decimal)
    c_annual: carry/benefit yield (annualized, as decimal)
    T_years: time to expiry in years
    """
    return S * math.exp((r_annual - c_annual) * T_years)

def basis(F: float, S: float) -> float:
    """Simple basis as a fraction: (F - S) / S."""
    return (F - S) / S

def annualize_basis(b: float, T_years: float) -> float:
    """
    Convert period basis into annualized rate.
    Approx: (1 + b)^(1/T) - 1 ; robust for small T.
    """
    if T_years <= 0:
        return float('nan')
    return (1.0 + b) ** (1.0 / T_years) - 1.0

def funding_cashflows(notional_usd: float, funding_rates: Iterable[float], side: Side) -> float:
    """
    Sum funding cashflows for a perp position.
    funding_rates: iterable of interval rates (e.g., per 8h), signed as defined by exchange convention:
        Positive funding rate => longs pay, shorts receive.
    side: "long" or "short".
    Returns USD PnL (positive = receive).
    """
    sgn = -1.0 if side == "long" else 1.0
    return notional_usd * sgn * float(np.sum(list(funding_rates)))

def cash_and_carry_pnl(spot_qty: float, entry_price: float, funding_rates: Iterable[float],
                       fees_bps_per_leg: float = 0.0) -> float:
    """
    Simple cash-and-carry on a perp:
      + Long spot (qty), - Short perp (same notional)
      + Receive funding when funding > 0 (since short)
      + Ignore spot financing, borrow costs, and mark-to-market for brevity
    fees_bps_per_leg: fee *per open leg* in basis points (e.g., 2.5 bps = 0.00025).
    Returns net USD PnL from funding minus entry/exit taker fees.
    """
    notional = spot_qty * entry_price
    fees = notional * (fees_bps_per_leg / 10000.0) * 2.0  # open 2 legs once
    funding_pnl = funding_cashflows(notional, funding_rates, side="short")
    return funding_pnl - fees

def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))

def predicted_funding_from_premium(premium_index: float, interest_per_interval: float = 0.0001) -> float:
    """
    Binance documentation (USD-M) describes funding rate formula as:
        Funding Rate = Premium Index + clamp(Interest Rate - Premium Index, +0.0005, -0.0005)
    where default Interest Rate per interval is approximately 0.01% (0.0001) and clamp bounds are +/-0.05% (+/-0.0005).
    This function applies that rule to estimate next funding given a current premium index.
    """
    adj = clamp(interest_per_interval - premium_index, -0.0005, 0.0005)
    return premium_index + adj
