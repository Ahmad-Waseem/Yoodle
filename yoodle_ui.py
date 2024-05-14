import streamlit as st
from streamlit_drawable_canvas import st_canvas
import yoodle_backend
import time
import requests
import json

YoodleV3 = yoodle_backend.MyModel()

st.set_page_config(page_title="Yoodle - AI Buildings classifier", page_icon="🎨", layout="wide")

page_bg_img = '''

<style>
[data-testid="stAppViewBlockContainer"]
    {
        background-image: url("https://raw.githubusercontent.com/Ahmad-Waseem/Yoodle/main/yoodle/Assets/toppng.com-jpg-black-and-white-istanbul-royalty-colorful-buildings-drawings-3001x1957.png");
        background-size: cover;
        padding-top: 1;
    }
</style>
'''


# Sidebar
st.sidebar.title("Yoodle V2")
st.sidebar.markdown(
    """
    ## Introduction
    Welcome to the Yoodle App! This app uses an AI model to classify buildings based on their features.

    ## Model Description
    Our model is trained on a large dataset of Augmented  images. It leverages deep learning techniques to predict the Famous Landmarks.

    ## Parameters
    - **Image Input**: Draw the doodle yourself!!.

    ## How to Use
    1. Select the Landmark name from DropDown
    2. Draw doodle under 20 second
    3. Click the "Predict" button to get the building classification.
    4. See if model gives you correct image

    Enjoy exploring Yoodle!
    """
)

labels = ['Badshahi Mosque', 'Big Ben', 'Burj Khalifa', 'Burj ul Arab', 'Chrysler Building', 'Cologne Cathedral', 'Colosseum of Rome', 'Easter Island', 'Eiffel Tower', 'Future Museum', 'Taj Mahal']

st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("Yoodle!!")

def printOutput(num):
    st.divider()
    st.write(f"It is: {labels[num[0]]}")
    st.divider()

def main():
    # Dropdown menu for building selection
    lockBoard = False
    submit_button = None
    N = 20
    current_N = N





    labels = ['Badshahi Mosque', 'Big Ben', 'Burj Khalifa', 'Burj ul Arab', 'Chrysler Building', 'Cologne Cathedral', 'Colosseum of Rome', 'Easter Island', 'Eiffel Tower', 'Future Museum', 'Taj Mahal']
    building = st.selectbox('Select Building', ['None', 'Badshahi Mosque', 'Big Ben', 'Burj Khalifa', 'Burj ul Arab', 'Chrysler Building', 'Cologne Cathedral', 'Colosseum of Rome', 'Easter Island', 'Eiffel Tower', 'Future Museum', 'Taj Mahal'])


    if building is None or building == 'None':
        lockBoard = True
        lockBoard = False
        submit_button = None
        N = 20
        current_N = N
    else:
        lockBoard = False

        TimerStates = [False, True]
        isTimerOn = TimerStates[0]

        if not lockBoard:

            # Layout using columns
            col1, col2 = st.columns(2)

            with col1:
            
                drawing_mode = "freedraw"
                stroke_width = 5
                stroke_color = "rgb(0, 0, 0)"
                bg_color = "rgb(255, 255, 255)"
                realtime_update = True

                # Create a canvas component
                canvas_result = st_canvas(
                    fill_color="rgb(255, 255, 255)",
                    stroke_width=stroke_width,
                    stroke_color=stroke_color,
                    background_color=bg_color,
                    background_image=None,
                    update_streamlit=realtime_update,
                    height=512,
                    width=512,
                    drawing_mode=drawing_mode,
                    point_display_radius=0 if drawing_mode == 'point' else 0,
                    display_toolbar=False
                )

            with col2:
                ph = st.empty()
                session_state = st.session_state
                if 'current_N' not in session_state:
                    session_state.current_N = N

                # Do something interesting with the image data and paths
                if canvas_result.image_data is not None and canvas_result is not None:
                    isTimerOn = TimerStates[1]
                    
                    
                

                    if submit_button is None and (20 - session_state.current_N) >= 5:
                        submit_button = st.button('Submit')
                        print(session_state.current_N)
                    # Send drawing data to the Flask server for prediction
                    if submit_button:
                        building = 'None'
                        drawing_data = canvas_result.image_data
                        response = YoodleV3.classify(drawing_data, building)

                        st.write("Drawing submitted!")
                        printOutput(response)
                        st.image(canvas_result.image_data)

                    if isTimerOn:
                        for secs in range(session_state.current_N, -1, -1):
                            ss = secs
                            session_state.current_N = ss
                            ph.metric("Countdown", f"{ss:02d}s left")
                            time.sleep(1)
                        prediction = None
                        if session_state.current_N <= 1:
                            isTimerOn = TimerStates[0]
                            LockBoard = True
                            print("Locked")

                            drawing_data = canvas_result.image_data
                            response = YoodleV3.classify(drawing_data, building)
                            printOutput(response)

                    # elif session_state.current_N % 5 == 0:
                    #     isTimerOn = TimerStates[1]
                    #     print(f"np{N},{isTimerOn}")

                    #     drawing_data = canvas_result.image_data
                    #     response = YoodleV3.classify(drawing_data, building)
                    #     printOutput(response)

        else:
            building = 'None'



if __name__ == "__main__":
  main()