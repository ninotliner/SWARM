from controllers.llc import LLC
from controllers.pid import PID
import yaml
import time
import os
import matplotlib.pyplot as plt
from config.constants import *
import numpy as np


def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def initialize_paths(base_dir):
    pid_params_path = os.path.join(base_dir, 'config', 'pid_params.yaml')
    llc_config_path = os.path.join(base_dir, 'config', 'llc_config.yaml')
    log_file_path = os.path.join(base_dir, 'log.txt')
    return pid_params_path, llc_config_path, log_file_path

def initialize_frequencies(file_path):
    #load frequencies from yaml file and return them
    with open(file_path, "r") as file:
        freqs = yaml.safe_load(file)
    planner_freq = freqs['planner_freq']
    loc_freq = freqs['loc_freq']
    imu_freq = freqs['imu_freq']
    llc_freq = freqs['llc_freq']
    return planner_freq, loc_freq, imu_freq, llc_freq

def initialize_time_steps(planner_freq, loc_freq, imu_freq, llc_freq):
    t_planner = 1 / planner_freq
    t_loc = 1 / loc_freq
    t_imu = 1 / imu_freq
    t_llc = 1 / llc_freq
    return t_planner, t_loc, t_imu, t_llc

def log_state(log_file, current_state, thrust_z, llc):
    log_file.write(f"Current Depth: {current_state['z']}, Current Depth Rate: {current_state['dz']}, "
                   f"Thrust in z direction: {thrust_z}, desired depth: {llc.depth_ctrl.desired_depth}, "
                   f"desired depth rate: {llc.depth_ctrl.desired_depth_rate}\n")

def update_current_state(current_state, thrust_z, torque_y, t_llc):
    current_state['z'] += current_state['dz'] * t_llc
    current_state['dz'] += thrust_z * t_llc
    current_state['roll'] += current_state['droll'] * t_llc
    current_state['droll'] += torque_y * t_llc



def plot_results(times, detectable_rolls, rolls, llc):
    plt.figure()
    plt.plot(times, detectable_rolls, label='Detectable Roll')
    plt.legend()
    plt.figure()
    plt.plot(times, rolls, label='Roll')
    plt.xlabel('Time (ms)')
    plt.ylabel('Roll (degrees)')
    plt.title('Roll over Time')
    plt.grid(True)

    plt.figure()
    plt.plot(times, llc.depth_ctrl.detectable_depths, label='Detectable Depth')
    plt.legend()
    plt.figure()
    plt.plot(times, llc.depth_ctrl.depths, label='Depth')
    plt.xlabel('Time (ms)')
    plt.ylabel('Depth (m)')
    plt.title('Depth over Time')
    plt.grid(True)
    plt.show()

def append_state(array, x=0, y=0, z=0, roll=0, pitch=0, yaw=0, dx=0, dy=0, dz=0, droll=0, dpitch=0, dyaw=0):
    # Create a dictionary with 6-DOF and derivatives
    new_row = {
        'x': x, 'y': y, 'z': z,
        'roll': roll, 'pitch': pitch, 'yaw': yaw,
        'dx': dx, 'dy': dy, 'dz': dz,
        'droll': droll, 'dpitch': dpitch, 'dyaw': dyaw
    }
    
    # Append the new row (dictionary) to the NumPy array
    array = np.append(array, new_row)
    
    return array