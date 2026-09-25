from datetime import date
from pydantic import BaseModel


class FinancialFact(BaseModel):
    ticker: str
    cik: str
    metric_name: str
    value: float
    unit: str
    fiscal_period: str
    filed_date: date
