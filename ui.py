import gradio as gr
from app import agent  # Importing the LangChain agent from app.py

def chatbot_response(user_input):
    """Function to interact with the LangChain agent and get a response."""
    response = agent.invoke(user_input)
    return response["output"] if isinstance(response, dict) else response

# Custom CSS for refined aesthetics
custom_css = """
/* General Container */
.gradio-container {
    background-color: #d3e6c2;  /* Light sap green */
    font-family: 'Inter', sans-serif;
    padding: 20px;
}

/* Header Styling */
h1 {
    text-align: center;
    color: #251F44; 
    font-size: 2.5em;
    font-weight: bold;
    margin-bottom: 5px;
}

h3 {
    text-align: center;
    color: #251F44;
    font-size: 1.2em;
    font-weight: 500;
    margin-bottom: 20px;
}

/* Input Row Styling */
.input-row {
    width: 70%;  /* Adjust width */
    max-width: 800px;  /* Prevents it from stretching too much */
    min-width: 500px;  /* Keeps it from being too small */
    margin: 0 auto;  /* Centers the row */
    background: #97a888;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 16px auto; /* Adjust spacing */
}


/* Textbox Styling (Input) */
textarea {
    font-size: 16px;
    color: #251F44;
    background: #f8fdee;  /* Off White */
    border: 1px solid #251F44;  /* Border Around Input */
    border-radius: 12px;
    padding: 12px;
    width: 70%;  /* Limits the width */
    max-width: 800px;  /* Prevents it from stretching too much */
    min-width: 300px;  /* Ensures it doesn't get too small */
    transition: all 0.3s ease-in-out;
    display: block
    
}

textarea::placeholder {
    color: #251F44;  /* Placeholder Text */
}

textarea:focus {
    border-color: #E26EE5;
    outline: none;
    box-shadow: 0px 0px 10px rgba(226, 110, 229, 0.5);
}

/* Button Styling */
button {
    background-color: #addb8a !important;
    color: #251F44 !important;
    border-radius: 10px !important;
    font-size: 18px !important;
    padding: 10px 20px !important;
    border: none !important;
    transition: all 0.3s ease-in-out;
}

button:hover {
    background-color: #8baf6e !important;
    box-shadow: 0px 4px 10px rgba(80, 125, 42, 0.3);
}

/* Ask AI Button Styling */
.ask-ai-button {
    width: auto;  /* Button width adjusts based on content */
    padding: 10px 20px;  /* Add some space around text */
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 16px auto; /* Adjust spacing */
}


/* AI Response Static Text */
.ai-response-text {
    text-align: center;
    font-size: 1.05em;
    font-weight: 500;
    color: #251F44;  /* Deep purple for readability */
    background: #f8fdee; /* Soft cool green */
    padding: 8px;
    border-radius: 6px;
    width: auto;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 16px auto; /* Adjust spacing */
}

/* Output Box */
.gr-textbox-output {
    background-color: #f8fdee;  /* Off White Green */
    border: 1px solid #49108B;  /* Border Around Output */
    border-radius: 12px;
    color: #251F44;
    font-size: 16px;
    padding: 12px;
    width: 70%;  /* Limits the width */
    max-width: 800px;  /* Prevents excessive stretching */
    min-width: 300px; 
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 16px auto; /* Adjust spacing */

}


"""

# Creating the Gradio App with Advanced UI
with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("# 🫁 🌿 BreathWell AI - Asthma Assistant 🌷")
    gr.Markdown("### Ask for your medical history, air quality, or recommendations with expert AI guidance.")

    with gr.Row(elem_classes=["input-row"]):
        user_input = gr.Textbox(
            lines=2, 
            placeholder="Hello! How can I assist you today?", 
            label="Your Question"
        )
    
    submit_button = gr.Button("Ask AI", elem_classes=["ask-ai-button"])

    gr.Markdown("#### *AI Response will appear down here...*", elem_classes=["ai-response-text"])
    
    with gr.Row(elem_classes=["gr-textbox-output"]):  # Use a row to style the output area
        response_output = gr.Markdown()  # Enables Markdown formatting 
    
    submit_button.click(chatbot_response, inputs=user_input, outputs=response_output)

# Launch the app
if __name__ == "__main__":
    demo.launch(share=True)
