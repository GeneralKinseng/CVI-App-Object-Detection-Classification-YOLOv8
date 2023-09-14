# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import matplotlib.pyplot as plt
import os
import glob
import requests
from ultralytics import YOLO
from PIL import Image
import cv2
import sys
import PySimpleGUI as sg
import os.path
from postprocessing import *
from gui import *
from resultview import *


window = make_window()
# This is an Event Loop
while True:
    event, values = window.read(timeout=1)
    # ---------- For Webcam --------------------
    if event == 'Run':
        window['web_model_name'].update(value=values['web_model_name'])
        # Set up model and parameter
        model_choice = values['web_model_name']
        model = YOLO(model_choice)

        print("[LOG] Running the camera...")

        cap = cv2.VideoCapture(0)

        # Loop through the video frames
        while cap.isOpened():
            # Read a frame from the video
            success, frame = cap.read()

            if success:
                #flip the frame horizontally
                frame = cv2.flip(frame, 1)

                # Run YOLOv8 inference on the frame
                results = model(frame)

                # Visualize the results on the frame
                annotated_frame = results[0].plot()

                # Display the annotated frame
                cv2.imshow("YOLOv8 Inference", annotated_frame)

                # Break the loop if 'q' is pressed or x is pressed
                if cv2.waitKey(1) & 0xFF == ord("q") or cv2.getWindowProperty("YOLOv8 Inference", cv2.WND_PROP_VISIBLE) < 1:
                    print("Webcam closed")
                    cap.release()
                    cv2.destroyAllWindows()
                    break
            else:
                # Break the loop if the end of the video is reached
                break

    # When press Stop or close window or press Close
    elif event in ('Stop', sg.WIN_CLOSED):
        print("[LOG] Program stopped...")
        break
    

    # ---------- For Image Prediction --------------------
    if event == 'Browse File' : 
        window['img_model_name'].update(value=values['img_model_name'])
        filename = sg.popup_get_file('Choose your file', keep_on_top=True)
        file = str(filename)
        if filename is None:
            continue
        sg.popup("You chose: " + str(filename))
        # Set up model and parameter
        model_choice = values['img_model_name']
        model = YOLO(model_choice)
        #Predict the image
        print("[LOG] Processing...")
        results = model.predict(source=file, save=True)
        sg.popup("Done")
        for r in results:
            im_array = r.plot()  # plot a BGR numpy array of predictions
            im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
            im.show()  # show image
        
    elif event == 'Browse Folder' : 
        window['img_model_name'].update(value=values['img_model_name'])
        folder = sg.popup_get_folder('Choose your folder', keep_on_top=True)
        if not folder:
            continue
        sg.popup("You chose: " + str(folder))
        # Set up model and parameter
        model_choice = values['img_model_name']
        model = YOLO(model_choice)
        # Predict the image
        print("[LOG] Processing...")
        results = model.predict(source=str(folder), save=True)
        sg.popup("Done")
        for r in results:
            im_array = r.plot()  # plot a BGR numpy array of predictions
            im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
            im.show()  # show image
            
    # When close window
    elif event == sg.WIN_CLOSED:
        break
    
    
    # ---------- For Viewing Results --------------------
    elif event == '-FOLDER-':                         # Folder name was filled in, make a list of files in the folder
        folder = values['-FOLDER-']
        try:
            file_list = os.listdir(folder)         # get list of files in folder
        except:
            file_list = []
        fnames = [f for f in file_list if os.path.isfile(
            os.path.join(folder, f)) and f.lower().endswith((".png", ".jpg", "jpeg", ".tiff", ".bmp"))]
        window['-FILE LIST-'].update(fnames)
    elif event == '-FILE LIST-':    # A file was chosen from the listbox
        try:
            filename = os.path.join(values['-FOLDER-'], values['-FILE LIST-'][0])
            window['-TOUT-'].update(filename)
            if values['-W-'] and values['-H-']:
                new_size = int(values['-W-']), int(values['-H-'])
            else:
                new_size = None
            window['-IMAGE-'].update(data=convert_to_bytes(filename, resize=new_size))
        
        except Exception as E:
            print(f'** Error {E} **')
            pass        # something weird happened making the full filename
    # --------------------------------- Close & Exit ---------------------------------
    
window.close()