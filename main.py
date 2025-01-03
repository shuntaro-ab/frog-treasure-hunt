import pyxel
import random

class FrogGame:
    def __init__(self):
        pyxel.init(256, 256)
        pyxel.window_title = "Frog Treasure Hunt"
        pyxel.load("frog_treasure.pyxres")
        self.treasure_count_options = [2, 5, 10]
        self.selected_treasure_count_index = 0
        self.reset_game(self.treasure_count_options[self.selected_treasure_count_index])
        pyxel.run(self.update, self.draw)

    def reset_game(self, treasure_count):
        self.state = "start"
        self.frog_x = 122
        self.frog_y = 193
        self.treasure_count = treasure_count
        self.selected_treasure = 0
        self.treasures = []
        self.generate_treasures()
        self.blink_counter = 0
        self.blink_flag = True

    def generate_treasures(self):
        if self.treasure_count == 2:
            start_x = (256 - (self.treasure_count * 73)) // 2
            self.treasures = [{"x": start_x + i * 128, "y": 25, "type": "miss"} for i in range(self.treasure_count)]
            self.treasures[random.randint(0, self.treasure_count - 1)]["type"] = "hit"
        elif self.treasure_count == 5:
            start_x = (256 - (self.treasure_count * 27)) // 5
            self.treasures = [{"x": start_x + i * 48, "y": 25, "type": "miss"} for i in range(self.treasure_count)]
            self.treasures[random.randint(0, self.treasure_count - 1)]["type"] = "hit"
        elif self.treasure_count == 10:
            start_x = (256 - (self.treasure_count * 17)) // 10
            self.treasures = [{"x": start_x + i * 24, "y": 25, "type": "miss"} for i in range(self.treasure_count)]
            self.treasures[random.randint(0, self.treasure_count - 1)]["type"] = "hit"

    def set_window(self, treasures):
        if treasures == 2:
            pyxel.bltm(0, 0, 0, 0, 0, 256, 256)
        elif treasures == 5:
            pyxel.bltm(0, 0, 0, 0, 256, 256, 256)
        elif treasures == 10:
            pyxel.bltm(0, 0, 0, 0, 512, 256, 256)

    def update(self):
        if self.state == "start":
            if pyxel.btnp(pyxel.KEY_LEFT):
                self.selected_treasure_count_index = max(0
                , self.selected_treasure_count_index - 1)
            elif pyxel.btnp(pyxel.KEY_RIGHT):
                self.selected_treasure_count_index = min(len(self.treasure_count_options) - 1, self.selected_treasure_count_index + 1)
            elif pyxel.btnp(pyxel.KEY_RETURN):
                self.reset_game(self.treasure_count_options[self.selected_treasure_count_index])
                self.state = "select"
        elif self.state == "select":
            if pyxel.btnp(pyxel.KEY_LEFT):
                self.selected_treasure = max(0, self.selected_treasure - 1)
            elif pyxel.btnp(pyxel.KEY_RIGHT):
                self.selected_treasure = min(self.treasure_count - 1, self.selected_treasure + 1)
            elif pyxel.btnp(pyxel.KEY_RETURN):
                self.state = "move"
        elif self.state == "move":
            target_x = self.treasures[self.selected_treasure]["x"]
            if abs(self.frog_x - target_x) > 1:
                if self.frog_x < target_x:
                    self.frog_x += 2
                elif self.frog_x > target_x:
                    self.frog_x -= 2
            else:
                self.frog_x = target_x
                if self.frog_y > self.treasures[self.selected_treasure]["y"] + 20:
                    self.frog_y -= 5
                else:
                    self.state = "reveal"
        elif self.state == "reveal":
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.reset_game(self.treasure_count_options[self.selected_treasure_count_index])
            self.blink_counter += 1
            if self.blink_counter % 10 == 0:
                self.blink_flag = not self.blink_flag

    def draw(self):
        pyxel.cls(0)
        if self.state == "start":
            pyxel.text(80, 100, "Select number of treasures", pyxel.COLOR_WHITE)
            for i, count in enumerate(self.treasure_count_options):
                color = pyxel.COLOR_YELLOW if i == self.selected_treasure_count_index else pyxel.COLOR_WHITE
                pyxel.text(98 + i * 30, 120, str(count), color)
            pyxel.text(90, 150, "Press ENTER to Start", pyxel.COLOR_WHITE)
        elif self.state == "select":
            self.set_window(self.treasure_count)
            for i, treasure in enumerate(self.treasures):
                pyxel.blt(treasure["x"], treasure["y"], 0, 0, 16, 16, 16, pyxel.COLOR_BLACK)
                if i == self.selected_treasure:
                    pyxel.blt(treasure["x"], treasure["y"] - 20, 0, 48, 0, 16, 16, pyxel.COLOR_BLACK)
            pyxel.blt(self.frog_x, self.frog_y, 0, 0, 0, 16, 16, pyxel.COLOR_BLACK)
        elif self.state == "move":
            self.set_window(self.treasure_count)
            for i, treasure in enumerate(self.treasures):
                pyxel.blt(treasure["x"], treasure["y"], 0, 0, 16, 16, 16, pyxel.COLOR_BLACK)
            pyxel.blt(self.frog_x, self.frog_y, 0, 0, 0, 16, 16, pyxel.COLOR_BLACK)
        elif self.state == "reveal":
            self.set_window(self.treasure_count)
            for i, treasure in enumerate(self.treasures):
                if i == self.selected_treasure:
                    if treasure["type"] == "hit":
                        pyxel.blt(treasure["x"], treasure["y"], 0, 16, 16, 16, 16, pyxel.COLOR_BLACK)
                        pyxel.text(90, 120, "You found a treasure!", pyxel.COLOR_YELLOW)
                    else:
                        if self.blink_flag:
                            pyxel.blt(treasure["x"], treasure["y"], 0, 32, 16, 16, 16, pyxel.COLOR_BLACK)
                        else:
                            pyxel.blt(treasure["x"], treasure["y"], 0, 48, 16, 16, 16, pyxel.COLOR_BLACK)
                        pyxel.text(90, 120, "You found a ghost!", pyxel.COLOR_RED)
                else:
                    pyxel.blt(treasure["x"], treasure["y"], 0, 0, 16, 16, 16, pyxel.COLOR_BLACK)
            for treasure in self.treasures:
                if treasure["type"] == "hit":
                    pyxel.blt(treasure["x"], treasure["y"], 0, 16, 16, 16, 16, pyxel.COLOR_BLACK)
            pyxel.blt(self.frog_x, self.frog_y, 0, 0, 0, 16, 16, pyxel.COLOR_BLACK)

FrogGame()
