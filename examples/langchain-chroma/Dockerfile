FROM python

RUN pip install langchain langchain-chroma langchain-community sentence-transformers langchain-core

# Below only if we plan to run in offline mode (-e HUGGINGFACE_OFFLINE=1)
# copy the HF model cache to ~/.cache/..
RUN mkdir -p /root/.cache/huggingface/
COPY ./resources/hub/ /root/.cache/huggingface/hub/

RUN mkdir /app
COPY ./src/* /app
COPY ./resources/*.txt /app
WORKDIR /app

CMD ["python", "main.py"]