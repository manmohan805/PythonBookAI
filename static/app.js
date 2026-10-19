// ========================================
// PythonBookAI - Frontend JavaScript
// ========================================

const questionForm = document.getElementById("question-form");
const questionInput = document.getElementById("question-input");
const sendButton = document.getElementById("send-button");
const bookSelect = document.getElementById("book-select");
const chatContainer = document.getElementById("chat-container");
const welcomeScreen = document.getElementById("welcome-screen");
const newChatButton = document.getElementById("new-chat-button");


// ========================================
// 1. Show or Hide Welcome Screen
// ========================================

function showChat() {
    welcomeScreen.style.display = "none";
    chatContainer.classList.add("active");
}

function showWelcome() {
    welcomeScreen.style.display = "";
    chatContainer.classList.remove("active");
}


// ========================================
// 2. Create a Chat Message
// ========================================

function createMessage(role, text) {
    const message = document.createElement("div");

    message.className = `message ${role}-message`;

    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.textContent = role === "user" ? "👤" : "🐍";

    const content = document.createElement("div");
    content.className = "message-content";

    const label = document.createElement("div");
    label.className = "message-label";
    label.textContent = role === "user" ? "You" : "PythonBookAI";

    const messageText = document.createElement("div");
messageText.className = "message-text";

if (role === "assistant" && window.marked && window.DOMPurify) {
    const cleanedText = text.replace(/\\([#*_`~])/g, "$1");

    messageText.innerHTML = DOMPurify.sanitize(
        marked.parse(cleanedText)
    );
} else {
    messageText.textContent = text;
}

    content.appendChild(label);
    content.appendChild(messageText);

    message.appendChild(avatar);
    message.appendChild(content);

    chatContainer.appendChild(message);

    return {
        message,
        content,
        messageText
    };
}


// ========================================
// 3. Display Retrieved Sources
// ========================================

function displaySources(content, sources) {
    if (!Array.isArray(sources) || sources.length === 0) {
        return;
    }

    const sourcesBox = document.createElement("div");
    sourcesBox.className = "sources-box";

    const heading = document.createElement("h4");
    heading.textContent = "📚 Retrieved Sources";

    sourcesBox.appendChild(heading);

    sources.forEach((source) => {
        const item = document.createElement("div");
        item.className = "source-item";

        const bookTag = document.createElement("span");
        bookTag.className = "source-tag";
        bookTag.textContent =
            source.source || source.book || "Unknown book";

        const pageTag = document.createElement("span");
        pageTag.className = "source-tag";
        pageTag.textContent = `Page ${source.page ?? "Unknown"}`;

        item.appendChild(bookTag);
        item.appendChild(pageTag);

        sourcesBox.appendChild(item);
    });

    content.appendChild(sourcesBox);
}


// ========================================
// 4. Display Code Validation
// ========================================

function displayValidation(content, validation) {
    if (!validation || typeof validation !== "object") {
        return;
    }

    const issues = [];

    // Support common validation result formats.
    if (Array.isArray(validation.errors)) {
        issues.push(...validation.errors);
    }

    if (Array.isArray(validation.warnings)) {
        issues.push(...validation.warnings);
    }

    if (validation.valid === false) {
        issues.push("The generated code may contain syntax or other issues.");
    }

    if (issues.length === 0) {
        return;
    }

    const box = document.createElement("div");
    box.className = "validation-box warning";

    const heading = document.createElement("strong");
    heading.textContent = "⚠️ Code validation notes";

    const list = document.createElement("ul");
    list.style.margin = "8px 0 0 18px";

    issues.forEach((issue) => {
        const item = document.createElement("li");

        // Avoid inserting model-generated content as HTML.
        item.textContent = typeof issue === "string"
            ? issue
            : JSON.stringify(issue);

        list.appendChild(item);
    });

    box.appendChild(heading);
    box.appendChild(list);

    content.appendChild(box);
}


// ========================================
// 5. Loading Indicator
// ========================================

function showLoadingIndicator() {
    const loading = document.createElement("div");
    loading.className = "message assistant-message";
    loading.id = "loading-indicator";

    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.textContent = "🐍";

    const content = document.createElement("div");
    content.className = "message-content";

    const label = document.createElement("div");
    label.className = "message-label";
    label.textContent = "PythonBookAI";

    const loadingText = document.createElement("div");
    loadingText.className = "loading-message";
    loadingText.textContent = "Searching your books and generating an answer ";

    const dots = document.createElement("span");
    dots.className = "loading-dots";

    for (let i = 0; i < 3; i++) {
        const dot = document.createElement("span");
        dots.appendChild(dot);
    }

    loadingText.appendChild(dots);
    content.appendChild(label);
    content.appendChild(loadingText);

    loading.appendChild(avatar);
    loading.appendChild(content);

    chatContainer.appendChild(loading);

    return loading;
}


// ========================================
// 6. Send Question to Flask Backend
// ========================================

async function askQuestion(question) {
    const cleanedQuestion = question.trim();

    if (!cleanedQuestion) {
        questionInput.focus();
        return;
    }

    showChat();

    // Display the user's question.
    createMessage("user", cleanedQuestion);

    // Clear the input box.
    questionInput.value = "";
    questionInput.style.height = "auto";

    // Prevent multiple simultaneous requests.
    sendButton.disabled = true;
    questionInput.disabled = true;

    const loadingIndicator = showLoadingIndicator();

    // Keep the newest message visible.
    loadingIndicator.scrollIntoView({
        behavior: "smooth",
        block: "end"
    });

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: cleanedQuestion,
                source: bookSelect ? bookSelect.value || null : null
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "The server could not process your question."
            );
        }

        // Remove the loading indicator.
        loadingIndicator.remove();

        // Display the AI's answer.
        const answerMessage = createMessage(
            "assistant",
            data.answer || "No answer was returned."
        );

        // Display the retrieved sources.
        displaySources(
            answerMessage.content,
            data.sources
        );

        // Display code validation notes when available.
        displayValidation(
            answerMessage.content,
            data.code_validation
        );

        answerMessage.message.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    } catch (error) {
        loadingIndicator.remove();

        const errorMessage = createMessage(
            "assistant",
            `Error: ${error.message}`
        );

        errorMessage.messageText.classList.add("error-message");

        console.error("PythonBookAI request failed:", error);

    } finally {
        sendButton.disabled = false;
        questionInput.disabled = false;
        questionInput.focus();
    }
}


// ========================================
// 7. Handle Form Submission
// ========================================

questionForm.addEventListener("submit", (event) => {
    event.preventDefault();
    askQuestion(questionInput.value);
});


// ========================================
// 8. Enter to Send, Shift+Enter for New Line
// ========================================

questionInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        questionForm.requestSubmit();
    }
});


// Automatically resize the question box.
questionInput.addEventListener("input", () => {
    questionInput.style.height = "auto";

    questionInput.style.height =
        Math.min(questionInput.scrollHeight, 160) + "px";
});


// ========================================
// 9. Suggested Questions
// ========================================

document.querySelectorAll(".suggestion-card").forEach((button) => {
    button.addEventListener("click", () => {
        const question = button.dataset.question;

        if (question) {
            askQuestion(question);
        }
    });
});


// ========================================
// 10. Start a New Question
// ========================================

newChatButton.addEventListener("click", () => {
    chatContainer.replaceChildren();

    questionInput.value = "";
    questionInput.style.height = "auto";

    showWelcome();
    questionInput.focus();
});


// ========================================
// 11. Initial Setup
// ========================================

showWelcome();

console.log("PythonBookAI frontend loaded successfully.");
