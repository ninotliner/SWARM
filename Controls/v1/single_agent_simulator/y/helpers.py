import yaml
import numpy as np
import os
import matplotlib.pyplot as plt

def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def initialize_vehicle():
    config_path = os.path.join(os.path.dirname(__file__), "sim_config.yaml")
    config = load_config(config_path)
    height = config["dimensions"]["height"] / 1000  #mm -> m
    width = config["dimensions"]["width"] / 1000    #mm -> m
    depth = config["dimensions"]["depth"] / 1000    #mm -> m
    m = config["mass"]
    Ixx = 1/12*m*(height**2 + width**2)
    Iyy = 1/12*m*(height**2 + depth**2)
    Izz = 1/12*m*(width**2 + depth**2)

    vehicle_model = {
    "weight": config["mass"],
    "MoI Tensor" : np.array([[Ixx,0,0],
                            [0,Iyy,0],
                            [0,0,Izz]])
    }

    return vehicle_model

def initialize_states():
    config_path = os.path.join(os.path.dirname(__file__), "sim_config.yaml")
    config = load_config(config_path)
    #print(config)
    states = np.array(list(config["initial_states"].values()))
    return states

def initialize_time_state_matrix():
    config_path = os.path.join(os.path.dirname(__file__), "sim_config.yaml")
    config = load_config(config_path)
    t0_s = 0
    tf_s = config["runtime"]
    h_s = 1/config["frequency"]
    states = initialize_states()

    #time array
    t_s = np.arange(t0_s, tf_s, h_s)

    #position matrix
    x = np.zeros([np.size(states), np.size(t_s)])
    x[:, 0] = states
    
    return t_s, x

def initialize():
    vehicle_model = initialize_vehicle()
    t_s, x = initialize_time_state_matrix()
    config_path = os.path.join(os.path.dirname(__file__), "sim_config.yaml")
    config = load_config(config_path)
    h_s = 1/config["frequency"]

    return vehicle_model, t_s, h_s, x

def plot(t_s, x, waypoints):
    fig, axes = plt.subplots(4,3, figsize=(8,12))

    axes[0,0].plot(t_s,x[6,:])
    axes[0,0].set_title("Forward Velocity")
    axes[0,0].set_xlabel("Time [s]")
    axes[0,0].set_ylabel("u [m/s]")

    axes[0,1].plot(t_s,x[7,:])
    axes[0,1].set_title("Sideways Velocity")
    axes[0,1].set_xlabel("Time [s]")
    axes[0,1].set_ylabel("v [m/s]")

    axes[0,2].plot(t_s,x[8,:])
    axes[0,2].set_title("Vertical Velocity")
    axes[0,2].set_xlabel("Time [s]")
    axes[0,2].set_ylabel("w [m/s]")

    axes[1,0].plot(t_s,x[9,:])
    axes[1,0].set_title("Roll Rate")
    axes[1,0].set_xlabel("Time [s]")
    axes[1,0].set_ylabel("p [r/s]")

    axes[1,1].plot(t_s,x[10,:])
    axes[1,1].set_title("Pitch Rate")
    axes[1,1].set_xlabel("Time [s]")
    axes[1,1].set_ylabel("q [r/s]")

    axes[1,2].plot(t_s,x[11,:])
    axes[1,2].set_title("Yaw Rate")
    axes[1,2].set_xlabel("Time [s]")
    axes[1,2].set_ylabel("r [r/s]")

    axes[2,0].plot(t_s,x[0,:])
    if waypoints[0] is not None:
        axes[2,0].plot(t_s, np.ones(np.size(t_s))*waypoints[0], color='green')
    axes[2,0].set_title("X Position")
    axes[2,0].set_xlabel("Time [s]")
    axes[2,0].set_ylabel("x [m]")

    axes[2,1].plot(t_s,x[1,:])
    if waypoints[1] is not None:
        axes[2,1].plot(t_s, np.ones(np.size(t_s))*waypoints[1], color='green')
    axes[2,1].set_title("Y Position")
    axes[2,1].set_xlabel("Time [s]")
    axes[2,1].set_ylabel("y [m]")
    
    axes[2,2].plot(t_s,x[2,:])
    axes[2,2].set_title("Z Position")
    if waypoints[2] is not None:
        axes[2,2].plot(t_s, np.ones(np.size(t_s))*waypoints[2], color='green')
    axes[2,2].set_xlabel("Time [s]")
    axes[2,2].set_ylabel("z [m]")

    axes[3,0].plot(t_s,x[3,:])
    axes[3,0].set_title("Roll Angle")
    if waypoints[3] is not None:
        axes[3,0].plot(t_s, np.ones(np.size(t_s))*waypoints[3], color='green')
    axes[3,0].set_xlabel("Time [s]")
    axes[3,0].set_ylabel("phi [rad]")

    axes[3,1].plot(t_s,x[4,:])
    axes[3,1].set_title("Pitch Angle")
    if waypoints[4] is not None:
        axes[3,1].plot(t_s, np.ones(np.size(t_s))*waypoints[4], color='green')
    axes[3,1].set_xlabel("Time [s]")
    axes[3,1].set_ylabel("roh [rad]")

    axes[3,2].plot(t_s,x[5,:])
    axes[3,2].set_title("Yaw Angle")
    if waypoints[5] is not None:
        axes[3,2].plot(t_s, np.ones(np.size(t_s))*waypoints[5], color='green')
    axes[3,2].set_xlabel("Time [s]")
    axes[3,2].set_ylabel("psi [rad]")

    #create some space between plots
    plt.subplots_adjust(hspace=0.7)
    plt.subplots_adjust(wspace=0.3)

    # create a legend outside of the plots: green = desired, blue = actual
    plt.legend(['Actual', 'Desired'])


    #plt.tight_layout()
    #plt.savefig("simplots/sim4.png")
    plt.show()

    """
    #positions
    ax = plt.figure().add_subplot(projection='3d')
    ax.plot(pos_ang[0], pos_ang[1], pos_ang[2], label='parametric curve')
    ax.set_xlabel('X[m]')
    ax.set_ylabel('Y[m]')
    ax.set_zlabel('Z[m]')
    ax.set_title('3D Line Plot')

    plt.show()

    #angles
    fig, axes = plt.subplots(1,3, figsize=(10,6))

    axes[0].plot(t_s,pos_ang[3,:])
    axes[0].set_title("Roll Angle")
    axes[0].set_xlabel("Time [s]")
    axes[0].set_ylabel("phi [rad]")

    axes[1].plot(t_s,x[4,:])
    axes[1].set_title("Pitch Angle")
    axes[1].set_xlabel("Time [s]")
    axes[1].set_ylabel("roh [rad]")

    axes[2].plot(t_s,x[5,:])
    axes[2].set_title("Yaw Angle")
    axes[2].set_xlabel("Time [s]")
    axes[2].set_ylabel("psi [m/s]")

    plt.show()
    """

