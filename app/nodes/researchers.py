
from app.state import TravelState
from app.llm import llm
from app.tools.web_search import web_search
from langchain.agents import create_agent


accommodation_agent = create_agent(
    model=llm,
    tools=[web_search],
    system_prompt="""
    You are an accommodation research agent for a travel planner.
    Research suitable hotels, hostels, and homestays for the trip.
    Consider dates, number of travelers, destination, and budget.
    Use web_search when research is requested.
    Include source URLs and clearly label estimated prices.
    Never invent availability or claim a price is verified unless
    the source supports it. State when information is unavailable.
    """
)


activities_agent = create_agent(
    model=llm,
    tools=[web_search],
    system_prompt="""
    You are an activities research agent for a travel planner.
    Research attractions and activities suited to the destination,
    travel dates, trip duration, and user's interests.
    Use web_search when research is requested.
    Include source URLs, estimated costs when available, and
    practical details. Never invent prices, opening hours, or
    availability. State when information is unavailable.
    """
)


def accommodation_researcher(state: TravelState) -> dict:
    tasks = state["research_plan"]["accommodation_tasks"]
    task_text = "\n".join(f"- {task}" for task in tasks)

    request = f"""
    Destination: {state['destination']}
    Dates: {state['start_date']} to {state['end_date']}
    Travelers: {state['travelers']}
    Total trip budget: ₹{state['budget']}

    Research tasks:
    {task_text}
    """

    response = accommodation_agent.invoke({
        "messages": [{"role": "user", "content": request}]
    })

    return {
        "accommodation_info": [{
            "summary": response["messages"][-1].content
        }]
    }


def activities_researcher(state: TravelState) -> dict:
    tasks = state["research_plan"]["activities_tasks"]
    task_text = "\n".join(f"- {task}" for task in tasks)

    request = f"""
    Destination: {state['destination']}
    Dates: {state['start_date']} to {state['end_date']}
    Travelers: {state['travelers']}
    Interests: {', '.join(state['interests'])}
    Total trip budget: ₹{state['budget']}

    Research tasks:
    {task_text}
    """

    response = activities_agent.invoke({
        "messages": [{"role": "user", "content": request}]
    })

    return {
        "activities_info": [{
            "summary": response["messages"][-1].content
        }]
    }
