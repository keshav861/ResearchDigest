# ResearchDigest 📚

A powerful web application for intelligent research paper discovery and summarization. ResearchDigest helps researchers and academics efficiently search, retrieve, and understand research papers using advanced semantic search and AI-powered summarization.

![GitHub](https://img.shields.io/github/license/keshav861/ResearchDigest)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)

## 🌟 Key Features

- **Smart Search**: Find relevant research papers using natural language queries or keywords
- **Multi-Source Integration**: Access papers from:
  - Semantic Scholar
  - arXiv
  - Google Scholar
- **AI-Powered Summarization**: Generate concise summaries using Google's Gemini API
- **Semantic Ranking**: Papers ranked by relevance using advanced semantic similarity
- **User-Friendly Interface**: Clean, responsive design with Bootstrap

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Google Gemini API key

### Installation

1. Clone the repository
```bash
git clone https://github.com/keshav861/ResearchDigest.git
cd ResearchDigest
```

2. Install required dependencies
```bash
pip install -r requirements.txt
```

3. Configure environment variables
```bash
# Create .env file and add your Gemini API key
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
```

> 📝 Get your free Gemini API key from [Google AI Studio](https://ai.google.dev/)

### Usage

1. Start the application
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`

3. Enter your research query and configure search parameters

4. Review and explore the semantically ranked results with AI-generated summaries

## 🛠️ Technology Stack

### Backend
- **Python**: Core programming language
- **Flask**: Web framework
- **Sentence Transformers**: Semantic search using all-MiniLM-L6-v2 model

### APIs
- Semantic Scholar API
- arXiv API
- Google Scholar (via scholarly)
- Google Gemini API (summarization)

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap

## 📋 Project Structure

```
ResearchDigest/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── static/            # Static assets (CSS, JS)
├── templates/         # HTML templates
└── .env              # Environment variables
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ Important Notes

- Google Scholar searches may be rate-limited
- Use specific, focused queries for best results
- Summary quality depends on:
  - Gemini API model
  - Paper abstract quality
  - Input query specificity

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google AI for the Gemini API
- Semantic Scholar for their comprehensive API
- arXiv for providing access to research papers
- The open-source community for various tools and libraries

## 📞 Contact

For questions, suggestions, or collaboration opportunities:

- Create an [issue](https://github.com/keshav861/ResearchDigest/issues)
- Email: [your-email@example.com]

---

⭐ If you find this project useful, please consider giving it a star!
