# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 16:01:16 2023

@author: Admin
"""

# https://www.pysimplegui.org/en/latest/#jump-start
import PySimpleGUI as sg
import subprocess
import os
import sys

# Create Layout of the GUI
def make_window():
    webcam_layout = [  
        [sg.Text('Webcam - Object Detection/Segmentation/Classification')],
        [sg.Text('Readme'), sg.Table([['Very Large', 'yolov8x', 'yolov8x-seg', 'yolov8x-cls'],
        ['Large', 'yolov8l', 'yolov8l-seg', 'yolov8l-cls'],
        ['Medium', 'yolov8m', 'yolov8m-seg', 'yolov8m-cls'],
        ['Small', 'yolov8s', 'yolov8s-seg', 'yolov8s-cls'],
        ['Very Small', 'yolov8n', 'yolov8n-seg', 'yolov8n-cls']],
        ['Batch Sizes', 'Detection', 'Segmentation', 'Classifcation'], 
            num_rows=5)],
        [sg.Text('Enter Model Name'),
         sg.Combo(values=('yolov8x', 'yolov8l', 'yolov8m', 'yolov8s', 'yolov8n',
                          'yolov8x-seg', 'yolov8l-seg', 'yolov8m-seg', 'yolov8s-seg', 'yolov8n-seg',
                          'yolov8x-cls', 'yolov8l-cls', 'yolov8m-cls', 'yolov8s-cls', 'yolov8n-cls'), 
                  enable_events=True, readonly=True, k='web_model_name'),],
        [sg.Text('Scale to Show (1-100)'), sg.InputText(default_text="100", key= 'scale_percent')],
        [sg.Button('Run'), sg.Button('Stop')],
        [sg.Image(filename='', key='image')]
        ]
    
    img_layout = [  
        [sg.Text('Predict a Static Image')],
        [sg.Text('Readme'), sg.Table([['Very Large', 'yolov8x', 'yolov8x-seg', 'yolov8x-cls'],
                                      ['Large', 'yolov8l', 'yolov8l-seg', 'yolov8l-cls'],
                                      ['Medium', 'yolov8m', 'yolov8m-seg', 'yolov8m-cls'],
                                      ['Small', 'yolov8s', 'yolov8s-seg', 'yolov8s-cls'],
                                      ['Very Small', 'yolov8n', 'yolov8n-seg', 'yolov8n-cls']],
                                     ['Batch Sizes', 'Detection', 'Segmentation', 'Classifcation'], 
                                     num_rows=5)],
        [sg.Text('CHOOSE A PRETRAINED MODEL', font=("bold")),
         sg.Combo(values=('yolov8x', 'yolov8l', 'yolov8m', 'yolov8s', 'yolov8n',
                          'yolov8x-seg', 'yolov8l-seg', 'yolov8m-seg', 'yolov8s-seg', 'yolov8n-seg',
                          'yolov8x-cls', 'yolov8l-cls', 'yolov8m-cls', 'yolov8s-cls', 'yolov8n-cls'), 
                  enable_events=True, readonly=True, k='img_model_name'),],
        [sg.Button('Browse File')],
        [sg.Button('Browse Folder')]
        ]
    
    left_col = [[sg.Text('Folder'), sg.In(size=(25,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse()],
            [sg.Listbox(values=[], enable_events=True, size=(40,20),key='-FILE LIST-')],
            [sg.Text('Resize to'), sg.In(default_text=640, key='-W-', size=(5,1)), sg.In(default_text=480, key='-H-', size=(5,1))]]

    images_col = [[sg.Text('You choose from the list:')],
              [sg.Text(size=(40,1), key='-TOUT-')],
              [sg.Image(key='-IMAGE-')]]
    
    result_layout = [[sg.Column(left_col, element_justification='c'), 
                      sg.VSeperator(),sg.Column(images_col, element_justification='c')]]
    
    layout = [ [sg.Text('Object Detection/Segmentation/Classification with Yolo V8', 
                    size=(50, 1), justification='center', font=("Helvetica", 16), 
                    relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)]]
    layout += [[sg.TabGroup([[sg.Tab('Webcam', webcam_layout),
                              sg.Tab('Predict Images', img_layout),
                              sg.Tab('View Results', result_layout)
                              ]], key = 'tabgroup', expand_x=True, expand_y=True),
                ]]
    layout[-1].append(sg.Sizegrip())
    
    window = sg.Window('CVI App', layout, grab_anywhere=True, resizable=True, margins=(0,0), 
                       use_custom_titlebar=True, finalize=True, keep_on_top=False)
    window.set_min_size(window.size)
    return window
