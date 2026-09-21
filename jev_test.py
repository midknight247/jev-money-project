import os

from typesafe_sdk import Score, TypeSafeClient


api_key = os.getenv("TYPESAFE_API_KEY")

if not api_key:
    raise RuntimeError("TYPESAFE_API_KEY is not set")


messages = [
    "The application won't open at all.",
    "Nothing loads when I try to access the dashboard.",
    "The entire service is unavailable right now.",
    "File uploads stopped working after yesterday's update.",
    "I can't sign into my account anymore.",
    "The app freezes every time I try to save a document.",
    "The website is down and I have an urgent client presentation.",
    "Where can I read about your features?",
]


with TypeSafeClient(api_key=api_key) as client:

    for message in messages:

        response = client.system_one(
            state=message,
            questions={
                "urgency": Score(
                    instructions=(
                        "Assess the urgency of this customer support "
                        "message. Focus on how immediately the customer "
                        "needs the issue addressed, not merely how broken "
                        "or technically severe the issue is."
                    ),
                    criteria=[
                        (
                            "Very low urgency. "
                            "The message is informational or the customer "
                            "can comfortably wait."
                        ),
                        (
                            "Low urgency. "
                            "There is a minor issue or inconvenience, with "
                            "no stated immediate consequence or time pressure."
                        ),
                        (
                            "Moderate urgency. "
                            "The customer has a meaningful problem that "
                            "affects their use of the service, but there is "
                            "no clear immediate deadline, severe consequence, "
                            "or urgent time pressure."
                        ),
                        (
                            "High urgency. "
                            "The problem significantly prevents the customer "
                            "from working or using an important service "
                            "function, especially when prompt resolution "
                            "would materially reduce the impact."
                        ),
                        (
                            "Critical urgency. "
                            "There is an immediate and severe consequence, "
                            "explicit urgent time pressure, or a broad outage "
                            "that requires immediate attention."
                        ),
                    ],
                )
            },
        )

        answer = response.answers["urgency"]

        urgency = answer.score + 1

        print()
        print("Message:", message)
        print("Urgency:", round(urgency, 2))