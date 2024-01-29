from tkinter import *
import random

HEIGHT = 500
WIDTH = 500
SPACE_SIZE = 20
GAME_SPEED = 100
SNAKE_COLOR = "GREEN"
BODY_SIZE = 2
FOOD_COLOR = "RED"


class Game:
    def __init__(self):
        # creating window
        self.window = Tk()
        self.window.title("SNAKE GAME")
        self.window.resizable(False, False)
        self.center_window()
        self.score = 0
        self.highscore = 0
        self.score_label = self.create_label()
        self.canvas = self.create_canvas()
        self.information_label()
        self.food = Food(self.canvas)
        self.snake = Snake(self.canvas)
        self.binding_keys()
        self.create_start_game()
        self.message_box()
        self.pause = False

    def update(self):
        if not self.pause:
            self.snake.snake_movement()
        if self.snake.check_self_collision() or self.snake.wall_collision():
            self.game_over()
            return

        food_position = self.food.position
        if self.snake.check_collision(food_position):
            self.score += 1
            self.update_score_label()
            if self.score > self.highscore:
                self.highscore += 1
                self.update_highscore()
            self.food.spawn_food()
        self.window.after(GAME_SPEED, self.update)

    def center_window(self):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - WIDTH) // 2
        y = (screen_height - HEIGHT) // 2
        self.window.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")

    def create_label(self):
        label_text = "scores: {} | highscore: {} ".format(self.score, self.highscore)
        label = Label(self.window, text=label_text,
                      font=("consolas", 15), fg="blue", bg="grey",
                      relief=RAISED, anchor='w', height=1)
        label.pack(fill=BOTH, side=TOP)
        return label

    def pause_action(self):
        self.pause = not self.pause

    def update_highscore(self):
        label_text = "scores: {} | highscore: {} ".format(self.score, self.highscore)
        self.score_label.config(text=label_text)

    def information_label(self):
        label = Label(self.window, text="snakes game by wilYoung7", font=('azure', 7, "bold italic"), anchor='center',
                      fg='aqua', height=1)
        label.configure(bg=self.canvas.cget("bg"))
        label.pack(side=BOTTOM, fill=BOTH)

    def create_canvas(self):
        canvas = Canvas(self.window, bg="black", width=WIDTH, height=421)
        canvas.pack(fill=BOTH, expand=True)

        return canvas

    def run(self):
        self.window.mainloop()

    def update_score_label(self):
        label_text = "scores: {} | highscore: {} ".format(self.score, self.highscore)
        self.score_label.config(text=label_text)

    def game_over(self):
        self.canvas.delete('all')
        game_over_label = Label(self.canvas, text="Game Over!", font=('consolas', 30, 'bold'), fg='red', bg='Black')
        game_over_label.pack(expand=True)
        restart_button = Button(self.canvas, text="Restart(press Enter)", font=('consolas', 20), fg='green'
                                , background='grey', command=lambda: self.restart_game())
        restart_button.pack(expand=True)
        self.game_over_label = game_over_label
        self.restart_button = restart_button

    def restart_game(self):
        self.canvas.delete("all")
        self.score = 0
        self.game_over_label.pack_forget()
        self.restart_button.pack_forget()
        self.update_score_label()
        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas)
        self.update()

    def create_start_game(self):
        button = Button(self.canvas, text='start(press space)', fg='green', bg='grey', font=('consolas', 20, 'bold')
                        , command=lambda: self.start_button())
        button.pack(side='top')

        self.button = button

    def start_button(self):
        self.update()
        self.button.pack_forget()
        self.message.pack_forget()

    def message_box(self):
        message = Message(self.canvas, text='You can press p to pause and resume the game')
        message.pack(side=TOP)
        self.message = message

    def binding_keys(self):
        self.window.bind("<Up>", lambda event: self.snake.changing_directions('Up'))
        self.window.bind("<Left>", lambda event: self.snake.changing_directions('Left'))
        self.window.bind("<Down>", lambda event: self.snake.changing_directions('Down'))
        self.window.bind("<Right>", lambda event: self.snake.changing_directions('Right'))
        self.window.bind("<Return>", lambda event: self.restart_game())
        self.window.bind("<space>", lambda event: self.start_button())
        self.window.bind('<p>', lambda event: self.pause_action())
        self.window.focus_set()


class Snake:
    def __init__(self, canvas):
        self.canvas = canvas
        self.body = [(100, 100), (90, 100), (80, 100)]
        self.direction = 'Right'
        # initializing the position of the snake on the canvas
        for x, y in self.body:
            self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags='snake')

        self.snake_movement()
        self.changing_directions(self.direction)

    def snake_movement(self):
        head = self.body[0]  # retrieves the coordinates of the head from body
        x, y = head
        if self.direction == 'Up':
            y -= SPACE_SIZE
        elif self.direction == 'Down':
            y += SPACE_SIZE
        elif self.direction == 'Left':
            x -= SPACE_SIZE
        elif self.direction == 'Right':
            x += SPACE_SIZE

        new_head = (x, y)
        self.body = [new_head] + self.body[:-1]
        self.canvas.delete('snake')
        for x, y in self.body:
            self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags='snake')

    def changing_directions(self, direction):
        if direction == 'Up' and self.direction != 'Down':
            self.direction = 'Up'
        elif direction == 'Down' and self.direction != 'Up':
            self.direction = 'Down'
        elif direction == 'Left' and self.direction != 'Right':
            self.direction = 'Left'
        elif direction == 'Right' and self.direction != 'Left':
            self.direction = 'Right'

    def check_collision(self, food_position):
        head = self.body[0]
        if head == food_position:
            self.grow()
            self.canvas.delete('food')
            return True
        return False

    def grow(self):
        tail = self.body[-1]
        x, y = tail
        if self.direction == 'Up':
            self.body.append((x, y + SPACE_SIZE))
        elif self.direction == 'Down':
            self.body.append((x, y - SPACE_SIZE))
        elif self.direction == 'Left':
            self.body.append((x + SPACE_SIZE, y))
        elif self.direction == 'Right':
            self.body.append((x - SPACE_SIZE, y))
        self.canvas.create_rectangle(*self.body[-1], *self.body[-1], fill=SNAKE_COLOR, tags='snake')

    def check_self_collision(self):
        head = self.body[0]
        if head in self.body[1:]:
            return True
        else:
            return False

    def wall_collision(self):
        head = self.body[0]
        x, y = head
        if x < 0 or x >= WIDTH:
            return True
        elif y < 0 or y >= 421:
            return True


class Food:

    def __init__(self, canvas):
        self.canvas = canvas
        self.position = None
        self.spawn_food()

    def spawn_food(self):
        max_x_position = WIDTH // SPACE_SIZE
        max_y_position = 421 // SPACE_SIZE
        x_grid = random.randint(0, max_x_position - 1)
        y_grid = random.randint(0, max_y_position - 1)

        x = x_grid * SPACE_SIZE
        y = y_grid * SPACE_SIZE

        self.position = (x, y)
        self.canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="red", tags='food')


if __name__ == "__main__":
    game = Game()
    game.run()
