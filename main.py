from kivy import clock
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty,NumericProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock  
from pipe import Pipe 
from random import randint
#Window.size = (400,800) 
class Background(Widget):
    cloud_texture = ObjectProperty(None)
    floor_texture = ObjectProperty(None)
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        #Create Texture
        #self.icon = "logo.png"
        #self.title = "Baishkeyar"
        self.cloud_texture = Image(source="cloud.png").texture
        self.cloud_texture.wrap = 'repeat'
        self.cloud_texture.uvsize = (Window.width/self.cloud_texture.width,-1)

        self.floor_texture = Image(source="floor.png").texture
        self.floor_texture.wrap = 'repeat'
        self.floor_texture.uvsize = (Window.width/self.floor_texture.width,-1)
    def scroll_texture(self,time_passed):
        #update the uvpos
        self.cloud_texture.uvpos=((self.cloud_texture.uvpos[0] + time_passed/2.0)%Window.width,self.cloud_texture.uvpos[1])
        self.floor_texture.uvpos=((self.floor_texture.uvpos[0] + time_passed/2.0)%Window.width,self.floor_texture.uvpos[1])

        #redraw the texture
        texture = self.property('cloud_texture')
        texture.dispatch(self)

        texture = self.property('floor_texture')
        texture.dispatch(self)
        
class Plane(Image):
    velocity = NumericProperty(0) 
    def on_touch_down(self, touch):
        self.source = "Plane.png"
        self.velocity  = 150
        super().on_touch_down(touch)
    def on_touch_up(self, touch):
        self.source = "Plane.png"
        super().on_touch_up(touch)    
class MainApp(App):
    pipes=[]
    GRAVITY = 300
    was_colliding = False
    #def on_start(self):
        #Clock.schedule_interval(self.root.ids.background.scroll_texture,1/60.)
    def move_plane(self,time_passed):
        plane = self.root.ids.plane
        plane.y = plane.y + plane.velocity * time_passed
        plane.velocity = plane.velocity - self.GRAVITY * time_passed 
        self.check_collision()
    def check_collision(self):
        plane = self.root.ids.plane
        is_colliding = False
        # check if it collides
        for pipe in self.pipes:
            if pipe.collide_widget(plane):
                is_colliding = True
                # Check if bird is between the gap
                if plane.y < (pipe.pipe_center - pipe.GAP_SIZE/2.0):
                    self.game_over()
                if plane.top > (pipe.pipe_center + pipe.GAP_SIZE/2.0):
                    self.game_over()
        if plane.y < 89:
            self.game_over()
        if plane.top > Window.height:
            self.game_over()    
        if self.was_colliding and not is_colliding:
            self.root.ids.score.text = str(int(self.root.ids.score.text) + 1 )  
        self.was_colliding = is_colliding           
    def game_over(self):
        self.root.ids.plane.pos = (20,(self.root.height - 89)/2.0)
        for pipe in self.pipes:
            self.root.remove_widget(pipe)
        self.frames.cancel()
        self.root.ids.start_button.disabled = False
        self.root.ids.start_button.opacity = 1

    def next_frame(self,time_passed):
        self.move_plane(time_passed)
        self.move_pipes(time_passed)
        self.root.ids.background.scroll_texture(time_passed)



    def start_game(self):
        self.root.ids.score.text = "0"
        self.was_colliding = False
        self.pipes = []
        #Clock.schedule_interval(self.move_plane,1/60.)
        #Create the pipes
        self.frames = Clock.schedule_interval(self.next_frame,1/60.)
        

        num_pipes = 3
        distance_between_the_pipes = Window.width / (num_pipes - 1) 
        for i in range(num_pipes):
            pipe = Pipe()
            pipe.pipe_center = randint(89 + 100, self.root.height - 100)
            pipe.size_hint = (None,None)
            pipe.pos = (Window.width+ i*distance_between_the_pipes,89)
            pipe.size = (57,self.root.height -89)
            
            self.pipes.append(pipe) 
            self.root.add_widget(pipe)

        

        #Move the pipes
        #Clock.schedule_interval(self.move_pipes,1/60.)
    def move_pipes(self,time_passed):
        for pipe in self.pipes:
            pipe.x -= time_passed * 100
        # check if we need to reposition the pipes at the right side 
        num_pipes = 3
        distance_between_the_pipes = Window.width / (num_pipes - 1)
        pipe_xs = list(map(lambda pipe: pipe.x , self.pipes)) 
        right_most_x = max(pipe_xs)
        if right_most_x <= Window.width - distance_between_the_pipes:
            most_left_pipe = self.pipes[pipe_xs.index(min(pipe_xs))]
            most_left_pipe.x = Window.width    
            
MainApp().run()
