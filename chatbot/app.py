from transformers import pipeline, Conversation
import gradio as gr


model = "meta-llama/Llama-2-7b-chat-hf"
chatbot = pipeline(model=model)

message_list = []
response_list = []

def vanilla_chatbot(message, history):
    conversation = Conversation(text=message, past_user_inputs=message_list, generated_responses=response_list)
    conversation = chatbot(conversation)

    return conversation.generated_responses[-1]

demo_chatbot = gr.ChatInterface(vanilla_chatbot, title="Vanilla Chatbot", description="Enter text to start chatting.")

demo_chatbot.launch()

# model = "facebook/blenderbot-400M-distill"
# model = "iocuydi/llama-2-amharic-3784m"