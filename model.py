"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
import pickle
import numpy as np
from mlgame.communication import ml as comm
import os.path as path

def ml_loop(side: str):
    """
    The main loop for the machine learning process

    The `side` parameter can be used for switch the code for either of both sides,
    so you can write the code for both sides in the same script. Such as:
    ```python
    if side == "1P":
        ml_loop_for_1P()
    else:
        ml_loop_for_2P()
    ```

    @param side The side which this script is executed for. Either "1P" or "2P".
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here
    ball_served = False
    filename = path.join(path.dirname(__file__),"clf_svr.pickle")
    with open(filename, 'rb') as file:
        clf = pickle.load(file)

    # 2. Inform the game process that ml process is ready
    comm.ml_ready()

    s = [93,93]
    def get_direction(ball_x,ball_y,ball_pre_x,ball_pre_y):
        VectorX = ball_x - ball_pre_x
        VectorY = ball_y - ball_pre_y
        if(VectorX>=0 and VectorY>=0):
            return 0
        elif(VectorX>0 and VectorY<0):
            return 1
        elif(VectorX<0 and VectorY>0):
            return 2
        elif(VectorX<0 and VectorY<0):
            return 3
        

    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.recv_from_game()
        feature = []
        feature.append(scene_info["ball"][0])
        feature.append(scene_info["ball"][1])
        feature.append(scene_info['ball_speed'][0])
        feature.append(scene_info['ball_speed'][1])
        feature.append(scene_info["blocker"][0])

        feature = np.array(feature)
        feature = feature.reshape((-1,5))
        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info["status"] != "GAME_ALIVE":
            # Do some stuff if needed
            ball_served = False

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information

        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_to_game({"frame": scene_info["frame"], "command": "SERVE_TO_LEFT"})
            ball_served = True
        else:
                
            y = clf.predict(feature)
            # print(y)
            
            if scene_info['platform_1P'][0]+20 == y:
                comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
                # print('NONE')
            elif scene_info['platform_1P'][0]+20 > y:
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
                # print('LEFT')
            else:
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
                # print('RIGHT')