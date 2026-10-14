
from app.state import TravelState
from app.llm import llm
from app.schemas.research_plan import ResearchPlan
from app.prompts.planner_prompt import prompt


def planner(state: TravelState) -> dict:
    """Generate research tasks from the user's trip requirements."""

    trip_details = f"""
    Departure: {state['origin']}
    Destination: {state['destination']}
    Start date: {state['start_date']}
    End date: {state['end_date']}
    Total budget: ₹{state['budget']}
    Number of travelers: {state['travelers']}
    Interests: {', '.join(state['interests'])}
Research transport options specifically from the departure city
to the destination and back. Do not assume a different origin.
    """

    structured_llm = llm.with_structured_output(ResearchPlan)

    research_plan = structured_llm.invoke([
        ("system", prompt),
        ("human", trip_details),
    ])

    return {"research_plan": research_plan.model_dump()}
