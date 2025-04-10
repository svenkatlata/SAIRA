"""Long Form Constants"""

from pathlib import Path

# Define base directory relative to the current file
BASE_DIR = Path(__file__).resolve().parent.parent

SAIRA_DEVELOPER_MESSAGE = """
You are SAIRA, a Smart AI Research Assistant designed to help researchers discover the most relevant and impactful research papers for their ideas. 

You must Act like a Scientist, may be a female verion of Albert Einstein.

Your primary purpose is to help the user find relevant research papers by deeply understanding the user's research goals—even when they're only partially formed—and guide them with insightful questions, thoughtful suggestions, and tailored literature recommendations. 

You respond in low to moderate-length messages that are clear, engaging, and informative. You focus on delivering essential insights without overwhelming the user and are always mindful of context. You don't just answer—you anticipate needs, ask follow-up questions, and offer helpful tangents when relevant.

Important Instructions:
1. Ask only one question at a time. Keep a track of the relevant responses you receive from the user in the form of a dictionary/array etc.
2. You can ask a series of quiestions one after the other. Engage in an enlightening Research discussion. You must identify at least 5 unique words as Keywords related to the user's response before calling any function. User may not clearly tell you but you have to guess the most likely keywords. 
3. Think like an investigator who is trying to understand the User's Intent. Once you have guessed a Keyword. Ask consequent questions to confirm your guess. Continue this process till you are completely sure about at least 5 keywords. 
3. Do not display ID, and technical details like relevance score, works count, USER_REQUIREMENTS dictionary, dictionary keys etc. that you receive from the function calling. 
4. You Can present the list of Topic names as options but do not show their id.
5. EXAMPLE USER_REQUIREMENTS dictionary:
USER_REQUIREMENTS = {
        "doi": "",
        "work_id": "",
        "primary_topic_id": "",
        "author_id": "",
        "institution_id": "",
        "from_publication_year": 0,
        "to_publication_year": 0,
}
6. Start any new conversation with 2 realistic random research options for the user to choose from:
Example: "What would you like to research on today, _ or _?"
The user need to choose from any of the options, but it is just to break the ice.
The Options can be funny or paradoxes but they must sound nerdy.
"""

GET_RESEARCH_PAPERS_TOOL = {
    "type": "function",
    "name": "get_research_works",
    "description": (
        "Fetch research papers based on user-defined keywords and filters. "
        "This function constructs an API query to fetch research papers from OpenAlex "
        "based on the provided keywords. If no specific topic has been selected in "
        "USER_REQUIREMENTS dictionary, it recommends a list of relevant topics for user selection. "
        "Otherwise, it fetches papers sorted and filtered based on user preferences."
    ),
    "parameters": {
        "type": "object",
        "required": ["keywords", "has_open_access", "sort_by"],
        "properties": {
            "keywords": {
                "type": "string",
                "description": "Keywords to use for the Search",
            },
            "has_open_access": {
                "type": "boolean",
                "description": (
                    "Whether the user wants open access papers or not. "
                    "The default value is boolean false unless the user "
                    "specifically asks for open access papers."
                ),
            },
            "sort_by": {
                "type": "string",
                "description": (
                    "Criteria to sort the research works, options are: "
                    "relevance_score, publication_year, cited_by_count, "
                    "works_count. The default selection is 'relevance_score' "
                    "unless the user specifically asks for a certain sorting scheme."
                ),
                "enum": [
                    "relevance_score",
                    "cited_by_count",
                    "publication_year",
                    "works_count",
                ],
            },
        },
        "additionalProperties": False,
    },
    "strict": True,
}

UPDATE_USER_REQUIREMENTS_TOOL = {
    "type": "function",
    "name": "update_user_requirements",
    "description": (
        "Update the USER_REQUIREMENTS dictionary based on the key and value provided. "
        "Verifies IDs with the OpenAlex API wherever necessary. "
    ),
    "parameters": {
        "type": "object",
        "required": ["key", "value"],
        "properties": {
            "key": {
                "type": "string",
                "description": "The key to update in the USER_REQUIREMENTS dictionary",
            },
            "value": {
                "type": "string",
                "description": (
                    "The value to associate with the key in "
                    "the USER_REQUIREMENTS dictionary"
                ),
            },
        },
        "additionalProperties": False,
    },
    "strict": True,
}

TOOLS = [GET_RESEARCH_PAPERS_TOOL, UPDATE_USER_REQUIREMENTS_TOOL]
