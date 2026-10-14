
from langchain.agents import create_agent

from app.llm import llm
from app.tools.web_search import web_search
from app.state import TravelState

transport_agent = create_agent(
    model=llm,
    tools=[web_search],
    system_prompt="""
    You are the transport research agent in an AI travel planner.

    Your job is to research transport options based on the user's
    destination, travel dates, number of travelers, and budget.

    Use the web_search tool to find relevant information.

    Research:
    1. Available transport modes.
    2. Estimated prices and total cost for all travelers.
    3. Journey duration and departure information when available.
    4. Relevant source URLs.

    Instructions:
    - Prefer information relevant to the specified travel dates.
    - Compare suitable transport options when possible.
    - Never invent prices, schedules, or availability.
    - Clearly label estimates and distinguish them from verified facts.
    - If information cannot be found, say so explicitly.
    - Finish with a concise comparison of the best options.
    """
)

from app.state import TravelState


def transport_researcher(state: TravelState) -> dict:
    """LangGraph node that runs the transport research agent."""

    research_plan = state["research_plan"]
    tasks = state["research_plan"]["transport_tasks"]

    task_text = "\n".join(f"- {task}" for task in tasks)

    user_request = f"""
    Research transport for this trip.
    Departure city: {state['origin']}
    Destination: {state['destination']}
    Start date: {state['start_date']}
    End date: {state['end_date']}
    Budget: ₹{state['budget']}
    Travelers: {state['travelers']}
    Interests: {', '.join(state['interests'])}

    Follow these research tasks:
    {task_text}

    Return a concise comparison of suitable transport options,
    estimated costs, journey duration, and source URLs.
    Clearly identify estimates and information that could not
    be verified.
    Research outbound transport from the departure city to the
    destination and return transport to the departure city.
    Never substitute another starting city.
    """

    response = transport_agent.invoke({
        "messages": [{"role": "user", "content": user_request}]
    })

    final_answer = response["messages"][-1].content

    return {
        "transport_info": [
            {"summary": final_answer}
        ]
    }
