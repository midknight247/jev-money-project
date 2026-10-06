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

    const urgencyPercentage =
        Math.min(Math.max(data.urgency / 5, 0), 1) * 100;

    const escalationPercentage =
        Math.min(Math.max(data.escalation_probability, 0), 1) * 100;

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

    history
        .slice()
        .reverse()
        .forEach((item) => {
            const card = document.createElement("article");

            card.className = "history-card";

            const message = document.createElement("p");
            message.className = "history-message";
            message.textContent = item.message;

            const meta = document.createElement("div");
            meta.className = "history-meta";

            const details = document.createElement("div");
            details.className = "history-details";

            const category = document.createElement("span");
            category.className = "history-category";
            category.textContent = item.result.category;

            const urgency = document.createElement("span");
            urgency.className = "history-stat";

            const urgencyValue = document.createElement("strong");
            urgencyValue.textContent =
                `${Number(item.result.urgency).toFixed(2)} / 5`;

            urgency.textContent = "Urgency ";
            urgency.appendChild(urgencyValue);

            const escalation = document.createElement("span");
            escalation.className = "history-stat";

            const escalationValue = document.createElement("strong");
            escalationValue.textContent =
                `${Math.round(item.result.escalation_probability * 100)}%`;

            escalation.textContent = "Escalation ";
            escalation.appendChild(escalationValue);

            details.appendChild(category);
            details.appendChild(urgency);
            details.appendChild(escalation);

            const action = document.createElement("span");

            action.className =
                "history-action " +
                (
                    item.result.action === "ESCALATE"
                        ? "escalate"
                        : "normal"
                );

            action.textContent = item.result.action;

            meta.appendChild(details);
            meta.appendChild(action);

            card.appendChild(message);
            card.appendChild(meta);

            historyList.appendChild(card);
        });
}


async function analyzeMessage() {
    const message = messageInput.value.trim();

    hideError();

    if (!message) {
        showError("Please enter a customer message.");
        messageInput.focus();
        return;
    }

    analyzeButton.disabled = true;
    analyzeButton.textContent = "Analyzing...";

    try {
        const response = await fetch(API_URL, {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });

        if (!response.ok) {
            throw new Error(
                `API request failed with status ${response.status}.`
            );
        }

        const data = await response.json();

        history.push({
            message: message,
            result: data
        });

        showResult(data);
        renderHistory();

    } catch (error) {
        console.error(error);

        showError(
            "Could not connect to the JEV backend. " +
            "Make sure the FastAPI server is running."
        );

    } finally {
        analyzeButton.disabled = false;
        analyzeButton.textContent = "Analyze Message";
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