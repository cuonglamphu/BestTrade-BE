from datetime import datetime, timedelta
from typing import Tuple
from app.config.settings import MAX_HISTORICAL_DAYS, DEFAULT_START_DATE

def validate_date_range(start_date: str, end_date: str) -> Tuple[str, str, str]:
    try:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        today = datetime.now()

        if end_dt > today:
            end_dt = today
            end_date = end_dt.strftime('%Y-%m-%d')

        date_range = (end_dt - start_dt).days

        if date_range > MAX_HISTORICAL_DAYS:
            start_dt = end_dt - timedelta(days=MAX_HISTORICAL_DAYS-1)
            start_date = start_dt.strftime('%Y-%m-%d')
            message = f"Date range exceeded maximum allowed ({MAX_HISTORICAL_DAYS} days). Adjusted to last {MAX_HISTORICAL_DAYS} days."
        else:
            message = ""

        return start_date, end_date, message

    except ValueError as e:
        print(f"Error validating dates: {e}")
        return DEFAULT_START_DATE, end_date, "Invalid date format. Using default date range." 