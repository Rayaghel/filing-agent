from pydantic import ValidationError
from src.models import FinancialFact

examples = [
    {
        "label": "VALID",
        "data": {
            "ticker": "AAPL",
            "cik": "0000320193",
            "metric_name": "Revenue",
            "value": 94930000000.0,
            "unit": "USD",
            "fiscal_period": "Q1-2024",
            "filed_date": "2024-02-02",
        },
    },
    {
        "label": "INVALID — value is not a number",
        "data": {
            "ticker": "AAPL",
            "cik": "0000320193",
            "metric_name": "Revenue",
            "value": "ninety-four billion",  # <-- bad
            "unit": "USD",
            "fiscal_period": "Q1-2024",
            "filed_date": "2024-02-02",
        },
    },
    {
        "label": "INVALID — filed_date missing, ticker is an integer",
        "data": {
            "ticker": 12345,            # <-- wrong type, but Pydantic will coerce int→str
            "cik": "0000320193",
            "metric_name": "EPS",
            "value": 2.18,
            "unit": "USD/share",
            "fiscal_period": "Q1-2024",
            # filed_date is missing entirely  <-- will error
        },
    },
]

for example in examples:
    print(f"\n{'='*50}")
    print(f"TEST: {example['label']}")
    print(f"{'='*50}")
    try:
        fact = FinancialFact(**example["data"])
        print("  OK:", fact)
    except ValidationError as e:
        for error in e.errors():
            print(f"  FIELD : {' -> '.join(str(x) for x in error['loc'])}")
            print(f"  ERROR : {error['msg']}")
            print(f"  INPUT : {error.get('input')}")
            print()
