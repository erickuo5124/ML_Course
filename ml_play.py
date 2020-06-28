class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0                            # speed initial
        self.car_pos = (0,0)                        # pos initial
        self.car_lane = self.car_pos[0] // 70       # lanes 0 ~ 8
        self.lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]  # lanes center
        pass

    def update(self, scene_info):
        
        if len(scene_info[self.player]) != 0:
            self.car_pos = scene_info[self.player]

        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]

        if scene_info["status"] != "ALIVE":
            return "RESET"
        self.car_lane = self.car_pos[0] // 70
        
        front = self.car_pos[1] - 40
        left = self.car_pos[0] - 20
        right = 630 - self.car_pos[0] - 20
        back = 800-self.car_pos[1]
        front_left = False
        front_right = False
        back_left = False
        back_right = False
        lane_dis = [self.car_pos[1]- 40] * 9

        for car in scene_info["cars_info"]:
            if car["id"] != self.player_no:
                x = self.car_pos[0] - car["pos"][0] # x relative position
                y = self.car_pos[1] - car["pos"][1] # y relative position

                if y < lane_dis[car["pos"][0]//70] and y > 0:
                    lane_dis[car["pos"][0]//70] = y

                if x <= 40 and x >= -40 :
                    if y > 0 and y < front: front = y
                    else: back = -y
                elif x < 0 :
                    if y > 80 and y < 250: front_right = True
                    elif y < -80 and y > -200: back_right = True
                    elif y < 200 and y > -80 and (-x) < right: right = -x
                elif x > 0:
                    if y > 80 and y < 250: front_left = True
                    elif y < -80 and y > -200: back_left = True
                    elif y < 200 and y > -80 and x < left: left = x
        
        max_dis_lane = self.car_lane 
        for i in range((self.car_pos[0]-left)//70+1, self.car_lane):
            if lane_dis[max_dis_lane] < lane_dis[i]:
                max_dis_lane = i
        for i in range((self.car_pos[0]+right)//70, self.car_lane, -1):
            if lane_dis[max_dis_lane] < lane_dis[i]:
                max_dis_lane = i
        
        if   lane_dis[self.car_pos[0]//70] < 200 and self.car_pos[0] - self.lanes[max_dis_lane] > 5  and  left > 5: return ["BRAKE", "MOVE_LEFT"]
        elif lane_dis[self.car_pos[0]//70] < 200 and self.car_pos[0] - self.lanes[max_dis_lane] < -5 and right > 5: return ["BRAKE", "MOVE_RIGHT"]
        elif lane_dis[self.car_pos[0]//70] < 200 : return["BRAKE"]
        elif self.car_pos[0] - self.lanes[max_dis_lane] > 5  and  left > 5: return ["SPEED", "MOVE_LEFT"]
        elif self.car_pos[0] - self.lanes[max_dis_lane] < -5 and right > 5: return ["SPEED", "MOVE_RIGHT"]
        else : return ["SPEED"]

    def reset(self):
        """
        Reset the status
        """
        pass