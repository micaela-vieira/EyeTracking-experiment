#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 17:50:57 2021

@author: micaelavieira
"""

from psychopy import core, event, monitors, visual
from psychopy.iohub import util, client
import pyautogui
from typing import List, Tuple


def extract_stimuli_from_txt(filename: str) -> List:
    """
    Purpose
    -------
    Extract stimuli from txt file created with generate_lists.py.

    Parameters
    ----------
    filename : str
        Name of the file containing the input data in the form 
        'sentence \t version \t text'.

    Returns
    -------
    list_of_stimuli_with_coordinates : List
        List containing one dictionary for each line in filename.
    """
    list_of_stimuli_with_coordinates = []
    with open(filename) as f:
        for line in f:
            line_triple_split = line.strip('\n').split('\t')
            line_dictionary = {'text': line_triple_split[2], 'sentence': line_triple_split[0], 'version': line_triple_split[1]}
            list_of_stimuli_with_coordinates.append(line_dictionary)
    return list_of_stimuli_with_coordinates

def monitor_and_window(eye_distance: int) -> Tuple[int, int, visual.window.Window]:
    """
    Purpose
    -------
    Get monitor size and define window with the same size as the monitor.

    Parameters
    ----------
    eye_distance : int
    Distance from the eye and the monitor in cm.
    
    Returns
    -------
    monitor_width : int
        Width of the monitor.
    monitor_height : int
        Height of the monitor.
    win : visual.window.Window
        Psychopy window.
    """
    #get monitor size in pixel
    monitor_width, monitor_height= pyautogui.size()
    #define monitor
    mon = monitors.Monitor("test_monitor", width=monitor_width, distance=eye_distance)
    #define window
    win = visual.Window(
        monitor=mon,
        size=(monitor_width, monitor_height),
        pos=(0,0),
        color='Gray',
        colorSpace='rgb',
        units='pix')
    return monitor_width, monitor_height, win

def fixation_cross(window: visual.window.Window, x_pos_cross: float, cross_size: float):
    """
    Purpose
    -------
    Define and display the fixation cross.

    Parameters
    ----------
    window : visual.window.Window
        Psychopy window.
    x_pos_cross : float
        x-position of the dot in pixels.
    cross_size : float
        Length of the cross arms in pixels.

    Returns
    -------
    None.
    """
    fixation_cross = visual.ShapeStim(window, 
                                vertices=((0, -cross_size), (0, cross_size), (0,0), (-cross_size,0), (cross_size, 0)),
                                lineWidth=20,
                                closeShape=False,
                                lineColor="white",
                                pos=(x_pos_cross, cross_size),
                                units='pix')    
    fixation_cross.draw()
    window.flip()
    return

def text_and_dot(window: visual.window.Window, my_text: str, x_pos_text: float, x_pos_dot: float, y_pos_dot: float): 
    """
    Purpose
    -------
    Define and display the text field and the dot.

    Parameters
    ----------
    window : visual.window.Window
        Psychopy window.
    my_text : str
        Text to insert into the text field.
    x_pos_text : float
        x-position of the text in pixels.
    x_pos_dot : float
        x-position of the dot in pixels.
    y_pos_dot : float
        y-position of the dot in pixels.

    Returns
    -------
    None.
    """
    text = visual.TextBox(window,
                          text=my_text,
                          font_name='Courier New',
                          font_size=22,
                          font_color=[1, 1, 1],
                          color_space='rgb',
                          size=(2000, 100),
                          pos=(x_pos_text, 0),
                          align_horz='left',
                          align_vert='bottom',
                          units='pix')
    dot = visual.Circle(window,
                        lineColor="white",
                        fillColor="white",
                        radius=2,
                        edges=128,
                        pos=(x_pos_dot, y_pos_dot),
                        units='pix')
    text.draw()
    dot.draw()
    window.flip()
    return

def device_for_experiment(window: visual.window.Window, io_client: client.ioHubConnection) -> client.ioHubDeviceView:
    """
    Purpose
    -------
    Depending on the yaml file, define what is the experiment device.

    Parameters
    ----------
    window : visual.window.Window
        Psychopy window.
    io_client : client.ioHubConnection
        ioHub connection.

    Returns
    -------
    experiment_device : client.ioHubDeviceView
        device connecte to ioHub.
    """
    #if the eyetracker is present and not commented in the yaml file use it, otherwise use mouse
    try:
        experiment_device = io_client.devices.tracker
        #calibrate the eyetracker
        experiment_device.runSetupProcedure()
    except:
        experiment_device = io_client.devices.mouse
        #set mouse to visible
        window.setMouseVisible(True)
    experiment_device.getPosition()
    return experiment_device

def fixation_routine(device: client.ioHubDeviceView, x_pos_min: float, x_pos_max: float, y_pos_min: float, y_pos_max: float, time_fix: float) -> bool:
    """
    Purpose
    -------
    Determine if a fixation routine is succesful or not.

    Parameters
    ----------
    device : client.ioHubDeviceView
        device connecte to ioHub.
    x_pos_min : float
        Minimal x-position of the fixation region.
    x_pos_max : float
        Maximal x-position of the fixation region.
    y_pos_min : float
        Minimal y-position of the fixation region.
    y_pos_max : float
        Maximal y-position of the fixation region.
    time_fix : float
        Minimal time that the experiment should stay without interruptions
        inside the fixation region to define the fixation as succesful.

    Returns
    -------
    fixation_succesful : bool
        Boolean that confirm if the fixation is passed or failed.
    """
    fixation_succesful = False
    time_already_started = False
    #keep fixation false until minimal time is reached
    while fixation_succesful == False:
        if x_pos_min <= device.getPosition()[0] <= x_pos_max and y_pos_min <= device.getPosition()[1] <= y_pos_max:
            correct_position = True
        #if the position is not correct, reset time_already_started
        else:
            correct_position = False
            time_already_started = False
        if correct_position == True:
            #if the position is correct, see if the initial time is already given
            if time_already_started == False:
                initial_time = core.getTime()
                time_already_started = True
            #if initial time is already given, determine time interval
            else:
                t = core.getTime()
                if t-initial_time > time_fix:
                    fixation_succesful = True
    return fixation_succesful







def main():
    """
    Parameters to modify
    """
    path_to_txt_file = 'Data/dummy.txt'
    path_to_yaml_file = 'iohub_config.yaml'
    border_margin = 150
    length_arm_cross = 30
    fixation_time_for_succesful = 0.3
    eyelink_distance = 70
    
    
    """
    main procedure
    """
    #get only text from the list of stimuli
    list_of_stimuli_only_text = [i.get('text') for i in extract_stimuli_from_txt(path_to_txt_file)]
    #get monitor sizes and window
    monitor_width, monitor_height, win = monitor_and_window(eyelink_distance)
    #get configuration file and connect to io
    io_config = util.readConfig(path_to_yaml_file)
    io = client.ioHubConnection(io_config)
    #get device
    experiment_device = device_for_experiment(win, io)

    #build a loop for every stimuli in our list
    for stimulus_index in range(len(list_of_stimuli_only_text)):
        #start infinite loop for validation cross
        while True:    
            fixation_cross(win, -monitor_width/2+border_margin/2+length_arm_cross/2, length_arm_cross-length_arm_cross/5)
            #if fixation of the cross satisfies the criteria, end the loop and procede
            fixation_succesful_cross = fixation_routine(experiment_device, -monitor_width/2+border_margin/2-0.5*length_arm_cross, -monitor_width/2+border_margin/2+1.5*length_arm_cross, -2*length_arm_cross-length_arm_cross/5, 0.5*length_arm_cross-length_arm_cross/5, fixation_time_for_succesful)
            if fixation_succesful_cross:
                break
        #start infinite loop for lower right dot
        while True:
            text_and_dot(win, list_of_stimuli_only_text[stimulus_index], -monitor_width+border_margin, monitor_width/2-monitor_width/20, -monitor_height/2+monitor_height/10)
            #if fixation of the dot satisfies the criteria, end the loop and procede
            fixation_succesful_dot = fixation_routine(experiment_device, monitor_width/2-monitor_width/10, monitor_width/2, -monitor_height/2, -monitor_height/2+monitor_height/8, fixation_time_for_succesful)
            if fixation_succesful_dot:
                break
    
    #close everything
    win.close()
    io.quit()
    core.quit()
    return


if __name__ == "__main__":
    main()