import streamlit as st
from scraper import fetch_reviews

# =======================
# СТИЛИ (CSS)
# =======================
st.set_page_config(page_title="App Store Reviews Scraper", layout="centered")

st.markdown("""
<style>
    /* Центрируем всё */
    .block-container {
        max-width: 780px !important;
        padding-top: 2rem;
    }

    /* Главный заголовок */
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.3rem;
        color: #1E1E1E;
    }

    /* Подзаголовок */
    .hero-subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #6A6A6A;
        margin-bottom: 2.5rem;
    }

    /* Секции */
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }

    /* Инпуты */
    input, textarea {
        border-radius: 8px !important;
    }

    /* Кнопка */
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

</style>
""", unsafe_allow_html=True)


# =======================
# HERO SECTION
# =======================
st.markdown("<div class='hero-title'>App Store Reviews Scraper</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='hero-subtitle'>Соберите отзывы любого приложения App Store по его ID — быстро и удобно</div>",
    unsafe_allow_html=True
)

# =======================
# ФОРМА ВВОДА
# =======================

st.markdown("<div class='section-title'>Введите параметры</div>", unsafe_allow_html=True)

app_id = st.text_input("App ID (например, 570060128 для Duolingo)", value="")
country = st.text_input("Страна (us, ru, gb...)", value="us")

# =======================
# КНОПКА
# =======================
if st.button("Собрать отзывы"):
    if not app_id.isdigit():
        st.error("App ID должен быть числом")
    else:
        with st.spinner("Собираем отзывы…"):
            df = fetch_reviews(int(app_id), country, limit=500)

        st.success(f"Скачано отзывов: {len(df)}")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Скачать CSV", csv, "reviews.csv")
