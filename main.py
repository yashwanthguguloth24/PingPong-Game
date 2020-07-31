from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty,ReferenceListProperty,ObjectProperty,ListProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.graphics import Color


class PongPaddle(Widget):
    score = NumericProperty(0)
    def bounce_ball(self, ball):
        # inbuilt in kivy -> collide_widget
        if self.collide_widget(ball):
            ball.velocity_x *= -1.1


class PongBall(Widget):
    # numerical property is an number that can be understood by java like int and similar list property too
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x,velocity_y)
    color = ListProperty((1, 1, 1, 1))

    # latest pos = current velocity + current pos
    def move(self):
        # velocity is a vector
        self.pos = Vector(*self.velocity) + self.pos


# on_touch_down() - when our fingers/mouse touches the screen
# on_touch_up() - when we lift our finger off the screen after touching it
# on_touch_move() - when we drag our finger on the screen


# updates movement by calling move() every time
class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)


    def serve_ball(self):
        self.ball.velocity = Vector(4,0).rotate(randint(0,360))


    def update(self,dt):
        self.ball.move()
        # we need to check if ball is going out if it does we need to bounce it
        if (self.ball.y < 0) or (self.ball.y > self.height - 50):
            self.ball.velocity_y *= -1
            self.ball.color = (1, 0, 0, 1)

        # bounce of left
        if self.ball.x < 0:
            self.ball.velocity_x *= -1
            self.ball.color = (0, 1, 0, 1)
            self.player1.score += 1

        # bounce of right
        if self.ball.x > self.width - 50:
            self.ball.velocity_x *= -1
            self.ball.color = (0, 1, 0, 1)
            self.player2.score += 1

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)


    def on_touch_move(self,touch):
        if touch.x < self.width * 1/4:
            self.player1.center_y = touch.y
        if touch.x >  self.width * 3/4:
            self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, (1.0/60.0))           #60 fps
        return game


PongApp().run()
