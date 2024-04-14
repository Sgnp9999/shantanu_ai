FROM python:3.8

RUN apt-get update

RUN pip3 install sentence_transformers langchain tabulate langchain_experimental langchain_community faiss-cpu pandas PyPDF2

WORKDIR /app

COPY . /app

EXPOSE 8501

CMD ["streamlit", "run", "main.py"]