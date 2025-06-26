import streamlit as st
import base64
import time
from tempfile import NamedTemporaryFile

# App title
st.set_page_config(page_title='🎈 AI App', page_icon='🎈')
st.title("AI App 🎈")
st.info(
    "In this app you can **Show** (provide mock-up image) or **Tell** (provide text prompt) how you want your Streamlit app to be built."
)


tabs = st.tabs(['Tell'])

# Tell how the app should be built
with tabs[0]:
    text_prompt = st.text_area(
        "Describe details on the functionalities of the Streamlit app that you want to build.",
        "", 
        height=240
    )

    with st.expander('Expand to see system prompt'):
        prompt_instructions = '''You are an experienced Python developer who can build amazing Streamlit apps.
            You will be given a mock-up image of a Streamlit app for which you will convert it to a Streamlit app by generating the Python code.
            If a graph is present in the app, instead of generating random data, please try to mimick the data points shown.
            If asked to do anything other than creating a Streamlit app, politely refuse.'''
        st.markdown(prompt_instructions)
        
    # Start LLM process
    start_button = st.button('Build', key='button_text_start')
    
    if text_prompt is not None and api_key and start_button:
        with st.spinner('Processing ...'):
            messages=[
                        {"role": "system", "content": "You are an experienced Python developer who can build amazing Streamlit apps."},
                        {"role": "user", "content": text_prompt}
                      ]
        try:
          # Response generation
          full_response = ''
          message_placeholder = st.empty()
              
          for completion in client.chat.completions.create(
            model='gpt-4', messages=messages, 
            max_tokens=1280, stream=True):
                      
              if completion.choices[0].delta.content is not None:
                full_response += completion.choices[0].delta.content
                message_placeholder.markdown(full_response + '▌')
                      
          message_placeholder.markdown(full_response)

          parsed_output = full_response.split('```python')[1].lstrip('\n').split('```')[0]
    
          # Clear results
          if st.button('Clear', key='button_text_clear'):
            os.remove(tmp.name)
        
        except Exception as e:
          st.error(f'An error occurred: {e}')
          
    else:
      if not text_prompt and start_button:
        st.warning('Please provide your text prompt.')
      if not api_key:
        st.warning('Please provide your OpenAI API key.')