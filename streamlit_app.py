import streamlit as st
import io
import openai 
import pdfplumber
import pdf2image
import streamlit as st
import os


def from_pdf_to_text(path: str):
   

    text = ""
    
    pdf = pdfplumber.open(path) 
    for pages in pdf.pages:
            text += pages.extract_text() + "     "
            
    return  text


def from_pdf_bytes_to_image(uploaded_pdf: bytes) -> str:
  
    pdf_pages = pdf2image.convert_from_bytes(uploaded_pdf, dpi=200)
    
    return pdf_pages



def get_report_from_numbers(bilan: str):
    key = "OPENAI_API_KEY"
    openai.api_key = os.getenv(key)
    #openai.api_key ="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"
    prompt = [{"role": "user", "content": f"write a detailed and well written finacial report using the text below:{bilan} "}]
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=prompt)
    return completion.choices[0].message.content
def get_X_Y_plot(text):
    key = "OPENAI_API_KEY"
    openai.api_key = os.getenv(key)
    prompt = [{"role": "user", "content": f"give back meaningful values from this text:{text} "}]
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=prompt)
    return completion.choices[0].message.content


st.set_page_config(layout="wide")
st.title("Financial report from balance sheet")

pdf_file = st.file_uploader("Choose a pdf file")



if pdf_file is not None:
  images = from_pdf_bytes_to_image(pdf_file.getvalue())
  col1,col2 = st.columns([10,7])
  col1.image(images[0])
  col3,col4,col5 =st.columns([2,2,5])
  
  if col4.button("Extract Finacial Report"):
    text = from_pdf_to_text(io.BytesIO(pdf_file.read()))
    report = get_report_from_numbers(text)
    #report = "waaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    txt = col2.text_area("**Extracted Finacial report**",report,height=1100)
    col2.download_button(
    label="Download report as pdf",
    data=csv,
    file_name='report.pdf',
    mime='text/csv',
)
    st.write(get_X_Y_plot(report))


