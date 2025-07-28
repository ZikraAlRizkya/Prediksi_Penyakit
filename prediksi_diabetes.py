import streamlit as st
import joblib
from PDF_process.pdf import extract_file_pdf
import pandas as pd

from process.preprocess import preprocessing

model = joblib.load('model/model_diabetes.pkl')
scaler = joblib.load('model/scaler_diabetes.pkl')
#encoder = joblib.load('model/encoder_diabetes.pkl')

st.title("Prediksi Diabetes")

upload_file = st.file_uploader("Upload file PDF hasil pemeriksaan:",type=['pdf'])

if upload_file is not None:
    st.success("PDF berhasil diunggah, tunggu sebentar...")
    data = extract_file_pdf(upload_file)
    
    st.write("Data yang berhasil disimpan: ", data)
    data = pd.DataFrame([data])
    atribut_diabetes = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction','Age']
    data = data.reindex(columns = atribut_diabetes)

    if st.button("Prediksi sekarang!"):
        input_process = preprocessing(data, scaler,training=False)

        prediction = model.predict(input_process)[0]

        print(prediction)

        if prediction == 1:
            st.success("Anda terkena penyakit diabetes!")
        else:
            st.success("Anda tidak terkena penyakit diabetes")