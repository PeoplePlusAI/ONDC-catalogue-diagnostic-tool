import gradio as gr
import pandas as pd
from core.ai import main_logic


# Create the Gradio interface
iface = gr.Interface(
    fn=main_logic, 
    inputs=[
        gr.File(type="filepath", label="Upload CSV"),
        gr.Textbox(label="Requirements", placeholder="Enter your requirements here")
    ], 
    outputs="text"
)

# Launch the app
iface.launch()
