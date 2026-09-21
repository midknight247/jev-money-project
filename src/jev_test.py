import os

from typesafe_sdk import Choice, Score, TypeSafeClient


api_key = os.getenv("TYPESAFE_API_KEY")

if not api_key:
    raise RuntimeError("TYPESAFE_API_KEY is not set")


message = "The website is completely down for me."


with TypeSafeClient(api_key=api_key) as client:
    response = client.system_one(
        state=message,
        questions={
            "urgency": Score(
                instructions="How urgent is this customer support message?",
                criteria=[
                    "Very low urgency. The issue is informational or can wait.",
                    "Low urgency. The customer has a minor issue with no immediate impact.",
                    "Moderate urgency. The customer is experiencing a meaningful problem.",
                    "High urgency. The problem is significantly affecting the customer.",
                    "Critical urgency. The problem is severe, immediate, or blocking important work.",
                ],
            ), 
        },
    )


urgency_answer = response.answers["urgency"]

print("Score:", urgency_answer.score)
print("Legend:", urgency_answer.legend)
print("Confidence:", urgency_answer.confidence)
print("Probabilities:", urgency_answer.probabilities)