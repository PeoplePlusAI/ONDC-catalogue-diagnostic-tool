import gradio as gr
from core.ai import validate_catalogue


# Create the Gradio interface
iface = gr.Interface(
    fn=validate_catalogue, 
    inputs=[
        gr.File(type="filepath", label="Upload CSV"),
        gr.Textbox(label="Requirements", placeholder="Enter your requirements here")
    ], 
    outputs="text"
)

# Launch the app
iface.launch()