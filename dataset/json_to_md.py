import html2text
from bs4 import BeautifulSoup
import logging
import chardet
import json
import threading
from tqdm.auto import tqdm
from typing import Any, Dict
import bz2
from pathlib import Path

# Configure logging with thread safety
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)
thread_lock = threading.Lock()
# Create an HTML2Text converter object
converter = html2text.HTML2Text()
converter.body_width = 0  # Set body width to 0 to avoid wrapping
converter.ignore_links = True  # Do not ignore links
converter.ignore_images = True  # Do not ignore images
converter.ignore_tables = True  # Do not ignore tables

# Sample HTML content
def read_html_file(file_path):
    """
    Read HTML file with proper encoding detection.
    Returns the content of the file using the detected encoding.
    """
    try:
        # First, read the file in binary mode to detect encoding
        with open(file_path, 'rb') as f:
            raw_data = f.read()

        # Detect the encoding
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        logger.debug(f"Detected encoding {encoding} for {file_path}")

        # Try different encodings if detection failed
        if not encoding:
            encodings_to_try = ['utf-8', 'utf-16', 'iso-8859-1', 'cp1252', 'windows-1252']
        else:
            encodings_to_try = [encoding] + ['utf-8', 'utf-16', 'iso-8859-1', 'cp1252', 'windows-1252']

        # Try each encoding until one works
        for enc in encodings_to_try:
            try:
                return raw_data.decode(enc)
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.warning(f"Error trying encoding {enc}: {str(e)}")
                continue

        # If all encodings fail, return None instead of raising an error
        logger.error(f"Failed to decode {file_path} with any encoding")
        return None

    except Exception as e:
        logger.error(f"Error reading file {file_path}: {str(e)}")
        return None

def load_json_file(file_path):
    """Load and return the content of a JSON file."""
    logger.info(f"Loading JSON from {file_path}")
    with open(file_path) as f:
        return json.load(f)
def html_to_markdown(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for script in soup(["script", "style", "meta", "link"]):
        script.decompose()
    return converter.handle(str(soup))


def load_data_in_batches(dataset_path, batch_size):
    """
    Generator function that reads data from a compressed file and yields batches of data.
    Each batch is a dictionary containing lists of interaction_ids, queries, search results, query times, and answers.

    Args:
    dataset_path (str): Path to the dataset file.
    batch_size (int): Number of data items in each batch.

    Yields:
    dict: A batch of data.
    """

    def initialize_batch():
        """ Helper function to create an empty batch. """
        return {"interaction_id": [], "query": [], "search_results": [], "query_time": [], "answer": []}

    try:
        with bz2.open(dataset_path, "rt") as file:
            batch = initialize_batch()
            for line in file:
                try:
                    item = json.loads(line)
                    for key in batch:
                        batch[key].append(item[key])

                    if len(batch["query"]) == batch_size:
                        yield batch
                        batch = initialize_batch()
                except json.JSONDecodeError:
                    logger.warn("Warning: Failed to decode a line.")
            # Yield any remaining data as the last batch
            if batch["query"]:
                yield batch
    except FileNotFoundError as e:
        logger.error(f"Error: The file {dataset_path} was not found.")
        raise e
    except IOError as e:
        logger.error(f"Error: An error occurred while reading the file {dataset_path}.")
        raise e

def batch_generate_file(batch: Dict[str, Any], output_path):
    """
    Save html into markdown files one by one
    """
    reference_uris = {}
    batch_interaction_ids = batch["interaction_id"]
    queries = batch["query"]
    batch_search_results = batch["search_results"]
    query_times = batch["query_time"]
    seen_urls = set()
    for idx, search_result in enumerate(batch_search_results):
        for idy, html_text in enumerate(search_result):
            page_id = batch_interaction_ids[idx] + "_" + str(idy)
            html_source = html_text["page_result"]

            url = html_text["page_url"]
            if url in seen_urls:
                continue

            seen_urls.add(url)

            page_name = html_text["page_name"]
            page_last_modified = html_text["page_last_modified"]
            page_snippet = html_text["page_snippet"]
            html_markdown = html_to_markdown(html_source)
            markdown_path = output_path / f"{page_id}.md"
            with thread_lock:
                with open(markdown_path, 'w', encoding='utf-8') as f:
                    f.write(html_markdown)
            # save to markdown file and id-markdown relations
            reference_uris[page_id] = {
                'url': url,
                'page_name': page_name,
                'page_last_modified': page_last_modified,
                "page_snippet": page_snippet
            }
    return reference_uris

def load_path_file(dataset_path, output_dir):
    batch_size = 500000
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    all_reference_uris = {}
    for batch in tqdm(load_data_in_batches(dataset_path, batch_size), desc="Loading Markdown"):
        reference_uris = batch_generate_file(batch, output_path)
        all_reference_uris.update(reference_uris)
    uri_mapping_path = output_path / "reference_uris.json"
    with open(uri_mapping_path, 'w', encoding='utf-8') as f:
        json.dump(all_reference_uris, f, indent=2)


file_path = "myown/input/crag_task_1_and_2_dev_v4.jsonl.bz2"
output_dir = "myown/output_ignore_link_image_table"
load_path_file(file_path, output_dir)

