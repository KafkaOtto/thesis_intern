from helpers.utils import load_json_file
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def load_queries(dataset_path):
    """
    Load queries from a dataset file.
    :param dataset_path: Path to the dataset file.
    :return: List of queries.
    """
    data = load_json_file(dataset_path)
    if data is None:
        return None
    all_queries = []
    for query in data:
        all_queries.append(query['request_config']['prompt'][0])
    return all_queries

def load_similarities(queries):
    """
    Load similarities from a dataset file.
    :param dataset_path: Path to the dataset file.
    :return: List of similarities.
    """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(queries)

    # Compute cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix)

    n = cosine_sim.shape[0]
    upper_triangle_indices = np.triu_indices(n, k=1)

    # Get the upper triangle values
    similarities = cosine_sim[upper_triangle_indices]

    # Summary statistics
    avg_similarity = np.mean(similarities)
    max_similarity = np.max(similarities)
    min_similarity = np.min(similarities)
    std_similarity = np.std(similarities)

    print(f"Average similarity: {avg_similarity:.4f}")
    print(f"Max similarity: {max_similarity:.4f}")
    print(f"Min similarity: {min_similarity:.4f}")
    print(f"Standard deviation: {std_similarity:.4f}")


if __name__ == '__main__':
    dataset_path = '../results/output_with_ram/t1_thresholds_0.68/run_1/RAG_batch_t1_thresholds_0.68_prod_responses.json'
    queries = load_queries(dataset_path)
    print(queries[0:10])  # Print the first 10 queries for verification
    load_similarities(queries)
