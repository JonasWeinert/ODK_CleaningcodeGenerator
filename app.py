import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title='ODKCleaner')
st.title('Apptest')
st.subheader('Upload your file')

code = '''foreach v in varlist{
    testststs   
    }'''

uploaded_file = st.file_uploader('Choose your XLSXFile', type='xlsx')

if uploaded_file:
        # Find columns containing the string 'label'
        st.markdown('---')
        dfsurvey = pd.read_excel(uploaded_file, 'survey', engine = 'openpyxl')
        dfchoices = pd.read_excel(uploaded_file, 'choices', engine = 'openpyxl')
        label_columns = [col for col in dfsurvey.columns if 'label' in col]
        if label_columns:
            st.markdown('### Which set of questionnaire labels do zou want to use as zour variable labels:')
            label_field = st.selectbox('', label_columns)
        else:
            st.error('No columns with "label" found in the DataFrame')
        
if uploaded_file and label_field:
    # Loop through the DataFrame and create the output string
        output = ""
        loop_finished = False
        try:
            for index, row in dfsurvey.iterrows():
                caution = ""
                if row["type"] not in ["note", "calculation"]:
                    caution = "Caution: "
                    line = f'{caution}This is {row["type"]} without {row[label_field]}\n\n'
                output += line
            else:
                loop_finished = True
        except KeyError:
            st.error('The column @label_field seems not to exist. Please select enter the correct column nameö')
        if loop_finished:
            st.code(output, language='html')

