import pygame
import json
from src.constants import *

def GenerateTiles(file_name, tile_width, tile_height, scale=3, colorkey=None):
    image = pygame.image.load(file_name)

    (img_width, img_height) = image.get_size()

    sheet_width = img_width//tile_width
    sheet_height = img_height//tile_height

    sheet_counter = 1
    tile_sheet = []

    for y in range(sheet_height):
        for x in range(sheet_width):
            tile = pygame.Surface((tile_width, tile_height))

            # surface, location, area of surface
            tile.blit(image, (0, 0), (x*tile_width, y*tile_height, tile_width, tile_height))

            # transparency
            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                tile.set_colorkey(colorkey, pygame.RLEACCEL)

            tile = pygame.transform.scale(
                tile, (tile_width * scale, tile_height * scale)
            )

            tile_sheet.append(tile)

            sheet_counter += 1

    return tile_sheet



class Animation:
    def __init__(self, images, idleSprite=None, looping=True, interval_time=0.15):
        self.images = images
        self.timer = 0
        self.index = 0
        if idleSprite is None:
            self.image = self.images[self.index]
        else:
            self.image = idleSprite
        self.idleSprite = idleSprite

        self.interval_time = interval_time

        self.looping = looping #default loop

        self.times_played = 0

    def Refresh(self):
        self.timer=0
        self.index = 0
        self.times_played=0

    def update(self, dt):
        # one time animation check (attacking)
        if self.looping is False and self.times_played>0:
            return

        self.timer = self.timer + dt

        if self.timer > self.interval_time:
            self.timer = self.timer % self.interval_time

            self.index = (self.index+1) % len(self.images)

            if self.index == 0:
                self.times_played += 1

        self.image = self.images[self.index]

    def Idle(self):
        self.image = self.idleSprite


class Sprite:
    def __init__(self, image, animation=None):
        self.image = image
        self.animation = animation


class SpriteManager:
    def __init__(self):
        self.spriteCollection = self.loadSprites(
            [
                "./sprite/King/KingFireGun.json",
                "./sprite/King/KingFireShotgun.json",
                "./sprite/King/KingSelectMap.json",
                "./sprite/Bosses/Kraken.json",
                "./sprite/Bosses/KrakenImage.json",
                "./sprite/Bosses/GreatShark.json",
                "./sprite/Bosses/GreatSharkImage.json",
                "./sprite/Bosses/KingMummy.json",
                "./sprite/Bosses/KingMummyImage.json",
                "./sprite/Bosses/BlackWidow.json",
                "./sprite/Bosses/BlackWidowImage.json",
                "./sprite/Bosses/Medusa.json",
                "./sprite/Bosses/MedusaImage.json",
                "./sprite/Bosses/BlueDragon.json",
                "./sprite/Bosses/BlueDragonImage.json",
                "./sprite/Bosses/TornadoFiend.json",
                "./sprite/Bosses/TornadoFiendImage.json",
                "./sprite/Bosses/SandWorm.json",
                "./sprite/Bosses/SandWormImage.json",
                "./sprite/Bosses/Wraith.json",
                "./sprite/Bosses/WraithImage.json",
            ]
        )

    def loadSprites(self, urlList, shrink_scale=1):
        resDict = {}
        for url in urlList:
            with open(url) as jsonData:
                data = json.load(jsonData)
                dic = {}

                if data["type"] == "animation":
                    for sprite in data["sprites"]:
                        images = []
                        # Load individual image files for animation frames
                        for image in sprite["images"]:
                            if "path" in image:
                                loaded_image = pygame.image.load(image["path"]).convert_alpha()
                                scale = image.get("scale", 1)  # Default scale to 1 if not specified
                                loaded_image = pygame.transform.scale(
                                    loaded_image,
                                    (loaded_image.get_width() * scale, loaded_image.get_height() * scale)
                                )
                                images.append(loaded_image)

                        # Load idle image if specified
                        idle_img = None
                        if "idle_image" in sprite:
                            idle_info = sprite["idle_image"]
                            idle_img = pygame.image.load(idle_info["path"]).convert_alpha()
                            idle_img = pygame.transform.scale(
                                idle_img,
                                (idle_img.get_width() * idle_info["scale"], idle_img.get_height() * idle_info["scale"])
                            )

                        # Looping flag
                        loop = sprite.get("loop", True)

                        dic[sprite["name"]] = Sprite(
                            None,
                            animation=Animation(images, idleSprite=idle_img, looping=loop, interval_time=sprite.get("interval_time", 0.15)),
                        )

                else:
                    # Handle loading non-animation sprites here (if needed)
                    for sprite in data["sprites"]:
                        try:
                            colorkey = sprite.get("colorKey")
                        except KeyError:
                            colorkey = None
                        try:
                            xSize = sprite['xsize']
                            ySize = sprite['ysize']
                        except KeyError:
                            xSize, ySize = data['size']

                        # Load individual image
                        dic[sprite["name"]] = Sprite(
                            pygame.image.load(sprite["path"]).convert_alpha(),
                        )
                    resDict.update(dic)
                    continue

                resDict.update(dic)

        return resDict



class SpriteSheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename)
            self.sheet = pygame.image.load(filename)
            if not self.sheet.get_alpha():
                self.sheet.set_colorkey((0, 0, 0))
        except pygame.error:
            raise SystemExit

    def image_at(self, x, y, scalingfactor, colorkey=None,
                 xTileSize=16, yTileSize=16):
        rect = pygame.Rect((x, y, xTileSize, yTileSize))
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return pygame.transform.scale(
            image, (xTileSize * scalingfactor, yTileSize * scalingfactor)
        )

def render_text(text, x, y, font, screen):
    """Render text at a given position."""
    text_surface = font.render(text, True, (0, 0, 0))  # Render text in black color
    screen.blit(text_surface, (x, y))
    
def read_saveFile():
    """Read the save file and return the data as a dictionary."""
    try:
        with open(SAVE_FILE_NAME, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return {}
    
def save_values(updated_values):
    """Update only the provided keys in the save file without overwriting other data."""
    try:
        # Load existing data from save file
        with open(SAVE_FILE_NAME, 'r') as file:
            data = json.load(file)
        
        # Update only the keys provided in updated_values
        data.update(updated_values)
        
        # Save the updated data back to the file
        with open(SAVE_FILE_NAME, 'w') as file:
            json.dump(data, file, indent=4)
    
    except (IOError, json.JSONDecodeError) as e:
        pass