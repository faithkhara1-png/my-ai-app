import gradio as gr
from duckduckgo_search import DDGS
from langchain_groq import ChatGroq

# Aapki poori attach ki gayi Groq API Key
GROQ_API_KEY = "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"

ai = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=GROQ_API_KEY)


def search_web(query):
    greetings = ["hi", "hello", "hey", "kaise ho", "namaste", "bye", "hye"]
    if query.strip().lower() in greetings or len(query) < 4:
        return ""
    try:
        results = DDGS().text(query, max_results=2)
        if not results:
            return ""
        return "\n".join([f"- {r.get('body', '')}" for r in results])
    except Exception:
        return ""


def chat_function(message, history):
    try:
        web_data = search_web(message)
        if web_data:
            prompt = (
                f"Web Context:\n{web_data}\n\nUser Question: {message}\nAnswer"
                " concisely:"
            )
        else:
            prompt = message

        partial_response = ""
        for chunk in ai.stream(prompt):
            if hasattr(chunk, "content"):
                partial_response += chunk.content
            else:
                partial_response += str(chunk)
            yield partial_response
    except Exception as e:
        yield f"Error: {str(e)}"


mobile_responsive_css = """
html, body, .gradio-container {
    background-color: #121212 !important;
    color: #e0e0e0 !important;
    max-width: 100% !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
}

#component-0, .contain, .block {
    max-width: 100% !important;
    width: 100% !important;
    padding: 8px !important;
}

@media screen and (max-width: 768px) {
    .gradio-container {
        padding: 5px !important;
    }
}

textarea, input[type="text"] {
    background-color: #1e1e1e !important;
    color: #ffffff !important;
    border: 1px solid #333333 !important;
    border-radius: 10px !important;
    font-size: 16px !important;
}

button.primary {
    background-color: #d97757 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

footer { display: none !important; }
"""

header_html = """
<div style="text-align: center; margin: 10px 0;">
    <h1 style="color: #ffffff; margin: 0; font-size: 26px;">🪐 adhy's AI</h1>
    <p style="color: #a0a0a0; font-size: 12px; margin-top: 4px;">Mobile Optimized • Super Fast • Web Connected</p>
</div>
"""

custom_css = """
.gradio-container {
    max-width: 100% !important;
    padding: 0 !important;
}
#chatbot {
    height: 75vh !important;
}
"""

with gr.Blocks(title="adhy's AI", css=custom_css) as demo:
    gr.HTML(header_html)
    gr.ChatInterface(fn=chat_function, elem_id="chatbot")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)
