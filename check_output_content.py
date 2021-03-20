#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 15:39:02 2021

@author: micaelavieira
"""

"""
Simple script to show that in the hdf5 file created by ioHub all information
are present"""


import h5py

iohub_output = 'events.hdf5'

def printall(name, obj):
    if name in ['data_collection/events/mouse/MouseInputEvent', 'data_collection/events/experiment/MessageEvent']:
        attributes = dict(obj.attrs)
        print(attributes)

with h5py.File(iohub_output,'r') as hf:
    hf.visititems(printall)

with h5py.File(iohub_output, 'r') as f:
    data_collection = f['data_collection']
    events = data_collection['events']
    experiment = events['experiment']
    MessageEvent = experiment['MessageEvent'][()]
    mouse = events['mouse']
    MouseInputEvent = mouse['MouseInputEvent'][()]
    
    

print(MessageEvent)
#print(MouseInputEvent)