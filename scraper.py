from app_store_web_scraper import AppStoreEntry
import pandas as pd

def fetch_reviews(app_id: int, country: str = "us", limit: int | None = None) -> pd.DataFrame:
    app = AppStoreEntry(app_id=app_id, country=country)
    reviews = []

    for r in app.reviews(limit=limit):
        text = getattr(r, "review", getattr(r, "content", ""))

        if hasattr(r, "developer_response") and r.developer_response:
            dev_resp = getattr(r.developer_response, "body", None)
        else:
            dev_resp = None

        reviews.append({
            "id": r.id,
            "date": r.date,
            "user_name": r.user_name,
            "rating": r.rating,
            "title": r.title,
            "review": text,
            "dev_response": dev_resp,
        })

    return pd.DataFrame(reviews)
