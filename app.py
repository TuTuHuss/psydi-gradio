# import gradio as gr
# from client import FlaskClient

# client = FlaskClient()

# def client_output(message,history):
#     client.run(message)
#     return client.run()



# demo = gr.ChatInterface(fn=client_output, title="Echo Bot")

# if __name__ == "__main__":
#     demo.queue().launch()


import gradio as gr

def image_classifier(inp):
    return {'cat': 0.3, 'dog': 0.7}

demo = gr.Interface(fn=image_classifier, inputs="image", outputs="label")
demo.launch(server_name='127.0.0.1')