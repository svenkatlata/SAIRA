# 🔍 SAIRA - Smart AI Research Assistant
### AI-powered Research Paper Explorer

This project allows users to explore academic research papers by dynamically updating search preferences and querying the OpenAlex API. It supports keyword filtering, author/institution/topic selection, DOI validation, and time-based publication filtering.

### 🤖 [App Link](https://saira-ai.streamlit.app/)

### 🚀 Features

- Search research papers using the [OpenAlex API](https://docs.openalex.org/)
- Search by:
  - Keywords
- Sort by:
  - Relevance scores,
  - Citations,
  - Publication Year,
  - Volumm of Works,
  - Relevance is the default feature
Filter by:
  - Author ID
  - Institution ID
  - Topic ID
  - Work ID
  - DOI
  - Year range (from–to)
  - Open Access status
- Reset the search context on demand
- Save and update preferences to `user_requirements.json`
```json
// Sample JSON schema for User Requirements
{
    "keywords": [
        "nanomaterials",
        "properties",
        "hydrogen",
        "energy",
        "electrical",
        "material",
        "bonding",
        "storage",
        "conductivity"
    ],
    "sort_by": "relevance_score",
    "has_open_access": false,
    "filters": {
        "primary_topic_id": "T10030",
        "author_id": "",
        "institution_id": "",
        "work_id": "",
        "doi": "",
        "from_publication_year": "",
        "to_publication_year": ""
    }
}
```
- Smart validation for IDs and DOIs
- Results are fetched and processed dynamically

### 🛠️ Requirements

- Python 3.12

Install dependencies:

```bash
pip install -r requirements.txt
```

### ⚙️ Usage

1. **Start with a clear research topic** – something that already has active research.
2. **Provide specific links** (e.g., DOI URLs) if you have particular papers or queries in mind.
3. **Mention preferences** like sorting (e.g., by citations, date) or whether you want only open-access papers.
4. SAIRA will suggest **keywords** based on your intent. You can customize them if needed.
5. Once keywords are finalized, SAIRA will list **relevant topics** to choose from.
6. Select a topic, and SAIRA will fetch a curated list of research papers for you.


### 📡 API Reference

- OpenAI Responses API: https://platform.openai.com/
- Model used: 'gpt-4o-mini'

- OpenAlex API: https://api.openalex.org/
- Sample Endpoints:
  - Topics: `/topics/{id}`
  - Works: `/works/{doi}`
  - Authors: `/authors/{id}`
  - Institutions: `/institutions/{id}`

### ✍️ Author

Created by [Lata Venkat] — feel free to reach out for collaboration or feedback!

### 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.









