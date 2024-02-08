import unittest

from RAGMultimodal import MultiModalRAG

PROJECT_ID = "nsx-sandbox"  # @param {type:"string"}
REGION = "us-central1"  # @param {type:"string"}


class TestMultiModalRAG(unittest.TestCase):

    # @unittest.skip("only for manual execution")
    def test_document_metadata(self):
        pdf_file = "../resources/google-10k-sample-14pages.pdf"
        output_image_dir = "../resources/images"
        rag = MultiModalRAG(PROJECT_ID)
        text_metadata_df, image_metadata_df = rag.process_document_metadata(pdf_file, output_image_dir)

        print(f"Inspecting the text metadata: {text_metadata_df.head()}")
        print(f"Inspecting the image metadata: {image_metadata_df.head()}")

        query = "I need details for basic and diluted net income per share of Class A, Class B, and Class C share for google?"
        rag.search_text(query)
        # rag.search_image(query)

        query = """Question: How has nasdaq and s&p performed with respect to class A shares and class C shares?
        Which one would be better to buy and why?
        Answer: """
        rag.perform_rag(query)