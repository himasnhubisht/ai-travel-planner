
from app.state import TravelState
from app.llm import llm


def synthesizer(state: TravelState) -> dict:
    research = f"""
    TRANSPORT:
    {state['transport_info']}

    ACCOMMODATION:
    {state['accommodation_info']}

    ACTIVITIES:
    {state['activities_info']}
    """

 
    prompt = f"""
    You are an expert AI travel planner. Create a practical,
    realistic itinerary using the provided trip details and research.

    TRIP DETAILS:
    Departure city: {state['origin']}
    Destination: {state['destination']}
    Dates: {state['start_date']} to {state['end_date']}
    Travelers: {state['travelers']}
    Total budget: ₹{state['budget']}
    Interests: {', '.join(state['interests'])}

    REQUIREMENTS:
    - Organize the itinerary day by day.
    - Include transport, accommodation, and activities.
    - Provide a budget breakdown for transport, accommodation,
    food, activities, and other relevant expenses.
    - Distinguish per-person costs from total costs for all travelers.
    - Calculate the estimated total and compare it with the budget.
    - Never invent prices, availability, schedules, or source details.
    - Clearly label estimates and identify missing information.
    - If the budget is insufficient, explain the shortfall and suggest
    practical alternatives.
    - Avoid scheduling activities outside the requested travel dates.
    - Return a clear, readable itinerary in Markdown, not JSON.

    PREVIOUS ITINERARY:
    {state['itinerary']}

    EVALUATION FEEDBACK:
    {state['evaluation_feedback']}

    REVISION INSTRUCTIONS:
    If previous evaluation feedback exists, address every actionable
    issue it identifies. Improve the previous itinerary rather than
    ignoring the feedback. Retain useful findings and recommendations.
    If there is no previous itinerary, create the initial itinerary
    from scratch.

    RESEARCH FINDINGS:
    {research}

    Use the supplied departure city for all transport planning.
Never assume a different origin. If transport prices cannot be
verified, label them as estimates or unavailable.
"""


    response = llm.invoke(prompt)

    return {
        "itinerary": {
            "content": response.content
        }
    }
