import streamlit as st
# from Audio import text_to_speech, get_audio
import cv2
import tempfile
import ExerciseAiTrainer as exercise
from chatbot import chat_ui
import time

def main():
    cap = None
    # Set configuration for the theme before any other Streamlit command
    st.set_page_config(page_title='Fitness AI Coach', layout='centered')
    
    # Define App Title and Structure
    st.title('FIT VISION')

    # 2 Options: Video, WebCam, Auto Classify, chatbot
    options = st.sidebar.selectbox('Select Option', ('Video', 'WebCam', 'Auto Classify', 'chatbot'))

    if options == 'chatbot':
        st.markdown('-------')
        st.markdown("The chatbot can make mistakes. Check important info.")
        chat_ui()

    # Define Operations if Video Option is selected
    if options == 'Video':
        st.markdown('-------')

        st.write('## Upload your video and select the correct type of Exercise to count repetitions')
        st.write("")
        st.write('Please ensure you are clearly visible and facing the camera directly. This will help the AI accurately track your movements.')

        st.set_option('deprecation.showfileUploaderEncoding', False)

        st.sidebar.markdown('-------')

        # User can select different types of exercise
        exercise_options = st.sidebar.selectbox(
            'Select Exercise', ('Bicept Curl', 'Push Up', 'Squat', 'Shoulder Press')
        )

        st.sidebar.markdown('-------')

        # User can upload a video:
        video_file_buffer = st.sidebar.file_uploader("Upload a video", type=["mp4", "mov", 'avi', 'asf', 'm4v'])

        # --- START OF FIX ---
        
        # We need to wait until a file is uploaded before we do anything
        if video_file_buffer is not None:
            tfflie = tempfile.NamedTemporaryFile(delete=False)
            tfflie.write(video_file_buffer.read())
            tfflie.close() # Close the file so cv2 can open it

            # Open the video file with cv2
            cap = cv2.VideoCapture(tfflie.name)

            # Visualize Video before analysis
            st.sidebar.text('Input Video')
            st.sidebar.video(tfflie.name)

            st.markdown('## Input Video')
            st.video(tfflie.name)

            st.markdown('-------')

            # Visualize Video after analysis (analysis based on the selected exercise)
            st.markdown(' ## Output Video')
            if exercise_options == 'Bicept Curl':
                exer = exercise.Exercise()
                counter, stage_right, stage_left = 0, None, None
                exer.bicept_curl(cap, is_video=True, counter=counter, stage_right=stage_right, stage_left=stage_left)

            elif exercise_options == 'Push Up':
                st.write("The exercise need to be filmed showing your left side or facing frontally")
                exer = exercise.Exercise()
                counter, stage = 0, None
                exer.push_up(cap, is_video=True, counter=counter, stage=stage)

            elif exercise_options == 'Squat':
                exer = exercise.Exercise()
                counter, stage = 0, None
                exer.squat(cap, is_video=True, counter=counter, stage=stage)

            elif exercise_options == 'Shoulder Press':
                exer = exercise.Exercise()
                counter, stage = 0, None
                exer.shoulder_press(cap, is_video=True, counter=counter, stage=stage)
        
        else:
            # Show a message if no video is uploaded yet
            st.sidebar.text('Input Video')
            st.sidebar.info("Upload a video to get started.")
            
        # --- END OF FIX ---
        
        #
        # THE DUPLICATED BUGGY CODE BLOCK WAS HERE AND HAS BEEN REMOVED.
        #
    
    # Added new section for Auto Classify
    elif options == 'Auto Classify':
        st.markdown('-------')
        st.write('Click button to start automatic exercise classification and repetition counting')
        st.markdown('-------')
        st.write("Please ensure you are clearly visible and facing the camera directly. This will help the AI accurately track your movements.")
        auto_classify_button = st.button('Start Auto Classification')

        if auto_classify_button:
            time.sleep(2)
            exer = exercise.Exercise()
            exer.auto_classify_and_count()

    # Define Operation if webcam option is selected
    elif options == 'WebCam':
        st.markdown('-------')

        st.sidebar.markdown('-------')

        # User can select different exercises
        exercise_general = st.sidebar.selectbox(
            'Select Exercise', ('Bicept Curl', 'Push Up', 'Squat', 'Shoulder Press')
        )

        # Define a button for start the analysis (pose estimation) on the webcam
        # st.write(' Click button and say "yes" when you are in the correct position for training')
        # button = st.button('Activate AI Trainer')

        # st.markdown('-------')

        # New button for direct activation
        st.write(' Click button to start training')
        start_button = st.button('Start Exercise')

        # # Visualize video that explain the correct forms for the exercises
        # if exercise_general == 'Bicept Curl':
        #     st.write('## Bicept Curl Execution Video')
        #     st.video('curl_form.mp4')

        # elif exercise_general == 'Push Up':
        #     st.write('## Push Up Execution Video')
        #     st.video('push_up_form.mp4')

        # elif exercise_general == 'Squat':
        #     st.write('## Squat Execution Video')
        #     st.video('squat_form_2.mp4')

        # elif exercise_general == 'Shoulder Press':
        #     st.write('## Shoulder Press Execution')
        #     st.video('shoulder_press_form.mp4')

        if start_button:
            time.sleep(2)  # Add a delay of 2 seconds
            ready = True
            # for each type of exercise call the method that analyze that exercise
            if exercise_general == 'Bicept Curl':
                while ready:
                    cap = cv2.VideoCapture(0)
                    exer = exercise.Exercise()
                    counter, stage_right, stage_left = 0, None, None
                    exer.bicept_curl(cap, counter=counter, stage_right=stage_right, stage_left=stage_left)
                    break

            elif exercise_general == 'Push Up':
                while ready:
                    cap = cv2.VideoCapture(0)
                    exer = exercise.Exercise()
                    counter, stage = 0, None
                    exer.push_up(cap, counter=counter, stage=stage)
                    break

            elif exercise_general == 'Squat':
                while ready:
                    cap = cv2.VideoCapture(0)
                    exer = exercise.Exercise()
                    counter, stage = 0, None
                    exer.squat(cap, counter=counter, stage=stage)
                    break

            elif exercise_general == 'Shoulder Press':
                while ready:
                    cap = cv2.VideoCapture(0)
                    exer = exercise.Exercise()
                    counter, stage = 0, None
                    exer.shoulder_press(cap, counter=counter, stage=stage)
                    break

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        st.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
