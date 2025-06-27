import arxiv
import requests
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
import time
from scholarly import scholarly
import xml.etree.ElementTree as ET
from datetime import datetime

# Initialize the sentence transformer model for semantic search
model = SentenceTransformer('all-MiniLM-L6-v2')

def search_semantic_scholar(query, max_results=10):
    """Search papers from Semantic Scholar API"""
    url = f"https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": max_results,
        "fields": "title,abstract,url,year,authors,venue"
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        papers = []
        for paper in data.get('data', []):
            if paper.get('abstract'):
                papers.append({
                    'title': paper.get('title', ''),
                    'abstract': paper.get('abstract', ''),
                    'url': paper.get('url', ''),
                    'year': paper.get('year'),
                    'authors': [author.get('name', '') for author in paper.get('authors', [])],
                    'source': 'Semantic Scholar'
                })
        return papers
    return []

def search_arxiv(query, max_results=10):
    """Search papers from arXiv API using direct requests instead of the arxiv package"""
    # Use HTTPS explicitly in the URL
    base_url = "https://export.arxiv.org/api/query"
    
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }
    
    papers = []
    try:
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            # Parse the XML response
            root = ET.fromstring(response.content)
            
            # Define XML namespaces
            namespaces = {
                '': 'http://www.w3.org/2005/Atom',
                'arxiv': 'http://arxiv.org/schemas/atom'
            }
            
            # Extract entries
            entries = root.findall('./entry', namespaces)
            
            for entry in entries:
                # Extract paper details
                title = entry.find('./title', namespaces).text.strip() if entry.find('./title', namespaces) is not None else ''
                
                summary = entry.find('./summary', namespaces).text.strip() if entry.find('./summary', namespaces) is not None else ''
                
                # Get authors
                authors_elements = entry.findall('./author/name', namespaces)
                authors = [author.text for author in authors_elements] if authors_elements else []
                
                # Get URL
                links = entry.findall('./link', namespaces)
                pdf_url = ''
                for link in links:
                    if link.get('title') == 'pdf':
                        pdf_url = link.get('href')
                        break
                
                # Get published date and extract year
                published_text = entry.find('./published', namespaces).text if entry.find('./published', namespaces) is not None else ''
                year = None
                if published_text:
                    try:
                        published_date = datetime.strptime(published_text, "%Y-%m-%dT%H:%M:%SZ")
                        year = published_date.year
                    except:
                        pass
                
                # Add to papers list
                papers.append({
                    'title': title,
                    'abstract': summary,
                    'url': pdf_url,
                    'year': year,
                    'authors': authors,
                    'source': 'arXiv'
                })
        
    except Exception as e:
        print(f"Error with arXiv search: {e}")
    
    return papers

def search_google_scholar(query, max_results=5):
    """Search papers from Google Scholar"""
    papers = []
    try:
        # Use scholarly cautiously as it might get blocked
        search_query = scholarly.search_pubs(query)
        count = 0
        
        for i in range(max_results):
            try:
                publication = next(search_query)
                # Fetch additional details if available
                if 'pub_url' in publication:
                    detailed_pub = scholarly.fill(publication)
                else:
                    detailed_pub = publication
                
                papers.append({
                    'title': detailed_pub.get('bib', {}).get('title', ''),
                    'abstract': detailed_pub.get('bib', {}).get('abstract', ''),
                    'url': detailed_pub.get('pub_url', ''),
                    'year': detailed_pub.get('bib', {}).get('pub_year'),
                    'authors': [detailed_pub.get('bib', {}).get('author', '')],
                    'source': 'Google Scholar'
                })
                count += 1
                # Add small delay to avoid blocking
                time.sleep(1)
            except StopIteration:
                break
            except Exception as e:
                print(f"Error fetching Google Scholar result: {e}")
                continue
        
        return papers
    except Exception as e:
        print(f"Error with Google Scholar search: {e}")
        return []

def calculate_relevance(query_embedding, text_embedding):
    """Calculate cosine similarity between query and paper embeddings"""
    similarity = cosine_similarity(
        query_embedding.reshape(1, -1),
        text_embedding.reshape(1, -1)
    )[0][0]
    
    # Convert to percentage for easier understanding
    return round(float(similarity) * 100, 2)

def search_papers(query, num_results=5):
    """Main function to search papers from multiple sources and rank by relevance"""
    # Get papers from multiple sources
    semantic_papers = search_semantic_scholar(query, max_results=num_results)
    arxiv_papers = search_arxiv(query, max_results=num_results)
    
    # Google Scholar tends to block automated requests, so we'll make it optional
    google_papers = []
    try:
        google_papers = search_google_scholar(query, max_results=min(3, num_results))
    except Exception as e:
        print(f"Skipping Google Scholar search: {e}")
        # Continue without Google Scholar results
    
    # Combine all papers
    all_papers = semantic_papers + arxiv_papers + google_papers
    
    # If no papers found, return empty list
    if not all_papers:
        return []
    
    # Get query embedding
    query_embedding = model.encode(query)
    
    # Calculate relevance for each paper
    for paper in all_papers:
        # Create a combined text from title and abstract for better semantic matching
        combined_text = f"{paper['title']} {paper.get('abstract', '')}"
        paper_embedding = model.encode(combined_text)
        paper['relevance'] = calculate_relevance(query_embedding, paper_embedding)
    
    # Sort by relevance
    sorted_papers = sorted(all_papers, key=lambda x: x['relevance'], reverse=True)
    
    # Limit results
    return sorted_papers[:num_results]