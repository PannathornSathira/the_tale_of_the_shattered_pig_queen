import pygame
from src.Util import SpriteManager, resource_path
from src.StateMachine import StateMachine

g_state_manager = StateMachine()

sprite_collection = SpriteManager().spriteCollection

background_dict = {
    "sea": pygame.image.load(resource_path("graphics/Backgrounds/Bg_Sea Level.JPG")),
    "forest": pygame.image.load(resource_path("graphics/Backgrounds/Bg_forest.JPG")),
    "sky": pygame.image.load(resource_path("graphics/Backgrounds/Bg_Sky.JPG")),
    "desert": pygame.image.load(resource_path("graphics/Backgrounds/Bg_Desert_New.PNG")),
    "castle": pygame.image.load(resource_path("graphics/Backgrounds/Bg_Last Level.PNG")),
    "sky_tutorial": pygame.image.load(resource_path("graphics/Backgrounds/sky_tutorial.png"))
}

tile_dict = {
    "sea": pygame.image.load(resource_path("graphics/platform/Sea Level.PNG")),
    "forest": pygame.image.load(resource_path("graphics/platform/Forest Level.PNG")),
    "sky": pygame.image.load(resource_path("graphics/platform/Sky Level.PNG")),
    "sand": pygame.image.load(resource_path("graphics/platform/Sand Level.PNG")),
    "castle": pygame.image.load(resource_path("graphics/platform/Last Level.PNG")),
    "special": pygame.image.load(resource_path("graphics/platform/Special.PNG")),
}

potion_dict = {
    "health": pygame.transform.scale(pygame.image.load(resource_path("graphics/shop/HP_potion2.PNG")), (30, 35)),
    "damage": pygame.transform.scale(pygame.image.load(resource_path("graphics/shop/damage_potion.PNG")), (30, 35)),
    "swiftness": pygame.transform.scale(pygame.image.load(resource_path("graphics/shop/swifness_potion.PNG")), (30, 35)),
}

shop_dict = {
    "health_potion": pygame.transform.scale(pygame.image.load(resource_path("graphics/shop/HP_potion2.PNG")), (50, 60)),
    "damage_potion": pygame.transform.scale(pygame.image.load(resource_path("graphics/shop/damage_potion.PNG")), (50, 60)),
    "swiftness_potion": pygame.transform.scale(pygame.image.load(resource_path("graphics/shop/swifness_potion.PNG")), (50, 60)),
    "hp_upgrade": pygame.transform.scale(pygame.image.load(resource_path("graphics/shop/Shop_HP.png")), (50, 50)),
    "def_upgrade": pygame.transform.scale(pygame.image.load(resource_path("graphics/shop/Shop_DEF.png")), (50, 50)),
    "shotgun_upgrade": pygame.transform.scale(pygame.image.load(resource_path("graphics/shop/Shop_Shotgun.png")), (50, 50)),
    "slow_upgrade": pygame.transform.scale(pygame.image.load(resource_path("graphics/shop/Shop_Slow.png")), (50, 50)),
    "speed_upgrade": pygame.transform.scale(pygame.image.load(resource_path("graphics/shop/Shop_SPD.png")), (50, 50)),
    "damage_upgrade": pygame.transform.scale(pygame.image.load(resource_path("graphics/shop/Shop_ATK.png")), (50, 50)),
    "2jump_upgrade": pygame.transform.scale(pygame.image.load(resource_path("graphics/shop/Shop_2Jump.png")), (50, 50)),
    "shop_continue": pygame.transform.scale(pygame.image.load(resource_path("graphics/shop/shop_continue.PNG")), (70, 70)),
}

gSounds = {
    'confirm': pygame.mixer.Sound(resource_path('sounds/common/confirm.wav')),
    'pause': pygame.mixer.Sound(resource_path('sounds/common/pause.wav')),
    'recover': pygame.mixer.Sound(resource_path('sounds/common/recover.wav')),
    'victory': pygame.mixer.Sound(resource_path('sounds/common/victory.wav')),
    'select': pygame.mixer.Sound(resource_path('sounds/common/select.wav')),
    'no-select': pygame.mixer.Sound(resource_path('sounds/common/no-select.wav')),
    'hit_player': pygame.mixer.Sound(resource_path('sounds/Mc/got hit.mp3')),
    'mc_gun': pygame.mixer.Sound(resource_path('sounds/Mc/gun.wav')),
    'mc_jump': pygame.mixer.Sound(resource_path('sounds/Mc/jump.wav')),
    'mc_potion': pygame.mixer.Sound(resource_path('sounds/Mc/potion drink.mp3')),
    'mc_change_gun': pygame.mixer.Sound(resource_path('sounds/Mc/change gun.wav')),
    'mc_shotgun': pygame.mixer.Sound(resource_path('sounds/Mc/shotgun.wav')),
    'mc_slow_motion': pygame.mixer.Sound(resource_path('sounds/Mc/slow motion.wav')),

    'kraken_bullet': pygame.mixer.Sound(resource_path('sounds/water stage/bullet sound.mp3')),
    'kraken_charge': pygame.mixer.Sound(resource_path('sounds/water stage/kraken charge.mp3')),
    'kraken_thunder': pygame.mixer.Sound(resource_path('sounds/water stage/thunder1.mp3')),

    'shark_missile': pygame.mixer.Sound(resource_path('sounds/water stage/missile sound.mp3')),
    'shark_missile_explode': pygame.mixer.Sound(resource_path('sounds/water stage/missile-explosion.wav')),
    'shark_vortex': pygame.mixer.Sound(resource_path('sounds/water stage/kraken charge.mp3')),
    'shark_rain': pygame.mixer.Sound(resource_path('sounds/water stage/rain.wav')),
    'shark_charge': pygame.mixer.Sound(resource_path('sounds/water stage/Shark Charge.mp3')),

    'medusa_arrow': pygame.mixer.Sound(resource_path('sounds/Forest stage/Medusa/arrow.wav')),
    'medusa_snake': pygame.mixer.Sound(resource_path('sounds/Forest stage/Medusa/snake.mp3')),
    'medusa_beam': pygame.mixer.Sound(resource_path('sounds/Forest stage/Medusa/fires beams.mp3')),

    'widow_cobweb': pygame.mixer.Sound(resource_path('sounds/Forest stage/BlackWidow/cobweb.mp3')),
    'widow_jump': pygame.mixer.Sound(resource_path('sounds/Forest stage/BlackWidow/jump.mp3')),
    'poison': pygame.mixer.Sound(resource_path('sounds/Forest stage/BlackWidow/poison.mp3')),
    'spiderling': pygame.mixer.Sound(resource_path('sounds/Forest stage/BlackWidow/Spiderling.mp3')),

    'dragon_bullet': pygame.mixer.Sound(resource_path('sounds/sky stage/bullet sound.mp3')),
    'dragon_ice': pygame.mixer.Sound(resource_path('sounds/sky stage/ice sound.mp3')),
    'dragon_ice_explode': pygame.mixer.Sound(resource_path('sounds/sky stage/ice explode.wav')),
    'dragon_stomp': pygame.mixer.Sound(resource_path('sounds/sky stage/Stomp.mp3')),
    'dragon_ice_pillar': pygame.mixer.Sound(resource_path('sounds/sky stage/ice pillar sound.wav')),

    'tornado_bullet': pygame.mixer.Sound(resource_path('sounds/sky stage/bullet sound.mp3')),
    'tornado_sound': pygame.mixer.Sound(resource_path('sounds/sky stage/tornado sound.mp3')),
    'tornado_beam': pygame.mixer.Sound(resource_path('sounds/sky stage/fires beams.mp3')),

    'sandworm_bullet': pygame.mixer.Sound(resource_path('sounds/Desert stage/SandBullet.mp3')),
    'sandworm_shockwave': pygame.mixer.Sound(resource_path('sounds/Desert stage/SandShockWave.mp3')),
    'sandworm_dash': pygame.mixer.Sound(resource_path('sounds/Desert stage/SandDashSound.mp3')),

    'mummy_sound': pygame.mixer.Sound(resource_path('sounds/Desert stage/SandMummySound.mp3')),
    'mummy_speed': pygame.mixer.Sound(resource_path('sounds/Desert stage/SandSpeedBoost.mp3')),
    'mummy_bandage_grab': pygame.mixer.Sound(resource_path('sounds/Desert stage/SandGrabSound.mp3')),

    'wraith_bullet': pygame.mixer.Sound(resource_path('sounds/Castle stage/CastleBossBullet.wav')),
    'wraith_spell': pygame.mixer.Sound(resource_path('sounds/Castle stage/CastleBossCastingSpell.mp3')),
    'wraith_teleport': pygame.mixer.Sound(resource_path('sounds/Castle stage/teleport.mp3')),
}

gMusic = {
    'main': pygame.mixer.Sound(resource_path('sounds/music/MainTheme.mp3')),
    'map': pygame.mixer.Sound(resource_path('sounds/music/MapTheme.mp3')),
    'shop': pygame.mixer.Sound(resource_path('sounds/music/ShopTheme.mp3')),
    'victory': pygame.mixer.Sound(resource_path('sounds/music/VictoryTheme.mp3')),
    'defeat': pygame.mixer.Sound(resource_path('sounds/music/DefeatTheme.mp3')),
    'kraken': pygame.mixer.Sound(resource_path('sounds/music/Kraken-music.mp3')),
    'greatshark': pygame.mixer.Sound(resource_path('sounds/music/Shark-music.mp3')),
    'blackwidow': pygame.mixer.Sound(resource_path('sounds/music/BlackWidow-music.wav')),
    'medusa': pygame.mixer.Sound(resource_path('sounds/music/Medusa-music.mp3')),
    'bluedragon': pygame.mixer.Sound(resource_path('sounds/music/Dragon-music.mp3')),
    'tornadofiend': pygame.mixer.Sound(resource_path('sounds/music/Tornado-music.mp3')),
    'mummy': pygame.mixer.Sound(resource_path('sounds/music/Mummy-music.mp3')),
    'sandworm': pygame.mixer.Sound(resource_path('sounds/music/SandWorm-music.mp3')),
    'wraith': pygame.mixer.Sound(resource_path('sounds/music/Wraith-music.mp3')),
}

gSounds["kraken_charge"].set_volume(0.7)
gSounds["shark_vortex"].set_volume(0.7)