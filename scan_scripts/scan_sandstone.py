#!/usr/bin/env python

import numpy as np
from epics import PV
import epics
import numpy as np
import time
import log
log.setup_custom_logger("./scan_sandstone.log")

tomoscan_prefix = '2bmb:TomoScan:'
ts_pvs = {}
ts_pvs['StartScan']             = PV(tomoscan_prefix + 'StartScan')
ts_pvs['DarkFieldMode']         = PV(tomoscan_prefix + 'DarkFieldMode')
ts_pvs['FlatFieldMode']         = PV(tomoscan_prefix + 'FlatFieldMode')
ts_pvs['FileName']              = PV(tomoscan_prefix + 'FileName')

ts_pvs['ProgramPSO']            = PV(tomoscan_prefix + 'ProgramPSO') 

ts_pvs['SampleY']               = PV('2bmb:m25')
ts_pvs['LoadValue']             = PV('2bmb:D4Ch12_raw')
ts_pvs['LoadMotor']             = PV('2bmb:m33')
ts_pvs['LoadMotorSpeed']        = PV('2bmb:m33.VELO')
ts_pvs['Autoincrement']         = PV('2bmbSP1:HDF1:AutoIncrement')
ts_pvs['NumAngles']             = PV('2bmb:TomoScan:NumAngles')
ts_pvs['RotationStart']         = PV('2bmb:TomoScan:RotationStart')
ts_pvs['RotationStep']          = PV('2bmb:TomoScan:RotationStep')
ts_pvs['ReturnToStart']         = PV('2bmb:TomoScan:ReturnRotation')



ts_pvs['ReturnToStart'].put('No',wait=True)
ts_pvs['ProgramPSO'].put('Yes',wait=True)
# pos_y = np.arange(14.7,21.2,3.2)#loading1
# pos_y = np.arange(20.6,28,3.2)#loading2
# pos_y[0]+=0.2
# pos_y[2]-=0.2
# pos_y = np.arange(20.9,28,3.2)#loading3

# pos_y = np.arange(20.3,28,3.2)#loading4
pos_y = np.arange(20.3,28,3.2)#loading5

letters = ['a','b','c']
rot_start = [0,180]
rot_step = [0.12,-0.12]
num_angles = 1501
load_step = 0.008
base_name='loading5'
flat_loops = 3

# for i_loop in range(1000000):
#     load_motor = ts_pvs['LoadMotor'].get()
#     load_motor_new = load_motor+load_step
#     log.warning(f"Current load {ts_pvs['LoadValue'].get()}.")
#     log.warning(f"Move load motor to {load_motor_new:.7f}. Load speed {ts_pvs['LoadMotorSpeed'].get()}.")
#     ts_pvs['LoadMotor'].put(load_motor_new,wait=True)
#     log.warning(f"New load {ts_pvs['LoadValue'].get()}.")    
#     time.sleep(14)
# exit()
for i_loop in range(10000):
    for i,y in enumerate(pos_y):        
        log.info(f'move Sample Y to {y:.2f}')
        ts_pvs['SampleY'].put(y,wait=True, timeout=600)        
        log.info(f'start scan')
        ts_pvs['FileName'].put(f"{base_name}_{letters[i]}",wait=True)         
        ts_pvs['NumAngles'].put(num_angles,wait=True)            
        ts_pvs['RotationStart'].put(rot_start[i%2],wait=True)
        ts_pvs['RotationStep'].put(rot_step[i%2],wait=True)
        ts_pvs['DarkFieldMode'].put('None',wait=True)
        ts_pvs['FlatFieldMode'].put('None',wait=True)                

        ts_pvs['StartScan'].put(1, wait=True, timeout=1200)
        ts_pvs['ProgramPSO'].put('No',wait=True)

        if i==1 and i_loop%flat_loops==0:
            log.info("Collect flat and dark")
            ts_pvs['DarkFieldMode'].put('Start',wait=True)
            ts_pvs['FlatFieldMode'].put('Start',wait=True)            
            ts_pvs['FileName'].put(f"{base_name}_flat_dark",wait=True)                     
            ts_pvs['NumAngles'].put(0,wait=True)

            ts_pvs['StartScan'].put(1, wait=True, timeout=1200)
    i_loop += 1
    pos_y = pos_y[::-1]    
    letters = letters[::-1]    
    rot_start = rot_start[::-1]    
    rot_step = rot_step[::-1]    

    load_motor = ts_pvs['LoadMotor'].get()
    load_motor_new = load_motor+load_step
    log.warning(f"Current load {ts_pvs['LoadValue'].get()}.")
    log.warning(f"Move load motor to {load_motor_new:.7f}. Load speed {ts_pvs['LoadMotorSpeed'].get()}.")
    ts_pvs['LoadMotor'].put(load_motor_new,wait=True)
    log.warning(f"New load {ts_pvs['LoadValue'].get()}.")    

