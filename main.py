import json

from dotenv import load_dotenv
import os
from getpass import getpass

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_community.tools import JinaSearch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, MessagesState, START, END

from map import geocode_address, GeocodeInput

# --- Load environment variables ---
load_dotenv()
if not os.environ.get("JINA_API_KEY"):
    os.environ["JINA_API_KEY"] = getpass("Enter your Jina API key: ")
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass("Enter your OpenAI API key: ")

# --- Initialize model and tool ---
model = ChatOpenAI(model="gpt-4o", temperature=0.7)
nano_model = ChatOpenAI(model="gpt-5-nano", temperature=0.5)
jina_tool = JinaSearch()

# Bind tools to the model (so the LLM can call them when needed)
model_with_tools = model.bind_tools([jina_tool, geocode_address])

# --- Define workflow graph ---
workflow = StateGraph(state_schema=MessagesState)


def call_model(state: MessagesState):
    system_prompt = (
        "You are a tourism assistant. Help the user plan their journey, "
        "and when needed, use Jina Search to find up-to-date travel info."
    )
    messages = [SystemMessage(content=system_prompt)] + state["messages"]

    # First call
    try:
        response = model_with_tools.invoke(messages)
    except:
        # just use last two history
        messages = [SystemMessage(content=system_prompt)] + state["messages"][-2:]
        response = model_with_tools.invoke(messages)

    # If the model requested a tool
    if hasattr(response, "tool_calls") and response.tool_calls:
        tool_outputs = []
        for tool_call in response.tool_calls:
            try:
                if tool_call["name"] == "jina_search":
                    query = tool_call["args"]["query"]
                    result = jina_tool.invoke(query)
                    result_dict = json.loads(result)
                    summaries = []
                    print("Search Results number:", len(result_dict))
                    for r in result_dict:
                        print("title: ", r['title'])
                        print("link: ", r['link'])
                        print("**" * 20)
                        summary_prompt = f"Summarize this search result in under 5 bullet points:\n\n{r['content']}"
                        summary = nano_model.invoke([HumanMessage(content=summary_prompt)])
                        summaries.append(summary.content)
                    tool_outputs.append(
                        ToolMessage(content="\n".join(summaries), tool_call_id=tool_call["id"])
                    )
                elif tool_call["name"] == "geocode_address":
                    address = tool_call["args"]["input"]["address"]
                    result = geocode_address(GeocodeInput(address=address))
                    tool_outputs.append(
                        ToolMessage(content=result.url, tool_call_id=tool_call["id"])
                    )
            except:
                tool_outputs.append(
                    ToolMessage(content="", tool_call_id=tool_call["id"])
                )
                continue
        # Call the model again with tool results
        response = model_with_tools.invoke(messages + [response] + tool_outputs)

    return {"messages": response}


workflow.add_node("chatbot", call_model)
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)

# --- Memory for persistence ---
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# --- Run interactive CLI chatbot ---
config = {"configurable": {"thread_id": "user-123"}}

print("🤖 Tourism Chatbot with Jina Search ready! Type 'exit' to quit.\n")
while True:
    try:
        user_input = input("You: ")
        if user_input.strip().lower() in {"exit", "quit"}:
            print("👋 Goodbye!")
            break

        response = app.invoke({"messages": [HumanMessage(content=user_input)]}, config)
        bot_reply = response["messages"][-1].content
        print("Bot:")
        print(bot_reply)
    except Exception as e:
        raise e
