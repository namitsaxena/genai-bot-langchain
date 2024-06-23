import google.cloud.logging


class GCPCloudLoggingUtility():

    def __init__(self):
        self.client = google.cloud.logging.Client()
        self.client.setup_logging()
        print("GCP Cloud Logging Initialized")

    def retrieve_logs(self, max_results=5, logger_name=None):
        return self.client.list_entries(max_results=max_results)