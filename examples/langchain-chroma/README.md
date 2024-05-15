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