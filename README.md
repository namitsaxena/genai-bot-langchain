# GCP Gen AI
This repo contains Gen AI code samples for Google's GCP/Vertex AI platform.


## Resources
* [Overview of Generative AI on Vertex AI  |  Google Cloud [cloud.google.com]](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/overview)
* https://github.com/GoogleCloudPlatform/generative-ai/blob/main/language/getting-started/intro_palm_api.ipynb
* https://github.com/GoogleCloudPlatform/generative-ai/blob/main/embeddings/intro-textemb-vectorsearch.ipynb

## Setup and Execution
* Setup virtual env
* Install requirements: 
  * ```pip3 install -r requirements.txt```
  * ```pip3 list```
* Authenticate to Google Using ```gcloud auth application-default login```
* Update project settings, primarily
  * project id
  * region
* Running:
  ```
  python3 main.py
  ```

## Troubleshooting
* pip3 install db-dtypes didn't work by default and had issues installing pyarrow (probably becasue it was trying to get version > 3.0.0 or using some stale cached version). Fixed by manually installing:
  ```
  pip3 install pyarrow==3.0.0
  pip3 install db-dtypes
  ```