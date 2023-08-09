from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
#from datetime import datetime
#from kivy.storage.jsonstore import JsonStore
#Video
import cv2
from kivy.uix.image import Image
from kivy.graphics.texture import Texture



class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball, paddle):
        if self.collide_widget(ball):
            ball.velocity_y *= -1
            ball.velocity_y += 0.2
            ball.velocity_x += 0.2
            paddle.score += 1


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    paddle = ObjectProperty(None)

    def serve_ball(self):
        self.ball.velocity = Vector(0, 10).rotate(randint(0, 360))

    def update(self, dt):
        self.ball.move()
        if self.ball.y < 0:
            self.ball.velocity_y *= -1
            self.paddle.score -= 1
        if self.ball.y > self.height - 150:
            self.ball.velocity_y *= -1
        if (self.ball.x < 10) or (self.ball.x > self.width - 60):
            self.ball.velocity_x *= -1
        self.paddle.bounce_ball(self.ball, self.paddle)
        global loc
        self.paddle.center_x = int((self.width / 520) *(520- loc))

    #def on_touch_move(self, touch):
        #self.paddle.center_x = touch.x

    #def build_lists(self):
        #self.ids.spinner_id.values = lst
        #print(lst)


    #def close_application(self):
        # closing application
        #end = datetime.now()
        #end = str(end)
        #date = end[:10]
        #end = end[len(end) - 15:]
        #minutes = str(int(end[3:5]) - int(start[3:5]))
        #final =date + "," +" Time: " + minutes+ "min, score: "+ str(self.paddle.score)

        #if (datetime.now()).weekday() == 0:
            #store['0'] = {'Monday': final}
        #elif (datetime.now()).weekday() == 1:
            #store['1'] = {'Tuesday': final}
        #elif (datetime.now()).weekday() == 2:
            #store['2'] = {'Wednesday': final}
        #elif (datetime.now()).weekday() == 3:
            #store['3'] = {'Thursday': final}
        #elif (datetime.now()).weekday() == 4:
            #store['4'] = {'Friday': final}
        #elif (datetime.now()).weekday() == 5:
            #store['5'] = {'Saturday': final}
        #elif (datetime.now()).weekday() == 6:
            #store['6'] = {'Sunday': final}
        #App.get_running_app().stop()




class PingApp(App):
    def build(self):
        # Video
        global loc
        loc =0
        self.image = Image()
        self.face_facade = cv2.CascadeClassifier("haarcascade_frontal_face.xml")
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.load_video, 1.0 / 30.0)

        #Game

        game = PongGame()
        game.serve_ball()
        #global start
        #start = datetime.now()
        #start = str(start)
        #start = start[len(start) - 15:]
        #global store
        #store = JsonStore('LOG.json')
        #global lst
        #lst = []
        #for i in store:
            #for j in store[i]:
                #lst.append(str(store[i][j]))
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

    def load_video(self, *args):
        ret, frame = self.capture.read()
        #frame initialize
        self.image_frame = frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        object = self.face_facade.detectMultiScale(gray, 1.3, 4)
        for (x, y, w, h) in object:
            global loc
            loc = x
            cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 5)
            #print(x,y)
        buffer = cv2.flip(gray, -1).tobytes()
        texture = Texture.create(size=(gray.shape[1], gray.shape[0]), colorfmt = 'luminance')
        texture.blit_buffer(buffer, colorfmt='luminance', bufferfmt='ubyte')
        self.root.ids.vid.texture = texture

if __name__ == '__main__':
    PingApp().run()