FROM python:3.11-slim

RUN mkdir /streamlit

COPY requirements.txt /streamlit/

WORKDIR /streamlit

RUN pip install --no-cache-dir -r requirements.txt

COPY . /streamlit

EXPOSE 8501

CMD ["streamlit", "run", "Library_App.py", "--server.address=0.0.0.0", "--server.port=8501"]