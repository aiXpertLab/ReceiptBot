import streamlit as st
from utils import st_def, ai
import openai, PyPDF2, os, time, pandas as pd

st_def.st_logo(title='👋 e-Recepit Extract')
tab1, tab2 = st.tabs(["Upload Receipt", "Display the Data"])
page_text = []     #array for page

with tab1:
    st.markdown('An electronic receipt, commonly known as an e-receipt, is a digital version of a traditional paper receipt that is generated and delivered electronically. Instead of a tangible piece of paper, e-receipts are sent via electronic channels, such as email or mobile applications, as proof of a transaction. They include the same transaction information as paper receipts, such as the date, time, and items purchased.')
    st.image("./data/invoice_Aaron Hawkins_38460.jpg")
    pdf1 = st.file_uploader('Upload your e-Receipt: ', type='pdf')
    #-----------------------------------------------
    with st.spinner('loading ...'):
        if pdf1:
            doc_obj = PyPDF2.PdfReader(pdf1)
            summary=' '
            with st.spinner('Analyzing...'):
                for i in range(0,len(doc_obj.pages)):
                    # creating a page object
                    pageObj = doc_obj.pages[i].extract_text()    # extract one page's text
                    pageObj = pageObj.replace('\t\r','')     # tab, enter
                    pageObj = pageObj.replace('\xa0','')     # non-breaking spaces
                    # extracting text from page
                    page_text.append(pageObj)                    # the whole pdf --> txt
            # st.session_state['page_text'] = page_text
            st.success("Load successfully. Continue to next tab: Display")
        else:
            st.info("waiting for uploading ...")
    

with tab2:
    if page_text is not None:
        # st.write(type(page_text))
        st.code(f'raw data:  {page_text}')
    else:
        st.warning("Please upload a PDF to display the data.")
    