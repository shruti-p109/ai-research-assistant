# not a job, a utility
# download_papers() # for now this one has fixed category and search_query
# save metadata

import time
import os
import urllib.parse
import urllib.request
import feedparser
from config import PDF_DIR, ARXIV_BASE_URL
from repo.storage.database import insert_document, SessionLocal
from datetime import datetime
from logger_setup import logger

def create_metatdata_entries(
        pdf_name,
        title,
        published,
        authors
    ):
        with SessionLocal() as session:
            inserted_doc_ids = insert_document(
                session,
                pdf_name,
                title,
                published,
                authors
            )
        return inserted_doc_ids

def donwload_papers(category, search, total_results):
    documents_metadata = []
    # search parameters
    query_params = {
        'search_query': category+'::'+search,
        'start': 0,
        'max_results': total_results,
        'sortBy': "submittedDate",
        "sortOrder": "descending",
    }
    encoded_url = ARXIV_BASE_URL + urllib.parse.urlencode(query_params)

    # add user agent (best practice), prevents blind IP block if script accidentally triggers rate limits
    headers= {
        'User-Agent': 'MyScienticReasearchAssistant/1.0 (contact: shruti.p109@gmail.com)'
    }
    # metadata request of {max_result} papers, fetch in chunk size of papers if need to scale in future
    time.sleep(5.0) # defensive delay if script is runs repeatedly
    request = urllib.request.Request(encoded_url, headers=headers)
    time.sleep(3.5) # delay before making first pdf download request (arxiv rate limits)

    try:
        if not os.path.exists(PDF_DIR):
            os.makedirs(PDF_DIR)

        # fecth atom feed metadata
        with urllib.request.urlopen(request) as response:
            feed_data = response.read()

        # parse with feedparser
        feed = feedparser.parse(feed_data)

        for entry in feed.entries:
            paper_id = entry.id.split('/abs/')[-1].split('v')[0]

            # extract pdf link
            pdf_link = None
            for link in entry.links:
                if link.get('title') == 'pdf':
                    # convert to dedicated export subdomain to optimize server load
                    pdf_link = link.href
                    break
            
            if pdf_link:
                logger.info(f"Fetching pdf for paper_id {paper_id}")
                pdf_request = urllib.request.Request(pdf_link, headers=headers)
                destination = os.path.join(PDF_DIR, f"{paper_id}.pdf")

                if os.path.exists(destination):
                    print(f"Skipping id {paper_id}. Already downloaded.")

                try:
                    # download binary file stream
                    with urllib.request.urlopen(pdf_request) as download, open(destination, 'wb') as local_file:
                        local_file.write(download.read())
                    logger.info(f"Downloaded {paper_id}")

                    # add to metadata
                    documents_metadata.append(
                        {
                            "title": entry.title.replace("\n", " ").strip(),
                            "time_tuple": entry.published_parsed,
                            "published": datetime(*entry.published_parsed[:3]).date(),
                            "authors": [author.name for author in entry.authors]
                        }
                    )

                    # arxiv rate limits - only 1 request every 3 seconds
                    time.sleep(3.5)
                except Exception as file_err:
                    logger.error(f"Failed to download file {paper_id}: {file_err}")
                    break # stop to avoid ban extension
        
        # insert documents metadata
        inserted_doc_ids = create_metatdata_entries(
            documents_metadata
        )
        logger.info(f"Inserted documets: {inserted_doc_ids}")
    except Exception as e:
        logger.error(f"Ingestion error occurred: {e}")