import fitz
import pandas as pd
import re

def extract_file_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype='pdf')
    data = {}
    
    keyword_map = {
        'Jumlah Kehamilan' : 'Pregnancies',
        'Glukosa (mg/dL)' : 'Glucose',
        'Tekanan Darah (mm Hg)' : 'BloodPressure',
        'Ketebalan Lipatan Kulit (mm)' : 'SkinThickness',
        'Insulin (mu U/ml)' : 'Insulin',
        'BMI' : 'BMI',
        'Diabetes Pedigree Function' : 'DiabetesPedigreeFunction',
        'Usia' : 'Age',
        'WBC' : 'WBC',
        'LYMp' : 'LYMp',
        'NEUTp' : 'NEUTp',
        'LYMn' : 'LYMn',
        'NEUTn' : 'NEUTn',
        'RBC' : 'RBC',
        'HGB' : 'HGB',
        'HCT' : 'HCT',
        'MCV' : 'MCV',
        'MCH' :'MCH',
        'MCHC' :'MCHC',
        'PLT' : 'PLT', 
        'PDW' : 'PDW',
        'PCT' : 'PCT',
    }

    for page in doc:
        textpage = page.get_textpage("text")
        text = textpage.extractText()
        lines = text.split('\n')
        total_lines = len(lines)
        for i, line in enumerate(lines):
            line = line.strip()
            if line in keyword_map:
                if i+1 < total_lines:
                    value_line = lines[i+1].strip()
                    mapped_key = keyword_map[line]
                    try:
                        if mapped_key in ['BMI', 'DiabetesPedigreeFunction', 'LYMp', 'NEUTp', 'LYMn', 'RBC', 'HGB', 'HCT', 'MCV', 'MCH', 'MCHC', 'PDW', 'PCT']:
                            data[mapped_key] = float(value_line)
                        else:
                            data[mapped_key] = int(float(value_line))
                    except ValueError:
                            data[mapped_key] = None
    return data