import pygame
import sys
import math
import json
import base64
import io
import os
import random

pygame.init()
pygame.mixer.init()
pygame.joystick.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60
FREEZE_DURATION = 5 * FPS
HITS_TO_FREEZE = 5
SLOWMO_SCALE = 0.4
SLOWMO_DURATION = 45
FREEZE_IMMUNITY = 2 * FPS
MAX_HEALTH = 3
MAX_SHOTS = 3
RELOAD_TIME = 2 * FPS

BLACK = (10, 10, 15)
WHITE = (240, 240, 240)
BLUE = (50, 120, 255)      
GREEN = (40, 200, 80)     
ORANGE = (255, 140, 0)     
RED = (230, 50, 50)
PURPLE = (160, 50, 230)
GOLD = (255, 215, 0)

RUN_PISKEL_JSON = {
    "modelVersion": 2,
    "piskel": {
        "name": "New Piskel",
        "description": "",
        "fps": 24,
        "height": 32,
        "width": 32,
        "layers": [
            '{"name":"Layer 1","opacity":1,"frameCount":3,"chunks":[{"layout":[[0],[1],[2]],"base64PNG":"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGAAAAAgCAYAAADtwH1UAAADB0lEQVR4AeyYAXLbMAwEifRJzXPa3/U5yZM6Ktejs2CUjARKctqMPLkBeATvSMKWM34p1+tTb2C9AdPbVLI48khZb+r/I//1BtTDTL9eS0Sl/+KogT8a6EbgETnG8EcD3Qg8IscYPoNNDWgJjpi1dEa5r+I/3IDRi7vWPd7A1YDH+3j6aFMD7GcpoPyYSg/Mg3LCC13Q84ZnHpxgfzv7TfuE829qQDyUmd0psyW/kycnZoun2ZKfbHuXN1s8zZb8XpBIhhqQ0L9KV25gqAHTVB9Fs7DPZ+r04D19frrxbOA9fT5Pp8JQA8zqx26GWc1TlvuLzarnDLOaZyV31ptVzxlmNd+hN9QA33Wf79hHaqn39HlKZEex9/T5iOS2Bkxvpf4cUay8L6icgZlj/oaRXaytqT5of0X/pQH8htLC2uW05kd0WmvgWvprHOuE+tap5XxptVCn5j/V+/hSv+y+fS8lA+S8hnL4BpYGNCZvxpHXZuB7OXNHAP2oAwfgiSDmjD34BDEmAvKt+P1eSgRr4YjA54wT+LgBEuKQQGPFHcaS2BTxBrF4q7+91s9BfYxqfbYJeAvSIG71p7aDbQ3ACHgRNsQ48nBHAw/gdUf8aYTgtdZyvAXVjvhrrYvbGqAFMtVYscdr/qjY8+nx8n18x1ulhZom/vABcUmLizWd8bYGyIB3QUfoVHqv/8i73h/I+x98B+sNkDkRxI1Fzs8fkUufCLwmY+A5cnu1IpT6n/MjSuolfaIggTgWn4jrDUiIXaX5G3hiA/Kb+/QVBz9uWudpN4CPL9VsIAvW7cVn+2v/PGJOPv/SAA4t+A2wiQjmI8cYXhoxMvcRfL3q0GyB+R6PDvNZsM5D63s+Pd5r+Fx6IS4NCBPX8Dk3cDWAe9bvNT7C9x4/vTl4rxFz5gOuBuhCWo+UFpetl4bWhXg1QBfSe7dHPluv9VoX4tUALsR/WZ6Z4xVwNSBcyLOHuQb0Pk49/ujT9Hx6/NH+J+h93AAdTNFvQBzR80fmaHt47R7va/6BfG0LfwAAAP//ClaxhgAAAAZJREFUAwCsmZx3UIhvJQAAAABJRU5ErkJggg=="}]}'
        ]
    }
}

SHOOT_PISKEL_JSON = {
    "modelVersion": 2,
    "piskel": {
        "name": "Shooting",
        "description": "",
        "fps": 0,
        "height": 32,
        "width": 32,
        "layers": [
            '{"name":"Layer 1","opacity":1,"frameCount":1,"chunks":[{"layout":[[0]],"base64PNG":"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABe0lEQVR4AexUAXLEIAiE9knNc9rf9Tl3T+pY1oNIjJ7itNPezGWyAVeEFZO80B9fYwHpkiiKwKbGAiRZ+tyohtAnDjHgI5gS0Eq4UqyVZ1lAK9kK9xgC+IMIoPdEPWAeoOC11AFm3sswF38nA86SgED+YeiSgJTkKDS195UKmSUBzNJ2BbP4oZLH4CUBftfeP6aeG80JSBeS3zExXQuEY0A5zGfM1d2jioDe/34PDTg+l0iXlXhpWqAiQKJO9+vbiSJwAGZggdrH2EM6lYewQB7cHvcF3GLoUNQ42K8rnmPwJn2QY7RIJ2JOAAoBlgDWdl7zmOsBQgwaMydAg3MnzPfWxHjO+27HQrPD4B2QyHxbgchu80J9VLtWNptxB6w4LJCX6QNjQIe74Y3JQPLlHkH+Ggvw0b/g/1MBaB92izOPAusCKB1AUYMlwPm2gPkejxyYn0QRMLngp8OeAp4deLAO2D+h/hR6fB3XGN/vgCU26xMYB+v5yh8NvwEAAP//RB0dtAAAAAZJREFUAwAcQMZNSfpDbAAAAABJRU5ErkJggg=="}]}'
        ]
    }
}

def load_piskel_from_dict(piskel_dict):
    layer_str = piskel_dict["piskel"]["layers"][0]
    layer_data = json.loads(layer_str)
    b64_string = layer_data["chunks"][0]["base64PNG"].split(",")[1]
    image_bytes = base64.b64decode(b64_string)
    return pygame.image.load(io.BytesIO(image_bytes)).convert_alpha()

ROLE_TINTS = {
    "TechnoBlade": (50, 150, 255),
    "Wizard": (255, 100, 130),
    "Dragon": (100, 200, 100),
}

def tint_surface(surf, role, is_player_two=False):
    """Colour a sprite for a class. Used by both the Player and the champion-select screen."""
    tinted = surf.copy()
    tinted.fill(ROLE_TINTS[role], special_flags=pygame.BLEND_ADD)
    if is_player_two and role != "Wizard":
        tinted.fill((80, 0, 80), special_flags=pygame.BLEND_ADD)
    return tinted

def load_b64_image(b64, scale=1):
    img = pygame.image.load(io.BytesIO(base64.b64decode(b64))).convert_alpha()
    if scale != 1:
        img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
    return img


class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y, image_b64):
        super().__init__()
        self.image = load_b64_image(image_b64, 2)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.home_pos = (x, y)
        self.carrier = None
        self.is_dropped = False

    def reset_to_home(self):
        self.carrier = None
        self.is_dropped = False
        self.rect.topleft = self.home_pos

    def update(self):
        if self.carrier:
            self.rect.centerx = self.carrier.rect.centerx
            self.rect.centery = self.carrier.rect.centery - 20

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, role="TechnoBlade", is_player_two=False, controller=None):
        super().__init__()
        self.role = role
        self.is_player_two = is_player_two
        self.controller = controller
        
        sprite_sheet = load_piskel_from_dict(RUN_PISKEL_JSON)
        self.frames = []
        for i in range(3):
            frame = sprite_sheet.subsurface((i * 32, 0, 32, 32))
            tinted = tint_surface(frame, role, is_player_two)
            self.frames.append(pygame.transform.scale(tinted, (64, 64)))

        shoot_surface = load_piskel_from_dict(SHOOT_PISKEL_JSON)
        tinted_shoot = tint_surface(shoot_surface, role, is_player_two)
        self.shoot_image = pygame.transform.scale(tinted_shoot, (64, 64))

        self.current_frame = 0
        self.anim_timer = 0
        self.facing_right = True
        self.shoot_timer = 0  
        
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.spawn = (x, y)
        
        self.vx = 0
        self.vy = 0
        self.normal_speed = 8 if role == "TechnoBlade" else (6 if role == "Wizard" else 5)
        self.gravity = 0.6
        self.jump_strength = -14 if role != "Dragon" else -11
        self.on_ground = False
        self.score = 0
        self.health = 3
        self.has_flag = False
        self.hit_count = 0
        self.freeze_timer = 0
        self.freeze_immunity = 0
        self.shots_left = MAX_SHOTS
        self.reload_timer = 0

    @property
    def is_frozen(self):
        return self.freeze_timer > 0

    def take_hit(self):
        self.health -= 1
        if self.is_frozen or self.freeze_immunity > 0:
            return
        self.hit_count += 1
        if self.hit_count >= HITS_TO_FREEZE:
            self.hit_count = 0
            self.freeze_timer = FREEZE_DURATION
            self.vx = 0

    def can_shoot(self):
        return not self.is_frozen and self.reload_timer == 0

    def trigger_shot(self):
        self.shoot_timer = 15
        self.shots_left -= 1
        if self.shots_left <= 0:
            self.reload_timer = RELOAD_TIME

    def handle_input(self):
        self.vx = 0
        if self.is_frozen:
            return
        current_speed = self.normal_speed * 0.75 if self.has_flag else self.normal_speed

        keys = pygame.key.get_pressed()
        if not self.is_player_two:
            if keys[pygame.K_a]:
                self.vx = -current_speed
                self.facing_right = False
            if keys[pygame.K_d]:
                self.vx = current_speed
                self.facing_right = True

            if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.on_ground:
                self.vy = self.jump_strength
                self.on_ground = False
        else:
            if not keys[pygame.K_RSHIFT]:
                if keys[pygame.K_LEFT]:
                    self.vx = -current_speed
                    self.facing_right = False
                if keys[pygame.K_RIGHT]:
                    self.vx = current_speed
                    self.facing_right = True

                if keys[pygame.K_UP] and self.on_ground:
                    self.vy = self.jump_strength
                    self.on_ground = False

            if self.controller:
                axis_x = self.controller.get_axis(0)
                if abs(axis_x) > 0.2:
                    self.vx = axis_x * current_speed
                    self.facing_right = axis_x > 0

                if self.controller.get_numhats() > 0:
                    hat = self.controller.get_hat(0)
                    if hat[0] < 0:
                        self.vx = -current_speed
                        self.facing_right = False
                    elif hat[0] > 0:
                        self.vx = current_speed
                        self.facing_right = True

    def update(self, platforms, jump_pads):
        if self.reload_timer > 0:
            self.reload_timer -= 1
            if self.reload_timer == 0:
                self.shots_left = MAX_SHOTS

        if self.freeze_timer > 0:
            self.freeze_timer -= 1
            self.vx = 0
            if self.freeze_timer == 0:
                self.freeze_immunity = FREEZE_IMMUNITY
        elif self.freeze_immunity > 0:
            self.freeze_immunity -= 1

        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for p in hit_list:
            if self.vx > 0:
                self.rect.right = p.rect.left
            elif self.vx < 0:
                self.rect.left = p.rect.right

        self.vy += self.gravity
        self.rect.y += self.vy
        self.on_ground = False

        hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for p in hit_list:
            if self.vy > 0:
                self.rect.bottom = p.rect.top
                self.vy = 0
                self.on_ground = True
            elif self.vy < 0:
                self.rect.top = p.rect.bottom
                self.vy = 0

        pad_hit_list = pygame.sprite.spritecollide(self, jump_pads, False)
        for pad in pad_hit_list:
            if self.vy > 0:
                self.rect.bottom = pad.rect.top
                self.vy = -24
                self.on_ground = False

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.top > SCREEN_HEIGHT + 200:
            self.rect.topleft = self.spawn
            self.vy = 0

        if self.shoot_timer > 0:
            self.shoot_timer -= 1
            img = self.shoot_image
        else:
            if self.vx != 0:
                self.anim_timer += 1
                if self.anim_timer >= 6:
                    self.anim_timer = 0
                    self.current_frame = (self.current_frame + 1) % len(self.frames)
            else:
                self.current_frame = 0
            img = self.frames[self.current_frame]

        if not self.facing_right:
            img = pygame.transform.flip(img, True, False)

        if self.is_frozen:
            img = img.copy()
            img.fill((90, 160, 255), special_flags=pygame.BLEND_RGB_ADD)
        elif self.freeze_immunity > 0 and (self.freeze_immunity // 6) % 2 == 0:
            img = img.copy()
            img.set_alpha(120)

        self.image = img

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color=GREEN):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

KILL_IMAGE_B64 = "iVBORw0KGgoAAAANSUhEUgAAACAAAAATCAYAAADxlA/3AAAAg0lEQVR42uVWWwrAIAxLRu9/5exrMJy1E0bzsYIgxZKYxgclCcYIAADpQZdwwBwPAjMtOMzHUdWv8lExHAt1y+szDyyA1d2CTvCUQBf4kgCdBNRIomwBXQS6fBBvFjFRJDstTDYxu1OiMp42VdFmPhxH77UHfkEgrnfZpgDp+o0AJHkCJJcZOx+Ntn0AAAAASUVORK5CYII="
FREEZE_IMAGE_B64 = "iVBORw0KGgoAAAANSUhEUgAAACAAAAASCAYAAAA6yNxSAAAAxklEQVR42sWWWxKAIAhFL+aO2v8SXFJDPzlTyENqGv2LRPAeYCQUZixcFQBwtIeRsYPQhs3SHn1Hdmz7lcC1SXPsSway9sl/nh8BKH/KS2jqxUYEt0wjB+1gzVcLPmIIEKjcAgTezTUENbrtjCJZ2VUEVvDMgV0xqVz3dxFkkpDMZ+tHQ0AozHysGUK0/dyGn2vAYqkNmGgiWng+dUHUjjPFW2cr2xuz2VZNtWGE425/k9CrIvT6PatGqggj+a354KlCqx8kJ05JY8muTMuOAAAAAElFTkSuQmCC"
FLAG_RED_B64 = "iVBORw0KGgoAAAANSUhEUgAAABYAAAAcCAYAAABlL09dAAAAsklEQVR42t2V2w7EIAhEGcP///Lsy7YhrqggTZMl8U3ODBdbSH1QRASnAC+wSIQH4hwIXShzy94gNJu4inbY5ylY5AF6M1ygUKANhooKOLJ76l206zZP4pwPYOhOt8oyzSEpAG7BXvi6q9vlkkfDm5ccGOv7jqMVaMbtjnuNOOzBvWMr2CLQEZDkfVI99vbW63eqFSPRNNg6tRBPcPkRiu7vVwit8lGUPJD/A9f8QX7XDR+wx0xILsA9yQAAAABJRU5ErkJggg=="
FLAG_BLUE_B64 = "iVBORw0KGgoAAAANSUhEUgAAABYAAAAcCAYAAABlL09dAAAAtUlEQVR42t2V0QrFIAxDE+n/f/LNfdlExE6thcEKe5snaU03Ir8EADwFeMXJQbqg4nB/BADaRFlTkFMWObRSBQAv++ngdjbpYFbnSQJlkJKU0TCaUzd6V9ymYOmZzzGCttRWc1gSSFbBXvh+15b3Vzq6vEfXJDc3703Hux1YxO2Ke9tx2IN7x61g2YGOgJLqE5qxl1tv3qFRjETD4NZpC/EEj78VTmcsmUuRsiDfA6f8QQZx4x+LPlQ/Bfe03wAAAABJRU5ErkJggg=="
kill_popups = pygame.sprite.Group()


class KillPopup(pygame.sprite.Sprite):
    LIFE = 75
    FADE = 25
    SCALE = 4

    def __init__(self, midtop, image_b64=KILL_IMAGE_B64):
        super().__init__()
        img = pygame.image.load(io.BytesIO(base64.b64decode(image_b64))).convert_alpha()
        self.base = pygame.transform.scale(img, (img.get_width() * self.SCALE, img.get_height() * self.SCALE))
        self.x = midtop[0]
        self.y = max(midtop[1] - 40, 140 + self.base.get_height() // 2)
        self.age = 0
        self.image = self.base.copy()
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.age += 1
        if self.age >= self.LIFE:
            self.kill()
            return
        self.y -= 0.6
        self.image = self.base.copy()
        remaining = self.LIFE - self.age
        if remaining < self.FADE:
            self.image.set_alpha(int(255 * remaining / self.FADE))
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))


def draw_ammo_pips(surface, x, y, player, color, max_shots=MAX_SHOTS):
    pip, gap = 30, 8
    lit = player.shots_left
    shade = color
    if player.reload_timer > 0:
        lit = int((1 - player.reload_timer / RELOAD_TIME) * max_shots)
        shade = tuple(c // 2 for c in color)
    for i in range(max_shots):
        r = pygame.Rect(x + i * (pip + gap), y, pip, pip)
        pygame.draw.rect(surface, shade if i < lit else (40, 48, 44), r)
        pygame.draw.rect(surface, (96, 118, 104), r, 2)


def draw_health_bar(surface, rect, health, color, max_health=MAX_HEALTH):
    
    pygame.draw.rect(surface, (10, 10, 15), rect)
    gap = 6
    seg_w = (rect.width - gap * (max_health + 1)) // max_health
    for i in range(max_health):
        seg = pygame.Rect(rect.x + gap + i * (seg_w + gap), rect.y + gap, seg_w, rect.height - gap * 2)
        pygame.draw.rect(surface, color if i < health else (40, 48, 44), seg)
    pygame.draw.rect(surface, (96, 118, 104), rect, 2)


BULLET_FRAMES = {
    "Pistol": {
        "start": [
            "iVBORw0KGgoAAAANSUhEUgAAAAMAAAAHCAYAAADNufepAAAALUlEQVR42mNgYGBgkJLX+88AYxw5tuO/lLzefyYGJIDJYdxUiynDCDeJgYEBAFhUChMb5d1vAAAAAElFTkSuQmCC",
            "iVBORw0KGgoAAAANSUhEUgAAAAMAAAAFCAYAAACAcVaiAAAAKElEQVR42mNgYGBgkJLX+88AYxw5tuO/lLzefyYGJIDCYYSrZ2BgAABu3wjfs+T/4AAAAABJRU5ErkJggg==",
        ],
        "loop": [
            "iVBORw0KGgoAAAANSUhEUgAAAAMAAAAICAYAAAA870V8AAAAL0lEQVR42mNgYGBgkJLX+88AYxw5tuO/lLzefyYGJIDCYYSrxwBP37//D6NR9AAAW1AQZUIuWRcAAAAASUVORK5CYII=",
            "iVBORw0KGgoAAAANSUhEUgAAAAMAAAAHCAYAAADNufepAAAAJUlEQVR42mNgYGBgkJLX+88AYxw5tuO/lLzefyYGJEAkhwHZNAAr+wjiFhSaPwAAAABJRU5ErkJggg==",
        ],
        "end": [
            "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAICAYAAAAx8TU7AAAAOElEQVR42mNggAIpeb3/DMhASl7v/5FjO/7DJBjRVT17eImRgXiw6+TZ/xj8p+/f/0eWhPEZ0DkAqEggqHdKfpQAAAAASUVORK5CYII=",
            "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAECAYAAABGM/VAAAAAIElEQVR42mOQktf7z4AEpOT1/jMhcxjQQe/MJZiCyCoBeBwIZDHztwgAAAAASUVORK5CYII=",
            "iVBORw0KGgoAAAANSUhEUgAAAAwAAAAGCAYAAAD37n+BAAAAFUlEQVR42mOQktf7zzBowAC6Bp/VAIrsBDO6WzKPAAAAAElFTkSuQmCC",
        ],
    },
    "Laser": {
        "start": [
            "iVBORw0KGgoAAAANSUhEUgAAABAAAAANCAYAAACgu+4kAAAAZElEQVR42mNgIADerlr8H588EwMRAJ8hRBlAsQuobgCyl8h2AcwQJnwBhEtOOCyWkWgXXJs0F688C7pNyKYTctnbVYv/M6FrIJRw0C1jwmYrLkOwuZQJl9PRDcHlTUZS0z66RQCk5jyuOTJ9YQAAAABJRU5ErkJggg==",
            "iVBORw0KGgoAAAANSUhEUgAAAAkAAAASCAYAAACJgPRIAAAAbUlEQVR42mNgQAOHbRz+o4sxMRABaKzo7arF/4kyCVkhVkXCYbGMyAqZkHUi64YphCuCSSJLYHUTugKsbkL3EVaTYW7CFi2M+MIHZhIjusMP2zj8tz1ygBFFA7rX0a17u2rxfyZ8XqdeKoA5AwCvkkfYuMklKwAAAABJRU5ErkJggg==",
        ],
        "loop": [
            "iVBORw0KGgoAAAANSUhEUgAAAAMAAAAQCAYAAADTasWKAAAATUlEQVR42mNgYGBgOGzj8P/tqsX/Gd6uWvz/sI3DfwYGBgYmBiSAnfN21eL/TMJhsYxYlTHClMDVwjhMDAwMDNcmzWUg0h44gDkUtzIA1JEgLZ8rdiIAAAAASUVORK5CYII=",
            "iVBORw0KGgoAAAANSUhEUgAAAAkAAAAVCAYAAACUhcTwAAAAcElEQVR42mNkQAJvVy3+D2MLh8UywthM6AquTZqLoYGJgYGB4en79/8ZsACYONPT9+//c+zegk0NA8fuLQxP37//z8RABIAr+uHqgyKBzGeSFhRkxGeKtKAgIxO6d5EBTJw0N6Fbi8wnzaRRRXRSBABHtyQvVFaZQQAAAABJRU5ErkJggg==",
        ],
        "end": [
            "iVBORw0KGgoAAAANSUhEUgAAAA8AAAAOCAYAAADwikbvAAAAbElEQVR42mNkgIK3qxb/ZyASCIfFMjIwMDCwwDQe7dlCrF6Gt6sW/xcOi2VkeLtq8f9NZuH/sSk4bOPwH5uLNpmF/3+7avF/FmQBXDbhkmMRDotlJORf6xIfnP7G6S9czoYBJgYKwKjmIaMZAN8wM+gampcAAAAAAElFTkSuQmCC",
            "iVBORw0KGgoAAAANSUhEUgAAABIAAAAJCAYAAAA/33wPAAAAsklEQVR42p2SvRHCMAyFnzlv4C0yQBoomIAyqVKlT8UYqdy7coXLHBtwNAzgLTyDaJAxRlBYjX90/vT0ZIVXpOAJDWGGSQGAZsh9vbZwkIInM0xKM+T0uKgyGa37etQt84cKANhWUAqetFRBggAA37OKMrfL5H6kGsIK6nO0Dil42vox+6rNMCk2+peSbplzjvfROuzP71Z12XM5OQkarUO3zKJXf6dRr7fDkVq/iQiX4gkdBGoCgpjQ6gAAAABJRU5ErkJggg==",
            "iVBORw0KGgoAAAANSUhEUgAAAB4AAAAMCAYAAAB1Lg0yAAAAqElEQVR42mNkoDJ4u2rxf2S+cFgsIzZ1LORowgeO9mzB6hB0sxiRFaBr8ju1kpES328yC4d7xLrEB8UzjOiWUmoZMQ4QDotlZCTVUvToICVKYA6wLvFBxDGxlqJHB0ycGMv9Tq1khFnORE7QweILRpMDWEhRLBwWywjzHTpNqsV0SVzY4hglnjaZhf9HToHUtnSTWfh/WOJkJJR4qBUC6AUJI7lFHqUAAPDdeLS4pxymAAAAAElFTkSuQmCC",
            "iVBORw0KGgoAAAANSUhEUgAAACgAAAAOCAYAAABdC15GAAAARklEQVR42mNgwALerlr8n2EAwEDZSz3HogsetnEYOj6iNaBJYBBj6GgsDLpoHo2S4QTerlr8f2iV3oM6PQ5kSA6pjIkeUACw0yu5ggs4zQAAAABJRU5ErkJggg==",
        ],
    },
    "Shotgun": {
        "start": [
            "iVBORw0KGgoAAAANSUhEUgAAAAkAAAANCAYAAAB7AEQGAAAAb0lEQVR42mOUktf7z0AAsDAwMDCsjmTHqSB0+U8GRgYGBgYpeb3/V6/4MXzaehJFgWX5S4ZnDy8xMjEQAUhTdMXzCAOftzlc4mKfEKrDYeCw820GBgYhCq0bAEWCbC+xKmKEMbDF4bOHlxgZGBgYAFBCGVchVifSAAAAAElFTkSuQmCC",
            "iVBORw0KGgoAAAANSUhEUgAAAA0AAAAJCAYAAADpeqZqAAAAdElEQVR42mNkwAKk5PX+w9jPHl5iRJdnwaZhhrgmnJ/BwPAfXSMTAw5gu1cVlxRuTfgA0/vPNf/ff675T6wt7z/X/GeEMWCC2jqbGK5e8WNA5j97eIkRWQ2G85A1IJsOYwvytjAyYpPAB1A0EdIoyNsCVwsAavgx+XYCP1oAAAAASUVORK5CYII=",
            "iVBORw0KGgoAAAANSUhEUgAAAAsAAAAMCAYAAAC0qUeeAAAAW0lEQVR42mNkQAJS8nr/GdDAs4eXGGFsFnTJq1f84GxtnU0ockwMJAAMxYedb6PQBE3GppByZ+ADGKFhu1cVwdG5jir5/nPNf5KcQUjD+881/7GqgQlikyTJgwC7oyMLaNG7lgAAAABJRU5ErkJggg==",
        ],
        "loop": [
            "iVBORw0KGgoAAAANSUhEUgAAAAoAAAAbCAYAAABFuB6DAAAAnElEQVR42mNkQAJS8nr/YexnDy8xIsuxICu6esUPLqGtw/AfWTETA5EAReFh59soNE6FRJtIkkJs1sIVvv9c8//qFT8GQbaXDBkvrzMIsr1kuHrFj+H955r/OE1EDiI6ekZnuw1+hYK8LYzYJJHFmbBJ2B45wEi0G9FtIdozGAA5kGkbjsMb4AxHXBLIGt9/rvnPhM8UmLggbwsjAOzoP3yDhsUeAAAAAElFTkSuQmCC",
            "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAXCAYAAADDcYV1AAAAgUlEQVR42mNkYGBgkJLX+88ABc8eXmJkkZLX+3/1ih9MjEFbh+E/EwMWwMTAwMBw2Pk2AzKNWyVOQZhWBgYGBqarV/wYBNleMmS8vM4gyPaS4eoVP4RKZGeRaJHOdhsiVQrytjAyMDAw2B45wEimj0gXFORtYcSqEg7ef675T7pFAN6KIBU5sgw4AAAAAElFTkSuQmCC",
        ],
        "end": [
            "iVBORw0KGgoAAAANSUhEUgAAABEAAAAGCAYAAAAlvnXZAAAAVUlEQVR42mNkwAHef675jy4myNvCiE0tCy4DDjvfxiqOzSAmbIZo62yCs233qjIwMDAwZLy8jiKODBiRnQ2zBZtXsHkJpg5DAJsibOGBTT3BgMXnOgDnpDC4ppQFcQAAAABJRU5ErkJggg==",
            "iVBORw0KGgoAAAANSUhEUgAAABMAAAALCAYAAACd1bY6AAAAR0lEQVR42mNgwALef675z4AHEJKnCmAkpEBKXg/uimcPL+FVz0LIoKtX/OB8bR2G//gMZCHksiueRwbGmyMd4EqYeMWpmZoBO9klZ1+Q94QAAAAASUVORK5CYII=",
        ],
    },
}

BULLET_STYLE = {"TechnoBlade": "Pistol", "Wizard": "Laser", "Dragon": "Shotgun"}
BULLET_SCALE = {"Pistol": 4, "Laser": 2, "Shotgun": 2}
START_TICKS, LOOP_TICKS, END_TICKS = 3, 5, 4
HEAD_LEAD = 8
_bullet_anim_cache = {}

impact_effects = pygame.sprite.Group()


def get_bullet_anim(role):
    style = BULLET_STYLE.get(role, "Pistol")
    if style in _bullet_anim_cache:
        return _bullet_anim_cache[style]
    scale = BULLET_SCALE[style]
    raw = {}
    for part, items in BULLET_FRAMES[style].items():
        frames = []
        for b64 in items:
            img = pygame.image.load(io.BytesIO(base64.b64decode(b64))).convert_alpha()
            frames.append(pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale)))
        raw[part] = frames
    max_w = max(f.get_width() for fs in raw.values() for f in fs)
    max_h = max(f.get_height() for fs in raw.values() for f in fs)
    cw, ch = max_w + 4, max_h * 2 + 8
    anim = {}
    for part, frames in raw.items():
        padded = []
        for f in frames:
            canvas = pygame.Surface((cw, ch), pygame.SRCALPHA)
            if part == "end":
                canvas.blit(f, ((cw - f.get_width()) // 2, (ch - f.get_height()) // 2))
            else:
                canvas.blit(f, ((cw - f.get_width()) // 2, ch // 2 - HEAD_LEAD))
            padded.append(canvas)
        anim[part] = padded
    _bullet_anim_cache[style] = anim
    return anim


def travel_angle(vx, vy):
    return math.degrees(math.atan2(-vy, vx)) - 90


class ImpactEffect(pygame.sprite.Sprite):
    def __init__(self, center, role, angle):
        super().__init__()
        self.frames = get_bullet_anim(role)["end"]
        self.center = center
        self.angle = angle
        self.age = 0
        self.image = pygame.transform.rotate(self.frames[0], angle)
        self.rect = self.image.get_rect(center=center)

    def update(self):
        self.age += 1
        idx = self.age // END_TICKS
        if idx >= len(self.frames):
            self.kill()
            return
        self.image = pygame.transform.rotate(self.frames[idx], self.angle)
        self.rect = self.image.get_rect(center=self.center)


class FreezeEffect:
    def __init__(self, area):
        self.area = pygame.Rect(area)
        self.age = 0
        self.surface = pygame.Surface(self.area.size, pygame.SRCALPHA)
        rng = random.Random()
        w, h = self.area.size
        self.flakes = [[rng.uniform(0, w), rng.uniform(0, h), rng.uniform(1.5, 4.0), rng.randint(3, 7), rng.uniform(0, 6.28)]
                       for _ in range(70)]
        self.spikes = [rng.randint(30, 90) for _ in range(w // 48 + 1)]
        self.label = font_title.render("FROZEN", True, (225, 245, 255))

    def draw(self, screen, remaining):
        self.age += 1
        w, h = self.area.size
        k = min(1.0, self.age / 20, remaining / 40)
        k = max(k, 0.0)
        pulse = 0.85 + 0.15 * math.sin(self.age * 0.15)
        surf = self.surface
        surf.fill((120, 190, 255, int(55 * k * pulse)))
        for i in range(8):
            pygame.draw.rect(surf, (210, 240, 255, int((110 - i * 12) * k)), (i * 6, i * 6, w - i * 12, h - i * 12), 6)
        for n, sh in enumerate(self.spikes):
            x = n * 48
            spike = int(sh * k)
            pygame.draw.polygon(surf, (200, 235, 255, int(150 * k)), [(x, 0), (x + 24, spike), (x + 48, 0)])
            pygame.draw.polygon(surf, (200, 235, 255, int(150 * k)), [(x, h), (x + 24, h - spike), (x + 48, h)])
        for f in self.flakes:
            f[1] += f[2]
            f[0] += math.sin(self.age * 0.05 + f[4]) * 0.8
            if f[1] > h:
                f[1] = -f[3]
            pygame.draw.rect(surf, (235, 248, 255, int(220 * k)), (int(f[0]) % w, int(f[1]), f[3], f[3]))
        label = self.label.copy()
        label.set_alpha(int(230 * k))
        surf.blit(label, label.get_rect(center=(w // 2, 190)))
        screen.blit(surf, self.area.topleft)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, role="TechnoBlade", shooter=None):
        super().__init__()
        self.image = pygame.Surface((14, 14), pygame.SRCALPHA)
        self.role = role
        self.anim = get_bullet_anim(role)
        self.age = 0
        self.rect = self.image.get_rect(center=(x, y))
        self.shooter = shooter
        
        angle = math.atan2(target_y - y, target_x - x)
        speed = 14 if role == "TechnoBlade" else (10 if role == "Wizard" else 8)
        
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.bounces_left = 6 if role == "TechnoBlade" else (3 if role == "Wizard" else 1)
        self.lifetime = 300  

    def update(self, platforms):
        self.age += 1
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
            return

        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, platforms, False)
        if hit_list and self.bounces_left > 0:
            self.vx = -self.vx
            self.rect.x += self.vx * 2  
            self.handle_bounce()
        elif hit_list and self.bounces_left == 0:
            self.kill()

        self.rect.y += self.vy
        hit_list = pygame.sprite.spritecollide(self, platforms, False)
        if hit_list and self.bounces_left > 0:
            self.vy = -self.vy
            self.rect.y += self.vy * 2  
            self.handle_bounce()
        elif hit_list and self.bounces_left == 0:
            self.kill()

    def draw(self, surface):
        start, loop = self.anim["start"], self.anim["loop"]
        start_len = len(start) * START_TICKS
        if self.age < start_len:
            frame = start[self.age // START_TICKS]
        else:
            frame = loop[((self.age - start_len) // LOOP_TICKS) % len(loop)]
        img = pygame.transform.rotate(frame, travel_angle(self.vx, self.vy))
        surface.blit(img, img.get_rect(center=self.rect.center))

    def kill(self):
        if self.alive():
            impact_effects.add(ImpactEffect(self.rect.center, self.role, travel_angle(self.vx, self.vy)))
        super().kill()

    def handle_bounce(self):
        self.bounces_left -= 1
        if self.bounces_left < 0:
            self.kill()  

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Haven's Arena - Capture the Flag")
clock = pygame.time.Clock()

MIDNIGHT = (10, 10, 15)
PARCHMENT = (244, 240, 222)
SAGE = (163, 180, 174)
MUTED_SAGE = (52, 66, 59)
PANEL = (10, 10, 15, 225)
CYAN = (100, 200, 255)

font_title = pygame.font.SysFont("Courier New", 72, bold=True)
font_sub = pygame.font.SysFont("Courier New", 34, bold=True)
font_ui = pygame.font.SysFont("Courier New", 25)
font_mono_small = pygame.font.SysFont("Courier New", 18, bold=True)


BACKGROUND_PATH = "/root/JuiceMind/project/assets/Free Pixel Art Forest/Preview/Background.png"


def load_background(BACKGROUND_PATH):
    try:
        img = pygame.image.load(BACKGROUND_PATH).convert()
    except Exception as e:
        print("Background image not found, using a plain dark background:", e)
        fallback = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
        fallback.fill((10, 14, 22))
        return fallback
    iw, ih = img.get_size()
    scale = max(SCREEN_WIDTH / iw, SCREEN_HEIGHT / ih)
    new_size = (math.ceil(iw * scale), math.ceil(ih * scale))
    img = pygame.transform.scale(img, new_size)
    x = (new_size[0] - SCREEN_WIDTH) // 2
    y = new_size[1] - SCREEN_HEIGHT
    return img.subsurface((x, y, SCREEN_WIDTH, SCREEN_HEIGHT)).copy()


bg_image = load_background(BACKGROUND_PATH)


CTF_CHARACTER_B64 = "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"


def load_ctf_character(height=165):
    img = pygame.image.load(io.BytesIO(base64.b64decode(CTF_CHARACTER_B64))).convert_alpha()
    w = round(img.get_width() * height / img.get_height())
    return pygame.transform.scale(img, (w, height))


ctf_character = load_ctf_character()


def draw_pixel_panel(surface, rect, accent, fill=(10, 10, 15, 225)):
    panel = pygame.Surface(rect.size, pygame.SRCALPHA)
    panel.fill(fill)
    surface.blit(panel, rect.topleft)
    pygame.draw.rect(surface, accent, rect, 2)
    inner = rect.inflate(-12, -12)
    pygame.draw.rect(surface, (40, 56, 48), inner, 1)
    pygame.draw.rect(surface, accent, (rect.left - 3, rect.top - 3, 8, 8))
    pygame.draw.rect(surface, accent, (rect.right - 5, rect.bottom - 5, 8, 8))
    pygame.draw.rect(surface, accent, (rect.left, rect.top, rect.width, 4))


def draw_centered(surface, text, font, color, center, shadow=False):
    image = font.render(text, True, color)
    rect = image.get_rect(center=center)
    if shadow:
        shadow_image = font.render(text, True, (0, 0, 0))
        surface.blit(shadow_image, rect.move(0, 5))
    surface.blit(image, rect)
    return rect

try:
    pygame.mixer.music.load("naruto_theme.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.6)
except Exception as e:
    print("Music file not found or couldn't play:", e)

def show_mode_screen():
    ctf_rect = pygame.Rect(SCREEN_WIDTH // 2 - 310, 400, 620, 440)
    button_rect = pygame.Rect(ctf_rect.x + 36, ctf_rect.bottom - 95, ctf_rect.width - 72, 62)
    while True:
        mouse = pygame.mouse.get_pos()
        screen.blit(bg_image, (0, 0))
        shade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        shade.fill((4, 7, 10, 105))
        screen.blit(shade, (0, 0))
        draw_centered(screen, "CHOOSE YOUR FATE", font_title, PARCHMENT, (SCREEN_WIDTH // 2, 280), True)

        ctf_hover = ctf_rect.collidepoint(mouse)
        draw_pixel_panel(screen, ctf_rect, (58, 79, 68), (10, 10, 15, 232))
        screen.blit(ctf_character, ctf_character.get_rect(midtop=(ctf_rect.centerx, ctf_rect.y + 50)))
        draw_centered(screen, "CAPTURE THE FLAG", font_sub, PARCHMENT, (ctf_rect.centerx, ctf_rect.y + 272))
        pygame.draw.line(screen, MUTED_SAGE, (ctf_rect.x + 36, ctf_rect.bottom - 120), (ctf_rect.right - 36, ctf_rect.bottom - 120), 2)
        btn_color = (70, 92, 80) if ctf_hover else (52, 66, 59)
        pygame.draw.rect(screen, btn_color, button_rect)
        pygame.draw.rect(screen, (96, 118, 104), button_rect.inflate(-8, -8), 2)
        draw_centered(screen, "PLAY CAPTURE THE FLAG   ›", font_mono_small, PARCHMENT, button_rect.center)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return "Capture the Flag"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and button_rect.collidepoint(event.pos):
                return "Capture the Flag"
        clock.tick(FPS)


def show_title_screen():
    selected_role = 0
    roles = ["TechnoBlade", "Wizard", "Dragon"]
    card_w, card_h, gap = 440, 290, 34
    run_sheet = load_piskel_from_dict(RUN_PISKEL_JSON)
    previews = [
        pygame.transform.scale(tint_surface(run_sheet.subsurface((0, 0, 32, 32)), r), (128, 128))
        for r in roles
    ]
    total_w = len(roles) * card_w + (len(roles) - 1) * gap
    first_x = (SCREEN_WIDTH - total_w) // 2
    while True:
        screen.blit(bg_image, (0, 0))
        shade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        shade.fill((4, 7, 10, 125)); screen.blit(shade, (0, 0))
        draw_centered(screen, "CHOOSE YOUR CHAMPION", font_title, PARCHMENT, (SCREEN_WIDTH // 2, 205), True)
        for i, role in enumerate(roles):
            rect = pygame.Rect(first_x + i * (card_w + gap), 360, card_w, card_h)
            accent = GOLD if i == selected_role else (58, 79, 68)
            draw_pixel_panel(screen, rect, accent, (10, 10, 15, 230))
            screen.blit(previews[i], previews[i].get_rect(midtop=(rect.centerx, rect.y + 58)))
            draw_centered(screen, role.upper(), font_sub, PARCHMENT, (rect.centerx, rect.y + 222))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    selected_role = (selected_role - 1) % len(roles)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    selected_role = (selected_role + 1) % len(roles)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return roles[selected_role]
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i in range(len(roles)):
                    rect = pygame.Rect(first_x + i * (card_w + gap), 360, card_w, card_h)
                    if rect.collidepoint(event.pos):
                        selected_role = i
                        return roles[selected_role]
        clock.tick(FPS)

def show_winner_screen(player_num, role, duration_ms=4000):
    """Winner screen: the mascot and the winning team's flag (blue = Player 1, red = Player 2),
    then control returns to the start screen."""
    color = CYAN if player_num == 1 else (255, 170, 95)

    sheet = load_piskel_from_dict(RUN_PISKEL_JSON)
    winner_sprite = tint_surface(sheet.subsurface((0, 0, 32, 32)), role, player_num == 2)
    mascot = pygame.transform.scale(winner_sprite, (256, 256))
    flag = load_b64_image(FLAG_BLUE_B64 if player_num == 1 else FLAG_RED_B64, 8)
    start = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start < duration_ms:
        t = pygame.time.get_ticks() - start
        screen.blit(bg_image, (0, 0))
        shade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        shade.fill((4, 7, 10, 170)); screen.blit(shade, (0, 0))
        draw_centered(screen, f"PLAYER {player_num} WINS!", font_title, color, (SCREEN_WIDTH // 2, 300), True)
        bob = int(math.sin(t / 220) * 10)
        screen.blit(mascot, mascot.get_rect(midbottom=(SCREEN_WIDTH // 2 - 170, 760)))
        screen.blit(flag, flag.get_rect(midbottom=(SCREEN_WIDTH // 2 + 170, 760 + bob)))
        draw_centered(screen, role.upper(), font_sub, PARCHMENT, (SCREEN_WIDTH // 2, 830))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()
        clock.tick(FPS)
    pygame.event.clear()


def run_game(chosen_role_p1):
    """Play one round. Returns (winner_number, winner_role) when someone captures the flag."""
    all_sprites = pygame.sprite.Group()
    impact_effects.empty()
    freeze_fx = {}
    slowmo_timer = 0
    step_acc = 1.0
    slow_tint = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    slow_tint.fill((30, 60, 120, 40))
    kill_popups.empty()
    platforms = pygame.sprite.Group()
    jump_pads = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    players_group = pygame.sprite.Group()

    ground = Platform(0, SCREEN_HEIGHT - 60, SCREEN_WIDTH, 60, color=(26, 43, 34))
    platforms.add(ground)
    all_sprites.add(ground)

    plat1 = Platform(400, 900, 300, 25, color=(67, 91, 65))
    plat2 = Platform(900, 800, 350, 25, color=(67, 91, 65))
    plat3 = Platform(1350, 700, 300, 25, color=(67, 91, 65))
    for p in [plat1, plat2, plat3]:
        platforms.add(p)
        all_sprites.add(p)

    pad1 = Platform(525, 875, 80, 25, color=ORANGE)
    jump_pads.add(pad1)
    platforms.add(pad1) 
    all_sprites.add(pad1)

    base_p1_rect = pygame.Rect(100, 800, 100, 150)
    base_p2_rect = pygame.Rect(1720, 800, 100, 150)

    flag_p1 = Flag(150, 850, FLAG_BLUE_B64)
    flag_p2 = Flag(1770, 850, FLAG_RED_B64)
    flags_group = pygame.sprite.Group(flag_p1, flag_p2)

    p2_controller = None
    if pygame.joystick.get_count() > 0:
        p2_controller = pygame.joystick.Joystick(0)
        p2_controller.init()
        print(f"Connected Controller for P2: {p2_controller.get_name()}")
    else:
        print("No controller detected - Player 2 uses the arrow keys (hold Right Shift + arrows to aim and shoot).")

    player1 = Player(300, 950, role=chosen_role_p1, is_player_two=False)
    player2 = Player(1500, 950, role="Wizard", is_player_two=True, controller=p2_controller)

    players_group.add(player1, player2)
    all_sprites.add(player1, player2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif (event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)
                      and pygame.key.get_pressed()[pygame.K_RSHIFT] and player2.can_shoot()):
                    held = pygame.key.get_pressed()
                    aim_x = int(held[pygame.K_RIGHT]) - int(held[pygame.K_LEFT])
                    aim_y = int(held[pygame.K_DOWN]) - int(held[pygame.K_UP])
                    if aim_x == 0 and aim_y == 0:
                        aim_x = 1 if player2.facing_right else -1
                    if aim_x != 0:
                        player2.facing_right = aim_x > 0
                    target_x = player2.rect.centerx + aim_x * 300
                    target_y = player2.rect.centery + aim_y * 300
                    bullet = Bullet(player2.rect.centerx, player2.rect.centery, target_x, target_y, role=player2.role, shooter=player2)
                    bullets.add(bullet)
                    all_sprites.add(bullet)
                    player2.trigger_shot()
                    slowmo_timer = SLOWMO_DURATION
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and player1.can_shoot():
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    bullet = Bullet(player1.rect.centerx, player1.rect.centery, mouse_x, mouse_y, role=player1.role, shooter=player1)
                    bullets.add(bullet)
                    all_sprites.add(bullet)
                    player1.trigger_shot()
                    slowmo_timer = SLOWMO_DURATION
            elif event.type == pygame.JOYBUTTONDOWN:
                if p2_controller and event.joy == p2_controller.get_id() and not player2.is_frozen:
                    if event.button == 0:
                        if player2.on_ground:
                            player2.vy = player2.jump_strength
                            player2.on_ground = False
                    elif (event.button == 1 or event.button == 2) and player2.can_shoot():
                        target_x = player2.rect.centerx + (300 if player2.facing_right else -300)
                        target_y = player2.rect.centery
                        bullet = Bullet(player2.rect.centerx, player2.rect.centery, target_x, target_y, role=player2.role, shooter=player2)
                        bullets.add(bullet)
                        all_sprites.add(bullet)
                        player2.trigger_shot()
                        slowmo_timer = SLOWMO_DURATION

        slow = slowmo_timer > 0
        if slow:
            slowmo_timer -= 1
        step_acc += SLOWMO_SCALE if slow else 1.0
        if step_acc >= 1.0:
            step_acc -= 1.0
            player1.handle_input()
            player2.handle_input()
            player1.update(platforms, jump_pads)
            player2.update(platforms, jump_pads)
            bullets.update(platforms)
            flags_group.update()
            impact_effects.update()
        kill_popups.update()

        if not flag_p2.carrier and player1.rect.colliderect(flag_p2.rect):
            flag_p2.carrier = player1
            player1.has_flag = True

        if not flag_p1.carrier and player2.rect.colliderect(flag_p1.rect):
            flag_p1.carrier = player2
            player2.has_flag = True

        for bullet in bullets:
            if bullet.shooter == player1 and bullet.rect.colliderect(player2.rect):
                player2.take_hit()
                bullet.kill()
                if player2.has_flag:
                    player2.has_flag = False
                    flag_p1.carrier = None
                    flag_p1.is_dropped = True
                if player2.health <= 0:
                    player1.score += 100
                    kill_popups.add(KillPopup(player2.rect.midtop))
                    player2.health = 3
                    player2.rect.topleft = (1500, 950)
                    if player2.has_flag:
                        player2.has_flag = False
                        flag_p1.reset_to_home()
                    
            elif bullet.shooter == player2 and bullet.rect.colliderect(player1.rect):
                player1.take_hit()
                bullet.kill()
                if player1.has_flag:
                    player1.has_flag = False
                    flag_p2.carrier = None
                    flag_p2.is_dropped = True
                if player1.health <= 0:
                    player2.score += 100
                    kill_popups.add(KillPopup(player1.rect.midtop))
                    player1.health = 3
                    player1.rect.topleft = (300, 950)
                    if player1.has_flag:
                        player1.has_flag = False
                        flag_p2.reset_to_home()

        if player1.has_flag and base_p1_rect.colliderect(player1.rect):
            player1.score += 500
            player1.has_flag = False
            flag_p2.reset_to_home()
            return 1, player1.role

        if player2.has_flag and base_p2_rect.colliderect(player2.rect):
            player2.score += 500
            player2.has_flag = False
            flag_p1.reset_to_home()
            return 2, player2.role

        screen.fill(BLACK)
        screen.blit(bg_image, (0, 0))


        all_sprites.draw(screen)
        for platform in platforms:
            if platform is not pad1:
                pygame.draw.line(screen, (112, 133, 83), platform.rect.topleft, platform.rect.topright, 4)
        flags_group.draw(screen)
        for b in bullets:
            b.draw(screen)
        impact_effects.draw(screen)
        kill_popups.draw(screen)

        if slow:
            screen.blit(slow_tint, (0, 0))

        half = SCREEN_WIDTH // 2
        for plr, area in ((player1, (0, 0, half, SCREEN_HEIGHT)), (player2, (half, 0, half, SCREEN_HEIGHT))):
            if plr.is_frozen:
                if plr not in freeze_fx:
                    freeze_fx[plr] = FreezeEffect(area)
                    kill_popups.add(KillPopup(plr.rect.midtop, FREEZE_IMAGE_B64))
                freeze_fx[plr].draw(screen, plr.freeze_timer)
            else:
                freeze_fx.pop(plr, None)

        hud = pygame.Surface((SCREEN_WIDTH - 60, 94), pygame.SRCALPHA)
        hud.fill((10, 10, 15, 205))
        screen.blit(hud, (30, 24))
        pygame.draw.rect(screen, (80, 100, 82), (30, 24, SCREEN_WIDTH - 60, 94), 2)
        p1_status = "FROZEN" if player1.is_frozen else ("FLAG CARRIED" if player1.has_flag else "")
        p2_status = "FROZEN" if player2.is_frozen else ("FLAG CARRIED" if player2.has_flag else "")
        p1_hud = font_ui.render(f"P1  {player1.role}   SCORE {player1.score}   HITS {player1.hit_count}/{HITS_TO_FREEZE}   {p1_status}", True, CYAN)
        p2_hud = font_ui.render(f"P2  {player2.role}   SCORE {player2.score}   HITS {player2.hit_count}/{HITS_TO_FREEZE}   {p2_status}", True, (255, 170, 95))
        screen.blit(p1_hud, (52, 39))
        screen.blit(p2_hud, (52, 78))

        bar_w, bar_h = 420, 30
        draw_health_bar(screen, pygame.Rect(40, SCREEN_HEIGHT - bar_h - 16, bar_w, bar_h), player1.health, CYAN)
        draw_health_bar(screen, pygame.Rect(SCREEN_WIDTH - bar_w - 40, SCREEN_HEIGHT - bar_h - 16, bar_w, bar_h), player2.health, (255, 170, 95))
        ammo_w = MAX_SHOTS * 30 + (MAX_SHOTS - 1) * 8
        draw_ammo_pips(screen, 40 + bar_w + 16, SCREEN_HEIGHT - bar_h - 16, player1, CYAN)
        draw_ammo_pips(screen, SCREEN_WIDTH - bar_w - 40 - 16 - ammo_w, SCREEN_HEIGHT - bar_h - 16, player2, (255, 170, 95))

        pygame.display.update()
        clock.tick(FPS)


while True:
    selected_mode = show_mode_screen()
    chosen_role_p1 = show_title_screen()
    winner_num, winner_role = run_game(chosen_role_p1)
    show_winner_screen(winner_num, winner_role)
