import unittest
from src.CodeApi import CodeBot
from src.EmbeddingEngine import EmbeddingEngine
from src.GCSUtil import GCSUtil
from src.VectorSearch import VectorSearchDB
import time

PROJECT_ID = "nsx-sandbox"
REGION = "us-central1"


def get_uid():
    from datetime import datetime
    return datetime.now().strftime("%m%d%H%M")


class TestEmbeddings(unittest.TestCase):

    def test_embedding_vertex_search(self):
        embeddings_json_file = "/tmp/questions.json"
        embed = EmbeddingEngine(PROJECT_ID, REGION)
        # if not os.path.exists(embeddings_json_file):
        #     print(f"embeddings file '{embeddings_json_file}' not found. creating new embeddings..")
        df = embed.load_data(50)
        df = embed.get_embeddings(df)
        embed.get_similarities(df)
        embed.export_embeddings(df, embeddings_json_file)
        # else:
        #     print(f"Embeddings already exist: {embeddings_json_file}")

        # Bucket create only if needed
        display_name_prefix = f"embvs-tutorial-index"
        uid = get_uid()
        display_name = f"{display_name_prefix}-{uid}"
        bucket_name = f"{display_name}"

        gcs = GCSUtil()
        bucket = None
        buckets = gcs.get_bucket_matching(display_name_prefix)
        if not buckets:
            print(f"No bucket found matching name prefix: {display_name_prefix}. Creating one")
            bucket = gcs.create_bucket(bucket_name, REGION)
            gcs.add_file(bucket.name, embeddings_json_file)
        else:
            print(f"bucket(s) already exists: {list(buckets)}. (first one will be used if more than one)")
            bucket = gcs.get_bucket(list(buckets)[0])

        bucket_uri = f"gs://{bucket.name}"
        print(f"Bucket uri: {bucket_uri}")

        try:
            vector_search = VectorSearchDB(PROJECT_ID, REGION)
            # TODO if existing bucket then vector search and bucket will have different names/id
            vector_search.create_index(display_name, bucket_uri)
            print("vector search index built!")

            time.sleep(60)  # TODO check if this resolves 503/SSL error
            print("Querying the vector...")
            # query
            query = "How to read JSON with Python?"
            test_embeddings = embed.get_embeddings_wrapper([query])
            response = vector_search.query(test_embeddings)

            # show the result
            import numpy as np

            for idx, neighbor in enumerate(response[0]):
                id = np.int64(neighbor.id)
                similar = df.query("id == @id", engine="python")
                print(f"{neighbor.distance:.4f} {similar.title.values[0]}")
        except Exception as e:
            print(f"Failed with error: {e}")
        finally:
            input("Press Enter to clean up...:")
            vector_search.destroy()
            # gcs.delete_bucket(bucket_name)
