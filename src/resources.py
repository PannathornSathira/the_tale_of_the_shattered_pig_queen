import pygame
from src.Util import SpriteManager
from src.StateMachine import StateMachine

g_state_manager = StateMachine()

sprite_collection = SpriteManager().spriteCollection

background_dict = {
    "sea": pygame.image.load("./graphics/Backgrounds/Bg_Sea Level.JPG"),
    "forest": pygame.image.load("./graphics/Backgrounds/Bg_forest.JPG"),
    "sky": pygame.image.load("./graphics/Backgrounds/Bg_Sky.JPG"),
    "desert": pygame.image.load("./graphics/Backgrounds/Bg_Desert_New.PNG"),
    "castle": pygame.image.load("./graphics/Backgrounds/Bg_Last Level.PNG")
}

tile_dict = {
    "sea": pygame.image.load("./graphics/platform/Sea Level.PNG"),
    "forest": pygame.image.load("./graphics/platform/Forest Level.PNG"),
    "sky": pygame.image.load("./graphics/platform/Sky Level.PNG"),
    "sand": pygame.image.load("./graphics/platform/Sand Level.PNG"),
    "castle": pygame.image.load("./graphics/platform/Last Level.PNG"),
    "special": pygame.image.load("./graphics/platform/Special.PNG"),
}

potion_dict = {
    "health": pygame.transform.scale(pygame.image.load("./graphics/shop/HP_potion2.PNG"), (30, 35)),
    "damage": pygame.transform.scale(pygame.image.load("./graphics/shop/damage_potion.PNG"), (30, 35)),
    "swiftness": pygame.transform.scale(pygame.image.load("./graphics/shop/swifness_potion.PNG"), (30, 35)),
}

gSounds = {
    'confirm': pygame.mixer.Sound('sounds/common/confirm.wav'),
    'pause': pygame.mixer.Sound('sounds/common/pause.wav'),
    'recover': pygame.mixer.Sound('sounds/common/recover.wav'),
    'victory': pygame.mixer.Sound('sounds/common/victory.wav'),
    'select': pygame.mixer.Sound('sounds/common/select.wav'),
    'no-select': pygame.mixer.Sound('sounds/common/no-select.wav'),
    'hit_player': pygame.mixer.Sound('sounds/Mc/got hit.mp3'),
    'mc_gun': pygame.mixer.Sound('sounds/Mc/gun.wav'),
    'mc_jump': pygame.mixer.Sound('sounds/Mc/jump.wav'),
    'mc_potion': pygame.mixer.Sound('sounds/Mc/potion drink.mp3'),
    'mc_change_gun': pygame.mixer.Sound('sounds/Mc/change gun.wav'),
    'mc_shotgun': pygame.mixer.Sound('sounds/Mc/shotgun.wav'),
    'mc_slow_motion': pygame.mixer.Sound('sounds/Mc/slow motion.wav'),

    'kraken_bullet': pygame.mixer.Sound('sounds/water stage/bullet sound.mp3'),
    'kraken_charge': pygame.mixer.Sound('sounds/water stage/kraken charge.mp3'),
    'kraken_thunder': pygame.mixer.Sound('sounds/water stage/thunder1.mp3'),
    
    'shark_missile': pygame.mixer.Sound('sounds/water stage/missile sound.mp3'),
    'shark_missile_explode': pygame.mixer.Sound('sounds/water stage/missile-explosion.wav'),
    'shark_vortex': pygame.mixer.Sound('sounds/water stage/kraken charge.mp3'),
    'shark_rain': pygame.mixer.Sound('sounds/water stage/rain.wav'),
    'shark_charge': pygame.mixer.Sound('sounds/water stage/Shark Charge.mp3'),
    
    'medusa_arrow': pygame.mixer.Sound('sounds/Forest stage/Medusa/arrow.wav'),
    'medusa_snake': pygame.mixer.Sound('sounds/Forest stage/Medusa/snake.mp3'),
    'medusa_beam': pygame.mixer.Sound('sounds/Forest stage/Medusa/fires beams.mp3'),
    
    'widow_cobweb': pygame.mixer.Sound('sounds/Forest stage/BlackWidow/cobweb.mp3'),
    'widow_jump': pygame.mixer.Sound('sounds/Forest stage/BlackWidow/jump.mp3'),
    'poison': pygame.mixer.Sound('sounds/Forest stage/BlackWidow/poison.mp3'),
    'spiderling': pygame.mixer.Sound('sounds/Forest stage/BlackWidow/Spiderling.mp3'),
    
    'dragon_bullet': pygame.mixer.Sound('sounds/sky stage/bullet sound.mp3'),
    'dragon_ice': pygame.mixer.Sound('sounds/sky stage/ice sound.mp3'),
    'dragon_ice_explode': pygame.mixer.Sound('sounds/sky stage/ice explode.wav'),
    'dragon_stomp': pygame.mixer.Sound('sounds/sky stage/Stomp.mp3'),
    'dragon_ice_pillar': pygame.mixer.Sound('sounds/sky stage/ice pillar sound.wav'),
    
    'tornado_bullet': pygame.mixer.Sound('sounds/sky stage/bullet sound.mp3'),
    'tornado_sound': pygame.mixer.Sound('sounds/sky stage/tornado sound.mp3'),
    'tornado_beam': pygame.mixer.Sound('sounds/sky stage/fires beams.mp3'),
    
    'sandworm_bullet': pygame.mixer.Sound('sounds/Desert stage/SandBullet.mp3'),
    'sandworm_shockwave': pygame.mixer.Sound('sounds/Desert stage/SandShockWave.mp3'),
    'sandworm_dash': pygame.mixer.Sound('sounds/Desert stage/SandDashSound.mp3'),
    
    'mummy_sound': pygame.mixer.Sound('sounds/Desert stage/SandMummySound.mp3'),
    'mummy_speed': pygame.mixer.Sound('sounds/Desert stage/SandSpeedBoost.mp3'),
    'mummy_bandage_grab': pygame.mixer.Sound('sounds/Desert stage/SandGrabSound.mp3'),
    
    'wraith_bullet': pygame.mixer.Sound('sounds/Castle stage/CastleBossBullet.wav'),
    'wraith_spell': pygame.mixer.Sound('sounds/Castle stage/CastleBossCastingSpell.mp3'),
    'wraith_teleport': pygame.mixer.Sound('sounds/Castle stage/teleport.mp3'),
}

gMusic = {
    'main': pygame.mixer.Sound('sounds/music/MainTheme.mp3'),
    'map': pygame.mixer.Sound('sounds/music/MapTheme.mp3'),
    'shop': pygame.mixer.Sound('sounds/music/ShopTheme.mp3'),
    'victory': pygame.mixer.Sound('sounds/music/VictoryTheme.mp3'),
    'defeat': pygame.mixer.Sound('sounds/music/DefeatTheme.mp3'),
    'kraken': pygame.mixer.Sound('sounds/music/Kraken-music.mp3'),
    'greatshark': pygame.mixer.Sound('sounds/music/Shark-music.mp3'),
    'blackwidow': pygame.mixer.Sound('sounds/music/BlackWidow-music.wav'),
    'medusa': pygame.mixer.Sound('sounds/music/Medusa-music.mp3'),
    'bluedragon': pygame.mixer.Sound('sounds/music/Dragon-music.mp3'),
    'tornadofiend': pygame.mixer.Sound('sounds/music/Tornado-music.mp3'),
    'mummy': pygame.mixer.Sound('sounds/music/Mummy-music.mp3'),
    'sandworm': pygame.mixer.Sound('sounds/music/SandWorm-music.mp3'),
    'wraith': pygame.mixer.Sound('sounds/music/Wraith-music.mp3'),
}

# s_paddle_image_list = [sprite_collection["p_blue_1"].image, sprite_collection["p_green_1"].image,
#                      sprite_collection["p_red_1"].image, sprite_collection["p_purple_1"].image]

# paddle_image_list = [sprite_collection["p_blue_2"].image, sprite_collection["p_green_2"].image,
#                      sprite_collection["p_red_2"].image, sprite_collection["p_purple_2"].image]

# ball_image_list = [sprite_collection["blue_ball"].image, sprite_collection["green_ball"].image,
#                                 sprite_collection["red_ball"].image, sprite_collection["purple_ball"].image,
#                                 sprite_collection["gold_ball"].image, sprite_collection["gray_ball"].image,
#                                 sprite_collection["last_ball"].image]

# gFonts = {
#         'small': pygame.font.Font('./fonts/font.ttf', 24),
#         'medium': pygame.font.Font('./fonts/font.ttf', 48),
#         'large': pygame.font.Font('./fonts/font.ttf', 96)
# }


# brick_image_list = [sprite_collection["b_blue_1"].image, sprite_collection["b_blue_2"].image,
#                    sprite_collection["b_blue_3"].image, sprite_collection["b_blue_4"].image,
#                    sprite_collection["b_green_1"].image, sprite_collection["b_green_2"].image,
#                    sprite_collection["b_green_3"].image, sprite_collection["b_green_4"].image,
#                    sprite_collection["b_red_1"].image, sprite_collection["b_red_2"].image,
#                    sprite_collection["b_red_3"].image, sprite_collection["b_red_4"].image,
#                    sprite_collection["b_purple_1"].image, sprite_collection["b_purple_2"].image,
#                    sprite_collection["b_purple_3"].image, sprite_collection["b_purple_4"].image,
#                    sprite_collection["b_orange_1"].image, sprite_collection["b_orange_2"].image,
#                    sprite_collection["b_orange_3"].image, sprite_collection["b_orange_4"].image,
#                    sprite_collection["b_gray"].image]
