import arcade
import random
ScreenWidth = 800
ScreenHeight = 600
ScreenTitle = "Space Shooter"
Scaling = 1.0

class FlyingSprite(arcade.Sprite):
    def update(self):
        super().update()
        if self.right < 0:
            self.remove_from_sprite_lists()
            
class otherFlyingSprite(arcade.Sprite):
    def update(self):
        super().update()
        if self.left > ScreenWidth:
            self.remove_from_sprite_lists()
            
class Shooter(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        
        #lots and lots of variables to be set up
    
        self.enemy_list = arcade.SpriteList()
        self.star_list = arcade.SpriteList()
        self.planet_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()
        self.lifebar_list = arcade.SpriteList()
        self.laser_list = arcade.SpriteList()
        self.pickup_list = arcade.SpriteList()
        self.collisionsound1 = arcade.load_sound("sounds/explosion1.wav")
        self.collisionsound2 = arcade.load_sound("sounds/explosion2.wav")
        self.bgmusic = arcade.load_sound("sounds/space.wav")
        self.lasersound = arcade.load_sound("sounds/laser.wav")
        self.titlemusic = arcade.load_sound("sounds/title.wav")
        self.powerupsound = arcade.load_sound("sounds/powerup.wav")
        self.lives = 3
        self.paused = bool()
        self.gamestarted = bool()
        self.gameover = bool()
        self.gamestarted = False
        self.score = int()
        self.highscore = int()
        
        hiscoreFile = open("files/highscore.txt")
        for value in hiscoreFile:
            self.highscore = int(value)
        hiscoreFile.close()
       
    def add_enemy(self, delta_time : float):
        enemy = FlyingSprite("images/enemy.png", 0.15)
        enemy.left = random.randint(self.width, self.width + 80)
        enemy.top = random.randint(10, self.height)
        enemy.velocity = (random.randint(-13, -6), 0)
        #the velocity attribute of any sprite has an x and a y value, expressed as a list
        self.enemy_list.append(enemy)
        self.all_sprites.append(enemy)
        
    def add_star(self, delta_time : float):
        star = FlyingSprite("images/star.png", random.uniform(0.01, 0.0175))
        star.left = random.randint(self.width, self.width + 80)
        star.top = random.randint(10, self.height - 10)
        star.velocity = (random.randint(-12, -2), 0)
        #the velocity attribute of any sprite has an x and a y value, expressed as a list
        self.star_list.append(star)
        self.all_sprites.append(star)
        
    def add_laser(self):
        if self.gamestarted==True:
            laser = otherFlyingSprite("images/laser.png", 0.025)
            laser.center_x = self.player.center_x + 5
            laser.center_y = self.player.center_y
            laser.velocity = (+10, 0)
            self.lasersound.play(volume = 0.075)
            self.laser_list.append(laser)
            self.all_sprites.append(laser)

    def add_pickup(self, delta_time : float):
        if self.lives != 3:
            pickup = FlyingSprite("images/health.png", 0.09)
            pickup.left = random.randint(self.width, self.width + 80)
            pickup.top = random.randint(10, self.height)
            pickup.velocity = (-5, 0)
            #the velocity attribute of any sprite has an x and a y value, expressed as a list
            self.pickup_list.append(pickup)
            self.all_sprites.append(pickup)
                    
    def planetsetup(self):
        planetnumber = random.randint(1, 4)
        if planetnumber == 1:
            planet = FlyingSprite("images/planet1.png", random.uniform(0.05, 0.125))
            return planet
        elif planetnumber == 2:
            planet = FlyingSprite("images/planet2.png", random.uniform(0.05, 0.125))
            return planet
        elif planetnumber == 3:
            planet = FlyingSprite("images/planet3.png", random.uniform(0.05, 0.125))
            return planet
        else:
            planet = FlyingSprite("images/planet4.png", random.uniform(0.05, 0.125))
            return planet
        
    def add_planet(self, delta_time : float):
        planet = self.planetsetup()
        planet.left = random.randint(self.width, self.width + 80)
        planet.top = random.randint(10, self.height - 10)
        planet.velocity = (random.randint(-5, -1), 0)
        #the velocity attribute of any sprite has an x and a y value, expressed as a list
        self.planet_list.append(planet)
        self.all_sprites.append(planet)
        
    def lifebarsetup(self):
        self.life1 = arcade.Sprite("images/lifebar1.png", 1.5)
        self.life2 = arcade.Sprite("images/lifebar2.png", 1.5)
        self.life3 = arcade.Sprite("images/lifebar3.png", 1.5)
        self.life1.left = 0
        self.life2.left = 0
        self.life3.left = 0
        self.life1.bottom = 0
        self.life2.bottom = 0
        self.life3.bottom = 0
        
    def titlesetup(self):
        self.score = 0
        arcade.set_background_color(arcade.color.BLACK)
        self.title = arcade.Sprite("images/title.png", 1)
        self.all_sprites.append(self.title)
        self.title.center_x = self.width / 2 
        self.title.center_y = self.height / 2
        arcade.schedule(self.add_star, 0.1)
        arcade.schedule(self.add_planet, 1.5)
        self.titlemusic.play(volume = 0.125)
        
    def setup(self):
        self.player = arcade.Sprite("images/player.png", 0.15)
        if self.gamestarted == True:
            self.lives = 3
            self.score = 0
            self.titlemusic.stop()
            self.all_sprites.append(self.player)
            self.lifebarsetup()
            self.player.center_y = self.height / 2
            self.player.left = 10
            arcade.schedule(self.add_enemy, 0.35)
            arcade.schedule(self.add_pickup, 10)
            self.bgmusic.play(volume = 0.175)
        
    def on_draw(self):
        arcade.start_render()
        self.star_list.draw()
        self.planet_list.draw()
        self.title.draw()
        self.enemy_list.draw()
        self.pickup_list.draw()
        if self.gamestarted==True:
            self.laser_list.draw()
            self.player.draw()
            arcade.draw_text("SCORE: " + str(self.score), 0, ScreenHeight, arcade.color.WHITE, 20, anchor_x = "left", anchor_y = "top", font_name = 'fonts/scorefont2.ttf')
            arcade.draw_text("HI-SCORE: " + str(self.highscore), ScreenWidth, ScreenHeight, arcade.color.WHITE, 20, anchor_x = "right", anchor_y = "top", font_name = 'fonts/scorefont2.ttf')
            if self.lives == 3:
                self.life3.draw()
            elif self.lives == 2:
                self.life2.draw()
            elif self.lives == 1:
                self.life1.draw()
        if self.gameover == True:
            self.gameovertext.draw()
            
    def on_key_press(self, keypressed, modifier):
        if keypressed==arcade.key.W or keypressed==arcade.key.UP:
            self.player.change_y = 5
        if keypressed==arcade.key.S or keypressed==arcade.key.DOWN:
            self.player.change_y = -5
        if keypressed==arcade.key.A or keypressed==arcade.key.LEFT:
            self.player.change_x = -5
        if keypressed==arcade.key.D or keypressed==arcade.key.RIGHT:
            self.player.change_x = 5
            
        if keypressed==arcade.key.Q:
            arcade.close_window()
        if keypressed==arcade.key.P:
            if self.paused == False:
                arcade.unschedule(self.add_enemy)
                arcade.unschedule(self.add_star)
                arcade.unschedule(self.add_planet)
                arcade.unschedule(self.add_pickup)
            else:
                arcade.schedule(self.add_enemy, 0.35)
                arcade.schedule(self.add_star, 0.1)
                arcade.schedule(self.add_planet, 1.5)
                arcade.schedule(self.add_pickup, 10)
            self.paused = not self.paused
            
        if keypressed == arcade.key.SPACE:
            self.add_laser()
        
        if self.gamestarted == False:
            if keypressed==arcade.key.ENTER:
                self.gamestarted = True
                self.title.remove_from_sprite_lists()
                self.setup()
                
        if self.gameover == True:
            if keypressed == arcade.key.ENTER:
                self.gameover = False
                self.gameovertext.remove_from_sprite_lists()
                self.setup()
            if keypressed == arcade.key.ESCAPE:
                arcade.close_window()
    
    def on_update(self, delta_time):
        if self.paused:
            return
        
        if self.gamestarted == True:
            collisionlist = self.player.collides_with_list(self.enemy_list)
            
            if collisionlist:
                for thing in collisionlist:
                    thing.remove_from_sprite_lists()
                self.lives = self.lives - 1
                collisiondecider = random.randint(1,2)
                if collisiondecider == 1:
                    self.collisionsound1.play(volume = 0.05)
                else:
                    self.collisionsound2.play(volume = 0.05)
                if self.lives == 0:
                    self.player.remove_from_sprite_lists()
                    self.bgmusic.stop()
                    hiscore = open("files/highscore.txt", 'w')
                    hiscore.write(str(self.highscore))
                    hiscore.close()
                    self.game_over()
                    
                    
            pickupcollision = self.player.collides_with_list(self.pickup_list)
                    
            if pickupcollision:
                self.powerupsound.play(volume = 0.1)
                for pickup in pickupcollision:
                    pickup.remove_from_sprite_lists()
                if self.lives != 3:
                    self.lives = self.lives + 1
                    
                    
            
            for laser in self.laser_list:
                lasercollision = laser.collides_with_list(self.enemy_list)
                if lasercollision:
                    for thing in lasercollision:
                        thing.remove_from_sprite_lists()
                    collisiondecider = random.randint(1,2)
                    if collisiondecider == 1:
                        self.collisionsound1.play(volume = 0.05)
                    else:
                        self.collisionsound2.play(volume = 0.05)
                    laser.remove_from_sprite_lists()
                    self.score = self.score + 100
                    
            if self.score >= self.highscore:
                self.highscore = self.score
            
        self.all_sprites.update()
        
        if self.gamestarted == True:
            if self.player.top > self.height:
                self.player.top = self.height
            if self.player.bottom < 0:
                self.player.bottom = 0
            if self.player.right > self.width:
                self.player.right = self.width
            if self.player.left < 0:
                self.player.left = 0
            
    def on_key_release(self, keypressed, modifier):
        if keypressed==arcade.key.W or keypressed==arcade.key.UP or keypressed==arcade.key.S or keypressed==arcade.key.DOWN:
            self.player.change_y = 0
        if keypressed==arcade.key.A or keypressed==arcade.key.LEFT or keypressed==arcade.key.D or keypressed==arcade.key.RIGHT:
            self.player.change_x = 0
            
    def game_over(self):
        self.gameover = True
        self.gameovertext = arcade.Sprite("images/gameover.png", 0.75)
        self.all_sprites.append(self.gameovertext)
        self.gameovertext.center_x = self.width / 2 
        self.gameovertext.center_y = self.height / 2
        arcade.unschedule(self.add_enemy)
        arcade.unschedule(self.add_pickup)
        
app = Shooter(ScreenWidth, ScreenHeight, ScreenTitle)
app.titlesetup()
arcade.run()