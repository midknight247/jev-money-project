const API_URL = "https://jev-money-project.onrender.com/analyze";

const messageInput = document.getElementById("message");
const analyzeButton = document.getElementById("analyzeButton");

const resultSection = document.getElementById("result");
const errorMessage = document.getElementById("error");

const categoryElement = document.getElementById("category");
const urgencyElement = document.getElementById("urgency");
const escalationElement = document.getElementById("escalation");

const actionBadge = document.getElementById("actionBadge");

const urgencyBar = document.getElementById("urgencyBar");
const escalationBar = document.getElementById("escalationBar");

const historySection = document.getElementById("historySection");
const historyList = document.getElementById("historyList");
const clearHistoryButton = document.getElementById("clearHistoryButton");

const history = [];


function hideError() {
    errorMessage.classList.add("hidden");
    errorMessage.textContent = "";
}


function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove("hidden");
}


function showResult(data) {
    categoryElement.textContent = data.category;

    urgencyElement.textContent =
        `${Number(data.urgency).toFixed(2)} / 5`;

    escalationElement.textContent =
        `${Math.round(data.escalation_probability * 100)}%`;

    actionBadge.textContent = data.action;

    /*
     * Urgency is on a 0-5 scale.
     * Convert it to a percentage for the progress bar.
     */
    const urgencyPercentage =
        Math.min(Math.max(data.urgency / 5, 0), 1) * 100;

    /*
     * Escalation probability is already between 0 and 1.
     */
    const escalationPercentage =
        Math.min(
            Math.max(data.escalation_probability, 0),
            1
        ) * 100;

    urgencyBar.style.width =
        `${urgencyPercentage}%`;

    escalationBar.style.width =
        `${escalationPercentage}%`;

    resultSection.classList.remove("hidden");
}


function renderHistory() {

    historyList.innerHTML = "";

    if (history.length === 0) {
        historySection.classList.add("hidden");
        return;
    }

    historySection.classList.remove("hidden");

    /*
     * Show the newest analysis first.
     */
    const reversedHistory = [...history].reverse();

    reversedHistory.forEach((item) => {

        const historyItem =
            document.createElement("div");

        historyItem.className = "history-item";


        const messageElement =
            document.createElement("p");

        messageElement.className =
            "history-message";

        messageElement.textContent =
            item.message;


        const detailsElement =
            document.createElement("div");

        detailsElement.className =
            "history-details";


        const categoryElement =
            document.createElement("span");

        categoryElement.textContent =
            item.result.category;


        const urgencyElement =
            document.createElement("span");

        urgencyElement.textContent =
            `Urgency ${Number(
                item.result.urgency
            ).toFixed(2)}`;


        const escalationElement =
            document.createElement("span");

        escalationElement.textContent =
            `Escalation ${Math.round(
                item.result.escalation_probability * 100
            )}%`;


        const actionElement =
            document.createElement("span");

        actionElement.textContent =
            item.result.action;


        detailsElement.appendChild(
            categoryElement
        );

        detailsElement.appendChild(
            urgencyElement
        );

        detailsElement.appendChild(
            escalationElement
        );

        detailsElement.appendChild(
            actionElement
        );


        historyItem.appendChild(
            messageElement
        );

        historyItem.appendChild(
            detailsElement
        );


        historyList.appendChild(
            historyItem
        );
    });
}


async function analyzeMessage() {

    const message =
        messageInput.value.trim();

    hideError();


    if (!message) {

        showError(
            "Please enter a customer message."
        );

        messageInput.focus();

        return;
    }


    analyzeButton.disabled = true;
    analyzeButton.textContent = "Analyzing...";


    try {

        const response =
            await fetch(
                API_URL,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    })
                }
            );


        if (!response.ok) {

            throw new Error(
                `API request failed with status ${response.status}.`
            );
        }


        const data =
            await response.json();


        history.push({
            message: message,
            result: data
        });


        showResult(data);

        renderHistory();


        /*
         * Clear the input after a successful analysis
         * so the user can immediately enter another message.
         */
        messageInput.value = "";


    } catch (error) {

        console.error(error);

        showError(
            "Could not connect to the JEV backend. " +
            "Make sure the FastAPI server is running."
        );


    } finally {

        analyzeButton.disabled = false;
        analyzeButton.textContent =
            "Analyze Message";
    }
}


function clearHistory() {

    history.length = 0;

    renderHistory();
}


analyzeButton.addEventListener(
    "click",
    analyzeMessage
);


clearHistoryButton.addEventListener(
    "click",
    clearHistory
);


messageInput.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "Enter" &&
            (event.ctrlKey || event.metaKey)
        ) {

            analyzeMessage();
        }
    }
);
