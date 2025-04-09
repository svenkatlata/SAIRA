"""Chat Services"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from openalex import get_research_papers, update_user_requirements
from constants import SAIRA_DEVELOPER_MESSAGE, TOOLS

load_dotenv()

# Set your OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)


def initialise_converstation():
    """Generates the Instructions to initiate the conversation."""
    print("🟢 Initialising conversation...")
    messages = [{"role": "system", "content": SAIRA_DEVELOPER_MESSAGE}]
    return messages


# def get_chat_responses(messages):
#     """Get Chat Responses from OpenAI"""
#     print("🟢 Starting chat response process...")

#     response = openai_client.responses.create(
#         model="gpt-4o-mini", input=messages, tools=TOOLS, temperature=0.5, store=True
#     )
#     print("🤖 Initial response from OpenAI model received.")

#     if response.output[0].type == "function_call":
#         print("📡 Detected function call in model response.")
#         tool_call = response.output[0]
#         args = json.loads(tool_call.arguments)
#         print(f"📦 Function arguments extracted: {args}")

#         if tool_call.name == "get_research_works":
#             print(f"⚙️ Calling function: {tool_call.name}")
#             works = get_research_papers(
#                 args["keywords"],
#                 args["sort_by"],
#                 args["has_open_access"],
#             )
#             print("📄 Function call completed. Appending messages.")

#             messages.append(
#                 {
#                     "type": "function_call",
#                     "call_id": tool_call.call_id,
#                     "name": tool_call.name,
#                     "arguments": tool_call.arguments,
#                 }
#             )

#             messages.append(
#                 {
#                     "type": "function_call_output",
#                     "call_id": tool_call.call_id,
#                     "output": str(works),
#                 }
#             )

#             print("🔁 Sending updated messages back to OpenAI.")
#             response = openai_client.responses.create(
#                 model="gpt-4o-mini",
#                 input=messages,
#                 tools=TOOLS,
#                 temperature=0.5,
#                 store=True,
#             )
#             print("✅ Updated response appended to messages.")
#             messages.append({"role": "assistant", "content": response.output_text})
#             return messages

#         messages.append(
#             {
#                 "role": "system",
#                 "content": (
#                     "❌ Invalid request: The specified function name was not found."
#                     "Please verify the function name and try again."
#                 ),
#             }
#         )
#         print("✅ Updated response appended to messages.")
#         messages.append({"role": "assistant", "content": response.output_text})
#         return messages

#     print("✅ Response appended to messages.")
#     messages.append({"role": "assistant", "content": response.output_text})
#     return messages


def get_chat_responses(messages):
    """Get Chat Responses from OpenAI"""
    print("🟢 Starting chat response process...")
    response = openai_client.responses.create(
        model="gpt-4o", input=messages, tools=TOOLS, temperature=0.5, store=True
    )
    print("🤖 Response from OpenAI model received.")

    if response.output[0].type == "function_call":
        return handle_function_call(response.output[0], messages)

    print("✅ Response appended to messages.")
    messages.append({"role": "assistant", "content": response.output_text})
    return messages


def handle_function_call(tool_call, messages):
    """Handles tool/function calls received from OpenAI model"""
    print("📡 Detected function call in model response.")
    args = json.loads(tool_call.arguments)
    print(f"📦 Function arguments extracted: {args}")

    handler_map = {
        "get_research_works": handle_get_research_works,
        "update_user_requirements": handle_update_user_requirements,
        # Add more function handlers here as needed
    }

    if tool_call.name in handler_map:
        return handler_map[tool_call.name](tool_call, args, messages)

    print("❌ No handler found for the requested function.")
    messages.append(
        {
            "role": "system",
            "content": (
                "❌ Invalid request: The specified function name was not found. "
                "Please verify the function name and try again."
            ),
        }
    )
    return messages


def handle_get_research_works(tool_call, args, messages):
    """Handles the get_research_works function call"""
    print(f"⚙️ Calling function: {tool_call.name}")
    works = get_research_papers(
        args["keywords"],
        args["sort_by"],
        args["has_open_access"],
    )
    print("📄 Function call completed. Appending messages.")

    messages.append(
        {
            "type": "function_call",
            "call_id": tool_call.call_id,
            "name": tool_call.name,
            "arguments": tool_call.arguments,
        }
    )

    messages.append(
        {
            "type": "function_call_output",
            "call_id": tool_call.call_id,
            "output": str(works),
        }
    )

    print("🔁 Sending updated messages back to OpenAI.")
    response = openai_client.responses.create(
        model="gpt-4o",
        input=messages,
        tools=TOOLS,
        temperature=0.5,
        store=True,
    )

    print("✅ Updated response appended to messages.")
    messages.append({"role": "assistant", "content": response.output_text})
    return messages


def handle_update_user_requirements(tool_call, args, messages):
    """Handles the get_research_works function call"""
    print(f"⚙️ Calling function: {tool_call.name}")
    update_response = update_user_requirements(
        args["key"],
        args["value"],
    )
    print("📄 Function call completed. Appending messages.")

    messages.append(
        {
            "type": "function_call",
            "call_id": tool_call.call_id,
            "name": tool_call.name,
            "arguments": tool_call.arguments,
        }
    )

    messages.append(
        {
            "type": "function_call_output",
            "call_id": tool_call.call_id,
            "output": str(update_response),
        }
    )

    print("🔁 Sending updated messages back to OpenAI.")
    response = openai_client.responses.create(
        model="gpt-4o",
        input=messages,
        tools=TOOLS,
        temperature=0.5,
        store=True,
    )

    print("✅ Updated response appended to messages.")
    messages.append({"role": "assistant", "content": response.output_text})
    return messages
