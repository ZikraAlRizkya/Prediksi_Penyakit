import streamlit as st
import joblib
from PDF_process.pdf import extract_file_pdf
import pandas as pd

from process.preprocess import preprocessing

model = joblib.load('model/model_anemia.pkl')
scaler = joblib.load('model/scaler_anemia.pkl')
#encoder = joblib.load('model/encoder_anemia.pkl')

st.title("Prediksi Anemia")

upload_file = st.file_uploader("Upload file PDF hasil pemeriksaan:",type=['pdf'])

if upload_file is not None:
    st.success("PDF berhasil diunggah, tunggu sebentar...")
    data = extract_file_pdf(upload_file)
    
    st.write("Data yang berhasil disimpan: ", data)
    data = pd.DataFrame([data])
    atribut_anemia = ['WBC', 'LYMp', 'NEUTp', 'LYMn', 'NEUTn', 'RBC', 'HGB', 'HCT', 'MCV', 'MCH', 'MCHC', 'PLT', 'PDW', 'PCT']
    data = data.reindex(columns = atribut_anemia)

    if st.button("Prediksi sekarang!"):
        input_process = preprocessing(data, scaler,training=False)

        prediction = model.predict(input_process)[0]

        print(prediction)

        if prediction == 'Healty':
            st.success("Anda sehat dari anemia")
        else:
            st.success(f"Anda terkena penyakit '{prediction}'")