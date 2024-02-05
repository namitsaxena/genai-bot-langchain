from google.cloud import aiplatform


class VectorSearchDB:

    def __init__(self, project_id, region):
        aiplatform.init(project=project_id, location=region)
        self.idx = None
        self.deployed_idx_id = None
        self.idx_endpoint = None

    def create_index(self
                     , display_name
                     , gcs_bucket_uri
                     , dimensions=768
                     , approx_neighbours_cnt=20
                     , dist_measure_type="DOT_PRODUCT_DISTANCE"
                     ):

        # create index
        # By calling the create_tree_ah_index function, it starts building an Index. This will take under a few minutes
        # if the dataset is small, otherwise about 50 minutes or more depending on the size of the dataset.
        print(f"Creating index: display_name: {display_name}, bucket_uri={gcs_bucket_uri} ....")
        self.idx = aiplatform.MatchingEngineIndex.create_tree_ah_index(
            display_name=display_name,
            contents_delta_uri=gcs_bucket_uri,
            dimensions=dimensions,
            approximate_neighbors_count=approx_neighbours_cnt,
            distance_measure_type=dist_measure_type,
        )

        # create IndexEndpoint
        # This tutorial utilizes a Public Endpoint and does not support Virtual Private Cloud (VPC). Unless you have a
        # specific requirement for VPC, we recommend using a Public Endpoint. Despite the term "public" in its name, it
        # does not imply open access to the public internet. Rather, it functions like other endpoints in Vertex AI
        # services, which are secured by default through IAM. Without explicit IAM permissions, as we have previously
        # established, no one can access the endpoint.
        print("Creating index endpoint...")
        self.idx_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
            display_name=display_name,
            public_endpoint_enabled=True,
        )

        # deploy the Index by specifying an unique deployed index ID.
        # Deployed Index ID should start with a letter and contain only letters, numbers and underscores.
        self.deployed_idx_id = display_name.replace("-", "_")
        print(f"Deploying the index with deployed index id: {self.deployed_idx_id}...")
        self.idx_endpoint.deploy_index(index=self.idx, deployed_index_id=self.deployed_idx_id)

    def destroy(self):
        print("Deleting Index Endpoint, Index...:")
        # delete Index Endpoint
        if self.idx_endpoint:
            print("undeploying the index...")
            self.idx_endpoint.undeploy_all()
            print("deleting index endpoint..")
            self.idx_endpoint.delete(force=True)
        # delete Index
        if self.idx:
            print("deleting index..")
            self.idx.delete()

    def query(self, query_embeddings, num_neighbors=20):
        """
        uses an embedding for a test question, and find similar question with the Vector Search.
        The find_neighbors function only takes milliseconds to fetch the similar items even when you have billions of
        items on the Index, thanks to the ScaNN algorithm.
        :param num_neighbors:
        :param query_embeddings: embedding for a single query/question
        :return:
        """
        response = self.idx_endpoint.find_neighbors(
            deployed_index_id=self.deployed_idx_id,
            queries=query_embeddings,
            num_neighbors=num_neighbors,
        )
        return response
