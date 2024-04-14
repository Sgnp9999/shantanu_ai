import streamlit as st
import pandas as pd
import streamlit_pdf_reader
import mistral
import os
st.title("AI ChatBot")
data_type = st.radio("Select Input Type:", ("Chat", "CSV", "Personal"))

from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import faiss
from langchain.text_splitter import CharacterTextSplitter
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2", cache_folder="emb")

if data_type == "Chat":
  user_input = st.text_input("Ask question:", placeholder="What is the currency of India?")
  if st.button("Send"):
    if user_input:
      output = mistral.ask_mistral(user_input)
      st.write("Output:")
      st.success(output)
    else:
      st.error("Please enter some text to process.")

elif data_type == "Personal":
  question = st.text_input("Ask question:", placeholder="What is the currency of India?")
  uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
  try:
    text=streamlit_pdf_reader.read_pdf(uploaded_file=uploaded_file)
    text_splitter = CharacterTextSplitter()
    texts= text_splitter.split_text(text=text)
    db = faiss.FAISS.from_texts(texts, embeddings)
  except:
    pass
  if st.button("Send"):
    if question:
        output=mistral.personal_mistral(question=question, db=db)
        st.write("Output:")
        st.success(output)
    else:
        st.error("Please enter some text to process.")

elif data_type == "CSV":
  question=st.text_input("Ask question on CSV:", placeholder="What is the maximum value in the 'Age' column?")
  uploaded_file = st.file_uploader("Upload CSV File:")
  try:
    df=pd.read_csv(uploaded_file)
  except:
    pass
  if uploaded_file is not None:
    if st.button("Send"):
      output = mistral.mistral_csv(df=df, question=question)
      st.write("Output:")
      st.success(output)