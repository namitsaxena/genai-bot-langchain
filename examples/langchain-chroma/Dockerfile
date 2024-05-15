FROM python

RUN pip install langchain langchain-chroma langchain-community sentence-transformers langchain-core

RUN mkdir /app
COPY ./src/* /app
COPY ./resources/* /app
WORKDIR /app

CMD ["python", "main.py"]