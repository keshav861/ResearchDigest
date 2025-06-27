from flask import Blueprint, render_template, request, jsonify
from app.services.paper_search import search_papers
from app.services.summarizer import generate_summary

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query', '')
    num_results = data.get('num_results', 5)
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    try:
        papers = search_papers(query, num_results)
        
        # Generate summaries for each paper
        for paper in papers:
            if paper.get('abstract'):
                paper['summary'] = generate_summary(paper['title'], paper['abstract'])
            else:
                paper['summary'] = "No abstract available for summarization."
                
        return jsonify({'papers': papers})
    except Exception as e:
        return jsonify({'error': str(e)}), 500