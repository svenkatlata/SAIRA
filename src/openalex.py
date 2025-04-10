"""API Services"""

import os
import json
import re
from datetime import datetime
import requests
import pandas as pd
from constants import BASE_DIR

data_path = BASE_DIR / "src" / "topics_mapping.csv"
topics_map = pd.read_csv(data_path)


def get_topic_id(topic_name):
    """Fetches the topic ID for a given topic name."""
    topics = (
        topics_map[["topic_id", "topic_name"]]
        .set_index("topic_name")
        .to_dict()["topic_id"]
    )
    return topics[topic_name] if topic_name in topics else False


def fetch_data(api_url, param="results"):
    """Fetches data from a specified endpoint."""
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()[param] if param else response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def get_page_count(api_url):
    """Gets Page Count"""
    metadata = fetch_data(api_url, "meta")
    pages = pages = (metadata["count"] // metadata["per_page"]) + 1
    return pages


# def get_research_papers(keywords, sort_by, has_open_access):
#     """Fetches research papers for a given set of keywords"""
#     print("🔍 Fetching research papers...")

#     keywords_query = format_keywords(keywords)

#     if USER_REQUIREMENTS["topic_id"] == "":
#         group_by = "primary_topic.id"
#         api_url = construct_group_by_api_url(keywords_query, group_by, has_open_access)
#         print(f"🌐 API URL constructed: {api_url}")

#         results = fetch_data(api_url, param="group_by")
#         print("📦 Data fetched from OpenAlex API.")

#         groups = process_groups(results)

#         print("✅ All results processed. Converting to JSON.")
#         response = {
#             "instructions": (
#                 "The provided keywords are too broad to return specific results. "
#                 "Please ask the user to select a topic from the list below. "
#                 "Then, call the update_user_requirements(key, value) function "
#                 "using the string 'primary_topic_id' as the key, "
#                 "and the selected topic's 'topic_id' as the value. "
#                 "Choose the topic that best matches the user's intent. "
#                 "For example, if the selected topic has 'topic_id' == 'T0000', "
#                 "call: update_user_requirements('primary_topic_id', 'T0000')."
#             ),
#             "data": groups,
#         }

#         response_json = json.dumps(response, indent=4)
#         return response_json

#     api_url = construct_sort_by_api_url(keywords_query, sort_by, has_open_access)
#     print(f"🌐 API URL constructed: {api_url}")

#     results = fetch_data(api_url)
#     print("📦 Data fetched from OpenAlex API.")

#     works = process_results(results)

#     print("✅ All results processed. Converting to JSON.")
#     works_json = json.dumps(works, indent=4)
#     return works_json


def get_research_papers(keywords, sort_by, has_open_access):
    """Fetch research papers based on user-defined keywords and filters.
    This function constructs an API query to fetch research papers from OpenAlex
    based on the provided keywords. If no specific topic has been selected in
    USER_REQUIREMENTS dictionary, it recommends a list of relevant topics for user selection.
    Otherwise, it fetches papers sorted and filtered based on user preferences."""
    print("🔍 Fetching research papers...")

    with open("user_requirements.json", "r+", encoding="utf-8") as fs:
        user_requirements = json.load(fs)
        user_requirements["keywords"] = list(
            {keyword.strip(" ,\t\n\r") for keyword in keywords.lower().split()}
        )
        user_requirements["sort_by"] = sort_by
        user_requirements["has_open_access"] = has_open_access
        fs.seek(0)
        json.dump(user_requirements, fs, indent=4, ensure_ascii=False)
        fs.truncate()

    keywords_query = "%20".join(user_requirements["keywords"])
    if user_requirements["filters"]["primary_topic_id"] == "":
        return recommend_relevant_topics(keywords_query, has_open_access)

    primary_topic_id = user_requirements["filters"]["primary_topic_id"]

    api_url = construct_sort_by_api_url(
        keywords_query, primary_topic_id, sort_by, has_open_access
    )
    print(f"🌐 API URL constructed: {api_url}")

    results = fetch_data(api_url)
    print("📦 Data fetched from OpenAlex API.")

    works = process_results(results)

    print("✅ All results processed. Converting to JSON.")
    return json.dumps(works, indent=4)


def recommend_relevant_topics(keywords_query, has_open_access):
    """Suggests relevant topics when the topic_id is not set in USER_REQUIREMENTS."""
    group_by = "primary_topic.id"
    api_url = construct_group_by_api_url(keywords_query, group_by, has_open_access)
    print(f"🌐 API URL constructed: {api_url}")

    results = fetch_data(api_url, param="group_by")
    print("📦 Data fetched from OpenAlex API.")

    groups = process_groups(results)

    print("✅ All results processed. Converting to JSON.")
    response = {
        "instructions": (
            "The provided keywords are too broad to return specific results. "
            "Please ask the user to select a topic from the list below. "
            "Then, call the update_user_requirements(key, value) function "
            "using the string 'primary_topic_id' as the key, "
            "and the selected topic's 'topic_id' as the value. "
            "Choose the topic that best matches the user's intent. "
            "For example, if the selected topic has 'topic_id' == 'T0000', "
            "call: update_user_requirements('primary_topic_id', 'T0000')."
        ),
        "data": groups,
    }

    return json.dumps(response, indent=4)


# def format_keywords(keywords):
#     """Formats the keywords into URL-friendly format"""
#     keywords_list = [keyword.strip() for keyword in keywords.lower().split()]
#     for keyword in keywords_list:
#         if keyword not in USER_REQUIREMENTS["keywords"]:
#             USER_REQUIREMENTS["keywords"].append(keyword)
#     formatted_keywords = "%20".join(keywords_list)
#     return formatted_keywords


def construct_sort_by_api_url(
    keywords_query, primary_topic_id, sort_by, has_open_access
):
    """Constructs the OpenAlex API URL with filters and sort options"""
    api_url = (
        f"https://api.openalex.org/works"
        f"?search={keywords_query}"
        f"&filter=primary_topic.id:{primary_topic_id},is_oa:{has_open_access},has_abstract:true"
        f"&select=id,doi,display_name,authorships,relevance_score,"
        f"publication_year,publication_date,best_oa_location"
        f"&per_page=10"
    )

    if sort_by == "publication_year":
        api_url += "&sort=publication_year:desc"
    elif sort_by == "cited_by_count":
        api_url += "&sort=cited_by_count:desc"
    elif sort_by == "works_count":
        api_url += "&sort=works_count:desc"

    return api_url


def construct_group_by_api_url(keywords_query, group_by, has_open_access):
    """Constructs the OpenAlex API URL with filters and grouping options"""
    api_url = (
        f"https://api.openalex.org/works"
        f"?search={keywords_query}"
        f"&filter=is_oa:{has_open_access},has_abstract:true"
        f"&per_page=10"
        f"&group_by={group_by}"
    )
    return api_url


def process_results(results):
    """Processes API results and extracts relevant paper metadata"""
    works = []
    for idx, res in enumerate(results):
        print(f"📝 Processing result {idx + 1}/{len(results)}")
        work = {
            "id": re.sub(r"https://openalex\.org/", "", res["id"]),
            "doi": res["doi"],
            "name": res["display_name"],
            "relevance_score": res["relevance_score"],
            "publication_year": res["publication_year"],
            "publication_date": res["publication_date"],
        }

        work["authorships"] = extract_authorships(res["authorships"])

        if res["best_oa_location"] and res["best_oa_location"]["is_oa"]:
            work["landing_page_url"] = res["best_oa_location"]["landing_page_url"]
            work["pdf_url"] = res["best_oa_location"]["pdf_url"]

        works.append(work)
    return works


def process_groups(results):
    """Processes API results and extracts relevant grouping metadata"""
    groups = []
    for idx, res in enumerate(results):
        print(f"📝 Processing result {idx + 1}/{len(results)}")
        group = {
            "id": re.sub(r"https://openalex\.org/", "", res["key"]),
            "name": res["key_display_name"],
        }
        groups.append(group)
    return groups


def extract_authorships(authorships_data):
    """Extracts and formats author and affiliation data"""
    authorships = []
    for author in authorships_data:
        authorships.append(
            {
                "author_position": author["author_position"],
                "author": author["author"]["display_name"],
                "institutions": author["raw_affiliation_strings"],
            }
        )
    return authorships


def save_user_requirements(user_requirements, file_stream):
    """Save the updated user requirements to the JSON file."""
    file_stream.seek(0)
    json.dump(user_requirements, file_stream, indent=4, ensure_ascii=False)
    file_stream.truncate()


def update_id_filter(key, value, user_requirements, file_stream):
    """Update OpenAlex ID-based filters such as topic, author, or institution."""
    prefix_map = {
        "T": ("topics", "primary_topic_id"),
        "W": ("works", "work_id"),
        "A": ("authors", "author_id"),
        "I": ("institutions", "institution_id"),
    }

    prefix = value[0].upper()
    if prefix not in prefix_map:
        return None

    endpoint, label = prefix_map[prefix]
    api_url = f"https://api.openalex.org/{endpoint}/{value}"
    results = fetch_data(api_url, param="")

    if (
        results
        and re.sub(r"https://openalex\.org/", "", results.get("id", "")) == value
    ):
        user_requirements["filters"][key] = value
        save_user_requirements(user_requirements, file_stream)
        print(f"✅ {label} updated successfully.")
        return get_research_papers(
            " ".join(user_requirements["keywords"]),
            user_requirements["sort_by"],
            user_requirements["has_open_access"],
        )
    return "❌ Invalid ID or API fetch failed."


def update_doi(value, user_requirements, file_stream):
    """Update DOI value after validating it through the API."""
    if not value.startswith("https://doi.org/"):
        value = f"https://doi.org/{value}"
    api_url = f"https://api.openalex.org/works/{value}"
    results = fetch_data(api_url, param="")

    if results:
        user_requirements["filters"]["doi"] = re.sub(
            r"https://openalex\.org/", "", value
        )
        save_user_requirements(user_requirements, file_stream)
        print("✅ DOI updated successfully.")
        return results
    return "❌ DOI not found or invalid."


def update_year_filter(key, value, user_requirements, file_stream):
    """Validate and update year filters."""
    try:
        year = int(value)
        if 1800 <= year <= datetime.now().year:
            user_requirements["filters"][key] = year
            save_user_requirements(user_requirements, file_stream)
            print(f"✅ {key} updated to {year}.")
            return get_research_papers(
                " ".join(user_requirements["keywords"]),
                user_requirements["sort_by"],
                user_requirements["has_open_access"],
            )
        else:
            return "❌ Year is out of valid range."
    except ValueError:
        return "❌ Invalid year format."


def update_user_requirements(key, value):
    """
    Main function to update user requirements dictionary based on a filter key and value.
    """
    with open("user_requirements.json", "r+", encoding="utf-8") as fs:
        user_requirements = json.load(fs)

        if key not in user_requirements["filters"] and key != "doi":
            return "❌ Invalid key."

        if key == "doi":
            return update_doi(value, user_requirements, fs)

        if key in ["from_publication_year", "to_publication_year"]:
            return update_year_filter(key, value, user_requirements, fs)

        return (
            update_id_filter(key, value, user_requirements, fs) or "❌ Update failed."
        )


def get_topics():
    """Fetch All topics in the Database."""
    filename = "topics_mapping.csv"
    # Check if the file exists and its last modified date
    if os.path.exists(filename):
        last_modified_time = os.path.getmtime(filename)
        last_modified_date = datetime.fromtimestamp(last_modified_time).date()

        # If file was updated today, do not fetch again
        if last_modified_date == datetime.today().date():
            print("Data already fetched today. Skipping API calls.")
            return False  # Indicates no new fetch was done

    topics = []
    pages = get_page_count("https://api.openalex.org/topics")
    for page in range(1, pages + 1):
        print(f"Extracting page {page}")
        api_url = f"https://api.openalex.org/topics?page={page}"
        results = fetch_data(api_url)
        for res in results:
            row = {}
            row["topic_id"] = re.sub(r"https://openalex\.org/", "", res["id"])
            row["topic_name"] = res["display_name"]
            row["subfield_id"] = re.sub(r"https://openalex\.org/", "", res["id"])
            row["subfield_name"] = res["subfield"]["display_name"]
            row["field_id"] = re.sub(r"https://openalex\.org/", "", res["id"])
            row["field_name"] = res["field"]["display_name"]
            row["domain_id"] = re.sub(r"https://openalex\.org/", "", res["id"])
            row["domain_name"] = res["domain"]["display_name"]
            row["keywords"] = " , ".join(res["keywords"])
            row["description"] = res["description"]
            row["siblings"] = " , ".join(
                [sibling["display_name"] for sibling in res["siblings"]]
            )
            topics.append(row)
    topics_df = pd.DataFrame(topics)
    topics_df.to_csv(filename, index=False, encoding="utf-8")

    print("Data successfully saved to topics_mapping.csv")

    return True


# For debugging anf regular update
# print(get_topics())


def get_work_details(work_id):
    """Get details for a specified work_id"""
    api_url = f"https://api.openalex.org/works/{work_id.upper()}"
    result = fetch_data(api_url, param=None)
    work = {}
    work["id"] = re.sub(r"https://openalex\.org/", "", result["id"])
    work["doi"] = result["doi"]
    work["name"] = result["display_name"]
    work["publication_year"] = result["publication_year"]
    work["publication_date"] = result["publication_date"]
    authors = []
    for author in result["authorships"]:
        authors.append(author["author"]["display_name"])
    work["authors"] = " , ".join(authors)
    work["primary_topic_id"] = re.sub(
        r"https://openalex\.org/", "", result["primary_topic"]["id"]
    )
    work["primary_topic_name"] = result["primary_topic"]["display_name"]
    if result["best_oa_location"]:
        if result["best_oa_location"]["is_oa"]:
            work["landing_page_url"] = result["best_oa_location"]["landing_page_url"]
            work["pdf_url"] = result["best_oa_location"]["pdf_url"]
            work["source_type"] = result["source"]["type"]
            work["version"] = result["ver sion"]
    return work


def initialise_requirements_dictionary():
    """Initialises the User Requirements dictionary"""
    return {
        "keywords": [],
        "sort_by": "relevance_score",
        "has_open_access": False,
        "filters": {
            "primary_topic_id": "",
            "author_id": "",
            "institution_id": "",
            "work_id": "",
            "doi": "",
            "from_publication_year": "",
            "to_publication_year": "",
        },
    }


# For debugging and testing
# print(get_work_details("W4320920036"))
