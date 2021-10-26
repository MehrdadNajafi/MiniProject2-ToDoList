import random
import arcade
from arcade import check_for_collision

class Snake(arcade.Sprite):
    def __init__(self, w, h):
        arcade.Sprite.__init__(self)
        self.color = arcade.color.GREEN
        self.speed = 3
        self.width = 18
        self.height = 18
        self.center_x = w // 2
        self.center_y = h // 2
        self.r = 9
        self.change_x = 0
        self.change_y = 0
        self.score = 0
        self.body = []
        self.body.insert(0, [self.center_x, self.center_y])
    
    def draw(self):
        for body in self.body:
            arcade.draw_circle_filled(body[0], body[1], self.r, arcade.color.GREEN)

    def move(self, x_apple, y_apple):
        if self.center_x < x_apple:
            self.change_x = 1
        elif self.center_x > x_apple:
            self.change_x = -1
        elif self.center_x == x_apple:
            self.change_x = 0
        
        if self.center_y < y_apple:
            self.change_y = 1
        elif self.center_y > y_apple:
            self.change_y = -1
        elif self.center_y == y_apple:
            self.change_y = 0
        
        self.center_x += self.speed * self.change_x
        self.center_y += self.speed * self.change_y
        self.body.append([self.center_x, self.center_y])
        
        if len(self.body) > 1 :
            del self.body[0]

    def eat(self, object):
        if object == 'apple':
            self.score += 1
        
        elif object == 'pear':
            self.score += 2

        elif object == 'trap':
            self.score -= 1

    def create_body(self):
        self.body.append([self.body[-1][0], self.body[-1][1]])

class Apple(arcade.Sprite):
    def __init__(self, w, h):
        arcade.Sprite.__init__(self)
        self.color = arcade.color.RED
        self.width = 16
        self.height = 16
        self.center_x = random.randint(10, w -10)
        self.center_y = random.randint(10, h - 10)
        self.r = 8
    
    def draw(self):
        arcade.draw_circle_filled(self.center_x, self.center_y, self.r, self.color)

class Pear(arcade.Sprite):
    def __init__(self, w, h):
        arcade.Sprite.__init__(self)
        self.color = arcade.color.YELLOW
        self.width = 16
        self.height = 16
        self.r = 8
        self.center_x = random.randint(10, w -10)
        self.center_y = random.randint(10, h -10)

    def draw(self):
        arcade.draw_circle_filled(self.center_x, self.center_y, self.r, self.color)

class Trap(arcade.Sprite):
    def __init__(self, w, h):
        arcade.Sprite.__init__(self)
        self.color = arcade.color.DARK_BROWN
        self.width = 16
        self.height = 16
        self.r = 8
        self.center_x = random.randint(10, w - 10)
        self.center_y = random.randint(10, h -10)

    def draw(self):
        arcade.draw_circle_filled(self.center_x, self.center_y, self.r, self.color)

class UpperWall(arcade.Sprite):
    def __init__(self, w, h):
        arcade.Sprite.__init__(self)
        self.width = w
        self.center_x = w // 2
        self.center_y = h

class LowerWall(arcade.Sprite):
    def __init__(self, w):
        arcade.Sprite.__init__(self)
        self.width = w
        self.center_x = w // 2
        self.center_y = 0

class RightWall(arcade.Sprite):
    def __init__(self, w, h):
        arcade.Sprite.__init__(self)
        self.width = 1
        self.height = h
        self.center_x = w
        self.center_y = h // 2

class LeftWall(arcade.Sprite):
    def __init__(self, w, h):
        arcade.Sprite.__init__(self)
        self.width = 1
        self.height = h
        self.center_x = 0
        self.center_y = h // 2


class Game(arcade.Window):
    def __init__(self):
        arcade.Window.__init__(self, 800, 600, 'Snake Game')
        arcade.set_background_color(arcade.color.SAND)
        self.snake = Snake(800, 600)
        self.apple = Apple(800, 600)
        self.pear = Pear(800, 600)
        self.trap = Trap(800, 600)
        self.upper_wall = UpperWall(800, 600)
        self.lower_wall = LowerWall(800)
        self.right_wall = RightWall(800, 600)
        self.left_wall = LeftWall(800, 600)
        self.walls_list = [self.upper_wall, self.lower_wall, self.right_wall, self.left_wall]
        self.game_over = GameOver()
        self.flag = 0
    
    def on_draw(self):
        arcade.start_render()
        self.snake.draw()
        self.apple.draw()
        self.pear.draw()
        self.trap.draw()
        arcade.draw_text(text=f'Score: {self.snake.score}',start_x=0 ,start_y=600 - 50, width=800, font_size=20, align="center", color=arcade.color.BLACK)
        
        if self.flag == 1:
            self.game_over.on_draw()

    def on_update(self, delta_time: float):
        self.snake.move(self.apple.center_x, self.apple.center_y)
        
        for wall in self.walls_list:
            if check_for_collision(self.snake, wall):
                self.flag = 1

        if arcade.check_for_collision(self.snake, self.apple):
            self.snake.eat('apple')
            self.snake.create_body()
            self.apple = Apple(800, 600)
            print(self.snake.score)

        elif arcade.check_for_collision(self.snake, self.pear):
            self.snake.eat('pear')
            self.pear = Pear(800, 600)
            print(self.snake.score)
            self.snake.create_body()
            self.snake.create_body()

        elif arcade.check_for_collision(self.snake, self.trap):
            self.snake.eat('trap')
            if self.snake.score <= 0:
                self.flag = 1
            self.trap = Trap(800, 600)
            del self.snake.body[-1]
            print(self.snake.score)
    
    def on_key_release(self, key, modifires):
        if key == arcade.key.ESCAPE:
            self.game_over.exit_game()

class GameOver(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.SAND)
        arcade.set_viewport(0, 800 - 1, 0, 600 - 1)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text('Game Over', 800 // 2.4, 600 // 2, arcade.color.BLACK, 20, 20)
        arcade.draw_text("Press 'ESC' for exit", 800 // 2.4, 600 // 2.3, arcade.color.BLACK, 12, 12)

    def exit_game(self):
        arcade.finish_render()
        arcade.exit()


game = Game()
arcade.run()