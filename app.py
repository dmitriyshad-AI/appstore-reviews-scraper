import streamlit as st
from scraper import fetch_reviews

st.title("App Store Reviews Scraper")

app_id = st.text_input("Введите App ID (например, 570060128 для Duolingo)")
country = st.text_input("Страна (us, ru, gb...)", value="us")

if st.button("Собрать отзывы"):
    if app_id.isdigit():
        df = fetch_reviews(int(app_id), country, limit=500)
        st.write(f"Скачано отзывов: {len(df)}")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Скачать CSV", csv, "reviews.csv")
    else:
        st.error("App ID должен быть числом")
