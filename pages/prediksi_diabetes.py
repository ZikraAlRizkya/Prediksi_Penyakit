import streamlit as st
import joblib
from PDF_process.pdf import extract_file_pdf
import pandas as pd
import time

from process.preprocess import preprocessing

model = joblib.load('model/model_diabetes.pkl')
scaler = joblib.load('model/scaler_diabetes.pkl')
#encoder = joblib.load('model/encoder_diabetes.pkl')

current_page = "Prediksi Diabetes"

st.title(current_page)

if "active_page" not in st.session_state:
    st.session_state["active_page"] = current_page
elif st.session_state.get("active_page") != current_page:
    st.session_state.clear()
    st.session_state["active_page"] = current_page

upload_file = st.file_uploader("Upload file PDF hasil pemeriksaan:",type=['pdf'])

if "data_valid" not in st.session_state:
    st.session_state.data_valid = False
if "data" not in st.session_state:
    st.session_state.data = None

if upload_file is not None and not st.session_state.data_valid:
    with st.spinner("Membaca file PDF ...", show_time=True):
        time.sleep(2)
    st.success("PDF berhasil diunggah!")

    data = extract_file_pdf(upload_file)
    atribut_diabetes = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction','Age']

    with st.spinner("Validasi file PDF ...", show_time=True):
        time.sleep(2)

    if any(key in atribut_diabetes for key in data):
        st.session_state.data_valid = True
        data = pd.DataFrame([data])
        data = data.reindex(columns = atribut_diabetes)
        st.session_state.data = data
    else:
        st.info("PDF yang anda masukan tidak sesuai, harap masukan PDF yang sesuai!")

if st.session_state.data_valid:
    st.write("Data yang berhasil disimpan: ")
    st.write(st.session_state.data)

    if st.button("Prediksi sekarang!"):
        with st.spinner("Prediksi sedang berlangsung ...", show_time=True):
            time.sleep(2)
        input_process = preprocessing(st.session_state.data, scaler,training=False)
        prediction = model.predict(input_process)[0]

        print(prediction)

        if prediction == 1:
            st.success("Anda terkena penyakit diabetes!")
        else:
            st.success("Anda tidak terkena penyakit diabetes")
        st.session_state.data_valid = False
        del st.session_state.data