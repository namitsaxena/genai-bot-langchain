import vertexai


def print_data(df):
    frames = df.head()
    print(f"Frame Head:-")
    print(frames)


class EmbeddingEngine:

    def __init__(self, project_id, region):
        self.project_id = project_id
        self.region = region
        vertexai.init(project=project_id, location=region)
        self.embeddings_model = self.load_embeddings_model()

    def load_embeddings_model(self, model_name="textembedding-gecko@001"):
        from vertexai.preview.language_models import TextEmbeddingModel
        return TextEmbeddingModel.from_pretrained(model_name)

    def load_data(self, size=1000):
        """
        Loads BQ public dataset for stackoverflow questions
        :param project_id:
        :param size:
        :return:
        """
        import pandas as pd
        from google.cloud import bigquery

        bq_client = bigquery.Client(project=self.project_id)
        QUERY_TEMPLATE = """
                SELECT distinct q.id, q.title
                FROM (SELECT * FROM `bigquery-public-data.stackoverflow.posts_questions`
                where Score > 0 ORDER BY View_Count desc) AS q
                LIMIT {limit} ;
                """
        print("Loading Data from BQ...")
        query = QUERY_TEMPLATE.format(limit=size)
        query_job = bq_client.query(query)
        rows = query_job.result()
        print(f"Rows Count: {rows.total_rows}")
        df = rows.to_dataframe()
        return df

    def get_embeddings_wrapper(self, texts, batch_size=5):
        """
        By default, the text embeddings API has a "request per minute" quota set to 60 for new Cloud projects and 600
        for projects with usage history (see Quotas and limits to check the latest quota value for
        base_model:textembedding-gecko). So, rather than using the function directly, you may want to define a
        wrapper like below to limit under 10 calls per second, and pass 5 texts each time. :param texts: :param
        batch_size: :return:
        """
        import time
        import tqdm  # to show a progress bar
        embs = []
        for i in tqdm.tqdm(range(0, len(texts), batch_size)):
            time.sleep(1)  # to avoid the quota error
            result = self.embeddings_model.get_embeddings(texts[i: i + batch_size])
            embs = embs + [e.values for e in result]
        return embs

    def get_embeddings(self, df):
        """
        get embeddings for the question titles and add them as "embedding" column
        :param df:
        :return:
        """
        print("Getting embeddings for the data...")
        df = df.assign(embedding=self.get_embeddings_wrapper(list(df.title)))
        print_data(df)
        return df

    def export_embeddings(self, df, filename, file_format="jsonl"):
        if file_format == "jsonl":
            jsonl_string = df[["id", "embedding"]].to_json(orient="records", lines=True)
            with open(filename, "w") as f:
                f.write(jsonl_string)
        else:
            raise Exception(f"Failed to export! Unsupported format: {file_format}")

    def get_similarities(self, df, metric_type="product"):
        """
        In case of the model textembedding-gecko@001, we need to use inner product (dot product).
        :param df:
        :param metric_type:
        :return:
        """
        import random
        import numpy as np

        # pick one of them as a key question
        key = random.randint(0, len(df))

        # calc dot product between the key and other questions
        embs = np.array(df.embedding.to_list())
        if metric_type == "product":
            similarities = np.dot(embs[key], embs.T)
        else:
            raise Exception(f"Metric Type: {metric_type} NOT supported")

        # print similarities for the first 5 questions
        similarities[:5]

        # sort the questions with the similarities and print the list.
        print(f"Key question: {df.title[key]}\n")

        # sort and print the questions by similarities
        sorted_questions = sorted(
            zip(df.title, similarities), key=lambda x: x[1], reverse=True
        )[:20]
        for i, (question, similarity) in enumerate(sorted_questions):
            print(f"{similarity:.4f} {question}")
