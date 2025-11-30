import streamlit as st
from scraper import fetch_reviews

# ===========================
# PAGE STYLE
# ===========================
st.set_page_config(page_title="App Store Reviews Scraper", layout="centered")

st.markdown("""
<style>

.block-container {
    max-width: 780px !important;
    padding-top: 2rem;
}

/* HERO */
.hero-title {
    font-size: 3rem;
    font-weight: 800;
    text-align: center;
    margin-bottom: 0.3rem;
}
.hero-subtitle {
    text-align: center;
    font-size: 1.1rem;
    color: #6A6A6A;
    margin-bottom: 2.5rem;
}

/* Input fields */
input, textarea {
    border-radius: 8px !important;
}

/* Button */
.stButton>button {
    border-radius: 8px;
    padding: 0.6rem 1.2rem;
    font-size: 1rem;
    background-color: #2C73FF;
    color: white;
}
.stButton>button:hover {
    background-color: #1450D2;
    color: white;
}

/* CARD STYLE */
.review-card {
    background: white;
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 18px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.05);
    border: 1px solid #E6E6E6;
}

.review-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 6px;
}

.review-meta {
    font-size: 0.85rem;
    color: #666;
    margin-bottom: 10px;
}

.review-text {
    font-size: 0.95rem;
    line-height: 1.45rem;
    margin-bottom: 10px;
}

.dev-response {
    background: #F7F9FF;
    border-left: 4px solid #2C73FF;
    padding: 10px 12px;
    margin-top: 10px;
    border-radius: 8px;
    font-size: 0.9rem;
}

</style>
""", unsafe_allow_html=True)


# ===========================
# HERO
# ===========================
st.markdown("<div class='hero-title'>App Store Reviews Scraper</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Соберите отзывы любого приложения App Store по его ID</div>", unsafe_allow_html=True)


# ===========================
# INPUTS
# ===========================
st.subheader("Введите параметры")

app_id = st.text_input("App ID (например, 570060128 для Duolingo)")
country = st.text_input("Страна (us, ru, gb...)", value="us")


# ===========================
# BUTTON
# ===========================
if st.button("Собрать отзывы"):
    if not app_id.isdigit():
        st.error("App ID должен быть числом")
    else:
        with st.spinner("Собираем отзывы…"):
            df = fetch_reviews(int(app_id), country, limit=500)

        st.success(f"Скачано отзывов: {len(df)}")

        # CSV download
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Скачать CSV", csv, "reviews.csv")

        st.markdown("---")
        st.subheader("Отзывы")

        # ===========================
        # RENDER AS CARDS
        # ===========================
        for _, row in df.iterrows():
            stars = "⭐" * int(row["rating"])

            st.markdown(f"""
                <div class="review-card">
                    <div class="review-title">{row['title']}</div>
                    <div class="review-meta">{stars} · {row['user_name']} · {row['date']}</div>
                    <div class="review-text">{row['review']}</div>
            """, unsafe_allow_html=True)

            if row["dev_response"]:
                st.markdown(f"""
                    <div class="dev-response">
                        <b>Ответ разработчика:</b><br>
                        {row['dev_response']}
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
