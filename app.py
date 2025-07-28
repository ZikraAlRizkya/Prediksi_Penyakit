import streamlit as st

st.title("Web Prediksi Penyakit")
st.set_page_config(page_title="Prediksi Penyakit", page_icon="🩺", layout="centered")

page = {
    "Prediksi Sekarang!":[
        st.Page("prediksi_diabetes.py", title="Prediksi Diabetes",),
        st.Page("prediksi_anemia.py", title="Prediksi Anemia"),
    ],
}

pg = st.navigation(page, position='sidebar')
pg.run()