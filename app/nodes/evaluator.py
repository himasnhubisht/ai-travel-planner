
from app.state import TravelState
from app.llm import llm
from app.schemas.evaluation import EvaluationResult


def evaluator(state: TravelState) -> dict:
    structured_llm = llm.with_structured_output(EvaluationResult)

    result = structured_llm.invoke([
        (
            "system",
            """
            You are a strict travel itinerary evaluator.

            Check:
            1. The itinerary covers the requested dates.
            2. Transport, accommodation, and activities are addressed.
            3. The estimated total cost is compared with the budget.
            4. Missing information and unverified prices are disclosed.
            5. Activities reflect the traveler's interests.
            
            Verify that the itinerary uses the supplied departure city for
            outbound and return transport.

            Reject the itinerary if it assumes a different departure city
            or presents transport costs based on an unconfirmed origin.

            If transport prices are estimates, ensure they are clearly
            labelled as estimates.

            Provide specific corrective feedback when these requirements
            are not met.
            Approve only if the itinerary is sufficiently complete
            and no obvious budget or planning issue remains.
            Give actionable feedback when it fails.
            Never treat estimated prices as confirmed prices.
            """
        ),
        (
            "human",
            f"""
            Departure city: {state['origin']}
            Destination: {state['destination']}
            Dates: {state['start_date']} to {state['end_date']}
            Budget: ₹{state['budget']}
            Travelers: {state['travelers']}
            Interests: {state['interests']}

            Itinerary:
            {state['itinerary']}
            """
        )
    ])

    return {
        "approved": result.approved,
        "evaluation_feedback": result.feedback,
    }
