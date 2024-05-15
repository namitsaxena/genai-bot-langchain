# Langchain Chroma
Loads and retrieves document from local Chroma db vector store. No GCP/Vertex integration has been done yet.
This is built using examples, etc found on langchain's website.


# status
Works only in Docker. Please refer to docker file. Failed to download all dependencies on mac(see below).

# Building and Running in Docker
```buildoutcfg
docker build . -t langchain-chroma:1

docker run langchain-chroma:1
docker run -e QUERY="What did the President say about Vladimir Putin" -e CHUNK_SIZE=500 langchain-chroma:1
```

# Note
* downloads the sentence transformer from huggingface at run time
  ```buildoutcfg
  OSError: We couldn't connect to 'https://huggingface.co' to load this file, couldn't find it in the cached files and it looks like sentence-transformers/all-MiniLM-L6-v2 is not the path to a directory containing a file named config.json.
  Checkout your internet connection or see how to run the library in offline mode at 'https://huggingface.co/docs/transformers/installation#offline-mode'.
  ```
Can be seen if we run from inside the container
```Dockerfile
| => docker run -it langchain-chroma:1 bash
root@c4a232f5055e:/app# 
root@c4a232f5055e:/app# ls -l
total 44
-rw-r--r-- 1 root root     0 Feb 19 05:44 __init__.py
-rw-r--r-- 1 root root  1391 May 15 02:17 main.py
-rw-r--r-- 1 root root 39027 May 15 00:53 state_of_the_union.txt
root@c4a232f5055e:/app# python main.py 
Running with input file: ./state_of_the_union.txt, Chunk Size: 1000, Query: What did the president say about Ketanji Brown Jackson
Loading Document...
modules.json: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 349/349 [00:00<00:00, 346kB/s]
config_sentence_transformers.json: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 116/116 [00:00<00:00, 118kB/s]
README.md: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 10.7k/10.7k [00:00<00:00, 12.0MB/s]
sentence_bert_config.json: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 53.0/53.0 [00:00<00:00, 74.6kB/s]
/usr/local/lib/python3.12/site-packages/huggingface_hub/file_download.py:1132: FutureWarning: `resume_download` is deprecated and will be removed in version 1.0.0. Downloads always resume when possible. If you want to force a new download, use `force_download=True`.
  warnings.warn(
config.json: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 612/612 [00:00<00:00, 1.20MB/s]
/usr/local/lib/python3.12/site-packages/huggingface_hub/file_download.py:1132: FutureWarning: `resume_download` is deprecated and will be removed in version 1.0.0. Downloads always resume when possible. If you want to force a new download, use `force_download=True`.
  warnings.warn(
model.safetensors: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 90.9M/90.9M [00:03<00:00, 29.2MB/s]
tokenizer_config.json: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 350/350 [00:00<00:00, 769kB/s]
vocab.txt: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 232k/232k [00:00<00:00, 9.02MB/s]
tokenizer.json: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 466k/466k [00:00<00:00, 24.9MB/s]
special_tokens_map.json: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 112/112 [00:00<00:00, 266kB/s]
1_Pooling/config.json: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 190/190 [00:00<00:00, 423kB/s]
Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. 

Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. 

One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. 

And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.

root@c4a232f5055e:/app# ls -l ~/.cache/huggingface/hub
total 8
drwxr-xr-x 6 root root 4096 May 15 02:22 models--sentence-transformers--all-MiniLM-L6-v2
-rw-r--r-- 1 root root    1 May 15 02:22 version.txt
root@c4a232f5055e:/app# find / -name config.json -print
/root/.cache/huggingface/hub/models--sentence-transformers--all-MiniLM-L6-v2/snapshots/e4ce9877abf3edfe10b0d82785e83bdcb973e22e/config.json
/root/.cache/huggingface/hub/models--sentence-transformers--all-MiniLM-L6-v2/snapshots/e4ce9877abf3edfe10b0d82785e83bdcb973e22e/1_Pooling/config.json
```

## Running Huggingface in offline mode
* Run the container like above in online mode
* Copy the cache from above using
  ```docker cp c4a232f5055e:/root/.cache/huggingface/hub .```
* Use the above to build the container
* Run in offline mode
  ```Dockerfile
  docker run -e QUERY="What did the President say about Vladimir Putin" -e HUGGINGFACE_OFFLINE=1  langchain-chroma:1
  ```

# Resources
- https://python.langchain.com/v0.1/docs/integrations/vectorstores/chroma/
- Vector stores | Langchain[[python.langchain.com](https://python.langchain.com/docs/modules/data_connection/vectorstores)]

# Mac direct building issues:
```
ERROR: Could not find a version that satisfies the requirement pulsar-client>=3.1.0 (from versions: 2.5.1, 2.5.2, 2.6.0, 2.7.0, 2.7.1)
ERROR: No matching distribution found for pulsar-client>=3.1.0
```

```
Cargo, the Rust package manager, is not installed or is not on PATH.
This package requires Rust and Cargo to compile extensions. Install it through
the system's package manager or via https://rustup.rs/
```