# Initialise project
import streamlit as st
import pandas as pd
import numpy as np

# Start Front End interface
st.set_page_config(page_title='ODKCleaner', page_icon="🧡")

# Set Styles
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
load_css('style.css')
# Supress streamlit branding
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

################### Front End ###################
# Set Front End appearance
st.title('ODK -> STATA') # Title
st.markdown('This website produces STATA cleaning code for your ODK generated dataset. Just upload your XLSForm below to get started. You can find the XLSForm of your questionnaire in your dashboard on Kobo/ODK Cloud/ SurveyCTO. Click [here](https://xlsform.org/en/) for more information.') # First paragraph
st.subheader('Upload your XLSForm') # Upload prompt
uploaded_file = st.file_uploader('Choose your XLSXFile', type='xlsx') # Save file to memory for duration of session
# Sidebar 
with st.sidebar:
    st.title('Need more specialised help?')
    st.sidebar.write("")
    st.markdown('##### To get specialised advice and assistance on your ODK and/or Stata projects, reach out via: ')
    st.markdown('[LinkedIn](https://www.linkedin.com/in/jweinert1997/)')
    st.markdown('[Github](https://github.com/JonasWeinert/)')
    st.markdown('[Email](emailto:jnas.weinert@gmail.com)')
    st.markdown('---')
    st.header('This project')
    st.markdown('#### Planned features:')
    st.markdown('- Reformatting date and time variables from strings')
    st.markdown('- Optionally split *select_multiple* fields in Stata instead of at export')
    st.markdown('- Create cleaning code for R')
    st.markdown('- [Request a feature](https://github.com/JonasWeinert/ODK_CleaningcodeGenerator/issues=)')
    st.markdown('#### Repository:')
    st.markdown('- [Contribute on GitHub](https://github.com/JonasWeinert/ODK_CleaningcodeGenerator/)')
    st.markdown('---')
    st.header('Was this helpful to you? ')
    st.markdown('- [Buy me a coffee](#)')
    st.markdown('---')

################# File Processing #################
# Import Survey and Choices sheets into dataframes & ask user relevant field information
if uploaded_file:
    try:
        filename = uploaded_file.name # store filename
        st.markdown('---')
    # Preparing dataframes 
        # Read excel sheets into data frames
        dfchoices = pd.read_excel(uploaded_file, 'choices', engine = 'openpyxl')
        dfsurvey = pd.read_excel(uploaded_file, 'survey', engine = 'openpyxl')
        # split type into two columns to get list_name
        dfsurvey[['type', 'list_name']] = dfsurvey['type'].str.split(' ', expand=True)
    # Prepare label/language selection field by identifying different labels
        # Find columns containing the string 'label'
        var_label_columns = [col for col in dfsurvey.columns if 'label' in col]
        var_label_columns.insert(0, 'Select a column')
    # Let user choose language
        st.subheader('Setup')
        st.markdown('### Label language')
        label_field = st.selectbox('Which set of questionnaire labels do you want to use as your variable labels:', var_label_columns)
    # Select_multiple seperator
        if 'select_multiple' in dfsurvey['type'].values: # Check if select_multiple fields are in survey
            st.markdown('### Handling *select_multiple* fileds')
            st.markdown('Your questionnaire uses *select_multiple* fields. Please indicate if you want to produce code that splits these into a set of binary variables, or if you already selected the "seperate select_multiple" option in ODK/Kobo/SurveyCTO/... when downloading your data.')
            col1, col2 = st.columns(2)
            with col1:
                s_m_handle = st.radio(
                    "How do you want to handle these questions:",
                    key="visibility",
                    options=["They are already split. Just label them for me", "Split and label them for me"],
                )
            with col2:
                if s_m_handle == "They are already split. Just label them for me":
                    s_m_splitter = st.text_input("Please type the seperator symbol that you used below. This is the symbol that is put between the question name and the respective answer option in your dummies' names. Leave blank for no symbol:")

                if s_m_handle == "Split and label them for me":
                    s_m_splitter = st.text_input("Please type the seperator symbol that you would like to use below. This is the symbol that is put between the question name and the respective answer option in your dummies' names. Leave blank for no symbol:")

    except ValueError:
        st.error('Your file does not contain survey & choices sheet. Make sure to include the sheets under these names. If you do not use choices, add an empty sheet')
# Generating cleaning lines
try:
    if uploaded_file and label_field:
    # Loop through the DataFrame and create the output string
        # Handling all variables except select_multiple
        varnames = "/// Variables labels: \n\n"
        line_reg = "" # regular variables
        line_note = "" # notes
        line_calc = "" # calc fields
        line_range = "" # range fields
        varnames_finished = False # indicating completion of this step
        ## Variable names
        try:
            for index, row in dfsurvey.iterrows():
                if row["type"] not in ["note", "calculate", "begin_group", "end_group" "rank"]:
                    line_reg = f'capture label variable {row["name"]} "{row[label_field]}" \n\n'
                    varnames += line_reg
                if row["type"] in ["calculate"]:
                    line_calc = f'capture label {row["name"]}  "calculation: {row["calculation"]}"\n\n'
                    varnames += line_calc   
                if row["type"] in ["range"]:
                    line_calc = f'capture label {row["name"]}  "{row[label_field]}" "range: {row["parameters"]}"\n\n'
                    varnames += line_range   
                if row["type"] in ["note"]:
                    line_note = f'capture drop {row["name"]}\n\n'
                    varnames += line_note   
            else:
                varnames_finished = True
        except KeyError:
            pass

        ## Value labels for select_one
        s_o_labelling_finished = False
        try:
            s_o_line = "/// Value labels for dummy variables: \n\n"
            # Iterate through survey sheet
            for index, survey_row in dfsurvey.iterrows():
                if survey_row["type"] == "select_one":
                    mpstr = survey_row["list_name"]
                    quest = survey_row[label_field]
                    name = survey_row["name"]
                    x = 1
                    s_o_line += f'capture label define {name} '
                    for index, choices_row in dfchoices.iterrows():
                        if choices_row["list_name"] == mpstr:
                            answ = choices_row[label_field]
                            num = choices_row["name"]
                            s_o_line += f'{num} "{answ}" '
                            x += 1
                    s_o_line += f', replace\n'
                    s_o_line += f'capture label val {name} {name}\n\n'
            else:
                s_o_labelling_finished = True
        except KeyError:
            pass

        # select_multiple variables: varnames + labels
        s_m_labelling_finished = False
        try:
            s_m_line = "\n /// Select_Multiple Questions: \n\n"
            # Iterate through survez sheet
            for index, survey_row in dfsurvey.iterrows():
                if survey_row["type"] == "select_multiple":
                    mpstr = survey_row["list_name"]
                    quest = survey_row[label_field]
                    name = survey_row["name"]
                    x = 1
                    for index, choices_row in dfchoices.iterrows():
                        if choices_row["list_name"] == mpstr:
                            answ = choices_row[label_field]
                            num = choices_row["name"]
                            s_m_line += f'capture label variable {name}{s_m_splitter}{num} "{num}_{answ}:{quest}"\n'
                            s_m_line += f'capture label define {name}{s_m_splitter}{num} 0 "No" 1 "Yes", replace\n'
                            s_m_line += f'capture label val {name}{s_m_splitter}{num} {name}{num}\n\n'
                            x += 1
            else:
                s_m_labelling_finished = True
        except KeyError:
            pass

    # Print code
        if varnames_finished and s_o_labelling_finished and s_m_labelling_finished:
                st.markdown('---')
                st.subheader('Your Stata Cleaning Code')
                st.markdown('This WebApp was developed with love and coffe. If you like the result, please consider [buying me a coffe](#).')
                header = '//////// Cleaning Code for ' + filename + '\n\n'
                outputcode = header + varnames + s_o_line + s_m_line
                st.code(outputcode, language='html')
except NameError:
    pass



    
