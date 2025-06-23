#FTL by Ian0822
# -*- coding: utf-8 -*-
import os
import sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
import math
import datetime
import time
import numpy as np
import copy

#基本定義
FPS = 60
WIDTH = 1000
HEIGHT = 750
GRAVITY = 10
GROUND = 475
LORE_WIDTH = 500
LORE_HEIGHT = 500
#顏色
BLACK = 0, 0, 0
WHITE = 255, 255, 255
YELLOW = 255, 255, 0
GREEN = 0, 255, 0
DGREEN = 0, 120, 0
RED = 255, 0, 0
LBLUE = 152, 245, 255
BLUE = 30, 144, 255
CYAN = 32, 178, 170
TEAL = 0, 160, 160
GOLD = 255, 215, 0
DGRAY = 105, 105, 105
GRAY = 192, 192, 192
LGRAY = 119, 136, 153
AGRAY = 64, 64, 64
BGRAY = 100, 100, 100
IGRAY = 80, 84, 92
PURPLE = 148, 0, 211
DCGRAY = 49, 51, 56
#稀有度顏色
COMMON = (195, 195, 195)
UNCOMMON = (181, 230, 29)
RARE = (0, 162, 232)
EPIC = (152, 70, 151)
LEGENDARY = (255, 127, 39)
#天空顏色
SKY_BACKBROUND = (0, 0, 255)
DAY_COLOR = (167, 236, 255)   # 白天（淺藍）
AFTERNOON_COLOR = (70, 130, 180) # 下午（藍）
DUSK_COLOR = (255, 140, 30)   # 黃昏/晨曦（橘紅）
NIGHT_COLOR = (25, 25, 112)   # 夜晚（深藍）
MIDNIGHT_COLOR = (0, 0, 0)
SKY_BACKGROUND = (0, 0, 255)
SUN_COLOR = (255, 204, 0)     # 太陽（黃色）
MOON_COLOR = (255, 255, 255)  # 月亮（白色）
#時間
DAWN = [5, 7]
DAY = [7, 11]
NOON = [11, 16]
AFTERNOON = [16, 17]
DUSK = [17, 19]
NIGHT = [19, 24]
MIDNIGHT = [0, 5]

#建立視窗
pygame.init()
try:
    pygame.mixer.init()
except:
    None
#全螢幕
FULLSCREEN = True
if FULLSCREEN:
    info = pygame.display.Info()
    SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
    display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)#pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
    scale = min(SCREEN_WIDTH / WIDTH, SCREEN_HEIGHT / HEIGHT)
    screen = pygame.Surface((WIDTH, HEIGHT))
else:
    SCREEN_WIDTH, SCREEN_HEIGHT = WIDTH, HEIGHT
    scale = 1
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
new_width = int(WIDTH * scale)
new_height = int(HEIGHT * scale)
x_offset = (SCREEN_WIDTH - new_width) // 2
y_offset = (SCREEN_HEIGHT - new_height) // 2
#標題
pygame.display.set_caption("Finding The Light")
pygame.display.set_icon(pygame.image.load(os.path.join("resource", "Finding The Light Logo.png")).convert_alpha())
clock = pygame.time.Clock()
now = datetime.datetime.now()
#載入圖片
# stderr_fileno = sys.stderr.fileno()
# devnull = os.open(os.devnull, os.O_WRONLY)
# os.dup2(devnull, stderr_fileno)
#玩家圖片
player_right_img = pygame.image.load(os.path.join("resource", "player_right.png")).convert()
player_left_img = pygame.image.load(os.path.join("resource", "player_left.png")).convert()
player_rise_hand_right_img = pygame.image.load(os.path.join("resource", "player_rise_hand_right.png")).convert()
player_rise_hand_left_img = pygame.image.load(os.path.join("resource", "player_rise_hand_left.png")).convert()
player_right_img.set_colorkey(BLACK)
player_left_img.set_colorkey(BLACK)
player_rise_hand_right_img.set_colorkey(BLACK)
player_rise_hand_left_img.set_colorkey(BLACK)
#攻擊動畫/特效
#特效:翅膀
player_wings_1_img = pygame.image.load(os.path.join("resource", "player_wings_1.png")).convert()
player_wings_2_img = pygame.image.load(os.path.join("resource", "player_wings_2.png")).convert()
#特效:衝刺
player_dash_right_img = pygame.image.load(os.path.join("resource", "player_dash_right.png")).convert()
player_dash_left_img = pygame.image.load(os.path.join("resource", "player_dash_left.png")).convert()
#特效:揮砍
slash_right_1_img = pygame.image.load(os.path.join("resource", "slash_right_1.png")).convert()
slash_right_2_img = pygame.image.load(os.path.join("resource", "slash_right_2.png")).convert()
slash_left_1_img = pygame.image.load(os.path.join("resource", "slash_left_1.png")).convert()
slash_left_2_img = pygame.image.load(os.path.join("resource", "slash_left_2.png")).convert()
slash_blade_dance_right_img = pygame.transform.scale(slash_right_1_img, (140, 100))
slash_blade_dance_left_img = pygame.transform.flip(slash_blade_dance_right_img, True, False)
#特效:黑洞
black_hole_1_img = pygame.image.load(os.path.join("resource", "black_hole_1.png")).convert()
#特效:混沌匕首
chaos_dagger_right_img = pygame.image.load(os.path.join("resource", "chaos_dagger_right.png")).convert()
chaos_dagger_left_img = pygame.image.load(os.path.join("resource", "chaos_dagger_left.png")).convert()
#特效:幻影分身
shadow_clone_right_img = pygame.image.load(os.path.join("resource", "shadow_clone.png")).convert()
shadow_clone_left_img = pygame.transform.flip(shadow_clone_right_img, True, False)
#調整大小&去背
slash_right_1_img = pygame.transform.scale(slash_right_1_img, (70, 50))
slash_left_1_img = pygame.transform.scale(slash_left_1_img, (70, 50))
player_wings_1_img.set_colorkey(GREEN)
player_wings_2_img.set_colorkey(GREEN)
player_dash_right_img.set_colorkey(GREEN)
player_dash_left_img.set_colorkey(GREEN)
slash_right_1_img.set_colorkey(BLACK)
slash_right_2_img.set_colorkey(GREEN)
slash_blade_dance_right_img.set_colorkey(BLACK)
slash_left_1_img.set_colorkey(BLACK)
slash_left_2_img.set_colorkey(GREEN)
slash_blade_dance_left_img.set_colorkey(BLACK)
black_hole_1_img.set_colorkey(GREEN)
chaos_dagger_right_img.set_colorkey(GREEN)
chaos_dagger_left_img.set_colorkey(GREEN)
bow_right_1_img = pygame.image.load(os.path.join("resource", "bow_right_1.png")).convert()
bow_left_1_img = pygame.image.load(os.path.join("resource", "bow_left_1.png")).convert()
bow_right_2_img = pygame.image.load(os.path.join("resource", "bow_right_2.png")).convert()
bow_left_2_img = pygame.image.load(os.path.join("resource", "bow_left_2.png")).convert()
bow_right_1_img.set_colorkey(GREEN)
bow_left_1_img.set_colorkey(GREEN)
bow_right_2_img.set_colorkey(GREEN)
bow_left_2_img.set_colorkey(GREEN)
wand_right_1_img = pygame.image.load(os.path.join("resource", "wand_right_1.png")).convert()
wand_left_1_img = pygame.image.load(os.path.join("resource", "wand_left_1.png")).convert()
wand_right_2_img = pygame.image.load(os.path.join("resource", "wand_right_2.png")).convert()
wand_left_2_img = pygame.image.load(os.path.join("resource", "wand_left_2.png")).convert()
wand_right_1_img.set_colorkey(GREEN)
wand_left_1_img.set_colorkey(GREEN)
wand_right_2_img.set_colorkey(GREEN)
wand_left_2_img.set_colorkey(GREEN)
arrow_right_img = pygame.image.load(os.path.join("resource", "arrow_right.png")).convert()
arrow_left_img = pygame.image.load(os.path.join("resource", "arrow_left.png")).convert()
fire_arrow_right_img = pygame.image.load(os.path.join("resource", "fire_arrow_right.png")).convert()
fire_arrow_left_img = pygame.image.load(os.path.join("resource", "fire_arrow_left.png")).convert()
kunai_right_img = pygame.image.load(os.path.join("resource", "kunai_right.png")).convert() #image by Ouroar
kunai_left_img = pygame.image.load(os.path.join("resource", "kunai_left.png")).convert() #image by Ouroar
arrow_right_img.set_colorkey(GREEN)
arrow_left_img.set_colorkey(GREEN)
fire_arrow_right_img.set_colorkey(GREEN)
fire_arrow_left_img.set_colorkey(GREEN)
kunai_right_img.set_colorkey(GREEN)
kunai_left_img.set_colorkey(GREEN)
kunai_right_img = pygame.transform.scale(kunai_right_img, (85, 20))
kunai_left_img = pygame.transform.scale(kunai_left_img, (85, 20))
meteor_img = pygame.image.load(os.path.join("resource", "meteor.png")).convert()
meteor_img = pygame.transform.scale(meteor_img, (90 * 2, 150 * 2))
water_burst_img = pygame.image.load(os.path.join("resource", "water_burst.png")).convert_alpha()
target_img = pygame.image.load(os.path.join("resource", "target.png")).convert()
magic_orb_img = pygame.image.load(os.path.join("resource", "magic_orb.png")).convert()
dmg_indicator_img = pygame.image.load(os.path.join("resource", "dmg_indicator.png")).convert()
dmg_indicator_img.set_colorkey(BLACK)
#普通怪物圖片
spawner_img = pygame.image.load(os.path.join("resource", "spawner.png")).convert()
slime_img = pygame.image.load(os.path.join("resource", "slime.png")).convert()
slime_img = pygame.transform.scale(slime_img, (29 * 5, 21 * 5))
skeleton_right_img = pygame.image.load(os.path.join("resource", "skeleton_right.png")).convert()
skeleton_left_img = pygame.image.load(os.path.join("resource", "skeleton_left.png")).convert()
tree_monster_img = pygame.image.load(os.path.join("resource", "tree_monster.png")).convert()
crack_wall_img = pygame.image.load(os.path.join("resource", "crack_wall.png")).convert()
zombie_right_img = pygame.image.load(os.path.join("resource", "zombie_right.png")).convert()
zombie_left_img = pygame.image.load(os.path.join("resource", "zombie_left.png")).convert()
skywing_beast_1_img = pygame.image.load(os.path.join("resource", "skywing_beast_1.png")).convert()
skywing_beast_2_img = pygame.image.load(os.path.join("resource", "skywing_beast_2.png")).convert()
storm_img = pygame.image.load(os.path.join("resource", "storm.png")).convert()
thunder_dragon_right_img = pygame.image.load(os.path.join("resource", "thunder_dragon_right.png")).convert()
thunder_dragon_left_img = pygame.image.load(os.path.join("resource", "thunder_dragon_left.png")).convert()
thunder_cloud_img = pygame.image.load(os.path.join("resource", "thunder_cloud.png")).convert()
lightning_img = pygame.image.load(os.path.join("resource", "lightning.png")).convert()
cursed_silver_knight_img = pygame.image.load(os.path.join("resource", "cursed_silver_knight.png")).convert()
silver_knight_spear_right_img = pygame.image.load(os.path.join("resource", "silver_knight_spear_right.png")).convert()
silver_knight_spear_left_img = pygame.image.load(os.path.join("resource", "silver_knight_spear_left.png")).convert()
silver_knight_shield_img = pygame.image.load(os.path.join("resource", "silver_knight_shield.png")).convert()
giant_rat_right_img = pygame.image.load(os.path.join("resource", "giant_rat_right.png")).convert()
giant_rat_left_img = pygame.image.load(os.path.join("resource", "giant_rat_left.png")).convert()
castle_guardian_img = pygame.image.load(os.path.join("resource", "castle_guardian.png")).convert()
skeleton_right_img.set_colorkey(GREEN)
skeleton_left_img.set_colorkey(GREEN)
zombie_left_img.set_colorkey(YELLOW)
zombie_right_img.set_colorkey(YELLOW)
cursed_silver_knight_img.set_colorkey(GREEN)
silver_knight_spear_right_img.set_colorkey(GREEN)
silver_knight_spear_left_img.set_colorkey(GREEN)
silver_knight_shield_img.set_colorkey(GREEN)
giant_rat_right_img.set_colorkey(GREEN)
giant_rat_left_img.set_colorkey(GREEN)
#魔王圖片
xerath_img = pygame.image.load(os.path.join("resource", "xerath.png")).convert()
stellaris_1_img = pygame.image.load(os.path.join("resource", "stellaris_1.png")).convert()
stellaris_2_img = pygame.image.load(os.path.join("resource", "stellaris_2.png")).convert()
stellaris_3_img = pygame.image.load(os.path.join("resource", "stellaris_3.png")).convert()
blight_path_img = pygame.image.load(os.path.join("resource", "blight_path.png")).convert()
from_the_star_wave_img = pygame.image.load(os.path.join("resource", "from_the_star_wave.png")).convert()
blight_pod_img = pygame.image.load(os.path.join("resource", "blight_pod.png")).convert()
blight_slime_img = pygame.image.load(os.path.join("resource", "blight_slime.png")).convert()
blight_laser_1_img = pygame.image.load(os.path.join("resource", "blight_laser_1.png")).convert()
blight_laser_2_img = pygame.image.load(os.path.join("resource", "blight_laser_2.png")).convert()
impaling_doom_1_img = pygame.image.load(os.path.join("resource", "impaling_doom_1.png")).convert()
impaling_doom_2_img = pygame.image.load(os.path.join("resource", "impaling_doom_2.png")).convert()
blight_bomb_img = pygame.image.load(os.path.join("resource", "blight_bomb.png")).convert()
blight_bomb_explode_img = pygame.image.load(os.path.join("resource", "blight_bomb_explode.png")).convert()
blight_meteor_img = pygame.image.load(os.path.join("resource", "blight_meteor.png")).convert()
shadow_dagger_img = pygame.image.load(os.path.join("resource", "shadow_dagger.png")).convert()
shadow_of_the_depth_img = pygame.image.load(os.path.join("resource", "shadow_of_the_depth.png")).convert()
cage_of_darkness_img = pygame.image.load(os.path.join("resource", "cage_of_darkness.png")).convert()
grasp_of_the_depth_img = pygame.image.load(os.path.join("resource", "grasp_of_the_depth.png")).convert()
corrupted_raindrop_img = pygame.image.load(os.path.join("resource", "corrupted_raindrop.png")).convert()
lava_eruption_img = {}
for i in range(8):
    lava_eruption_temp_img = pygame.image.load(os.path.join("resource", "lava_eruption_" + str(i) + ".png")).convert()
    lava_eruption_temp_img.set_colorkey(BLACK)
    original_width = lava_eruption_temp_img.get_width()
    original_height = lava_eruption_temp_img.get_height()
    scale_factor = 140 / original_width
    scaled_img = pygame.transform.scale(lava_eruption_temp_img, (140, int(original_height * scale_factor)))
    lava_eruption_img[i] = scaled_img
gaze_of_the_depth_img = {}
for i in range(4):
    gaze_of_the_depth_temp_img = pygame.image.load(os.path.join("resource", "gaze_of_the_depth_" + str(i) + ".png")).convert()
    gaze_of_the_depth_temp_img = pygame.transform.scale(gaze_of_the_depth_temp_img, (300, 300))
    gaze_of_the_depth_temp_img.set_colorkey(GREEN)
    gaze_of_the_depth_img.update({i:gaze_of_the_depth_temp_img})
    earth_rift_img = {}
    for i in range(3):
        earth_rift_temp_img = pygame.image.load(os.path.join("resource", "earth_rift_" + str(i) + ".png")).convert_alpha()
        earth_rift_temp_img.set_colorkey(GREEN)
        earth_rift_img.update({i:earth_rift_temp_img})
thunder_judgement_img = {}
for i in range(5):
    thunder_judgement_temp_img = pygame.image.load(os.path.join("resource", "thunder_judgement_" + str(i) + ".png")).convert_alpha()
    thunder_judgement_temp_img.set_colorkey(WHITE)
    thunder_judgement_img.update({i:thunder_judgement_temp_img})
giant_rock_img = pygame.image.load(os.path.join("resource", "giant_rock.png")).convert()
crimson_finale_img = {0:pygame.image.load(os.path.join("resource", "crimson_finale_0.png")).convert(), 1:pygame.image.load(os.path.join("resource", "crimson_finale_1.png")).convert()}
crimson_finale_img[0].set_colorkey(GREEN)
crimson_finale_img[1].set_colorkey(GREEN)
corrupted_raindrop_img.set_colorkey(GREEN)
giant_rock_img.set_colorkey(GREEN)
stellaris_1_img.set_colorkey(GREEN)
stellaris_2_img.set_colorkey(GREEN)
stellaris_3_img.set_colorkey(GREEN)
from_the_star_wave_img.set_colorkey(GREEN)
blight_pod_img.set_colorkey(GREEN)
blight_slime_img.set_colorkey(GREEN)
blight_laser_1_img.set_colorkey(GREEN)
impaling_doom_1_img.set_colorkey(GREEN)
impaling_doom_2_img.set_colorkey(GREEN)
blight_bomb_img.set_colorkey(GREEN)
blight_bomb_explode_img.set_colorkey(GREEN)
blight_meteor_img.set_colorkey(GREEN)
grasp_of_the_depth_img.set_colorkey(GREEN)
#NPC圖片
#任務「星疫之災」
aurora_1_img = pygame.image.load(os.path.join("resource", "aurora_1.png")).convert()
aurora_2_img = pygame.image.load(os.path.join("resource", "aurora_2.png")).convert()
aurora_skill_1 = pygame.image.load(os.path.join("resource", "aurora_skill_1.png")).convert()
aurora_star_img = pygame.image.load(os.path.join("resource", "aurora_star.png")).convert()
aurora_skill_2_1_img = pygame.image.load(os.path.join("resource", "aurora_skill_2_1.png")).convert()
aurora_skill_2_2_img = pygame.image.load(os.path.join("resource", "aurora_skill_2_2.png")).convert()
aurora_skill_2_3_img = pygame.image.load(os.path.join("resource", "aurora_skill_2_3.png")).convert()
aurora_skill_2_4_img = pygame.image.load(os.path.join("resource", "aurora_skill_2_4.png")).convert()
aurora_skill_2_5_img = pygame.image.load(os.path.join("resource", "aurora_skill_2_5.png")).convert()
tuleen_img = pygame.image.load(os.path.join("resource", "tuleen.png")).convert()
tuleen_skill_1_1_img = pygame.image.load(os.path.join("resource", "tuleen_skill_1_1.png")).convert()
#任務「黑暗王座的終焉」
nightblade_1_img = pygame.image.load(os.path.join("resource", "nightblade_1.png")).convert()
reinhardt_1_img = pygame.image.load(os.path.join("resource", "reinhardt_1.png")).convert()
kevin_1_img = pygame.image.load(os.path.join("resource", "kevin_1.png")).convert()
nightblade_1_img.set_colorkey(GREEN)
reinhardt_1_img.set_colorkey(GREEN)
kevin_1_img.set_colorkey(GREEN)
#商店
rogue_charm_shop_img = pygame.image.load(os.path.join("resource", "rogue_charm_shop.png")).convert()
aurora_1_img.set_colorkey(GREEN)
aurora_2_img.set_colorkey(GREEN)
aurora_skill_1.set_colorkey(GREEN)
aurora_skill_2_images = [aurora_star_img, aurora_skill_2_1_img, aurora_skill_2_1_img, aurora_skill_2_2_img, aurora_skill_2_3_img, aurora_skill_2_4_img, aurora_skill_2_5_img]
rogue_charm_shop_img.set_colorkey(GREEN)
for i in range(7): aurora_skill_2_images[i].set_colorkey(GREEN)
tuleen_img.set_colorkey(GREEN)
tuleen_skill_1_1_img.set_colorkey(GREEN)
#物件圖片
cloud_1_img = pygame.image.load(os.path.join("resource", "cloud_1.png")).convert()
cloud_2_img = pygame.image.load(os.path.join("resource", "cloud_2.png")).convert()
cloud_3_img = pygame.image.load(os.path.join("resource", "cloud_3.png")).convert()
cloud_4_img = pygame.image.load(os.path.join("resource", "cloud_4.png")).convert()
cloud_5_img = pygame.image.load(os.path.join("resource", "cloud_5.png")).convert()
falling_rock_img = pygame.image.load(os.path.join("resource", "falling_rock.png")).convert()
falling_stick_img = pygame.image.load(os.path.join("resource", "falling_stick.png")).convert()
falling_star_raindrop_img = pygame.image.load(os.path.join("resource", "falling_star_raindrop.png")).convert()
falling_brick_img = pygame.image.load(os.path.join("resource", "falling_brick.png")).convert()
falling_meteor_img = pygame.image.load(os.path.join("resource", "falling_meteor.png")).convert()
falling_log_img = pygame.image.load(os.path.join("resource", "falling_log.png")).convert()
falling_pillar_img = pygame.image.load(os.path.join("resource", "falling_pillar.png")).convert()
falling_star_frag_img = pygame.image.load(os.path.join("resource", "falling_star_frag.png")).convert()
cloud_images = [cloud_1_img, cloud_2_img, cloud_3_img, cloud_4_img, cloud_5_img]
for i in range(5): cloud_images[i].set_colorkey(GREEN)
falling_items_images = [falling_rock_img, falling_stick_img, falling_star_raindrop_img, falling_brick_img, falling_meteor_img, falling_log_img, falling_pillar_img, falling_star_frag_img]
for i in range(8): falling_items_images[i].set_colorkey(GREEN)
#按鈕圖片
button_play_img = pygame.image.load(os.path.join("resource", "button_play.png")).convert()
button_options_img = pygame.image.load(os.path.join("resource", "button_options.png")).convert()
button_quit_img = pygame.image.load(os.path.join("resource", "button_quit.png")).convert()
button_save_img = pygame.image.load(os.path.join("resource", "button_save.png")).convert()
button_load_img = pygame.image.load(os.path.join("resource", "button_load.png")).convert()
button_keys_img = pygame.image.load(os.path.join("resource", "button_keys.png")).convert()
button_back_img = pygame.image.load(os.path.join("resource", "button_back.png")).convert()
button_right_img = pygame.image.load(os.path.join("resource", "button_right.png")).convert()
button_left_img = pygame.image.load(os.path.join("resource", "button_left.png")).convert()
button_use_img = pygame.image.load(os.path.join("resource", "button_use.png")).convert()
button_close_img = pygame.image.load(os.path.join("resource", "button_close.png")).convert()
button_yes_img = pygame.image.load(os.path.join("resource", "button_yes.png")).convert()
button_no_img = pygame.image.load(os.path.join("resource", "button_no.png")).convert()
button_music_on_img = pygame.image.load(os.path.join("resource", "button_music_on.png")).convert()
button_music_off_img = pygame.image.load(os.path.join("resource", "button_music_off.png")).convert()
button_space_img = pygame.image.load(os.path.join("resource", "button_space.png")).convert()
button_submit_img = pygame.image.load(os.path.join("resource", "button_submit.png")).convert()
t1_lootchest_img = pygame.image.load(os.path.join("resource", "t1_lootchest.png")).convert()
t2_lootchest_img = pygame.image.load(os.path.join("resource", "t2_lootchest.png")).convert()
t3_lootchest_img = pygame.image.load(os.path.join("resource", "t3_lootchest.png")).convert()
t4_lootchest_img = pygame.image.load(os.path.join("resource", "t4_lootchest.png")).convert()
lootchest_images = [t1_lootchest_img, t2_lootchest_img, t3_lootchest_img, t4_lootchest_img]
for i in range(4): lootchest_images[i].set_colorkey(WHITE)
icon_backpack_img = pygame.image.load(os.path.join("resource", "icon_backpack.png")).convert()
icon_backpack_img.set_colorkey(YELLOW)
icon_stats_img = pygame.image.load(os.path.join("resource", "icon_stats.png")).convert()
icon_stats_img.set_colorkey(YELLOW)
icon_menu_img = pygame.image.load(os.path.join("resource", "icon_menu.png")).convert()
icon_menu_img.set_colorkey(YELLOW)
icon_info_img = pygame.image.load(os.path.join("resource", "icon_info.png")).convert_alpha()
icon_info_img = pygame.transform.scale(icon_info_img, (60, 60))
inventory_img = pygame.image.load(os.path.join("resource", "inventory.png")).convert()
hotbar_img = pygame.image.load(os.path.join("resource", "hotbar.png")).convert()
inv_weapons_img = pygame.image.load(os.path.join("resource", "inv_weapons.png")).convert()
inv_armors_img = pygame.image.load(os.path.join("resource", "inv_armors.png")).convert()
inv_charms_img = pygame.image.load(os.path.join("resource", "inv_charms.png")).convert()
inv_misc_img = pygame.image.load(os.path.join("resource", "inv_misc.png")).convert()
quest_col_img = pygame.image.load(os.path.join("resource", "quest_col.png")).convert_alpha()
save_ui_img = pygame.image.load(os.path.join("resource", "save_ui.png")).convert()
selected_save_img = pygame.image.load(os.path.join("resource", "selected_save.png")).convert()
load_warning_img = pygame.image.load(os.path.join("resource", "load_warning.png")).convert()
save_warning_img = pygame.image.load(os.path.join("resource", "save_warning.png")).convert()
message_background_img = pygame.image.load(os.path.join("resource", "message_background.png")).convert_alpha()
message_background_img.set_alpha(128)
#waepon
item_iron_sword_img = pygame.image.load(os.path.join("resource", "item_iron_sword.png")).convert()
item_wooden_bow_img = pygame.image.load(os.path.join("resource", "item_wooden_bow.png")).convert()
item_wand_img = pygame.image.load(os.path.join("resource", "item_wand.png")).convert()
item_spirit_harvester_img = pygame.image.load(os.path.join("resource", "item_spirit_harvester.png")).convert()
item_silvermoon_blade_img = pygame.image.load(os.path.join("resource", "item_silvermoon_blade.png")).convert()
#armor
#charm
item_basic_shadow_charm = pygame.image.load(os.path.join("resource", "item_basic_shadow_charm.png")).convert()
item_intermediate_shadow_charm = pygame.image.load(os.path.join("resource", "item_intermediate_shadow_charm.png")).convert()
item_advanced_shadow_charm = pygame.image.load(os.path.join("resource", "item_advanced_shadow_charm.png")).convert()
item_basic_air_blade_charm = pygame.image.load(os.path.join("resource", "item_basic_air_blade_charm.png")).convert()
item_intermediate_air_blade_charm = pygame.image.load(os.path.join("resource", "item_intermediate_air_blade_charm.png")).convert()
item_advanced_air_blade_charm = pygame.image.load(os.path.join("resource", "item_advanced_air_blade_charm.png")).convert()
#currency
item_coin_img = pygame.image.load(os.path.join("resource", "item_coin.png")).convert()
#loot
item_slime_glue_img = pygame.image.load(os.path.join("resource", "item_slime_glue.png")).convert()
item_bone_img =  pygame.image.load(os.path.join("resource", "item_bone.png")).convert()
item_stick_img = pygame.image.load(os.path.join("resource", "item_stick.png")).convert()
item_tree_frag_img = pygame.image.load(os.path.join("resource", "item_tree_frag.png")).convert()
item_rotten_flesh_img = pygame.image.load(os.path.join("resource", "item_rotten_flesh.png")).convert()
item_basic_ore_img = pygame.image.load(os.path.join("resource", "item_basic_ore.png")).convert()
item_iron_ingot_img = pygame.image.load(os.path.join("resource", "item_iron_ingot.png")).convert()
#consumable
item_honey_bread_img = pygame.image.load(os.path.join("resource", "item_honey_bread.png")).convert()
item_breeze_cookie_img = pygame.image.load(os.path.join("resource", "item_breeze_cookie.png")).convert()
item_autumn_delicacy_img = pygame.image.load(os.path.join("resource", "item_autumn_delicacy.png")).convert()
#quest item
item_soul_frag_img = pygame.image.load(os.path.join("resource", "item_soul_frag.png")).convert()
item_crystal_of_life_img = pygame.image.load(os.path.join("resource", "item_crystal_of_life.png")).convert()
item_crystal_of_strength_img = pygame.image.load(os.path.join("resource", "item_crystal_of_strength.png")).convert()
item_aurora_wing_img = pygame.image.load(os.path.join("resource", "item_aurora_wing.png")).convert()
item_crimson_blade_img = pygame.image.load(os.path.join("resource", "item_crimson_blade.png")).convert()
c_stats_img = pygame.image.load(os.path.join("resource", "c_stats.png")).convert()
c_total_img = pygame.image.load(os.path.join("resource", "c_total.png")).convert()
c_bonus_img = pygame.image.load(os.path.join("resource", "c_bonus.png")).convert()
c_base_img = pygame.image.load(os.path.join("resource", "c_base.png")).convert()
trade_arrow_img = pygame.image.load(os.path.join("resource", "trade_arrow.png")).convert()
trade_arrow_img.set_colorkey(GREEN)
puzzle_01_img = pygame.image.load(os.path.join("resource", "puzzle_01.png")).convert()
p_water_rune_img = pygame.image.load(os.path.join("resource", "p_water_rune.png")).convert()
p_fire_rune_img = pygame.image.load(os.path.join("resource", "p_fire_rune.png")).convert()
p_air_rune_img = pygame.image.load(os.path.join("resource", "p_air_rune.png")).convert()
p_earth_rune_img = pygame.image.load(os.path.join("resource", "p_earth_rune.png")).convert()
p_thunder_rune_img = pygame.image.load(os.path.join("resource", "p_thunder_rune.png")).convert()
#圖標:屬性
icon_water_img = pygame.image.load(os.path.join("resource", "icon_water.png")).convert()
icon_fire_img = pygame.image.load(os.path.join("resource", "icon_fire.png")).convert()
icon_air_img = pygame.image.load(os.path.join("resource", "icon_air.png")).convert()
icon_earth_img = pygame.image.load(os.path.join("resource", "icon_earth.png")).convert()
icon_thunder_img = pygame.image.load(os.path.join("resource", "icon_thunder.png")).convert()
icon_physical_img = pygame.image.load(os.path.join("resource", "icon_physical.png")).convert()
icon_light_img = pygame.image.load(os.path.join("resource", "icon_light.png")).convert()
icon_dark_img = pygame.image.load(os.path.join("resource", "icon_dark.png")).convert()
#圖標:效果
icon_strength_img = pygame.image.load(os.path.join("resource", "icon_strength.png")).convert()
icon_weakness_img = pygame.image.load(os.path.join("resource", "icon_weakness.png")).convert()
icon_burning_img = pygame.image.load(os.path.join("resource", "icon_burning.png")).convert()
icon_vulnerable_img = pygame.image.load(os.path.join("resource", "icon_vulnerable.png")).convert()
icon_slowness_img = pygame.image.load(os.path.join("resource", "icon_slowness.png")).convert()
icon_crimson_harvest_img = pygame.image.load(os.path.join("resource", "icon_crimson_harvest.png")).convert()
icon_strength_img = pygame.transform.scale(icon_strength_img, (60, 60))
icon_weakness_img = pygame.transform.scale(icon_weakness_img, (60, 60))
icon_burning_img = pygame.transform.scale(icon_burning_img, (60, 60))
icon_vulnerable_img = pygame.transform.scale(icon_vulnerable_img, (60, 60))
icon_slowness_img = pygame.transform.scale(icon_slowness_img, (60, 60))
icon_strength_img.set_colorkey(YELLOW)
icon_weakness_img.set_colorkey(YELLOW)
icon_burning_img.set_colorkey(YELLOW)
icon_vulnerable_img.set_colorkey(YELLOW)
icon_slowness_img.set_colorkey(YELLOW)
mini_icon_water_img = pygame.transform.scale(icon_water_img, (20, 20))
mini_icon_fire_img = pygame.transform.scale(icon_fire_img, (20, 20))
mini_icon_air_img = pygame.transform.scale(icon_air_img, (20, 20))
mini_icon_earth_img = pygame.transform.scale(icon_earth_img, (20, 20))
mini_icon_thunder_img = pygame.transform.scale(icon_thunder_img, (20, 20))
mini_icon_physical_img = pygame.transform.scale(icon_physical_img, (20, 20))
mini_icon_light_img = pygame.transform.scale(icon_light_img, (20, 20))
mini_icon_dark_img = pygame.transform.scale(icon_dark_img, (20, 20))
mini_icon_water_img.set_colorkey(BLACK)
mini_icon_fire_img.set_colorkey(BLACK)
mini_icon_air_img.set_colorkey(BLACK)
mini_icon_earth_img.set_colorkey(BLACK)
mini_icon_thunder_img.set_colorkey(BLACK)
mini_icon_physical_img.set_colorkey(WHITE)
mini_icon_light_img.set_colorkey(WHITE)
mini_icon_dark_img.set_colorkey(WHITE)
effect_icons = {"strength":icon_strength_img, "weakness":icon_weakness_img, "burn":icon_burning_img, "vulnerable":icon_vulnerable_img, "slowness":icon_slowness_img}
forge_img = pygame.image.load(os.path.join("resource", "forge.png")).convert()
#天賦樹
#介面
ability_tree_selected_img = pygame.image.load(os.path.join("resource", "ability_tree_selected.png")).convert()
ability_tree_arrow_right_img = pygame.image.load(os.path.join("resource", "ability_tree_arrow_right.png")).convert()
ability_tree_arrow_left_img = pygame.image.load(os.path.join("resource", "ability_tree_arrow_left.png")).convert()
ability_tree_arrow_top_img = pygame.image.load(os.path.join("resource", "ability_tree_arrow_top.png")).convert()
ability_tree_sidebar_img = pygame.image.load(os.path.join("resource", "ability_tree_sidebar.png")).convert()
ability_tree_hotbar_img = pygame.image.load(os.path.join("resource", "ability_tree_hotbar.png")).convert()
ability_tree_rogue_img = pygame.image.load(os.path.join("resource", "ability_tree_rogue.png")).convert()
ability_tree_archer_img = pygame.image.load(os.path.join("resource", "ability_tree_archer.png")).convert()
ability_tree_mage_img = pygame.image.load(os.path.join("resource", "ability_tree_mage.png")).convert()
ability_tree_reset_button_img = pygame.image.load(os.path.join("resource", "ability_tree_reset_button.png")).convert()
ability_tree_upgrade_img = pygame.image.load(os.path.join("resource", "ability_tree_upgrade.png")).convert()
ability_tree_cancel_img = pygame.image.load(os.path.join("resource", "ability_tree_cancel.png")).convert()
ability_tree_empty_button_img = pygame.image.load(os.path.join("resource", "ability_tree_empty_button.png")).convert()
ability_tree_w_button_img = pygame.image.load(os.path.join("resource", "ability_tree_w_button.png")).convert()
ability_tree_e_button_img = pygame.image.load(os.path.join("resource", "ability_tree_e_button.png")).convert()
ability_tree_r_button_img = pygame.image.load(os.path.join("resource", "ability_tree_r_button.png")).convert()
ability_tree_s_button_img = pygame.image.load(os.path.join("resource", "ability_tree_s_button.png")).convert()
mouse_mid_click_img = pygame.image.load(os.path.join("resource", "mouse_mid_click.png")).convert()
mouse_mid_click_img = pygame.transform.scale(mouse_mid_click_img, (20, 30))
ability_tree_selected_img.set_colorkey(AGRAY)
ability_tree_arrow_right_img.set_colorkey(AGRAY)
ability_tree_arrow_left_img.set_colorkey(AGRAY)
ability_tree_arrow_top_img.set_colorkey(AGRAY)
#節點
ability_tree_rogue_node = []
ability_tree_archer_node = []
ability_tree_mage_node = []
for i in range(19): ability_tree_rogue_node.append(pygame.image.load(os.path.join("resource", "ability_tree_rogue_" + str(i) + ".png")).convert())
for i in range(6): ability_tree_archer_node.append(pygame.image.load(os.path.join("resource", "ability_tree_archer_" + str(i) + ".png")).convert())
for i in range(6): ability_tree_mage_node.append(pygame.image.load(os.path.join("resource", "ability_tree_mage_" + str(i) + ".png")).convert())
#技能圖標
icon_recast_img = pygame.image.load(os.path.join("resource", "icon_recast.png")).convert()
rogue_skill1_img = pygame.image.load(os.path.join("resource", "rogue_skill1.png")).convert()
rogue_skill2_img = pygame.image.load(os.path.join("resource", "rogue_skill2.png")).convert()
rogue_skill3_img = pygame.image.load(os.path.join("resource", "rogue_skill3.png")).convert()
rogue_skill4_img = pygame.image.load(os.path.join("resource", "rogue_skill4.png")).convert()
rogue_skill5_img = pygame.image.load(os.path.join("resource", "rogue_skill5.png")).convert()
rogue_skill6_img = pygame.image.load(os.path.join("resource", "rogue_skill6.png")).convert()
rogue_ultimate_img = pygame.image.load(os.path.join("resource", "rogue_ultimate.png")).convert()
archer_skill1_img = pygame.image.load(os.path.join("resource", "archer_skill1.png")).convert()
archer_ultimate_img = pygame.image.load(os.path.join("resource", "archer_ultimate.png")).convert()
mage_skill1_img = pygame.image.load(os.path.join("resource", "mage_skill1.png")).convert()
mage_ultimate_img = pygame.image.load(os.path.join("resource", "mage_ultimate.png")).convert()
icon_recast_img.set_colorkey(WHITE)
rogue_skill1_img.set_colorkey(GREEN)
rogue_skill2_img.set_colorkey(GREEN)
rogue_skill3_img.set_colorkey(GREEN)
rogue_skill4_img.set_colorkey(GREEN)
rogue_skill5_img.set_colorkey(GREEN)
rogue_skill6_img.set_colorkey(GREEN)
rogue_ultimate_img.set_colorkey(GREEN)
archer_skill1_img.set_colorkey(GREEN)
archer_ultimate_img.set_colorkey(GREEN)
mage_skill1_img.set_colorkey(GREEN)
mage_ultimate_img.set_colorkey(GREEN)
smoke_bomb_img = rogue_skill6_img.subsurface(rogue_skill6_img.get_bounding_rect()).copy()
portal_img = pygame.image.load(os.path.join("resource", "portal.png")).convert()
depth_room_menu_img = pygame.image.load(os.path.join("resource", "depth_room_menu.png")).convert()
depth_blessing_menu_img = pygame.image.load(os.path.join("resource", "depth_blessing_menu.png")).convert()
depth_blessing_upgrade_img = pygame.image.load(os.path.join("resource", "depth_blessing_upgrade.png")).convert()
depth_blessing_list_img = pygame.image.load(os.path.join("resource", "depth_blessing_list.png")).convert()
depth_blessing_slot_img = pygame.image.load(os.path.join("resource", "depth_blessing_slot.png")).convert()
depth_sewer_img = pygame.image.load(os.path.join("resource", "depth_sewer.png")).convert()
depth_disguiseMerchant_img = pygame.image.load(os.path.join("resource", "depth_disguiseMerchant.png")).convert()
depth_attackGuard_img = pygame.image.load(os.path.join("resource", "depth_attackGuard.png")).convert()
depth_combat_img = pygame.image.load(os.path.join("resource", "depth_combat.png")).convert()
depth_event_img = pygame.image.load(os.path.join("resource", "depth_event.png")).convert()
depth_market_img = pygame.image.load(os.path.join("resource", "depth_market.png")).convert()
depth_challenge_img = pygame.image.load(os.path.join("resource", "depth_challenge.png")).convert()
dd_blessing_atk = [pygame.image.load(os.path.join("resource", f"dd_blessing_atk_t{i}.png")).convert() for i in range(1, 6)]
dd_blessing_def = [pygame.image.load(os.path.join("resource", f"dd_blessing_def_t{i}.png")).convert() for i in range(1, 6)]
dd_blessing_spd = [pygame.image.load(os.path.join("resource", f"dd_blessing_spd_t{i}.png")).convert() for i in range(1, 6)]
dd_blessing_hpr = [pygame.image.load(os.path.join("resource", f"dd_blessing_hpr_t{i}.png")).convert() for i in range(1, 6)]
dd_blessing_cd = [pygame.image.load(os.path.join("resource", f"dd_blessing_cd_t{i}.png")).convert() for i in range(1, 6)]
dd_blessing_physical = [pygame.transform.scale(pygame.image.load(os.path.join("resource", f"dd_blessing_physical_t{i}.png")).convert(), (90, 90)) for i in range(1, 6)]
dd_blessing_water = [pygame.image.load(os.path.join("resource", f"dd_blessing_water_t{i}.png")).convert() for i in range(1, 6)]
dd_blessing_fire = [pygame.image.load(os.path.join("resource", f"dd_blessing_fire_t{i}.png")).convert() for i in range(1, 6)]
dd_blessing_explode = [pygame.image.load(os.path.join("resource", f"dd_blessing_explode_t{i}.png")).convert() for i in range(1, 6)]
dd_blessing_lbonus = [pygame.image.load(os.path.join("resource", f"dd_blessing_lbonus_t{i}.png")).convert() for i in range(1, 6)]
dd_blessing_lquality = [pygame.image.load(os.path.join("resource", f"dd_blessing_lquality_t{i}.png")).convert() for i in range(1, 6)]
dd_start_img = [pygame.image.load(os.path.join("resource", f"dd_start_{i}.png")).convert() for i in range(1, 4)]
dd_abandoned_sewer_img = pygame.image.load(os.path.join("resource", "dd_abandoned_sewer.png")).convert()
dd_boss_challenge_1_img = pygame.image.load(os.path.join("resource", "dd_boss_challenge_1.png")).convert()
dd_boss_challenge_2_img = pygame.image.load(os.path.join("resource", "dd_boss_challenge_2.png")).convert()
dd_boss_challenge_3_img = pygame.image.load(os.path.join("resource", "dd_boss_challenge_3.png")).convert()
dd_reward_img = pygame.image.load(os.path.join("resource", "dd_reward.png")).convert()
dd_normal_skill_img = pygame.image.load(os.path.join("resource", "dd_normal_skill.png")).convert()
dd_normal_upgrade_img = pygame.image.load(os.path.join("resource", "dd_normal_upgrade.png")).convert()
dd_normal_treasure_img = pygame.image.load(os.path.join("resource", "dd_normal_treasure.png")).convert()
dd_utility_img = pygame.image.load(os.path.join("resource", "dd_utility.png")).convert()
dd_elite_skill_img = pygame.image.load(os.path.join("resource", "dd_elite_skill.png")).convert()
dd_elite_upgrade_img = pygame.image.load(os.path.join("resource", "dd_elite_upgrade.png")).convert()
dd_elite_treasure_img = pygame.image.load(os.path.join("resource", "dd_elite_treasure.png")).convert()
dd_boss_img = pygame.image.load(os.path.join("resource", "dd_boss.png")).convert()
depth_room_background_img = {"起始房間1":dd_start_img[0], "起始房間2":dd_start_img[1], "起始房間3":dd_start_img[2], "廢棄下水道":dd_abandoned_sewer_img, "假扮商隊":dd_start_img[0], "攻擊守衛":dd_start_img[0] ,"魔王1":dd_boss_challenge_1_img, "魔王2":dd_boss_challenge_2_img, "魔王3":dd_boss_challenge_3_img, "獎勵房":dd_reward_img}
depth_room_icon = {"戰鬥":depth_combat_img, "事件":depth_event_img, "黑市":depth_market_img, "挑戰":depth_challenge_img, "魔王":dd_boss_img, "廢棄下水道":depth_sewer_img, "假扮商隊":depth_disguiseMerchant_img, "攻擊守衛":depth_attackGuard_img, "魔王1":dd_boss_img, "魔王2":dd_boss_img, "魔王3":dd_boss_img}
#背景
area_background_imgs = {}
special_areas = [6, 8, 12, 16]
for i in range(-8, 21):
    img = pygame.image.load(os.path.join("resource", "area" + str(i) + ".png")).convert()
    img.set_colorkey(SKY_BACKBROUND)
    area_background_imgs.update({str(i):img})
    if i in special_areas:
        img = pygame.image.load(os.path.join("resource", "area" + str(i) + ("_2" if i in special_areas else "") + ".png")).convert()
        img.set_colorkey(SKY_BACKBROUND)
        area_background_imgs.update({str(i) + "_2":img})
background_forward_img = pygame.image.load(os.path.join("resource", "area2.png")).convert()
background_backward_img = pygame.image.load(os.path.join("resource", "area0.png")).convert()
background_img = pygame.image.load(os.path.join("resource", "area1.png")).convert()
area_tower_top_img = pygame.image.load(os.path.join("resource", "area-2.png")).convert()
hotbar_class_slot_img = pygame.image.load(os.path.join("resource", "hotbar_class_slot.png")).convert()
Rogue1_icon_img = pygame.transform.scale(item_iron_sword_img, (40, 40))
Rogue2_icon_img = pygame.transform.scale(item_iron_sword_img, (25, 25))
Archer1_icon_img = pygame.transform.scale(item_wooden_bow_img, (40, 40))
Archer2_icon_img = pygame.transform.scale(item_wooden_bow_img, (25, 25))
Mage1_icon_img = pygame.transform.scale(item_wand_img, (40, 40))
Mage2_icon_img = pygame.transform.scale(item_wand_img, (25, 25))
icon_health_regen_img = pygame.transform.scale(dd_blessing_hpr[0], (40, 40))
icon_speed_img = pygame.transform.scale(dd_blessing_spd[0], (40, 40))
icon_crimson_harvest_img = pygame.transform.scale(icon_crimson_harvest_img, (40, 40))
# os.dup2(sys.__stderr__.fileno(), stderr_fileno)
# os.close(devnull)
#載入字體
text_font = os.path.join("resource", "font.ttf")
text_font_2 = os.path.join("resource", "font2.ttf")
#玩家名稱
player_name = "Player"
#切換音樂
def switch_music(music, time = -1):
    if music == 1 and Music.music:
        pygame.mixer.music.load(os.path.join("resource", "music_vast_valley.wav"))
        new_message("正在播放 - Vast Valley by Radiarc")
    if music == 2 and Music.music:
        pygame.mixer.music.load(os.path.join("resource", "music_street.wav"))
        new_message("正在播放 - 街 by 煉獄小僧")
    if music == 3 and Music.music:
        pygame.mixer.music.load(os.path.join("resource", "music_the_great_race.wav"))
        new_message("正在播放 - The Great Race by abiswas")
    if music == 4 and Music.music:
        pygame.mixer.music.load(os.path.join("resource", "music_forest_dance.wav"))
        new_message("正在播放 - Forest Dance by Salted")
    if music == 5 and Music.music:
        pygame.mixer.music.load(os.path.join("resource", "music_ruins_of_harmony.wav"))
        new_message("正在播放 - Ruins of Harmony by Radiarc")
    if music == 6 and Music.music:
        pygame.mixer.music.load(os.path.join("resource", "music_tangled_in_endless_roots.wav"))
        new_message("正在播放 - Tangled in Endless Roots by Corpe_")
    if music == 7 and Music.music:
        pygame.mixer.music.load(os.path.join("resource", "music_one_against_the_world.wav"))
        new_message("正在播放 - One Against the World by Antti Martikainen")
    if music == 8 and Music.music:
        pygame.mixer.music.load(os.path.join("resource", "music_hopes_and_dreams.wav"))
        new_message("正在播放 - Hopes and Dreams by Toby Fox")
    if music == 9 and Music.music:
        pygame.mixer.music.load(os.path.join("resource", "music_adventure.mp3"))
        new_message("正在播放 - Adventure by Salted")
    if music == 10 and Music.music:
        pygame.mixer.music.load(os.path.join("resource", "music_ascension_to_heaven.mp3"))
        new_message("正在播放 - Ascension to Heaven by xi")
    if music == 11 and Music.music:
        pygame.mixer.music.load(os.path.join("resource", "music_cataclysm_from_the_stars.mp3"))
        new_message("正在播放 - Cataclysm from the Stars by CmdrGod")
    if Music.music:
        pygame.mixer.music.play(time)
        pygame.mixer.music.set_volume(0.6)
#畫出圖片
def draw_img(surf, img, x, y):
    if type(img) != int:
        img_rect = img.get_rect()
        img_rect.x = x
        img_rect.y = y
        surf.blit(img, img_rect)
#文字顯示
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(text_font, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)
#中文字+顏色
def draw_color_text(surf, text, size, x, y, color):
    font = pygame.font.Font(text_font_2, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)
#外框字
def outline_text(text, size, x, y, color):
    font = pygame.font.Font(text_font_2, size)
    base = font.render(str(text), True, BLACK)  # 渲染外框
    outline = pygame.Surface((base.get_width() + 4, base.get_height() + 4), pygame.SRCALPHA)
    text_surface = font.render(str(text), True, color)  # 渲染主文字
    # 繪製外框 (上下左右四個方向)
    for dx in [-2, 2]:
        for dy in [-2, 2]:
            outline.blit(base, (dx + 2, dy + 2))
    # 中心繪製主文字
    outline.blit(text_surface, (2, 2))
    screen.blit(outline, (x, y))
#NPC
def summon_npc(coord_x, y, interactions, name, img):
    coord_x = player.rect.x - (Player_location.coord_x - coord_x)
    draw_color_text(screen,f"[{name}]", 20, coord_x, y - 40 , LBLUE)
    draw_img(screen, img, coord_x - img.get_width() / 2, y)
    if abs(player.rect.x - (coord_x + 80 - img.get_width() / 2)) <= 80:
        y_move = 0
        for option, action in interactions.items():
            y_move += 60
            draw_img(screen, ability_tree_empty_button_img, coord_x + 50, y - 50 + y_move)
            draw_color_text(screen, option, 30, coord_x + 125, y - 45 + y_move, WHITE)
            press_button = pygame.mouse.get_pressed()
            if is_hovering(coord_x + 50, coord_x + 200, y - 50 + y_move, y + y_move, Mouse.x, Mouse.y):
                pygame.draw.rect(screen, WHITE, (coord_x + 50, y - 50 + y_move, 150, 50), 3)
                if press_button[0]:
                    return option, action
#血條
def draw_health(surf, hp, limit, x, y, color):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 150
    BAR_HEIGHT = 20
    fill = (hp/limit) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    fill_rect_2 = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    pygame.draw.rect(surf, GRAY, fill_rect_2)
    pygame.draw.rect(surf, color, fill_rect)
    pygame.draw.rect(surf, BLACK, outline_rect, 2)
    draw_color_text(screen, str(math.ceil(hp)) + "/" + str(round(limit)), 20, x + 70, y - 5, BLACK)
#普通怪物血條
def draw_mob_health(hp, limit, x, y, name, level, effect, weakness, defense, rank):
    draw_health(screen, hp, limit, x, y, RED)
    draw_color_text(screen, "[Lv." + str(level) + "] " + name, 20, x + 75, y - 65, BLACK if rank == "normal" else GOLD)
    #顯示防禦屬性
    element_icons = [mini_icon_physical_img, mini_icon_water_img, mini_icon_fire_img, mini_icon_air_img, mini_icon_earth_img, mini_icon_thunder_img, mini_icon_light_img, mini_icon_dark_img]
    draw_color_text(screen, "弱點:", 20, x + 50, y - 45, RED)
    w_move = 0
    for w in weakness:
        draw_img(screen, element_icons[w], x + 80 + w_move, y - 40)
        w_move += 20
    draw_color_text(screen, "抗性:", 20, x + 50, y - 25, RED)
    d_move = 0
    for d in defense:
        draw_img(screen, element_icons[d], x + 80 + d_move, y - 20)
        d_move += 20
    #顯示狀態效果
    e_move = 0
    for key, value in effect.items():
        if value > 0 and key != None:
            draw_img(screen, effect_icons.get(key), x - 20 + e_move, y - 120)
            e_move += 50
#魔王血條
def draw_boss_health(surf, hp, limit, color, name, subname, effect, weakness, defense):
    All_mobs.boss_fight_active = True
    outline_text(str(name), 30, 400, 10, WHITE)
    outline_text(str(subname), 20, 450, 45, WHITE)
    if hp < 0:
        hp = 0
    BAR_LENGTH = 500
    BAR_HEIGHT = 15
    fill = (hp/limit)*BAR_LENGTH
    outline_rect = pygame.Rect(250, 80, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(250, 80, fill, BAR_HEIGHT)
    fill_rect_2 = pygame.Rect(250, 80, BAR_LENGTH, BAR_HEIGHT)
    pygame.draw.rect(surf, GRAY, fill_rect_2)
    pygame.draw.rect(surf, color, fill_rect)
    pygame.draw.rect(surf, BLACK, outline_rect, 2)
    draw_color_text(screen, str(math.ceil(hp)) + "/" + str(limit) + "  (" + str(round(hp / limit * 100)) + "%)", 13, 500, 78, BLACK)
    draw_color_text(screen, "弱點:", 25, 300, 30, (230, 50, 50))
    w_move = 0
    element_icons = [mini_icon_physical_img, mini_icon_water_img, mini_icon_fire_img, mini_icon_air_img, mini_icon_earth_img, mini_icon_thunder_img,mini_icon_light_img, mini_icon_dark_img]
    for w in weakness:
        draw_img(screen, element_icons[w], 330 + w_move, 40)
        w_move += 20
    draw_color_text(screen, "抗性:", 25, 300, 50, LBLUE)
    d_move = 0
    for d in defense:
        draw_img(screen, element_icons[d], 330 + d_move, 60)
        d_move += 20
    #顯示狀態效果
    if any(effects[1] > 0 for effects in effect.items()): draw_color_text(screen, "狀態:", 25, 620, 40, RED)
    e_move = 0
    for key, value in effect.items():
        if value > 0:
            draw_img(screen, effect_icons[key], 640 + e_move, 25)
            e_move += 50
#進度條(任意)
def progress_bar(progress, max_progress, name, subname, unit, namecolor, subnamecolor, barcolor):
    draw_color_text(screen, str(name), 40, 500, 10, namecolor)
    draw_color_text(screen, str(subname), 30, 500, 55, subnamecolor)
    BAR_LENGTH = 500
    BAR_HEIGHT = 30
    fill = (progress / max_progress) * BAR_LENGTH
    outline_rect = pygame.Rect(250, 90, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(250, 90, fill, BAR_HEIGHT)
    fill_rect_2 = pygame.Rect(250, 90, BAR_LENGTH, BAR_HEIGHT)
    pygame.draw.rect(screen, GRAY, fill_rect_2)
    pygame.draw.rect(screen, barcolor, fill_rect)
    pygame.draw.rect(screen, BLACK, outline_rect, 2)
    draw_color_text(screen, str(math.ceil(progress)) + "/" + str(max_progress) + unit, 30, 500, 85, BLACK)
#怪物技能提示條
def mob_skill_bar(x, y, name, time, total_time):
    BAR_LENGTH = 80
    BAR_HEIGHT = 15
    fill = (time/total_time)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    fill_rect_2 = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    pygame.draw.rect(screen, GRAY, fill_rect_2)
    pygame.draw.rect(screen, RED, fill_rect)
    pygame.draw.rect(screen, BLACK, outline_rect, 2)
    draw_color_text(screen, "!" + name + "!" , 20, x + 35, y - 30, RED)
#魔王技能提示條
def boss_skill_bar(name, time, total_time, location, bar_color = TEAL):
    BAR_LENGTH = 500
    BAR_HEIGHT = 10
    location = location * 40
    fill = (time/total_time) * BAR_LENGTH
    outline_rect = pygame.Rect(250, 130 + location, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(250, 130 + location, fill, BAR_HEIGHT)
    fill_rect_2 = pygame.Rect(250, 130 + location, BAR_LENGTH, BAR_HEIGHT)
    pygame.draw.rect(screen, GRAY, fill_rect_2)
    pygame.draw.rect(screen, bar_color, fill_rect)
    pygame.draw.rect(screen, BLACK, outline_rect, 2)
    draw_color_text(screen, name, 20, 500, 100 + location, (230, 100, 21))
#怪物除錯資訊
def mob_debug_info(mob_name, x, y, radius, damage, element, code, source, player_name, duration, kb, effect, effect_duration, health, health_limit):
    print(f"""
Attack #{code}
{mob_name} 在 ({x}, {y}) 受到了攻擊，剩餘生命值({health}/{health_limit})!
攻擊範圍: 半徑 {radius} 格內
傷害: 受到 {damage} 點 {element} 屬性傷害
攻擊來源: {source} ({player_name})
攻擊剩餘時間: {duration}
擊退距離: {kb}
附加效果: {effect} (持續 {effect_duration})
--------------------
""")
#被動能力條
def draw_passive_bar(surf, value, limit, x, y, color, name):
    if value < 0:
        value = 0
    BAR_LENGTH = 250
    BAR_HEIGHT = 20
    fill = (value/limit)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    fill_rect_2 = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    pygame.draw.rect(surf, GRAY, fill_rect_2)
    pygame.draw.rect(surf, color, fill_rect)
    pygame.draw.rect(surf, BLACK, outline_rect, 2)
    draw_color_text(screen, name + " " + str(math.ceil(value / 60)) + "/" + str(limit // 60), 20, x + 125, y - 5, BLACK)
#檢測圓是否相交
def are_circles_intersecting(x1, y1, r1, x2, y2, r2):
    # 計算圓心距離
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    # 檢查是否相交
    if distance <= r1 + r2:# and distance >= abs(r1 - r2):
        return True
    return False
#選單文字
def menu_text(surf, text, size, x, y):
    font = pygame.font.Font(text_font, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)
#鍛造進度條
def forge_progress(surf, time, max_time, x, y):
    if time < 0:
        time = 0
    BAR_LENGTH = 430
    BAR_HEIGHT = 10
    fill = (time/max_time)*BAR_LENGTH
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GOLD, fill_rect)
#物品欄文字
def inv_item_text(displayItem):
    displayItem = search_item(displayItem)
    if Inv.use and Inv.type == "normal" and displayItem.get("equip", False): equip_item(displayItem, displayItem["itemType"], displayItem.get("charmSlot", 0))
    y_move = 0
    #顯示物品名稱&圖像
    pygame.draw.rect(screen, DCGRAY, (Inv.info_loc_x, Inv.info_loc_y - 20, 500, 600))
    draw_img(screen, displayItem["img"], Inv.info_loc_x + 200, Inv.info_loc_y)
    pygame.draw.rect(screen, BLACK, (Inv.info_loc_x + 200, Inv.info_loc_y, 90, 90), 3)
    draw_color_text(screen, displayItem["name"], 30, Inv.info_loc_x + 250, Inv.info_loc_y + 90, displayItem["rarity"])
    #顯示物品是否裝備
    if displayItem.get("equip", False) and is_item_equipped(displayItem) and Inv.open: outline_text("(已裝備)", 20, Inv.info_loc_x + 208, Inv.info_loc_y + 60, GREEN)
    rarity_map = {COMMON:"普通", UNCOMMON:"常見", RARE:"稀有", EPIC:"史詩", LEGENDARY:"傳奇"}
    #顯示物品稀有度
    draw_color_text(screen, "稀有度: " + rarity_map.get(displayItem["rarity"], '未知') , 20, Inv.info_loc_x + 250, Inv.info_loc_y + 130, displayItem["rarity"])
    #顯示物品來源
    draw_color_text(screen, displayItem["location"]["locationName"], 20, Inv.info_loc_x + 250, Inv.info_loc_y + 150, displayItem["location"]["locationColor"])
    #顯示物品屬性
    if displayItem.get("attribute", False):
        for attribute, value in displayItem["attribute"].items():
            negative_attribute = ["冷卻時間"]
            special_prefix = {"%":"%", "t":""}
            attribute_suffix = ""
            hide_plus_sign = attribute[-1] == "t"
            for prefix, suffix in special_prefix.items():
                if attribute[-1] == prefix:
                    attribute = attribute[:-1]
                    attribute_suffix = suffix
            if attribute in negative_attribute: effect_color = RED if (type(value) != int or value > 0) else LBLUE
            else: effect_color = LBLUE if (type(value) != int or value > 0) else RED
            draw_color_text(screen, attribute + (" " if hide_plus_sign else " + ") + str(value) + attribute_suffix, 20, Inv.info_loc_x + 250, Inv.info_loc_y + 190 + y_move, effect_color)
            y_move += 30
    #顯示護符槽
    if displayItem.get("charmSlot", False):
        draw_color_text(screen, "護符槽: [ " + "★" * displayItem["charmSlot"] + " ]", 20, Inv.info_loc_x + 250, Inv.info_loc_y + 200 + y_move, GOLD)
        y_move += 30
    #顯示物品技能
    if displayItem.get("skill", False):
        skill_info = displayItem["skill"]
        draw_color_text(screen, skill_info["skillType"] + " " + ("[" if skill_info.get("skillTrigger", False) else "") + (skill_info.get("skillTrigger", False)) + ("]" if skill_info.get("skillTrigger", False) else "") + " " + skill_info["skillName"], 20, Inv.info_loc_x + 250, Inv.info_loc_y + 200 + y_move, GOLD)
        draw_color_text(screen, "消耗: " + skill_info["skillCost"], 20, Inv.info_loc_x + 250, Inv.info_loc_y + 230 + y_move, GREEN)
        draw_color_text(screen, "冷卻: " + str(skill_info["skillCD"]), 20, Inv.info_loc_x + 250, Inv.info_loc_y + 260 + y_move, GREEN)
        for skill_effect in skill_info["skillEffect"]: 
            draw_color_text(screen, skill_effect, 20, Inv.info_loc_x + 250, Inv.info_loc_y + 290 + y_move, LBLUE)
            y_move += 30
    #顯示物品敘述
    if displayItem.get("itemLore", False):
        if displayItem.get("attribute", False) == False: y_move -= 50
        if displayItem.get("skill", False) == False: y_move -= 100
        for item_lore in displayItem["itemLore"]:
            draw_color_text(screen, item_lore, 20, Inv.info_loc_x + 250, Inv.info_loc_y + 330 + y_move, GRAY)
            y_move += 30
    else: y_move -= 30
    if Inv.type == "normal": draw_color_text(screen, "已擁有: " + str(displayItem["count"]), 20, Inv.info_loc_x + 250, Inv.info_loc_y + 330 + y_move, GREEN)
#物品名稱查詢
def search_item(itemName):
    #搜索
    for item in Inv.inventory:
        if itemName == item["name"]: return item
#護符排序
def charm_order(name):
    #所有護符
    charms = [
    {"name": "初階影脈護符", "skill": "暗影脈衝", "rarity": "普通", "img":item_basic_shadow_charm, "slot":1},
    {"name": "中階影脈護符", "skill": "暗影脈衝", "rarity": "常見", "img":item_intermediate_shadow_charm, "slot":2},
    {"name": "高階影脈護符", "skill": "暗影脈衝", "rarity": "稀有", "img":item_advanced_shadow_charm, "slot":3},
    {"name": "初階空刃護符", "skill": "破空突擊", "rarity": "普通", "img":item_basic_air_blade_charm, "slot":1},
    {"name": "中階空刃護符", "skill": "破空突擊", "rarity": "常見", "img":item_intermediate_air_blade_charm, "slot":2},
    {"name": "高階空刃護符", "skill": "破空突擊", "rarity": "稀有", "img":item_advanced_air_blade_charm, "slot":3},
]
    # 技能的排序優先級
    skill_order = ["暗影脈衝", "破空突擊"]
    # 稀有度的排序優先級
    rarity_order = {"普通": 1, "常見": 2, "稀有": 3, "史詩": 4, "傳奇": 5}
    # 執業的排序優先級
    class_order = {"rogue": 1, "archer": 2, "mage": 3}
    # 排序規則函式
    def sort_key(charm):
        skill_priority = skill_order.index(charm["skill"]) if charm["skill"] in skill_order else len(skill_order)
        rarity_priority = rarity_order.get(charm["rarity"], len(rarity_order) + 1)
        class_priority = class_order.get(charm.get("class_type", ""), len(class_order) + 1) 
        return (class_priority, skill_priority, rarity_priority, charm["name"], charm["slot"])
    # 按規則排序護符列表
    sorted_charms = sorted(charms, key=sort_key)
    for index, charm in enumerate(sorted_charms):
        if charm["name"] == name:
            return (index, charm["img"], charm["slot"], name)
    return None
#從陣列中移除0
def remove_zero(arr):
    arr = [items for items in arr if items != 0]
    return arr
#裝備物品
def equip_item(item, item_type, charm_slot_cost = 0):
    if item_type not in ["charm", "consumable", "questItem"]:
        if item["name"] == Inv.equip[item_type]: Inv.equip[item_type] = ""
        else: Inv.equip[item_type] = item["name"]
    if item_type == "consumable":
        if is_item_equipped(item):
            Inv.equip["hotbar"].remove(item["name"])
        elif len(Inv.equip["hotbar"][1:]) < 4:
            Inv.equip["hotbar"].append(item["name"])
    elif item_type in ["charm", "questItem"]:
        if item["name"] in Inv.equip[item_type]:
            Inv.equip[item_type].remove(item["name"])
            Inv.charm_slot[0] -= charm_slot_cost 
        elif Inv.charm_slot[0] + charm_slot_cost <= Inv.charm_slot[1] or item_type != "charm":
            Inv.equip[item_type].append(item["name"])
            Inv.charm_slot[0] += charm_slot_cost
    Inv.use = False
#檢測物品是否裝備
def is_item_equipped(item):
    if item["itemType"] != "consumable":
        return item["name"] in (Inv.equip[item["itemType"]] if Inv.type == "normal" else Inv.equip_preview[item["itemType"]])
    if item["itemType"] == "consumable":
        return item["name"] in (Inv.equip["hotbar"] if Inv.type == "normal" else Inv.equip_preview["hotbar"])
#升級天賦能力
def upgrade_ability(class_type, ability, req_ability):
    class_dict = {1: ('rogue', Assassin), 2: ('archer', Archer), 3: ('mage', Mage)}
    class_name, class_obj = class_dict.get(class_type, (None, None))
    ability_tree = getattr(A_tree, class_name)
    if ability_tree[ability] == 0 and class_obj.a_point > 0 and all(ability_tree[req] > 0 for req in req_ability):
        ability_tree[ability] = 1
        class_obj.a_point -= 1
    elif ability_tree[ability] == 1 or any(ability_tree[req] < 0 for req in req_ability):
        ability_tree[ability] = 0
        class_obj.a_point += 1
#調整按鍵
def tweak_keybind(key, ability):
    if A_tree.cate == 1:ability_tree = A_tree.rogue
    elif A_tree.cate == 2:ability_tree = A_tree.archer
    elif A_tree.cate == 3:ability_tree = A_tree.mage
    if ability_tree[A_tree.showing_info[0]] and A_tree.showing_info[2].startswith("技能 -"):
        keybinds = A_tree.keybind[A_tree.cate - 1]
        #檢查該技能是否已經綁定在其他按鍵上
        for existing_key, bound_ability in keybinds.items():
            if bound_ability == ability:
                if existing_key == key:
                    #在同一按鍵重複綁定，則解除綁定
                    keybinds[existing_key] = ""
                    return
                else:
                    #否則交換按鍵
                    keybinds[existing_key], keybinds[key] = keybinds[key], keybinds[existing_key]
                    return
        #技能未綁定在其他按鍵上，直接綁定到新按鍵
        keybinds[key] = ability
#天賦樹節點
def draw_ability_tree_node(class_code, img_code, info):
    class_dict = {1: ('rogue', Assassin), 2: ('archer', Archer), 3: ('mage', Mage)}
    class_name, class_obj = class_dict.get(A_tree.cate, (None, None))
    ability_tree = getattr(A_tree, class_name)
    #檢測是否有前節點未學習
    if (info[-1] != "職業" and info[-1] != "二轉") and ability_tree[info[0]] == 1 and any(ability_tree[req] == 0 for req in info[1]):
        ability_tree[info[0]] = 0
        class_obj.a_point += 1
    if class_code == 1: node_img = ability_tree_rogue_node[img_code]
    if class_code == 2: node_img = ability_tree_archer_node[img_code]
    if class_code == 3: node_img = ability_tree_mage_node[img_code]
    draw_img(screen, node_img, info[-4] + A_tree.gui_location_x, info[-3] + A_tree.gui_location_y)
    if is_hovering_circle(info[-4] + info[-2] + A_tree.gui_location_x, info[-3] + info[-2] + A_tree.gui_location_y, info[-2], Mouse.x, Mouse.y): pygame.draw.circle(screen, GRAY, (info[-4] + A_tree.gui_location_x + info[-2], info[-3] + A_tree.gui_location_y + info[-2]), info[-2], 5)
    if is_hovering_circle(info[-4] + info[-2] + A_tree.gui_location_x, info[-3] + info[-2] + A_tree.gui_location_y, info[-2], Mouse.x, Mouse.y) and A_tree.lclick and Mouse.x < 700:
        A_tree.showing_info = info
        A_tree.node_img = node_img
#天賦樹資訊
def draw_ability_info():
    class_dict = {1: ('rogue', Assassin), 2: ('archer', Archer), 3: ('mage', Mage)}
    class_name, class_obj = class_dict.get(A_tree.cate, (None, None))
    ability_tree = getattr(A_tree, class_name)
    info = A_tree.showing_info
    draw_img(screen, ability_tree_selected_img, info[-4] + info[-2] + A_tree.gui_location_x - 25, info[-3] + info[-2] + A_tree.gui_location_y - 120)
    pygame.draw.circle(screen, WHITE, (info[-4] + A_tree.gui_location_x + info[-2], info[-3] + A_tree.gui_location_y + info[-2]), info[-2], 5)
    draw_img(screen, ability_tree_sidebar_img, 700, 0)
    if A_tree.cate == 1:
        acolor = GRAY
        draw_img(screen, A_tree.node_img, 800, 50)
    if A_tree.cate == 2:
        acolor = YELLOW
        draw_img(screen, A_tree.node_img, 800, 50)
    if A_tree.cate == 3:
        acolor = PURPLE
        draw_img(screen, A_tree.node_img, 800, 50)
    if info[-1] == "職業":
        draw_color_text(screen, str(info[0]), 30, 850, 150, acolor)
        for i in range(1, 12):
            if i == 3: color = YELLOW
            elif i == 8: color = BLUE
            elif i == 11: color = GREEN
            else: color = WHITE
            draw_color_text(screen, str(info[i]), 20, 850, 200 + (i - 1) * 30, color)
        draw_img(screen, ability_tree_reset_button_img, 775, 530)
        if is_hovering(775, 925, 530, 580, Mouse.x, Mouse.y): pygame.draw.rect(screen, WHITE, (775, 530, 150, 50), 2)
        if is_hovering(775, 925, 530, 580, Mouse.x, Mouse.y) and A_tree.lclick:
            if A_tree.cate == 1:
                for items in A_tree.rogue:
                    if A_tree.rogue[items] > 0 and items != "被動":
                        A_tree.rogue[items] = 0
                        Assassin.a_point += 1
                        if items in list(A_tree.specialization_unlock["rogue"].keys()):
                            Assassin.a_point -= 1
            if A_tree.cate == 2:
                for items in A_tree.archer:
                    if A_tree.archer[items] > 0 and items != "被動" and items:
                        A_tree.archer[items] = 0
                        Archer.a_point += 1
                        if items in list(A_tree.specialization_unlock["archer"].keys()):
                            Archer.a_point -= 1
            if A_tree.cate == 3:
                for items in A_tree.mage:
                    if A_tree.mage[items] > 0 and items != "被動" and items not in list(A_tree.specialization_unlock["mage"].keys()):
                        A_tree.mage[items] = 0
                        Mage.a_point += 1
                        if items in list(A_tree.specialization_unlock["rogue"].keys()):
                            Mage.a_point -= 1
    if info[-1] == "技能":
        if any(ability_tree[req] < 0 for req in info[1]):
            ability_tree[info[0]] = 0
            class_obj.a_point += 1
        draw_color_text(screen, str(info[2]), 30, 850, 150, GREEN)
        flag = True
        for key, skill in A_tree.keybind[A_tree.cate - 1].items():
            if skill == info[0]:
                info[3] = "觸發: " + key
                flag = False
        if flag: info[3] = "觸發: 未設定"
        for i in range(3, 11):
            if i == 8: color = YELLOW
            else: color = WHITE
            draw_color_text(screen, str(info[i]), 20, 850, 200 + (i - 3) * 30, color)
        if ability_tree[A_tree.showing_info[0]]: draw_color_text(screen, "已解鎖", 20, 850, 440, GREEN)
        else: draw_color_text(screen, "未解鎖", 20, 850, 440, RED)
        if A_tree.showing_info[2].startswith("技能 -") and ability_tree[A_tree.showing_info[0]]:
            draw_color_text(screen, "自訂按鍵", 13, 735, 560, WHITE)
            draw_img(screen, ability_tree_w_button_img, 765, 540)
            draw_img(screen, ability_tree_e_button_img, 825, 540)
            draw_img(screen, ability_tree_r_button_img, 885, 540)
            if is_hovering(765, 815, 540, 590, Mouse.x, Mouse.y): pygame.draw.rect(screen, WHITE, (765, 540, 50, 50), 2)
            if is_hovering(825, 875, 540, 590, Mouse.x, Mouse.y): pygame.draw.rect(screen, WHITE, (825, 540, 50, 50), 2)
            if is_hovering(885, 935, 540, 590, Mouse.x, Mouse.y): pygame.draw.rect(screen, WHITE, (885, 540, 50, 50), 2)
            if is_hovering(765, 815, 540, 590, Mouse.x, Mouse.y) and A_tree.lclick: tweak_keybind("W" + str(A_tree.row), info[0])
            if is_hovering(825, 875, 540, 590, Mouse.x, Mouse.y) and A_tree.lclick: tweak_keybind("E" + str(A_tree.row), info[0])
            if is_hovering(885, 935, 540, 590, Mouse.x, Mouse.y) and A_tree.lclick: tweak_keybind("R" + str(A_tree.row), info[0])
        if A_tree.showing_info[2].startswith("終結技 -") and ability_tree[A_tree.showing_info[0]]: A_tree.keybind[A_tree.cate - 1]["Q"] = info[0]
    if info[-1] == "升級":
        draw_color_text(screen, str(info[2]), 30, 850, 150, PURPLE)
        for i in range(3, 7):
            draw_color_text(screen, str(info[i]), 20, 850, 200 + (i - 3) * 30, WHITE)
            if ability_tree[info[0]]:
                draw_color_text(screen, "已解鎖", 20, 850, 320, GREEN)
            else:
                draw_color_text(screen, "未解鎖", 20, 850, 320, RED)
    if info[-1] == "二轉":
        draw_color_text(screen, str(info[0]), 30, 850, 150, acolor)
        for i in range(1, 11):
            if i == 3: color = YELLOW
            elif i == 8: color = BLUE
            else: color = WHITE
            draw_color_text(screen, str(info[i]), 20, 850, 200 + (i - 1) * 30, color)
            if ability_tree[info[11]]:
                draw_img(screen, ability_tree_empty_button_img, 775, 530)
                draw_color_text(screen, "取消", 30, 775 + 75, 533, WHITE)
            else:
                draw_img(screen, ability_tree_empty_button_img, 775, 530)
                draw_color_text(screen, "啟用", 30, 775 + 75, 533, WHITE)
            if is_hovering(775, 925, 530, 580, Mouse.x, Mouse.y): pygame.draw.rect(screen, WHITE, (775, 530, 150, 50), 2)
            if is_hovering(775, 925, 530, 580, Mouse.x, Mouse.y) and A_tree.lclick:
                if ability_tree[info[11]]:
                    ability_tree[info[11]] = 0
                else:
                    for spec in list(A_tree.specialization_unlock[class_name].keys()):
                        if ability_tree.get(spec, False):
                            ability_tree[spec] = 0
                    ability_tree[info[11]] = 1
                A_tree.lclick = False
    if (info[-1] != "職業" and info[-1] != "二轉"):
        if is_hovering(775, 925, 480, 530, Mouse.x, Mouse.y) and A_tree.lclick: upgrade_ability(A_tree.cate, info[0], info[1])
        if ability_tree[info[0]]:draw_img(screen, ability_tree_cancel_img, 775, 480)
        else: draw_img(screen, ability_tree_upgrade_img, 775, 480)
        if is_hovering(775, 925, 480, 530, Mouse.x, Mouse.y): pygame.draw.rect(screen, WHITE, (775, 480, 150, 50), 2)
#天賦樹連結線
def draw_ability_tree_line(start_x, start_y, end_x, end_y, color = BLACK):
    pygame.draw.line(screen, color, (start_x + A_tree.gui_location_x, start_y + A_tree.gui_location_y), (end_x + A_tree.gui_location_x, end_y + A_tree.gui_location_y), 5)
#強化深淵祝福
def upgrade_blessing(name, level):
    for blessing in Depth.blessings:
        if blessing["name"] == name:
            blessing["rarity"] = min(blessing["rarity"] + level + 1, 5)
#深淵祝福顯示器
def blessing_indicator(displayBlessing, level):
    for blessing in Depth.blessings:
        if blessing["name"] == displayBlessing:
            displayBlessing = blessing
            break
    rarity = min(level, 5)
    pygame.draw.rect(screen, DCGRAY, (Inv.info_loc_x, Inv.info_loc_y - 20, 500, 600))
    draw_img(screen, displayBlessing["img"][min(rarity - 1, 4)], Inv.info_loc_x + 200, Inv.info_loc_y)
    pygame.draw.rect(screen, BLACK, (Inv.info_loc_x + 200, Inv.info_loc_y, 90, 90), 5)
    draw_color_text(screen, displayBlessing["name"], 30, Inv.info_loc_x + 250, Inv.info_loc_y + 90, LBLUE)
    rarity_map = {1:"普通", 2:"常見", 3:"稀有", 4:"史詩", 5:"傳奇"}
    #顯示祝福稀有度
    draw_color_text(screen, "稀有度: " + rarity_map.get(rarity, '未知') , 20, Inv.info_loc_x + 250, Inv.info_loc_y + 130, RED)
    trigger_map = {"tripleMainAttack":"三次普通攻擊", "castSkill":"施放技能", "castUltimate":"施放終結技", "healthLow":"生命值低於20%", "killMob":"擊敗敵人", "passive":"永久觸發"}
    draw_color_text(screen, "觸發方式: " + trigger_map.get(displayBlessing["trigger"], "無法觸發"), 20, Inv.info_loc_x + 250, Inv.info_loc_y + 150, GOLD)
    #觸發效果
    if displayBlessing.get("effects", False):
        for attribute, value in displayBlessing["effects"].items():
            if attribute[-1] == "%":
                attribute = attribute[:-1]
                suffix = "%"
            else:
                suffix = ""
            draw_color_text(screen, attribute + " + " + str(value * rarity) + suffix, 20, Inv.info_loc_x + 250, Inv.info_loc_y + 190, LBLUE)
#深淵房間資訊顯示器
def room_info_indicator(displayRoom):
    pygame.draw.rect(screen, DCGRAY, (Inv.info_loc_x, Inv.info_loc_y - 20, 500, 600))
    #顯示房間名稱、類型
    room_name = displayRoom
    displayRoom = Depth.room_info[displayRoom]
    draw_img(screen, depth_room_icon.get(displayRoom["type"], 0), Inv.info_loc_x + 200, Inv.info_loc_y)
    pygame.draw.rect(screen, BLACK, (Inv.info_loc_x + 200, Inv.info_loc_y, 90, 90), 5)
    draw_color_text(screen, room_name, 30, Inv.info_loc_x + 250, Inv.info_loc_y + 90, LBLUE)
    #顯示祝福稀有度
    draw_color_text(screen, "類型: " + (displayRoom["type"]), 20, Inv.info_loc_x + 250, Inv.info_loc_y + 130, GOLD)
    #顯示房間效果
    if displayRoom.get("effect", False):
        y_move = 0
        for attribute, value in displayRoom["effect"].items():
            negative_effect = {"警戒值%"}
            if int(attribute not in negative_effect) == int(value > 0):
                text_color = LBLUE
            else:
                text_color = RED
            y_move += 30
            if attribute[-1] == "%":
                attribute = attribute[:-1]
                suffix = "%"
            else:
                suffix = ""
            mark = " + " if value > 0 else " - "
            draw_color_text(screen, attribute + mark + str(abs(value)) + suffix, 20, Inv.info_loc_x + 250, Inv.info_loc_y + 160 + y_move, text_color)
        #顯示房間敘述
        for string in displayRoom["info"].split("，"):
            y_move += 30
            draw_color_text(screen, string, 20, Inv.info_loc_x + 250, Inv.info_loc_y + 200 + y_move, WHITE)
#計算天空顏色
def calculate_sky_color(time, start_color, end_color):
    t = (Game_time.hour - time[0]) / (time[1] - time[0])
    return (
        int(start_color[0] * (1 - t) + end_color[0] * t),
        int(start_color[1] * (1 - t) + end_color[1] * t),
        int(start_color[2] * (1 - t) + end_color[2] * t),
        )
#滾動式背景
def scrolling_background(first_load = False):
    global background_backward_img, background_img, background_forward_img
    #初次執行
    if first_load:
        Areas.changed = True
        global background_location_x, background_location_y
        background_location_x = 0
        background_location_y = 0
    #檢測更換區域
    area_temp = Areas.area
    #當前區域
    Areas.area = (Player_location.coord_x // 1000) + 1
    if area_temp != Areas.area:
        Areas.lock_right = False
        Areas.lock_left = False
        Areas.changed = True
        Lootchest_info.claimed = 0
        if All_mobs.boss_fight_active == False: Areas.spawn = True
    #特殊區域
    if Areas.area == 6 and Area6.cata_open:
        Areas.special_area = "_2"
    elif Areas.area == 8 and Area8.puzzle_complete:
        Areas.special_area = "_2"
    elif Areas.area == 12 and Player_location.disable_ground:
        Areas.special_area = "_2"
    elif Areas.area == 16 and 0 < Area16.ascension_distant < 1500:
        Areas.special_area = "_2"
    else:
        Areas.special_area = ""
    #導入背景圖片 前/中/後
    Areas.area = int(Areas.area)
    if Areas.area < Areas.areas + 1 and Areas.changed and Areas.lock_right == False:
        background_forward_img = area_background_imgs[str(Areas.area + 1)]
    if Areas.area < Areas.areas and Areas.changed:
        background_img = area_background_imgs[str(Areas.area) + Areas.special_area]
    if Areas.changed and Areas.lock_left == False:
        background_backward_img = area_background_imgs[str(Areas.area - 1)]
    Areas.changed = False
    #當前區域座標
    global current_coord_x
    current_coord_x = Player_location.coord_x - (Areas.area - 1) * 1000
    #計算背景位置
    if (Areas.lock_left and current_coord_x <= 500) or (Areas.lock_right and current_coord_x >= 500) or (Areas.lock_left and Areas.lock_right):
        background_location_x = 0
        Player_location.player_move = True
    if ((Areas.lock_left and current_coord_x > 500) or (Areas.lock_right and current_coord_x < 500) or (Areas.lock_right == False and Areas.lock_left == False)) and not (Areas.lock_left and Areas.lock_right):
        background_location_x = -(Player_location.coord_x - ((Areas.area - 1) * 1000) - 500 - Player_location.background_moving)
        Player_location.player_move = False
    #使玩家在畫面中央
    if Player_location.player_move == False and Areas.lock_right == False and Areas.lock_left == False and Areas.area != 17:
        player.rect.x = 500
    if Areas.lock_left and Areas.lock_right:
        player.rect.x = current_coord_x
    #畫出天空
    Game_time.minute += 1
    Game_time.hour += 1/3600 * (1) #日夜循環速度
    if Game_time.minute == 60: Game_time.minute = 0 
    if Game_time.hour >= 24: Game_time.hour = 0
    # 計算天空顏色變化
    if DAWN[0] <= Game_time.hour <= DAWN[1]:  # 早晨
        sky_color = calculate_sky_color(DAWN, NIGHT_COLOR, AFTERNOON_COLOR)
    elif DAY[0] <= Game_time.hour <= DAY[1]:  # 白天
        sky_color = calculate_sky_color(DAY, AFTERNOON_COLOR, DAY_COLOR)
    elif NOON[0] <= Game_time.hour <= NOON[1]:# 中午
        sky_color = calculate_sky_color(NOON, DAY_COLOR, AFTERNOON_COLOR)
    elif AFTERNOON[0] <= Game_time.hour <= AFTERNOON[1]:  # 下午
        sky_color = calculate_sky_color(AFTERNOON_COLOR, AFTERNOON_COLOR, AFTERNOON_COLOR)
    elif DUSK[0] <= Game_time.hour <= DUSK[1]:  # 日落
        sky_color = calculate_sky_color(DUSK, AFTERNOON_COLOR, NIGHT_COLOR)
    elif NIGHT[0] <= Game_time.hour <= NIGHT[1]:  # 初夜
        sky_color = calculate_sky_color(NIGHT, NIGHT_COLOR, MIDNIGHT_COLOR)
    elif MIDNIGHT[0] <= Game_time.hour  <= MIDNIGHT[1]:  # 深夜
        sky_color = calculate_sky_color(MIDNIGHT, MIDNIGHT_COLOR, NIGHT_COLOR)
    screen.fill(sky_color)
    #畫出日月（06:00 ~ 12:00，18:00 ~ 24:00）
    if 6 <= Game_time.hour < 12:
        sun_y = HEIGHT - ((Game_time.hour - 6) / 6) * HEIGHT
        pygame.draw.circle(screen, SUN_COLOR, (WIDTH // 2 - 25, int(sun_y)), 30)
    if 18 <= Game_time.hour < 24:
        moon_y = HEIGHT - ((Game_time.hour - 18) / 6) * HEIGHT
        pygame.draw.circle(screen, MOON_COLOR, (WIDTH // 2 - 25, int(moon_y)), 30)
    #畫出背景
    if Areas.area != -7:
        #下一個區域
        if background_location_x < 0 and Areas.lock_right == False and current_coord_x > 500:
            draw_img(screen, background_forward_img, background_location_x + 1000, background_location_y)
        #當前區域
        draw_img(screen, background_img, background_location_x, 0)
        #上一個區域
        if background_location_x > 0 and Areas.lock_left == False and current_coord_x < 500:
            draw_img(screen, background_backward_img, background_location_x - 1000, 0)
#圓形冷卻顯示器
def circle_cd_indicator(x, y, radius, time, total_time, thickness, color = GREEN):
    angle = (time / total_time) * 360
    start_angle = 90
    end_angle = start_angle + angle
    rect = pygame.Rect(x, y, radius * 2, radius * 2)
    pygame.draw.arc(screen, color, rect, math.radians(start_angle), math.radians(end_angle), thickness)
#傳送
def teleport(coord_x):
    if (Areas.lock_left and coord_x % 1000 <= 500) or (Areas.lock_right and coord_x % 1000 > 500):
        player.rect.centerx = coord_x % 1000
    else:
        All_mobs.coord_x += (Player_location.coord_x - coord_x)
    Player_location.coord_x = coord_x
#偵測鼠標懸停(長方形)
def is_hovering(x1, x2, y1, y2, mouse_x = 0, mouse_y = 0, mouse_icon = ""):
    if x1 < Mouse.x < x2 and y1 < Mouse.y < y2 and mouse_icon:
        outline_text(mouse_icon, 30, Mouse.x, Mouse.y - 10, RED)
    return x1 < Mouse.x < x2 and y1 < Mouse.y < y2
#偵測鼠標懸停(圓形)
def is_hovering_circle(x, y, radius, mouse_x = 0, mouse_y = 0):
    return abs(Mouse.x - x) ** 2 + abs(Mouse.y - y) ** 2 <= radius ** 2
#更新玩家屬性
def update_stats():
    #基礎屬性
    Stats.basic = {"攻擊力":3, "攻擊力%":0, "防禦力":0, "防禦力%":0, "魔力回復":3 + (Mage.level - 1) * 0.1, "魔力上限":100, "生命上限":90 + (Assassin.level * 10), "生命上限%":0, "生命回復":Assassin.level + Archer.level + Mage.level, "冷卻減免%":0, "移動速度":0, "跳躍次數":1, "跳躍高度":200}
    #重新計算加成屬性
    Stats.bonus = {"攻擊力":0, "攻擊力%":0, "防禦力":0, "防禦力%":0, "魔力回復":0, "魔力上限":0, "生命上限":0, "生命上限%":0, "生命回復":0, "冷卻減免%":0, "移動速度":0, "跳躍次數":0, "跳躍高度":0}
    #重新計算護符加成
    Stats.charm = {"重擊傷害%":0, "破空突擊傷害%":0}
    #計算技能加成
    #物品欄加成屬性
    #計算武器加成
    if player.weapon == 1 and Inv.equip["sword"] != "":
        for attributeName, attributeValue in search_item(Inv.equip["sword"])["attribute"].items():
            Stats.bonus[attributeName] += attributeValue
    if player.weapon == 2 and Inv.equip["bow"] != "":
        for attributeName, attributeValue in search_item(Inv.equip["bow"])["attribute"].items():
            Stats.bonus[attributeName] += attributeValue
    if player.weapon == 3 and Inv.equip["wand"] != "":
        for attributeName, attributeValue in search_item(Inv.equip["wand"])["attribute"].items():
            Stats.bonus[attributeName] += attributeValue
    #計算護符加成
    equip_charm = Inv.equip["charm"] if Inv.type == "normal" else Inv.equip_preview["charm"]
    if equip_charm != []:
        for charm in equip_charm:
            for attributeName, attributeValue in search_item(charm)["attribute"].items():
                Stats.charm[attributeName] += attributeValue
    #計算任務道具加成
    if Inv.equip["questItem"] != []:
        for questItem in Inv.equip["questItem"]:
            if search_item(questItem).get("attribute", False):
                for attributeName, attributeValue in search_item(questItem)["attribute"].items():
                    Stats.bonus[attributeName] += attributeValue
    #效果狀態
    for effect in Stats.bonus:
        for existing_effect in player.effects:
            if existing_effect["name"] == effect:
                Stats.bonus[existing_effect["name"]] += existing_effect["level"]
    #魔王debuff
    Stats.bonus["生命上限%"] -= player.blight
    if player.crimson_harvest >= 1: Stats.bonus["移動速度"] -= 20
    if player.crimson_harvest >= 2: Stats.bonus["防禦力%"] -= 20
    if player.crimson_harvest >= 3: Stats.bonus["攻擊力%"] -= 20
    if player.crimson_harvest >= 4: Stats.bonus["冷卻減免%"] -= 20
    if player.crimson_harvest == 5: Damage_to_player.damage = 0.3
    #計算總屬性
    for key in Stats.basic:
        Stats.total[key] = Stats.basic[key] + Stats.bonus[key]
#時間轉換
def time_to_ticks(time_str):
    minutes, seconds = map(int, time_str.split(":"))
    return (minutes * 60 + seconds) * 60
#隨機抽取
def choose(probabilities):
    items = list(probabilities.keys())
    probabilities = list(probabilities.values())
    chosen_item = random.choices(items, probabilities, k=1)[0]
    return chosen_item
#自訂按鈕
def button(x, y, type, buttonInfo, text, textSize, text_move, img = False):
    #外框
    if type == "square":
        buttonWidth, buttonHeight, outlineWidth, buttonColor, outlineColor = buttonInfo["width"], buttonInfo["height"], buttonInfo["outlineWidth"], buttonInfo["color"], buttonInfo["outlineColor"]
        pygame.draw.rect(screen, buttonColor, (x, y, buttonWidth, buttonHeight))
    if type == "circle":
        buttonRadius, outlineWidth, buttonColor, outlineColor = buttonInfo["radius"], buttonInfo["outlineWidth"], buttonInfo["color"], buttonInfo["outlineColor"]
        pygame.draw.circle(screen, buttonColor, (x, y), buttonRadius)
    if type == "img":
        buttonWidth, buttonHeight, outlineWidth, outlineColor = img.get_width(), img.get_height(), buttonInfo["outlineWidth"], buttonInfo["outlineColor"]
        draw_img(screen, img, x, y)
    if type in ["square", "img"]:
        draw_color_text(screen, text, textSize, (x + text_move[0]), (y + text_move[1]), WHITE)
        if is_hovering(x, x + buttonWidth, y, y + buttonHeight, Mouse.x, Mouse.y):
            if outlineColor: pygame.draw.rect(screen, WHITE, (x, y, buttonWidth, buttonHeight), outlineWidth // 2)
            return True
        elif outlineColor: pygame.draw.rect(screen, outlineColor, (x, y, buttonWidth, buttonHeight), outlineWidth)
    if type == "circle":
        draw_color_text(screen, text, textSize, (x + text_move[0]), (y + text_move[1]), WHITE)
        if is_hovering_circle(x, y, buttonRadius):
            pygame.draw.circle(screen, WHITE, (x, y), buttonRadius, outlineWidth)
            return True
        else:
            pygame.draw.circle(screen, outlineColor, (x, y), buttonRadius, outlineWidth)
#預設設定
def default():
    player.blight = 0
    player.health = Stats.total["生命上限"]
    Mage.mana = Stats.total["魔力上限"]
    Player.cooldowns["暗影脈衝"] = 0
    Player.cooldowns["破空突擊"] = 0
    Player.cooldowns["暗影襲擊"] = 0
    Assassin.ultimate_time = 0
    Assassin.magic_enchant = 1
    Archer.kunai_amount = 0
    Mage.ultimate = False
    Player.cooldowns["火焰箭矢"] = 0
    Player.cooldowns["苦無"] = 0
    Player.cooldowns["隕石"] = 0
    Player.cooldowns["瞬水爆"] = 0
    player.flying = False
    Player_location.dash_distance = 0
    Player_location.disable_move = False
    Player_location.disable_jump = False
    Player_location.disable_ground = False
    Player_location.anti_gravity = False
#選單
def show_menu():
    forge_tick = 0
    if Quest.open:
        menu = 4
        Quest.skippable = False
    elif Inv.open: menu = 5
    elif Puzzle.open: menu = 6
    elif Forge.open: menu = 7
    elif Stats.open: menu = 8
    elif A_tree.open: menu = 9
    elif Portal.open: menu = 11
    elif Depth.menu_open: menu = 12
    elif Depth.blessing_menu: menu = 13
    elif Trade.open:
        menu = 14
        current_value = 1
        knob_x = 700
        knob_dragging = False
        sidebar_item_index = 0
    else:
        menu = 1
        hide_gui = False
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 將滑鼠座標轉換成遊戲內座標
        t_x, t_y = pygame.mouse.get_pos()
        mouse_x = (t_x - x_offset) / scale
        mouse_y = (t_y - y_offset) / scale
        Mouse.x, Mouse.y = mouse_x, mouse_y
        #繪製主螢幕
        if FULLSCREEN:
            scaled_surface = pygame.transform.smoothscale(screen, (new_width, new_height))
            display.fill((0, 0, 0))  # 填充黑邊
            display.blit(scaled_surface, (x_offset, y_offset))
        #控制音樂
        pygame.mixer.music.pause()
        if menu == 1:#主選單
            pygame.display.set_caption("Finding The Light - Menu")
            if hide_gui == False:
                pygame.draw.rect(screen, LGRAY, (350, 150, 300, 410))
                menu_text(screen,"Menu", 50, WIDTH / 2, 180)
                draw_img(screen, button_play_img, 415, 280)
                draw_img(screen, button_options_img, 415, 380)
                draw_img(screen, button_quit_img, 415, 470)
                draw_img(screen, button_save_img, 350, 470)
                button_save_img.set_colorkey(WHITE)
            pygame.display.update()
            hovering_play_button = is_hovering(410, 580, 280, 350, mouse_x, mouse_y)
            hovering_options_button = is_hovering(410, 580, 380, 450, mouse_x, mouse_y)
            hovering_quit_button = is_hovering(410, 580, 470, 530, mouse_x, mouse_y)
            hovering_saves_button = is_hovering(350, 410, 470, 530, mouse_x, mouse_y)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        waiting = False
                        return False
                    if event.key == pygame.K_o:
                        menu = 2
                    if event.key == pygame.K_q:
                        pygame.quit()
                        return True
                    if event.key == pygame.K_h:
                        hide_gui = not hide_gui
                press_button = pygame.mouse.get_pressed()
                if (press_button[0]):
                    if hovering_play_button == True:
                        waiting = False
                        return False
                    if hovering_options_button == True:
                        menu = 2
                    if hovering_saves_button == True:
                        menu = 10
                    if hovering_quit_button == True:
                        pygame.quit()
                        return True
        if menu == 2:#選項
            pygame.display.set_caption("Finding The Light - Options")
            pygame.draw.rect(screen, LGRAY, (350, 150, 300, 410))
            menu_text(screen,"Options", 40, WIDTH / 2, 180)
            draw_img(screen, button_keys_img, 415, 280)
            draw_img(screen, button_back_img, 415, 470)
            button_music_off_img.set_colorkey(WHITE)
            button_music_on_img.set_colorkey(WHITE)
            if Music.music == True: draw_img(screen, button_music_off_img, 345, 470)
            if Music.music == False: draw_img(screen, button_music_on_img, 345, 470)
            pygame.display.update()
            hovering_keys_button = is_hovering(410, 580, 280, 350, mouse_x, mouse_y)
            hovering_back_button = is_hovering(410, 580, 470, 530, mouse_x, mouse_y)
            hovering_music_button = is_hovering(350, 410, 470, 530, mouse_x, mouse_y)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
                        return False
                    if event.key == pygame.K_b:
                        menu = 1
                    if event.key == pygame.K_k:
                        menu = 3
                press_button = pygame.mouse.get_pressed()
                if (press_button[0]):
                    if hovering_back_button == True:
                        menu = 1
                    if hovering_keys_button == True:
                        menu = 3
                    if hovering_music_button == True:
                        Music.music = not Music.music
        if menu == 3:#按鍵
            pygame.display.set_caption("Finding The Light - Keys")
            pygame.draw.rect(screen, LGRAY, (350, 150, 300, 410))
            menu_text(screen,"Keys", 50, WIDTH / 2, 180)
            draw_text(screen,"D :Move Right", 20, WIDTH / 2, 240)
            draw_text(screen,"A :Move Left", 20, WIDTH / 2 - 10, 280)
            draw_text(screen,"W :Main Attack", 20, WIDTH / 2 + 10, 320)
            draw_text(screen,"E :Spell", 20, WIDTH / 2 - 50, 360)
            draw_text(screen,"Q :Ultimate", 20, WIDTH / 2 - 20, 400)
            draw_text(screen,"R :Ability", 20, WIDTH / 2 - 30, 440)
            draw_img(screen, button_back_img, 415, 470)
            pygame.display.update()
            hovering_back_button = is_hovering(410, 580, 470, 530, mouse_x, mouse_y)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
                        return False
                    if event.key == pygame.K_b:
                        menu = 2
                press_button = pygame.mouse.get_pressed()
                if (press_button[0]):
                    if hovering_back_button == True:
                        menu = 2
        if menu == 4:#任務(對話)
            hovering_yes_button = is_hovering(340, 460, 500, 570, mouse_x, mouse_y)
            hovering_no_button = is_hovering(530, 650, 500, 570, mouse_x, mouse_y)
            draw_img(screen, quest_col_img, 0, 450)
            if Quest.next_stage == True and Quest.skippable:
                if Quest.tracking == 1: Quest_01.stage += 1
                if Quest.tracking == 2: Quest_02.stage += 1
                if Quest.tracking == 3: Quest_03.stage += 1
                if Quest.tracking == 4: Quest_04.stage += 1
                Quest.next_stage = False
            #對話類型
            def normal_dialogue(name, subname, dialogue_1 = "", dialogue_2 = ""):
                Quest.skippable = True
                draw_color_text(screen, name, 30, 500, 450, GOLD)
                draw_color_text(screen, subname, 20, 500, 480, GOLD)
                draw_color_text(screen, dialogue_1, 30, 500, 520, WHITE)
                draw_color_text(screen, dialogue_2, 30, 500, 550, WHITE)
            def choice_dialogue(dialogue_1 = "", dialogue_2 = ""):
                Quest.skippable = True
                draw_color_text(screen, dialogue_1, 30, 500, 450, GOLD)
                draw_color_text(screen, dialogue_2, 20, 500, 480, GOLD)
                draw_img(screen, button_yes_img, 340, 500)
                draw_img(screen, button_no_img, 530, 500)
            #任務
            if Quest.tracking == 1: #任務01
                if Quest_01.stage == 0:
                    normal_dialogue("艾爾德里克", "煉金術士", "你好，冒險家，我正計劃製作一種神奇的藥水", "，但我缺少史萊姆黏液。你能給我8個史萊姆黏液嗎?")
                if Quest_01.stage == 1:
                    choice_dialogue("是否開啟支線任務:藥水實驗?")
                    press_button = pygame.mouse.get_pressed()
                    if (press_button[0]):
                        if hovering_yes_button:
                            Quest_01.stage += 1
                        if hovering_no_button:
                            Quest_01.stage = 0
                            Quest.tracking = 0
                            Quest.open = False
                            waiting = False
                            return False
                if Quest_01.stage == 2:
                    normal_dialogue(str(Player.name), "冒險家", "當然，這應該不難。", "太感謝了!現在我可以開始我的實驗了。等一下，這不對...")
                if Quest_01.stage == 3:
                    Quest_01.progressing = True
                    Quest.skippable = True
                    Quest_01.stage += 1
                    title("藥水實驗", "支線任務已開啟")
                    Quest.open = False
                    waiting = False
                    return False
                if Quest_01.stage == 4:
                    choice_dialogue("是否交付8個史萊姆黏液?", str(search_item("史萊姆黏液")["count"]) + "/8")
                    if search_item("史萊姆黏液")["count"] >= 8:
                        Quest.skippable = True
                    else: Quest.skippable = False
                    press_button = pygame.mouse.get_pressed()
                    if (press_button[0]):
                        if hovering_yes_button and search_item("史萊姆黏液")["count"] >= 8:
                            Quest_01.stage += 1
                        if hovering_no_button:
                            Quest_01.stage = 4
                            Quest.open = False
                            waiting = False
                            return False
                if Quest_01.stage == 5:
                    normal_dialogue("艾爾德里克", "煉金術士", "太感謝了!現在我可以開始我的實驗了。等一下，這不對...  ")
                if Quest_01.stage == 6:
                    normal_dialogue("", "", "[瓶子內突然傳來爆炸聲，一隻史萊姆從瓶子裡跳了出來]")
                if Quest_01.stage == 7:
                    normal_dialogue(Player.name, "冒險家", "怎麼了？發生了什麼事？")
                if Quest_01.stage == 8:
                    normal_dialogue("艾爾德里克", "煉金術士", "我的實驗出了問題，看來我做錯了一些事情。史萊姆跑出來了！ ")
                if Quest_01.stage == 9:
                    player.gain_item("史萊姆黏液", -8)
                    title("[提示] 擊敗跑出來的史萊姆", "")
                    summon_mob(WIDTH - 100, GROUND + 30, 6, 2, "slime")
                    switch_music(3)
                    Areas.lock_right = True
                    Areas.lock_left = True
                    Areas.regen_lock = True
                    Quest_01.stage += 1
                    Quest.open = False
                    waiting = False
                    return False
                if Quest_01.stage == 10:
                    if All_mobs.count == 0:
                        Quest_01.stage += 1
                    else:
                        Quest.open = False
                        waiting = False
                        return False
                if Quest_01.stage == 11:
                    Areas.lock_right = False
                    Areas.lock_left = False
                    Areas.regen_lock = False
                    normal_dialogue("", "", "[史萊姆開始四處亂跑，冒險家將其擊敗]")
                if Quest_01.stage == 12:
                    normal_dialogue("艾爾德里克", "煉金術士", "雖然我的實驗失敗了，但感謝你的幫助", "，冒險家。我很抱歉給你帶來了這些麻煩。作為報答，我想給你一些獎勳。")
                if Quest_01.stage == 13:
                    normal_dialogue(Player.name, "冒險家", "沒關係，這也是一個冒險的一部分。謝謝你的獎勳，艾爾德里克。")
                if Quest_01.stage == 14:
                    Quest_01.stage += 1
                    switch_music(2)
                    title("藥水實驗", "支線任務已完成")
                    new_message("全職業經驗 + 50")
                    player.gain_item("金幣", 50)
                    Assassin.xp += 50
                    Archer.xp += 50
                    Mage.xp += 50
                    Quest_01.complete = True
                    Quest.open = False
                    waiting = False
                    return False
                if Quest_01.stage == 15:
                    normal_dialogue("艾爾德里克", "煉金術士", "這個實驗確實令人印象深刻，我學到了不少。感謝你的幫助，冒險者。")
                if Quest_01.stage == 16:
                    Quest_01.stage = 15
                    Quest.open = False
                    waiting = False
                    return False
            if Quest.tracking == 2: #任務02
                if Quest_02.stage == 0:
                    Quest.skippable = True
                    draw_color_text(screen, "艾德溫", 30, 500, 450, GOLD)
                    draw_color_text(screen, "市長", 20, 500, 480, GOLD)
                    draw_color_text(screen, str(Quest_02.dialogue[0]), 30, 500, 500, WHITE)
                if Quest_02.stage == 1:
                    Quest.skippable = True
                    draw_color_text(screen, str(Quest_02.dialogue[1]), 30, 500, 450, GOLD)
                    draw_img(screen, button_yes_img, 340, 500)
                    draw_img(screen, button_no_img, 530, 500)
                    press_button = pygame.mouse.get_pressed()
                    if (press_button[0]):
                        if hovering_yes_button:
                            Quest_02.stage += 1
                        if hovering_no_button:
                            Quest_02.stage = 0
                            Quest.tracking = 0
                            Quest.open = False
                            waiting = False
                            return False
                if Quest_02.stage == 2:
                    Quest.skippable = True
                    draw_color_text(screen, str(Player.name), 30, 500, 450, GOLD)
                    draw_color_text(screen, "冒險家", 20, 500, 480, GOLD)
                    draw_color_text(screen, str(Quest_02.dialogue[2]), 30, 500, 520, WHITE)
                if Quest_02.stage == 3:
                    Quest.skippable = True
                    draw_color_text(screen, "艾德溫", 30, 500, 450, GOLD)
                    draw_color_text(screen, "市長", 20, 500, 480, GOLD)
                    draw_color_text(screen, str(Quest_02.dialogue[3]), 30, 500, 500, WHITE)
                    draw_color_text(screen, str(Quest_02.dialogue[4]), 30, 500, 550, WHITE)
                if Quest_02.stage == 4:
                    Quest.skippable = True
                    draw_color_text(screen, str(Player.name), 30, 500, 450, GOLD)
                    draw_color_text(screen, "冒險家", 20, 500, 480, GOLD)
                    draw_color_text(screen, str(Quest_02.dialogue[5]), 30, 500, 520, WHITE)
                if Quest_02.stage == 5:
                    Quest.skippable = True
                    draw_color_text(screen, "艾德溫", 30, 500, 450, GOLD)
                    draw_color_text(screen, "市長", 20, 500, 480, GOLD)
                    draw_color_text(screen, str(Quest_02.dialogue[6]), 30, 500, 500, WHITE)
                if Quest_02.stage == 6:
                    Quest.skippable = True
                    draw_color_text(screen, str(Player.name), 30, 500, 450, GOLD)
                    draw_color_text(screen, "冒險家", 20, 500, 480, GOLD)
                    draw_color_text(screen, str(Quest_02.dialogue[7]), 30, 500, 520, WHITE)
                if Quest_02.stage == 7:
                    Quest.skippable = True
                    draw_color_text(screen, "艾德溫", 30, 500, 450, GOLD)
                    draw_color_text(screen, "市長", 20, 500, 480, GOLD)
                    draw_color_text(screen, str(Quest_02.dialogue[8]), 30, 500, 520, WHITE)
                if Quest_02.stage == 8:
                    Quest.skippable = True
                    draw_color_text(screen, str(Player.name), 30, 500, 450, GOLD)
                    draw_color_text(screen, "冒險家", 20, 500, 480, GOLD)
                    draw_color_text(screen, str(Quest_02.dialogue[9]), 30, 500, 520, WHITE)
                if Quest_02.stage == 9:
                    Quest.skippable = True
                    draw_color_text(screen, "艾德溫", 30, 500, 450, GOLD)
                    draw_color_text(screen, "市長", 20, 500, 480, GOLD)
                    draw_color_text(screen, str(Quest_02.dialogue[10]), 30, 500, 520, WHITE)
                if Quest_02.stage == 10:
                    Quest.skippable = True
                    draw_color_text(screen, str(Player.name), 30, 500, 450, GOLD)
                    draw_color_text(screen, "冒險家", 20, 500, 480, GOLD)
                    draw_color_text(screen, str(Quest_02.dialogue[11]), 30, 500, 520, WHITE)
                if Quest_02.stage == 11:
                    Quest.skippable = True
                    draw_color_text(screen, "艾德溫", 30, 500, 450, GOLD)
                    draw_color_text(screen, "市長", 20, 500, 480, GOLD)
                    draw_color_text(screen, str(Quest_02.dialogue[12]), 30, 500, 520, WHITE)
                    draw_color_text(screen, str(Quest_02.dialogue[13]), 30, 500, 550, WHITE)
                    draw_color_text(screen, str(Quest_02.dialogue[14]), 30, 500, 580, WHITE)
                if Quest_02.stage == 12:
                    Quest.skippable = True
                    draw_color_text(screen, str(Player.name), 30, 500, 450, GOLD)
                    draw_color_text(screen, "冒險家", 20, 500, 480, GOLD)
                    draw_color_text(screen, str(Quest_02.dialogue[15]), 30, 500, 520, WHITE)
                if Quest_02.stage == 13:
                    Quest.skippable = True
                    draw_color_text(screen, "艾德溫", 30, 500, 450, GOLD)
                    draw_color_text(screen, "市長", 20, 500, 480, GOLD)
                    draw_color_text(screen, str(Quest_02.dialogue[16]), 30, 500, 520, WHITE)
                if Quest_02.stage == 14:
                    Quest_02.progressing = True
                    title("黑暗勢力的威脅", "主線任務已開啟")
                    Quest_02.stage += 1
                    Quest.open = False
                    waiting = False
                    return False
                if Quest_02.stage == 15 and Quest_02.complete == False and Areas.area == -1 and search_item("生命水晶")["count"] == 0:
                    Quest.skippable = True
                    draw_color_text(screen, "艾德溫", 30, 500, 450, GOLD)
                    draw_color_text(screen, "市長", 20, 500, 480, GOLD)
                    draw_color_text(screen, str(Quest_02.dialogue[17]), 30, 500, 520, WHITE)
                if Quest_02.stage == 16 and Quest_02.complete == False and Areas.area == -1 and search_item("生命水晶")["count"] == 0:
                    Quest_02.stage = 15
                    Quest.open = False
                    waiting = False
                    return False
                if Quest_02.stage == 15 and Area6.cata_open == False and Areas.area == 6:
                    draw_color_text(screen, "是否交付靈魂碎片?", 30, 500, 450, GOLD)
                    draw_color_text(screen, str(search_item("靈魂碎片")["count"]) + "/1", 20, 500, 480, GOLD)
                    draw_img(screen, button_yes_img, 340, 500)
                    draw_img(screen, button_no_img, 530, 500)
                    if search_item("靈魂碎片")["count"] >= 1:
                        Quest.skippable = True
                    else: Quest.skippable = False
                    press_button = pygame.mouse.get_pressed()
                    if (press_button[0]):
                        if hovering_yes_button and search_item("靈魂碎片")["count"] >= 1:
                            Quest_02.stage += 1
                        if hovering_no_button:
                            Quest.open = False
                            waiting = False
                            return False
                if Quest_02.stage == 16 and Areas.area == 6:
                    Area6.cata_open = True
                    All_mobs.kill = True
                    player.gain_item("靈魂碎片", -1)
                    Quest_02.stage = 15
                    Quest.open = False
                    waiting = False
                    return False
                if Quest_02.stage == 15 and Areas.area == -1 and search_item("生命水晶")["count"] > 0:
                    Quest.skippable = True
                    draw_color_text(screen, "艾德溫", 30, 500, 450, GOLD)
                    draw_color_text(screen, "市長", 20, 500, 480, GOLD)
                    draw_color_text(screen, str(Quest_02.dialogue[18]), 30, 500, 520, WHITE)
                if Quest_02.stage == 16:
                    Quest.skippable = True
                    Quest.skippable = True
                    draw_color_text(screen, str(Player.name), 30, 500, 450, GOLD)
                    draw_color_text(screen, "冒險家", 20, 500, 480, GOLD)
                    draw_color_text(screen, str(Quest_02.dialogue[19]), 30, 500, 520, WHITE)
                if Quest_02.stage == 17:
                    Quest.skippable = True
                    draw_color_text(screen, "艾德溫", 30, 500, 450, GOLD)
                    draw_color_text(screen, "市長", 20, 500, 480, GOLD)
                    draw_color_text(screen, str(Quest_02.dialogue[20]), 30, 500, 500, WHITE)
                    draw_color_text(screen, str(Quest_02.dialogue[21]), 30, 500, 550, WHITE)
                if Quest_02.stage == 18:
                    title("黑暗勢力的威脅", "主線任務已完成")
                    new_message("金幣 + 80")
                    new_message("全職業經驗 + 300")
                    Quest_02.stage += 1
                    player.gain_item("金幣", 80)
                    Assassin.xp += 300
                    Archer.xp += 300
                    Mage.xp += 300
                    Quest_02.complete = True
                    Quest.open = False
                    waiting = False
                    return False
                if Quest_02.stage == 19:
                    Quest.skippable = True
                    draw_color_text(screen, "艾德溫", 30, 500, 450, GOLD)
                    draw_color_text(screen, "市長", 20, 500, 480, GOLD)
                    draw_color_text(screen, str(Quest_02.dialogue[22]), 30, 500, 500, WHITE)
                if Quest_02.stage == 20:
                    Quest_02.stage = 19
                    Quest.open = False
                    waiting = False
                    return False
            if Quest.tracking == 3: #任務03
                if Quest_03.stage == 0:
                    normal_dialogue("Aurora", "魔法師", "你!陌生的冒險者!你來得正是時候!")
                if Quest_03.stage == 1:
                    normal_dialogue(Player.name, "冒險家", "發生什麼事了?")
                if Quest_03.stage == 2:
                    normal_dialogue("Aurora", "魔法師", "上方的『天堂』正在遭受一場浩劫。邪惡的『星辰令使·Stellaris』降臨了!", "他帶來的『星疫』正在侵蝕那片淨土，銀騎士們都快支撐不住了。")
                if Quest_03.stage == 3:
                    normal_dialogue(Player.name, "冒險家", "Stellaris……這名字聽起來就不妙。我能做什麼？")
                if Quest_03.stage == 4:
                    normal_dialogue("Aurora", "魔法師", "我需要你的協助!這裡離天堂非常遙遠，我會給你一雙翅膀，讓你飛往那裡。", "途中小心!令使的力量已滲透到天空群島，飛行時須各種閃避攻擊!")
                if Quest_03.stage == 5:
                    choice_dialogue("是否開啟主線任務:星疫之災?")
                    press_button = pygame.mouse.get_pressed()
                    if (press_button[0]):
                        if hovering_yes_button:
                            Quest_03.stage += 1
                        if hovering_no_button:
                            Quest_03.stage = 5
                            Quest.tracking = 0
                            Quest.open = False
                            waiting = False
                            return False
                if Quest_03.stage == 6:
                    normal_dialogue(Player.name, "冒險家", "明白了，我準備好了。")
                if Quest_03.stage == 7:
                    normal_dialogue("", "", "Aurora舉起法杖，吟唱古老的咒語，冒險家獲得一對散發光輝的羽翼。")
                if Quest_03.stage == 8:
                    normal_dialogue("Aurora", "魔法師", "去吧，勇敢的冒險者!我和銀騎士Tuleen會與你並肩作戰!")
                if Quest_03.stage == 9:
                    Quest_03.progressing = True
                    Quest.skippable = True
                    Quest_03.stage += 1
                    title("星疫之災", "主線任務已開啟")
                    Player_location.disable_jump = True
                    teleport(15500)
                    Quest.open = False
                    waiting = False
                    return False
                if Quest_03.stage == 12:
                    normal_dialogue("Aurora", "魔法師", "(凝視著被星疫感染的天空)", "")
                if Quest_03.stage == 13:
                    normal_dialogue("Aurora", "魔法師", "我們的時間不多了...Stellaris的力量正在吞噬這片領域。", "如果我們不阻止它，天堂將徹底淪陷。")
                if Quest_03.stage == 14:
                    normal_dialogue("Tuleen", "銀騎士", "(將長劍插入地面，神情堅毅)")
                if Quest_03.stage == 15:
                    normal_dialogue("Tuleen", "銀騎士", "銀騎士的使命就是守護這片土地。我已召喚了古老的銀刃", "隨時準備與令使交鋒。")
                if Quest_03.stage == 16:
                    normal_dialogue("Tuleen", "銀騎士", "(轉向冒險者)")
                if Quest_03.stage == 17:
                    normal_dialogue("Tuleen", "銀騎士", "冒險者，我們需要你的力量。", "這場戰鬥，不僅關乎天堂，也關乎整個世界的命運。")
                if Quest_03.stage == 18:
                    normal_dialogue(Player.name, "冒險者", "我會全力以赴。")
                if Quest_03.stage == 19:
                    normal_dialogue("Aurora", "魔法師", "(揮舞魔杖，憑空畫出發光的魔法符文)")
                if Quest_03.stage == 20:
                    normal_dialogue("Aurora", "魔法師", "Stellaris的核心是它的弱點，但它的堅硬外殼讓我們無法直接攻擊。", "當核心暴露時，抓住每一個機會攻擊它，否則，星疫將讓我們再無退路。")
                if Quest_03.stage == 21:
                    normal_dialogue("Tuleen", "銀騎士", "(握住劍柄，目光如炬)")
                if Quest_03.stage == 22:
                    normal_dialogue("Tuleen", "銀騎士", "我將抓準時機進行攻擊，在此過程中，我可能遭受攻擊", "請保護我，直到力量聚集完成。")
                if Quest_03.stage == 23:
                    normal_dialogue(Player.name, "冒險家", "明白了。Tuleen，我會確保你不被干擾", "。Aurora，我會全力支援你對抗星疫的侵蝕。")
                if Quest_03.stage == 24:
                    normal_dialogue("Aurora", "魔法師", "(微微一笑，目光中流露出堅定)")
                if Quest_03.stage == 25:
                    normal_dialogue("Aurora", "魔法師", "很好，保持冷靜，記住每一步都至關重要。", "當星疫蔓延時，我會在場上布下魔法陣，為你們淨化。")
                if Quest_03.stage == 26:
                    normal_dialogue("Tuleen", "銀騎士", "不必害怕，冒險者。這是我們銀騎士與 Stellaris 最終的決戰。", "只要我們並肩作戰，就一定能將它逐出天堂。")
                if Quest_03.stage == 27:
                    normal_dialogue("Tuleen", "銀騎士", "(拔起長劍，高舉過頭)")
                if Quest_03.stage == 28:
                    normal_dialogue("Aurora", "魔法師", "為了光明，為了希望!")
                if Quest_03.stage == 29:
                    normal_dialogue(Player.name, "冒險者", "我們一起，擊退 Stellaris!")
                if Quest_03.stage == 30:
                    Quest_03.stage += 1
                    Quest.open = False
                    waiting = False
                    return False
                if Quest_03.stage == 32:
                    normal_dialogue("Aurora", "魔法師", "我們成功將 Stellaris 驅逐出天堂了!")
                if Quest_03.stage == 33:
                    normal_dialogue("Tuleen", "銀騎士", "冒險者，你展現了非凡的勇氣與智慧。", "沒有你的幫助，我們無法達成這場艱難的勝利。")
                if Quest_03.stage == 34:
                    normal_dialogue("Aurora", "魔法師", "願這次的勝利成為傳說，而你的名字將被永遠銘記。")
                if Quest_03.stage == 35:
                    normal_dialogue(Player.name, "冒險者", "這只是我的責任，能與你們並肩作戰是我的榮幸。")
                if Quest_03.stage == 36:
                    normal_dialogue("Aurora", "魔法師", "(展開手心，一道七彩的光輝形成翅膀的輪廓)")
                if Quest_03.stage == 37:
                    normal_dialogue("Aurora", "魔法師", "為了感謝你的無畏與貢獻，我願將「極光之翼」贈予你。", "它蘊含著天堂的力量，將助你在未來的旅途中突破各種難關。")
                if Quest_03.stage == 38:
                    normal_dialogue("Tuleen", "銀騎士", "(從背後取出一柄閃爍著銀光的長劍，劍身刻有精緻的銀騎士紋章)")
                if Quest_03.stage == 39:
                    normal_dialogue("Tuleen", "銀騎士", "而這是象徵銀騎士的長劍，名為「銀月之刃」", "。它代表著榮耀與正義，現在，它的使命將由你延續。")
                if Quest_03.stage == 40:
                    normal_dialogue("Aurora", "魔法師", "冒險者，未來的道路或許更為險惡", "但我相信，你一定能克服所有挑戰。願光明與希望永遠伴隨著你。")
                if Quest_03.stage == 41:
                    normal_dialogue("Tuleen", "銀騎士", "我們將會守護這片天空，而你，則代表我們，走向更遠的未知領域。")
                if Quest_03.stage == 42:
                    normal_dialogue(Player.name, "冒險者", "保重，我們一定還會再見的。")
                if Quest_03.stage == 43:
                    title("星疫之災", "主線任務已完成")
                    player.gain_item("銀月之刃", 1)
                    player.gain_item("金幣", 150)
                    player.gain_item("力量水晶", 1)
                    player.gain_item("極光之翼", 1)
                    new_message("全職業經驗 + 500")
                    Assassin.xp += 500
                    Archer.xp += 500
                    Mage.xp += 500
                    Quest_03.complete = True
                    Quest_03.stage += 1
                    Quest.open = False
                    waiting = False
                    return False
                if Quest_03.stage == 44:
                    normal_dialogue("Tuleen", "銀騎士", "願你的旅途一帆風順!")
                if Quest_03.stage == 45:
                    Quest_03.stage = 44
                    Quest.open = False
                    waiting = False
                    return False
            if Quest.tracking == 4: #任務04
                if Quest_04.stage == 0:
                    normal_dialogue("", "", "(踏入營地的瞬間，一道黑影閃過。)")
                if Quest_04.stage == 1:
                    normal_dialogue("夜刃", "流放者", "你踏入的地方，可不是個善地。")
                if Quest_04.stage == 2:
                    normal_dialogue(player.name, "冒險者", "我就知道是你，「夜刃」。")
                if Quest_04.stage == 3:
                    normal_dialogue("夜刃", "流放者", "(夜刃沉默片刻，手中的匕首微微收回，眼神中帶著試探。)")
                if Quest_04.stage == 4:
                    normal_dialogue("夜刃", "流放者", "這名字……已經很久沒有人敢叫了。你知道我的故事?")
                if Quest_04.stage == 5:
                    normal_dialogue(player.name, "冒險者", "流放者、王國的影子、曾經的建城者之一——如今卻成了被追殺的對象。", "我聽說你比誰都更想讓這座城堡脫離黑暗。")
                if Quest_04.stage == 6:
                    normal_dialogue("夜刃", "流放者", "有趣。那麼，你是來找我幫忙，還是來取我的命?")
                if Quest_04.stage == 7:
                    normal_dialogue(player.name, "冒險者", "我要奪回國王手中的水晶，作為交換，我願意協助你推翻國王。")
                if Quest_04.stage == 8:
                    normal_dialogue("夜刃", "流放者", "有趣。那麼，你是來找我幫忙，還是來取我的命?")
                if Quest_04.stage == 9:
                    normal_dialogue("夜刃", "流放者", "(嘴角揚起一抹冷笑，目光掠過冒險者的武器，似乎在衡量他的實力。)")
                if Quest_04.stage == 10:
                    normal_dialogue("夜刃", "流放者", "你要的是力量，還是知識?")
                if Quest_04.stage == 11:
                    normal_dialogue(player.name, "冒險者", "如果能同時擁有，那再好不過。")
                if Quest_04.stage == 12:
                    normal_dialogue("夜刃", "流放者", "(夜刃低聲一笑，將匕首插回腰間，轉身朝深淵的方向走去。)")
                if Quest_04.stage == 13:
                    normal_dialogue("夜刃", "流放者", "那就跟上我們吧，讓我看看你的價值。")
                if Quest_04.stage == 14:
                    choice_dialogue("是否開啟主線任務:黑暗王座的終焉?")
                    press_button = pygame.mouse.get_pressed()
                    if (press_button[0]):
                        if hovering_yes_button:
                            Quest_04.stage += 1
                        if hovering_no_button:
                            Quest_04.stage = 13
                            Quest.tracking = 0
                            Quest.open = False
                            waiting = False
                            return False
                if Quest_04.stage == 15:
                    title("黑暗王座的終焉", "主線任務已開啟")
                    Quest_04.stage += 1
                    Quest_04.progressing = True
                    Quest.open = False
                    waiting = False
                    return False
                if Quest_04.stage == 16:
                    normal_dialogue(player.name, "冒險者", "（與凱文、雷恩哈特會合）")
                if Quest_04.stage == 17:
                    normal_dialogue("凱文", "學者", "這裡……這裡曾經是王國最偉大的堡壘，而現在，只剩下噬人的黑暗。", "我們曾經以為，這片土地終有一天能重見光明……可惜，國王選擇了讓它沉淪。")
                if Quest_04.stage == 18:
                    normal_dialogue("雷恩哈特", "反叛軍騎士", "曾經的榮耀早已被國王的貪婪與恐懼吞噬，現在只剩下這無盡的深淵。", "我曾是他的劍，但如今——我寧願將這把劍刺向他的咽喉。")
                if Quest_04.stage == 19:
                    normal_dialogue("夜刃", "流放者", "深淵中的城堡不是靜止的，每次踏入，它的形態都會改變。", "這是某種詛咒，還是某種……防禦機制？不論如何，這裡藏著我們的目標。")
                if Quest_04.stage == 20:
                    normal_dialogue(player.name, "冒險者", "黃色水晶……它是關鍵。但我們還不清楚國王如何利用它。")
                if Quest_04.stage == 21:
                    normal_dialogue("凱文", "學者", "傳聞說，黃色水晶賦予了他不滅的護盾。", "刀劍難以傷及……若你真要挑戰國王，光有勇氣是不夠的。")
                if Quest_04.stage == 22:
                    normal_dialogue("雷恩哈特", "反叛軍騎士", "我們不可能正面擊潰他，但我們可以利用這座城堡的變幻特性來找到突破口……", "如果你能生存下去的話。")
                if Quest_04.stage == 23:
                    normal_dialogue("夜刃", "流放者", "我們會在暗中協助你。但這場戰鬥，終究是你必須面對的試煉。")
                if Quest_04.stage == 24:
                    normal_dialogue("夜刃", "流放者", "既然你已經準備好了，是時候選擇進入城堡的方式了。")
                if Quest_04.stage == 25:
                    normal_dialogue("夜刃", "流放者", "第一個方法，是從這座廢棄的下水道潛入，路線隱蔽，不易被守衛察覺。")
                if Quest_04.stage == 26:
                    normal_dialogue("夜刃", "流放者", "另一個選項，是偽裝成黑市商隊的成員，混跡在商人之中隨他們一同入城。")
                if Quest_04.stage == 27:
                    normal_dialogue("夜刃", "流放者", "最後一個……是最危險的選擇:正面突破城門，與守軍硬碰硬。", 
                    "但我要提醒你，這不是戰鬥，而是賭命。請慎重考慮。")
                if Quest_04.stage == 28:
                    normal_dialogue(player.name, "冒險者", "(握緊武器，深吸一口氣)", "那就讓我們開始吧")
                if Quest_04.stage == 29:
                    Quest.open = False
                    waiting = False
                    return False
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and Quest.skippable:
                        Quest.next_stage = True
        if menu == 5:#物品欄
            update_stats()
            if Inv.type == "normal": inventory = Inv.inventory
            elif Inv.type == "load": inventory = Inv.preview
            def draw_inventory_category(cate, mouse_x, mouse_y):
                cateName = ["武器", "裝備", "護符", "貨幣", "戰利品", "消耗品", "任務道具"]
                for i in range(7):
                    pygame.draw.line(screen, BLACK, (35 + i * 94, 158), (35 + 96 + i * 94, 158), 4)
                    pygame.draw.line(screen, BLACK, (35 + i * 94, 158), (35 + i * 94, 188), 4)
                    pygame.draw.line(screen, BLACK, (35 + 94 + i * 94, 158), (35 + 94 + i * 94, 188), 4)
                    if i + 1 == Inv.cate: pygame.draw.line(screen, AGRAY, (38 + i * 94, 188), (35 + 92 + i * 94, 188), 4)
                    draw_color_text(screen, ("→" if i + 1 == Inv.cate else "") + cateName[i] + ("←" if i + 1 == Inv.cate else ""), 20, 82 + i * 94, 148 + 12, WHITE)
                if Inv.cate == 1:
                    pygame.display.set_caption("Finding The Light - Inventory (Weapons)")
                    draw_items(["sword", "bow", "wand"])
                elif Inv.cate == 2:
                    pygame.display.set_caption("Finding The Light - Inventory (Armors)")
                    armor_items = []
                    for item in inventory:
                        if item["itemType"] in ["helmet", "armor", "legs", "boots"] and item["count"]: armor_items.append(item)
                    draw_items(armor_items)
                elif Inv.cate == 3:
                    pygame.display.set_caption("Finding The Light - Inventory (Charms)")
                    draw_items(["charm"])
                    #顯示護符槽
                    #外框
                    if Inv.type == "normal": charm_slot = Inv.charm_slot
                    if Inv.type == "load": charm_slot = Inv.charm_slot_preview
                    for i in range(20):
                        x_move = i * 90 % 900
                        y_move = i // 10 * 70
                        pygame.draw.rect(screen, IGRAY, (100 + x_move, 610 + y_move, 60, 60))
                        pygame.draw.rect(screen, BLACK, (100 + x_move, 610 + y_move, 60, 60), 3)
                        draw_color_text(screen, "x" if i >= charm_slot[1] else "", 60, 130 + x_move, 590 + y_move, RED)
                    #使用狀態
                    draw_color_text(screen, "護符槽: ", 25, 55, 650, WHITE)
                    draw_color_text(screen, str(charm_slot[0]) + "/" + str(charm_slot[1]), 25, 55, 680, WHITE)
                    #顯示護符槽
                    drawing_charms = []
                    for i in range(len(Inv.equip["charm"]) if Inv.type == "normal" else len(Inv.equip_preview["charm"])):
                        for k in range(charm_order(Inv.equip["charm"][i])[2] if Inv.type == "normal" else charm_order(Inv.equip_preview["charm"][i])[2]):
                            drawing_charms.append(charm_order(Inv.equip["charm"][i]) if Inv.type == "normal" else charm_order(Inv.equip_preview["charm"][i]))
                    for i in range(len(drawing_charms)):
                        x_move = i * 90 % 900
                        y_move = i // 10 * 70
                        draw_img(screen, pygame.transform.scale(drawing_charms[i][1], (54, 54)), 103 + x_move, 613 + y_move)
                        outline_text(drawing_charms[i][2], 30, 135 + x_move, 605 + y_move, WHITE)
                    #顯示護符詞條
                    pygame.draw.rect(screen, DCGRAY, (830, 150, 170, 400))
                    pygame.draw.rect(screen, DGRAY, (830, 150, 170, 400), 3)
                    pygame.draw.line(screen, DGRAY, (830, 190), (1000, 190), 3)
                    draw_color_text(screen, "護符加成", 20, 915, 155, WHITE)
                    y_move = 0
                    for id, value in Stats.charm.items():
                        if value:
                            y_move += 25
                            draw_color_text(screen, (id[0:-1] if id.endswith("%") else id) + ": " + str(value) + ("%" if id.endswith("%") else ""), 15, 915, 170 + y_move, LBLUE)
                    #
                    for i in range(len(drawing_charms)):
                        x_move = i * 90 % 900
                        y_move = i // 10 * 70
                        if is_hovering(100 + x_move, 160 + x_move, 610 + y_move, 670 + y_move, mouse_x, mouse_y): inv_item_text(drawing_charms[i][-1])
                    #卸下未裝備護符
                    for charm in Inv.equip["charm"]:
                        if search_item(charm)["count"] <= 0: Inv.equip["charm"].remove(charm)
                elif Inv.cate == 4:
                    pygame.display.set_caption("Finding The Light - Inventory (Currency)")
                    draw_items(["currency"])
                elif Inv.cate == 5:
                    pygame.display.set_caption("Finding The Light - Inventory (Loot)")
                    draw_items(["loot"])
                elif Inv.cate == 6:
                    pygame.display.set_caption("Finding The Light - Inventory (Consumables)")
                    draw_items(["consumable"])
                elif Inv.cate == 7:
                    pygame.display.set_caption("Finding The Light - Inventory (Quest Items)")
                    draw_items(["questItem"])
            def draw_items(itemCate):
                drawing_items = []
                for item in inventory:
                    if item["itemType"] in itemCate and item["count"]: drawing_items.append(item)
                #排序方式
                #drawing_items = sorted(drawing_items, key=lambda x : x["name"])
                for i in range(len(drawing_items)):
                    item = drawing_items[i]
                    draw_color_text(screen, str(item["count"]), 15, 82 + (i % 8 * 94) , 282 + (i // 8 * 115), WHITE)
                    draw_img(screen, item["img"], 37 + (i % 8 * 94), 191 + (i // 8 * 115))
                    if item.get("equip", False) and is_item_equipped(item):
                        outline_text("(已裝備)", 20, 45 + (i % 8 * 94), 250 + (i // 8 * 115), GREEN)
                for i in range(len(drawing_items)):
                    drawing_item = drawing_items[i]
                    if is_hovering(35 + (i * 95 % 800), 125 + (i * 95 % 800), 190 + (i // 8 * 115), 290 + (i // 8 * 115), mouse_x, mouse_y): inv_item_text(drawing_item["name"])
            def inventory_screen(mouse_x, mouse_y):
                scrolling_background()
                pygame.draw.rect(screen, AGRAY, (30, 50, 800, 500))
                outline_text("物品欄", 40, 770 / 2, 70, WHITE)
                for i in range(5):
                    pygame.draw.line(screen, BLACK, (35, 188 + 115 * i), (790, 188 + 115 * i), 4)
                    pygame.draw.line(screen, BLACK, (35, 282 + 115 * i), (790, 282 + 115 * i), 4)
                for i in range(9):
                    pygame.draw.line(screen, BLACK, (35 + i * 94, 188), (35 + i * 94, 532), 4)
                #裝備欄
                pygame.draw.rect(screen, DCGRAY, (0, 600, 1000, 150))
                pygame.draw.rect(screen, BLACK, (0, 600, 1000, 150), 5)
                if Inv.cate != 3:
                    for i in range(5):
                        pygame.draw.rect(screen, AGRAY, (17 + i * 110, 627, 96, 96))
                        pygame.draw.rect(screen, WHITE if i == 0 else BLACK, (17 + i * 110, 627, 96, 96), 3)
                    if (Inv.equip["hotbar"] if Inv.type == "normal" else Inv.equip_preview["hotbar"]) != [""]:
                        for idx, item in enumerate((Inv.equip["hotbar"][1:] if Inv.type == "normal" else Inv.equip_preview["hotbar"][1:])):
                            draw_img(screen, search_item(item)["img"], 130 + idx * 110, 630)
                            if search_item(item)["count"] == 0 and Inv.type == "normal": Inv.equip["hotbar"].remove(item)
                    if (Inv.equip["hotbar"][0] if Inv.type == "normal" else Inv.equip_preview["hotbar"][0]) :draw_img(screen, search_item(Inv.equip["hotbar"][0] if Inv.type == "normal" else Inv.equip_preview["hotbar"][0])["img"], 20, 630)
                    if (Inv.equip["hotbar"] if Inv.type == "normal" else Inv.equip_preview["hotbar"]) != [""]:
                        for idx, item in enumerate((Inv.equip["hotbar"] if Inv.type == "normal" else Inv.equip_preview["hotbar"])):
                            if is_hovering(30 + idx * 110, 130 + idx * 110, 630, 720, mouse_x, mouse_y): inv_item_text(item)
                #顯示武器欄
                if Inv.equip["sword"] and player.weapon == 1: Inv.equip["hotbar"][0] = Inv.equip["sword"]
                elif Inv.equip["bow"] and player.weapon == 2: Inv.equip["hotbar"][0] = Inv.equip["bow"]
                elif Inv.equip["wand"] and player.weapon == 3: Inv.equip["hotbar"][0] = Inv.equip["wand"]
                else: Inv.equip["hotbar"][0] = ""
                draw_img(screen, button_close_img, 740, 80)
                Inv.info_loc_x = mouse_x if mouse_x + 500 < WIDTH else mouse_x - 500
                Inv.info_loc_y = mouse_y if mouse_y - 500 > 0 else mouse_y - 100
                if mouse_y + 300 >= HEIGHT: Inv.info_loc_y = mouse_y - 300
                draw_inventory_category(Inv.cate, mouse_x, mouse_y)
            hovering_inventory_buttons = [is_hovering(35 + i * 94, 35 + 96 + i * 94, 158, 188, mouse_x, mouse_y) for i in range(7)]
            inventory_screen(mouse_x, mouse_y)
            Inv.use = False
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_i:
                        if Inv.type == "normal":
                            Inv.open = False
                            waiting = False
                            return False
                        else:
                            menu = 10
                            Inv.open = False
                    if event.key == pygame.K_f:
                        Inv.use = True
                press_button = pygame.mouse.get_pressed()
                if (press_button[0]):
                    if True in hovering_inventory_buttons: Inv.cate = hovering_inventory_buttons.index(True) + 1
                    elif is_hovering(740, 810, 80, 150, mouse_x, mouse_y):
                        if Inv.type == "normal":
                            Inv.open = False
                            waiting = False
                            return False
                        else:
                            menu = 10
                            Inv.type = "normal"
                            Inv.open = False
        if menu == 6:#解謎
            def draw_rune(slot_index, x, y):
                # 根據符文插槽的值繪製符文
                rune_images = [None, p_water_rune_img, p_fire_rune_img, p_air_rune_img, p_earth_rune_img, p_thunder_rune_img]
                if Area8.rune_slot[slot_index] != 0:
                    draw_img(screen, rune_images[Area8.rune_slot[slot_index]], x, y)
            def draw_puzzle_rune(rune_id, x, y):
                #根據持有的符文繪製符文
                rune_images = [None, p_water_rune_img, p_fire_rune_img, p_air_rune_img, p_earth_rune_img, p_thunder_rune_img]
                if Area8.puzzle_rune_holding == rune_id:
                    draw_img(screen, rune_images[rune_id], x, y)
            def handle_slot_hover(x_min, x_max, y_min, y_max):
                #檢查滑鼠是否懸停在某個區域
                return x_min < mouse_x < x_max and y_min < mouse_y < y_max
            def handle_button_hover(x_min, x_max, y_min, y_max):
                #檢查是否滑鼠懸停在按鈕上
                return x_min <= mouse_x <= x_max and y_min <= mouse_y <= y_max
            #畫面繪製
            draw_img(screen, puzzle_01_img, 30, 50)
            draw_img(screen, button_close_img, 900, 80)
            draw_img(screen, button_submit_img, 240, 450)
            draw_rune(0, 730, 280)
            draw_rune(1, 725, 153)
            draw_rune(2, 600, 280)
            draw_rune(3, 730, 412)
            draw_rune(4, 860, 280)
            #根據是否持有符文來繪製符文
            for rune_id in range(1, 6):
                x_positions = {1: 40, 2: 140, 3: 240, 4: 340, 5: 435}
                draw_puzzle_rune(rune_id, mouse_x, mouse_y) if Area8.puzzle_rune_holding == rune_id else draw_img(screen, [p_water_rune_img, p_fire_rune_img, p_air_rune_img, p_earth_rune_img, p_thunder_rune_img][rune_id - 1], x_positions[rune_id], 280)
                #檢查滑鼠懸停情況
            hovering_status = {
    'water': handle_slot_hover(40, 140, 280, 380),
    'fire': handle_slot_hover(140, 240, 280, 380),
    'air': handle_slot_hover(240, 340, 280, 380),
    'earth': handle_slot_hover(340, 440, 280, 380),
    'thunder': handle_slot_hover(440, 540, 280, 380),
    'slot_1': handle_slot_hover(720, 820, 270, 370),
    'slot_2': handle_slot_hover(730, 830, 150, 250),
    'slot_3': handle_slot_hover(600, 700, 280, 380),
    'slot_4': handle_slot_hover(730, 830, 410, 510),
    'slot_5': handle_slot_hover(860, 960, 280, 380),
    'close_button': handle_button_hover(900, 970, 80, 150),
    'submit_button': handle_button_hover(240, 410, 450, 520)
}
            pygame.display.update()
            # 事件處理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    Puzzle.open = False
                    Area8.puzzle_rune_holding = 0
                    Area8.rune_slot = [0, 0, 0, 0, 0]
                    waiting = False
                    return False
                press_button = pygame.mouse.get_pressed()
                if press_button[0]:
                    #處理符文選擇
                    for rune_id, rune_name in enumerate(['water', 'fire', 'air', 'earth', 'thunder'], start=1):
                        if hovering_status[rune_name] and all(Area8.rune_slot[i] != rune_id for i in range(5)):
                            Area8.puzzle_rune_holding = 0 if Area8.puzzle_rune_holding == rune_id else rune_id
                    # 處理關閉按鈕
                    if hovering_status['close_button']:
                        Puzzle.open = False
                        Area8.puzzle_rune_holding = 0
                        Area8.rune_slot = [0, 0, 0, 0, 0]
                        waiting = False
                        return False
                    for i in range(5):
                        if hovering_status[f'slot_{i + 1}']:
                            Area8.old_holding = Area8.rune_slot[i]
                            Area8.rune_slot[i] = Area8.puzzle_rune_holding
                            Area8.puzzle_rune_holding = Area8.old_holding
                    if hovering_status['submit_button']:
                        if Area8.rune_slot == [1, 2, 3, 4, 5]:
                            new_dialogue("(當你成功解開符文鎖的機關時，一陣神秘的力量填滿了房間。", "你感受到了古老的祝福，似乎是古代的守護者賜予的。)", str(Player.name), "冒險家")
                            new_message("在房間盡頭，一道通往未知的門為你打開")
                            new_message("生命值已回滿")
                            Area8.puzzle_complete = True
                            player.health = Stats.total["生命上限"]
                            Puzzle.open = False
                            waiting = False
                            return False
                        else:
                            new_message("甚麼事也沒發生")
                            Area8.rune_slot = [0, 0, 0, 0, 0]
                            Puzzle.open = False
                            waiting = False
                            return False
        if menu == 7:#鍛造
            if Player.cooldowns["forge"] > 0: Player.cooldowns["forge"] -= 1
            draw_img(screen, forge_img, 30, 50)
            draw_img(screen, button_close_img, 900, 80)
            if Player.cooldowns["forge"] > 0:
                forge_progress(screen, Player.cooldowns["forge"], Forge.max_last_time, 505, 312)
                draw_color_text(screen, "剩餘時間:" + str(Player.cooldowns["forge"] // 60), 15, 700, 305, BLACK)
            else:
                Forge.max_last_time = 0
            if Player.cooldowns["forge"] == 0:
                if Forge.working == 1:
                    player.gain_item("粗鐵劍", 1)
                if Forge.working == 2:
                    player.gain_item("鐵塊", 1)
                Forge.working = 0
            #鍛造介面
            def forge_gui(forgeItem, costItem):
                #鍛造物品
                for name, count in forgeItem.items():
                    draw_img(screen, search_item(name)["img"], 655, 185)
                    draw_text(screen, str(count), 15, 700, 280)
                x_move = 0
                for name, count in costItem.items():
                    draw_text(screen, str(search_item(name)["count"]) + "/" + str(count), 15, 505 + x_move, 500)
                    draw_img(screen, search_item(name)["img"], 462 + x_move, 402)
                    x_move += 100
            if Forge.selected == 1 and Forge.cate == 1: forge_gui({"粗鐵劍":1}, {"樹枝":1, "骨頭":2, "鐵塊":3})
            if Forge.selected == 1 and Forge.cate == 4: forge_gui({"鐵塊":1}, {"基礎礦石":2})
            if Forge.cate == 1:
                draw_img(screen, inv_weapons_img, 31, 160)
                draw_img(screen, item_iron_sword_img, 35, 190)
                draw_color_text(screen, "粗鐵劍", 15, 80, 280, BLACK)
            if Forge.cate == 2:
                draw_img(screen, inv_armors_img, 131, 160)
            if Forge.cate == 3:
                draw_img(screen, inv_charms_img, 231, 160)
            if Forge.cate == 4:
                draw_img(screen, inv_misc_img, 331, 160)
                draw_img(screen, item_iron_ingot_img, 35, 190)
                draw_color_text(screen, "鐵塊", 15, 80, 280, BLACK)
            hovering_weapons_button = is_hovering(30, 130, 160, 180, mouse_x, mouse_y)
            hovering_armors_button = is_hovering(130, 230, 160, 180, mouse_x, mouse_y)
            hovering_charms_button = is_hovering(230, 330, 160, 180, mouse_x, mouse_y)
            hovering_misc_button = is_hovering(330, 430, 160, 180, mouse_x, mouse_y)
            hovering_forge_button = is_hovering(650, 750, 335, 375, mouse_x, mouse_y)
            hovering_close_button = is_hovering(900, 970, 80, 150, mouse_x, mouse_y)
            hovering_slot_01 = is_hovering(35, 135, 190, 290, mouse_x, mouse_y)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Forge.open = False
                        waiting = False
                        return False
                press_button = pygame.mouse.get_pressed()
                if (press_button[0]):
                    if hovering_weapons_button:Forge.cate = 1
                    if hovering_slot_01:Forge.selected = 1
                    if hovering_armors_button:Forge.cate = 2
                    if hovering_charms_button:Forge.cate = 3
                    if hovering_misc_button:Forge.cate = 4
                    if hovering_forge_button and Player.cooldowns["forge"] == 0:
                        if Forge.cate == 1:
                            if Forge.selected == 1:
                                if search_item("樹枝")["count"] >= 1 and search_item("骨頭")["count"] >= 2 and search_item("鐵塊")["count"] >= 3:
                                    Player.cooldowns["forge"] = 1800
                                    Forge.max_last_time = 1800
                                    player.gain_item("樹枝", -1)
                                    player.gain_item("骨頭", -2)
                                    player.gain_item("鐵塊", -3)
                                    Forge.working = 1
                        if Forge.cate == 4:
                            if Forge.selected == 1:
                                if search_item("基礎礦石")["count"] >= 2:
                                    Player.cooldowns["forge"] = 300
                                    Forge.max_last_time = 300    
                                    player.gain_item("基礎礦石", -2)
                                    Forge.working = 2
                    if hovering_close_button:
                        Forge.open = False
                        waiting = False
                        return False
        if menu == 8:#角色屬性
            draw_img(screen, c_stats_img, 30, 50)
            draw_img(screen, button_close_img, 900, 80)
            pygame.display.set_caption("Finding The Light - Stats")
            if Stats.cate == 1:
                stats = Stats.total
                draw_img(screen, c_total_img, 31, 160)
            if Stats.cate == 2:
                stats = Stats.bonus
                draw_img(screen, c_bonus_img, 131, 160)
            if Stats.cate == 3:
                stats = Stats.basic
                draw_img(screen, c_base_img, 231, 160)
            #顯示公式
            if player.weapon == 1: draw_color_text(screen, "當前職業: 刺客", 20, 110, 120, WHITE)
            if player.weapon == 2: draw_color_text(screen, "當前職業: 弓箭手", 20, 110, 120, WHITE)
            if player.weapon == 3: draw_color_text(screen, "當前職業: 法師", 20, 110, 120, WHITE)
            draw_color_text(screen, "公式(" + Stats.info + "): ", 20, 150, 200, WHITE)
            if Stats.info == "攻擊力":
                draw_color_text(screen, "總傷害 = ", 20, 160, 230, WHITE)
                draw_color_text(screen, "攻擊力×(1+攻擊力%)×", 20, 180, 260, WHITE)
                draw_color_text(screen, "技能倍率×獨立加成", 20, 170, 290, WHITE)
                draw_color_text(screen, "= " + str(round(stats["攻擊力"] * (1 + stats["攻擊力%"] / 100), 1)) + "×技能倍率×獨立加成", 20, 170, 340, WHITE)
            if Stats.info == "防禦力":
                draw_color_text(screen, "承受傷害 = ", 20, 145, 230, WHITE)
                draw_color_text(screen, "原始傷害", 20, 180, 260, WHITE)
                pygame.draw.line(screen, WHITE, (100, 285), (250, 285), 1)
                draw_color_text(screen, "1+(防禦力×0.01×(1+防禦力%))", 20, 180, 290, WHITE)
                draw_color_text(screen, "=" + "原始傷害", 20, 170, 340, WHITE)
                pygame.draw.line(screen, WHITE, (100, 365), (250, 365), 1)
                draw_color_text(screen, str(round(1 + (stats["防禦力"] * 0.01 * (1 + stats["防禦力%"] / 100)), 1)), 20, 180, 360, WHITE)
            if Stats.info == "生命值":
                draw_color_text(screen, "總生命值 = ", 20, 160, 230, WHITE)
                draw_color_text(screen, "生命值×(1+生命值%)", 20, 175, 260, WHITE)
                draw_color_text(screen, "= " + str(round(stats["生命上限"] * (1 + stats["生命上限%"] / 100), 1)), 20, 170, 300, WHITE)
                draw_color_text(screen, "有效生命值(EHP) = " + str(round(stats["生命上限"] * (1 + stats["生命上限%"] / 100) * (1 + stats["防禦力"] * 0.01 * (1 + stats["防禦力%"] / 100)), 1)), 20, 160, 340, WHITE)
            if Stats.info == "魔力值":
                draw_color_text(screen, "總魔力值 = ", 20, 160, 230, WHITE)
                draw_color_text(screen, str(stats["魔力上限"]) + "+其他加成", 20, 170, 260, WHITE)
            if Stats.info == "魔力值回復量":
                draw_color_text(screen, "總魔力值回復量 = ", 20, 160, 230, WHITE)
                draw_color_text(screen, "3+(法師等級-1)*0.1+其他加成", 20, 175, 260, WHITE)
                draw_color_text(screen, "= " + str(stats["魔力回復"]) + "+其他加成", 20, 170, 300, WHITE)
            if Stats.info == "生命值回復量":
                draw_color_text(screen, "生命回復效果每秒回復量 = ", 20, 160, 230, WHITE)
                draw_color_text(screen, "所有等級+其他加成", 20, 170, 260, WHITE)
                draw_color_text(screen, "= " + str(stats["生命回復"]) + "+其他加成", 20, 170, 300, WHITE)
            if Stats.info == "移動速度":
                draw_color_text(screen, "移動速度 = ", 20, 160, 230, WHITE)
                draw_color_text(screen, "10*(1+移動速度%)", 20, 170, 260, WHITE)
                draw_color_text(screen, "= " + str(round(10 * (1 + stats["移動速度"] / 100), 1)), 20, 170, 300, WHITE)
            if Stats.info == "技能冷卻":
                draw_color_text(screen, "技能冷卻時間 = ", 20, 160, 230, WHITE)
                draw_color_text(screen, "原始冷卻*(1-冷卻減免%)", 20, 170, 260, WHITE)
                draw_color_text(screen, "= " + "原始冷卻*" + str(round(1 - stats["冷卻減免%"] / 100, 1)), 20, 170, 300, WHITE)
            #第一欄
            draw_color_text(screen, str(stats["攻擊力"]), 20, 500, 200, WHITE)
            draw_color_text(screen, str(stats["攻擊力%"]) + "%", 20, 500, 260, WHITE)
            draw_color_text(screen, str(stats["防禦力"]), 20, 500, 320, WHITE)
            draw_color_text(screen, str(stats["防禦力%"]) + "%", 20, 500, 380, WHITE)
            draw_color_text(screen, str(stats["生命上限"]), 20, 500, 440, WHITE)
            draw_color_text(screen, str(stats["生命上限%"]) + "%", 20, 500, 500, WHITE)
            #第二欄
            draw_color_text(screen, str(stats["魔力上限"]), 20, 850, 200, WHITE)
            draw_color_text(screen, str(stats["魔力回復"]), 20, 850, 260, WHITE)
            draw_color_text(screen, str(stats["生命回復"]), 20, 850, 320, WHITE)
            draw_color_text(screen, str(stats["移動速度"]) + "%", 20, 850, 380, WHITE)
            draw_color_text(screen, str(stats["冷卻減免%"]) + "%", 20, 850, 440, WHITE)
            #第一欄
            draw_color_text(screen, "攻擊力:", 20, 400, 200, WHITE)
            draw_color_text(screen, "攻擊力百分比:", 20, 400, 260, WHITE)
            draw_color_text(screen, "防禦力:", 20, 400, 320, WHITE)
            draw_color_text(screen, "防禦力百分比:", 20, 400, 380, WHITE)
            draw_color_text(screen, "生命值:", 20, 400, 440, WHITE)
            draw_color_text(screen, "生命值百分比:", 20, 400, 500, WHITE)
            #第二欄
            draw_color_text(screen, "魔力值上限:", 20, 750, 200, WHITE)
            draw_color_text(screen, "魔力值回復:", 20, 750, 260, WHITE)
            draw_color_text(screen, "生命值回復:", 20, 750, 320, WHITE)
            draw_color_text(screen, "移動速度:", 20, 750, 380, WHITE)
            draw_color_text(screen, "冷卻減免百分比:", 20, 750, 440, WHITE)
            draw_color_text(screen, "", 20, 750, 500, WHITE)
            draw_color_text(screen, "", 20, 750, 560, WHITE)

            hovering_atk_button = is_hovering(320, 670, 200, 300, mouse_x, mouse_y)
            hovering_def_button = is_hovering(320, 670, 300, 400, mouse_x, mouse_y)
            hovering_hp_button = is_hovering(320, 670, 400, 500, mouse_x, mouse_y)
            hovering_mana_button = is_hovering(670, 1000, 200, 250, mouse_x, mouse_y)
            hovering_mana_regen_button = is_hovering(670, 1000, 250, 300, mouse_x, mouse_y)
            hovering_hp_regen_button = is_hovering(670, 1000, 300, 350, mouse_x, mouse_y)
            hovering_spd_button = is_hovering(670, 1000, 350, 400, mouse_x, mouse_y)
            hovering_cd_button = is_hovering(670, 1000, 400, 450, mouse_x, mouse_y)
            hovering_total_button = is_hovering(30, 130, 160, 180, mouse_x, mouse_y)
            hovering_bonus_button = is_hovering(130, 230, 160, 180, mouse_x, mouse_y)
            hovering_base_button = is_hovering(230, 330, 160, 180, mouse_x, mouse_y)
            hovering_close_button = is_hovering(900, 970, 80, 150, mouse_x, mouse_y)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_c:
                        Stats.open = False
                        waiting = False
                        return False
                press_button = pygame.mouse.get_pressed()
                if (press_button[0]):
                    if hovering_atk_button: Stats.info = "攻擊力"
                    if hovering_def_button: Stats.info = "防禦力"
                    if hovering_hp_button: Stats.info = "生命值"
                    if hovering_mana_button: Stats.info = "魔力值"
                    if hovering_mana_regen_button: Stats.info = "魔力值回復量"
                    if hovering_hp_regen_button: Stats.info = "生命值回復量"
                    if hovering_spd_button: Stats.info = "移動速度"
                    if hovering_cd_button: Stats.info = "技能冷卻"
                    if hovering_total_button: Stats.cate = 1
                    if hovering_bonus_button: Stats.cate = 2
                    if hovering_base_button: Stats.cate = 3
                    if hovering_close_button:
                        Stats.open = False
                        waiting = False
                        return False
                if (press_button[1]): print(mouse_x, mouse_y)
        if menu == 9:#天賦樹
            pygame.display.set_caption("Finding The Light - Ability Tree")
            if mouse_x + 500 >= WIDTH: A_tree.info_loc_x = mouse_x - 500
            else:A_tree.info_loc_x = mouse_x
            if mouse_y - 200 <= 0: A_tree.info_loc_y = mouse_y
            else:A_tree.info_loc_y = mouse_y - 200
            #介面
            pygame.draw.rect(screen, DGRAY, (0, 0, 1000, 750))
            pygame.draw.rect(screen, AGRAY, (A_tree.gui_location_x - 1000, A_tree.gui_location_y - 900, 2000, 1500))
            pygame.draw.rect(screen, BLACK, (A_tree.gui_location_x - 1000, A_tree.gui_location_y - 900, 2000, 1500), 5)
            if A_tree.cate == 1:
                #[刺客]
                #被動 - 激流(Riptide)
                draw_ability_tree_node(1, 0, ["刺客 (Rouge)", "刺客是一個狡詐的職業，", "擅長使用詭計來偷襲敵人。", "永久被動技能 - 激流:", "觸發:使用技能後下一次普通攻擊", "消耗:無消耗", "效果:獲得持續5秒的激流狀態。","冷卻時間:0秒", "激流狀態", "激流狀態可強化終結技，","並決定使用次數。", "永久解鎖", 300, 480, 50, "職業"])
                draw_ability_tree_line(350, 480, 350, 150)
                #技能 - 暗影脈衝
                draw_ability_tree_node(1, 1, ["暗影脈衝", ["被動"], "技能 - 暗影脈衝", "", "消耗:無消耗", "效果:獲得5秒50%速度提升", "下次普通攻擊改為重擊。", "冷卻時間:10秒", "重擊", "造成攻擊力200%物理傷害，", "並進入激流狀態。", 450, 250, 50, "技能"])
                draw_ability_tree_line(350, 300, 450, 300)
                #技能升級 - 重擊強化
                draw_ability_tree_node(1, 2, ["重擊強化", ["暗影脈衝"], "技能升級 - 重擊強化", "觸發:使用技能後下一次普通攻擊", "效果:強化重擊和激流重擊傷害", "至攻擊力300%", "冷卻時間:0秒", 600, 100, 50, "升級"])
                draw_ability_tree_line(500 + 35, 300 - 35, 650 - 35, 150 + 35)
                #終結技 - 暗影襲擊
                draw_ability_tree_node(1, 3, ["暗影襲擊", ["被動"], "終結技 - 暗影襲擊", "", "消耗:全部激流秒數", "效果:瞬移到敵人身邊，", "根據激流秒數獲得激流重擊", "冷卻時間:15秒", "激流重擊", "造成攻擊力200%水屬性傷害，", "並消耗一層激流重擊。", 200, 100, 50, "技能"])
                draw_ability_tree_line(350, 150, 300, 150)
                draw_ability_tree_line(250, 100, 250, -100, DGRAY)
                #暗影襲擊 - 降低冷卻
                draw_ability_tree_node(1, 4, ["暗影襲擊降低冷卻", ["暗影襲擊"], "終結技升級 - 降低冷卻", "觸發:使用大招後", "效果:降低大招的冷卻5秒", "", "冷卻時間:0秒", 50, -50, 50, "升級"])
                draw_ability_tree_line(250 - 35, 150 - 35, 100 + 35, 0 + 35)
                #暗影襲擊 - 激流強化
                draw_ability_tree_node(1, 5, ["激流強化", ["暗影襲擊"], "終結技升級 - 激流強化", "觸發:使用大招後", "效果:額外獲得激流重擊次數 + 3", "", "冷卻時間:0秒", 50, 250, 50, "升級"])
                draw_ability_tree_line(250 - 35, 150 + 35, 100 + 43, 250 + 35)
                #技能 - 破空突擊
                draw_ability_tree_node(1, 6, ["破空突擊", ["暗影脈衝"], "技能 - 破空突擊", " + 離地", "消耗:無消耗", "效果:快速下落並攻擊，", "造成攻擊力300%物理傷害", "冷卻時間:5秒(未命中則為1秒)", "", "", "", 450, -50, 50, "技能"])
                draw_ability_tree_line(500, 50, 500, 250)
                draw_ability_tree_line(500, -50, 500, -100)
                draw_ability_tree_line(500, -100, 250, -100, DGRAY)
                #技能 - 次元斬 I
                draw_ability_tree_node(1, 7, ["次元斬 I", ["破空突擊", "暗影襲擊"], "技能 - 次元斬 I", "", "消耗:無消耗", "效果:擊敗普通怪刷新1秒技能冷卻", "擊敗菁英怪刷新全部技能冷卻", "冷卻時間:無(此技能無法施放)", "", "", "", 200, -150, 50, "技能"])
                #技能升級 - 再生
                draw_ability_tree_node(1, 8, ["破空突擊強化", ["破空突擊"], "技能升級 - 再生", "觸發:使用破空突擊擊敗敵人", "效果:擊敗普通怪恢復15%生命值", "擊敗菁英怪恢復25%生命值", "冷卻時間:0秒", 600, -300, 50, "升級"])
                draw_ability_tree_line(500, -100, 650 - 35, -250 + 35)
                #技能 - 混沌匕首
                draw_ability_tree_node(1, 9, ["混沌匕首", ["破空突擊強化"], "技能 - 混沌匕首", "", "消耗:無消耗", "效果:向前投擲混沌匕首", "", "冷卻時間:10秒", "混沌匕首", "標記第一個觸碰到的敵人", "使其降低20%抗性，持續5秒。", 800, -500, 50, "技能"])
                draw_ability_tree_line(650 + 35, -250 - 35, 850 -35, -450 + 35)
                #技能升級 - 渾沌匕首強化
                draw_ability_tree_node(1, 10, ["混沌匕首強化", ["混沌匕首"], "技能升級 - 渾沌匕首強化", "觸發:混沌匕首命中", "效果:混沌匕首將降低敵人30%抗性", "", "冷卻時間:0秒", 800, -300, 50, "升級"])
                draw_ability_tree_line(850, -400, 850, -300)
                #技能升級 - 次元斬 II
                draw_ability_tree_node(1, 11, ["次元斬 II", ["次元斬 I"], "技能升級 - 次元斬 II", "觸發:次元斬 I", "效果:額外降低1秒冷卻", "", "冷卻時間:0秒", 50, -300, 50, "升級"])
                draw_ability_tree_line(200 + 20, -100 - 35, 100 + 30, -250 + 35)
                #[刺客二轉]
                #流放者 (The Exiled)
                draw_ability_tree_node(1, 12, ["流放者 (The Exiled)", "暗屬性的流放者可以隱去行蹤，", "並透過擊敗敵人來強化自身。", "被動技能強化 - 夜幕潛行:", "觸發:擊敗敵人", "消耗:無消耗", "效果:獲得一層夜幕潛行", "冷卻時間:0秒", "夜幕潛行", "夜幕潛行將取代激流，且不會衰退，", "原本消耗激流將改為消耗夜幕潛行。", "流放者", -200, -300, 50, "二轉"])
                draw_ability_tree_line(50, -250, -100, -250, PURPLE)
                #技能 - 幻影分身
                draw_ability_tree_node(1, 13, ["幻影分身", ["次元斬 II", "流放者"], "技能 - 幻影分身", "", "消耗:無/3層夜幕潛行", "效果:在前方召喚持續3秒的幻影分身並揮砍，", "造成攻擊力200%暗屬性傷害。", "冷卻時間:7秒", "幻影分身", "玩家可消耗夜幕潛行移動至分身位置，", "再次揮砍造成攻擊力300%暗屬性傷害。", -200, -500, 50, "技能"])
                draw_ability_tree_line(-150, -300, -150, -400)
                #技能升級 - 隱身
                draw_ability_tree_node(1, 14, ["隱身", ["幻影分身"], "技能升級 - 隱身", "觸發:傳送至幻影分身處", "效果:進入隱身持續2秒，在此狀態", "擊敗敵人額外獲得一層夜幕潛行。", "冷卻時間:0秒", -50, -650, 50, "升級"])
                draw_ability_tree_line(0 - 35, -600 + 35, -150 + 35, -450 - 35)
                #技能升級 - 刀舞
                draw_ability_tree_node(1, 15, ["刀舞", ["幻影分身"], "技能升級 - 刀舞", "觸發:傳送至幻影分身處", "效果:將分身的普通攻擊改為", "原範圍200%更大的刀舞。", "冷卻時間:0秒", 50, -500, 50, "升級"])
                draw_ability_tree_line(-100, -450, 50, -450)
                #技能升級 - 無聲絞喉
                draw_ability_tree_node(1, 16, ["無聲絞喉", ["幻影分身"], "技能升級 - 無聲絞喉", "觸發:目標生命值低於10%", "效果:立即處決非魔王階級目標。", "", "冷卻時間:0秒", -400, -500, 50, "升級"])
                draw_ability_tree_line(-300, -450, -200, -450)
                #技能 - 煙霧彈
                draw_ability_tree_node(1, 17, ["煙霧彈", ["無聲絞喉"], "技能 - 煙霧彈", "", "消耗:無/所有層夜幕潛行", "效果:以70度角投擲煙霧彈，", "持續5秒。", "冷卻時間:10秒", "煙霧彈", "對範圍內敵人每秒造成攻擊力50%", "暗屬性傷害，並降低敵人50%移動速度。", -400, -700, 50, "技能"])
                draw_ability_tree_line(-350, -600, -350, -500)
                #技能升級 - 煙霧範圍提升
                draw_ability_tree_node(1, 18, ["煙霧範圍提升", ["煙霧彈"], "技能升級 - 煙霧範圍提升", "觸發:使用煙霧彈", "效果:影響範圍 + 50%", "", "冷卻時間:0秒", -600, -700, 50, "升級"])
                draw_ability_tree_line(-400, -650, -500, -650)
            if A_tree.cate == 2:
                #弓箭手1頁[被動/火焰箭矢/點燃/苦無/雙面苦無/專注力強化]
                #被動 - 專注力(Focus)
                draw_ability_tree_node(2, 0, ["弓箭手(Archer)", "弓箭手是一個善於遠程攻擊的職業，", "連續命中敵人能造成大量傷害。", "永久被動技能 - 專注力:", "觸發:使用普通攻擊", "消耗:無消耗", "效果:命中時獲得1點專注力，每3秒降低1點。", "冷卻:0秒", "專注力", "專注力可強化技能，", "使下一擊造成更多傷害。", "永久解鎖", 300, 480, 50, "職業"])
                draw_ability_tree_line(350, 480, 350, 0)
                #技能 - 火焰箭矢
                draw_ability_tree_node(2, 1, ["火焰箭矢", ["被動"], "技能 - 火焰箭矢", "", "消耗:全部專注力", "效果:射出一根火焰箭矢，", "命中後造成攻擊力(1+專注力)*100%火屬性傷害。", "冷卻時間:10秒", "", "", "", 580, 280, 50, "技能"])
                draw_ability_tree_line(350, 330, 580, 330)
                #技能升級 - 點燃
                draw_ability_tree_node(2, 2, ["點燃", ["火焰箭矢"], "技能升級 - 點燃", "觸發:使用技能命中敵人", "效果:對敵人施加燃燒狀態，", "每秒造成攻擊力80%火屬性傷害，持續3秒。", "冷卻時間:0秒", "", "", 580, 80, 50, "升級"])
                draw_ability_tree_line(630, 280, 630, 180)
                #終結技 - 苦無
                draw_ability_tree_node(2, 3, ["苦無", ["被動"], "終結技 - 苦無", "", "消耗:所有專注力", "效果:獲得(1+專注力)個苦無，", "再次按Q投擲。", "冷卻時間:20秒", "苦無", "命中後造成攻擊力300%物理傷害。", "", 0, 0, 50, "技能"])
                draw_ability_tree_line(100, 50, 350, 50)
                #大招升級 - 雙向苦無
                draw_ability_tree_node(2, 4, ["雙向苦無", ["苦無"], "終結技升級 - 雙向苦無", "觸發:使用大招後", "效果:施放大招時苦無變為雙向，", "但消耗2倍數量。", "", "冷卻時間:0秒", "", "", -200, 0, 50, "升級"])
                draw_ability_tree_line(0, 50, -100, 50)
                #被動升級 - 專注力強化
                draw_ability_tree_node(2, 5, ["專注力強化", ["被動"], "被動升級 - 專注力強化", "觸發:被動", "效果:增加2點專注力上限", "", "冷卻時間:0秒", "", "", 150, 150, 50, "升級"])
                draw_ability_tree_line(250, 200, 350, 200)
            if A_tree.cate == 3:
                #法師第一頁[被動/隕石/隕石增加傷害/瞬水爆/水爆延長/水爆節省魔力]
                #被動 - 魔力(Mana)
                draw_ability_tree_node(3, 0, ["法師(Mage)", "法師是一個善於法術攻擊的職業，", "適當控管魔力的使用能在戰鬥中獲得優勢。", "永久被動技能 - 魔力:", "觸發:使用能力", "消耗:根據技能消耗量", "效果:無", "冷卻:0秒", "魔力", "魔力隨時間恢復。", "", "永久解鎖", 300, 480, 50, "職業"])
                draw_ability_tree_line(350, 480, 350, 0)
                #技能 - 隕石
                draw_ability_tree_node(3, 1, ["隕石", ["被動"], "技能 - 隕石", "", "消耗:30魔力", "效果:召喚一顆從天而降的隕石，", "對命中的敵人造成攻擊力400%火屬性傷害。", "冷卻時間:10秒", "", "", "", 550, 100, 50, "技能"])
                draw_ability_tree_line(350, 150, 550, 150)
                #技能升級 - 隕石增加傷害
                draw_ability_tree_node(3, 2, ["隕石增加傷害", ["隕石"], "技能升級 - 增加傷害", "觸發:使用技能後", "效果:傷害提升至攻擊力500%。", "", "冷卻時間:0秒", "", "", 550, 300, 50, "升級"])
                draw_ability_tree_line(600, 200, 600, 300)
                #終結技 - 瞬水爆
                draw_ability_tree_node(3, 3, ["瞬水爆", ["被動"], "終結技 - 瞬水爆", "", "消耗:50魔力", "效果:進入瞄準狀態，再次施放會瞬移到準心位置，施放水爆領域，並切換至刺客，", "獲得火傷害附魔，若有激流重擊，則獲得暗屬性附魔。", "冷卻時間:30秒", "水爆領域", "對範圍內敵人每秒造成", "攻擊力200%水屬性傷害，持續2秒。", 100, 200, 50, "技能"])
                draw_ability_tree_line(200, 250, 350, 250)
                #終結技升級 - 水爆延長
                draw_ability_tree_node(3, 4, ["水爆延長", ["瞬水爆"], "終結技升級 - 延長水爆領域", "觸發:使用大招後", "效果:延長水爆領域持續時間2秒。", "", "冷卻時間:0秒", "", "", 100, 0, 50, "升級"])
                draw_ability_tree_line(150, 200, 150, 100)
                #終結技升級 - 節省魔力
                draw_ability_tree_node(3, 5, ["水爆節省魔力", ["瞬水爆"], "終結技升級 - 節省魔力", "觸發:使用大招後", "效果:魔法附魔狀態每秒減少消耗2點魔力。", "", "冷卻時間:0秒", "", "", -40, 60, 50, "升級"])
                draw_ability_tree_line(150 - 35, 250 - 35, 10 + 35, 110 + 35)
            #快捷欄
            draw_ability_info()
            draw_img(screen, ability_tree_hotbar_img, 0, 600)
            draw_color_text(screen, "技能列: " + str(A_tree.row), 20, 387, 610, WHITE)
            draw_img(screen, mouse_mid_click_img, 377, 710)
            if is_hovering(364, 414, 650, 700, Mouse.x, Mouse.y): pygame.draw.rect(screen, WHITE, (364, 650, 50, 50), 2)
            draw_color_text(screen, str("W"), 20, 490, 725, WHITE)
            draw_color_text(screen, str("E"), 20, 600, 725, WHITE)
            draw_color_text(screen, str("R"), 20, 710, 725, WHITE)
            draw_color_text(screen, str("S"), 20, 820, 725, WHITE)
            draw_color_text(screen, str("Q"), 20, 930, 725, WHITE)
            #畫出W技能
            if A_tree.keybind[A_tree.cate - 1]["W" + str(A_tree.row)] != "":draw_img(screen, A_tree.skill_img[A_tree.cate - 1][A_tree.keybind[A_tree.cate - 1]["W" + str(A_tree.row)]], 447, 630)
            #畫出E技能
            if A_tree.keybind[A_tree.cate - 1]["E" + str(A_tree.row)] != "":draw_img(screen, A_tree.skill_img[A_tree.cate - 1][A_tree.keybind[A_tree.cate - 1]["E" + str(A_tree.row)]], 557, 630)
            #畫出R技能
            if A_tree.keybind[A_tree.cate - 1]["R" + str(A_tree.row)] != "":draw_img(screen, A_tree.skill_img[A_tree.cate - 1][A_tree.keybind[A_tree.cate - 1]["R" + str(A_tree.row)]], 667, 630)
            #畫出Q技能
            if A_tree.rogue["暗影襲擊"] and A_tree.cate == 1:draw_img(screen, rogue_ultimate_img, 887, 640)
            if A_tree.archer["苦無"] and A_tree.cate == 2:draw_img(screen, archer_ultimate_img, 887, 640)
            if A_tree.mage["瞬水爆"] and A_tree.cate == 3:draw_img(screen, mage_ultimate_img, 887, 640)
            draw_img(screen, ability_tree_rogue_img, 20, 630)
            draw_img(screen, ability_tree_archer_img, 130, 630)
            draw_img(screen, ability_tree_mage_img, 240, 630)
            if is_hovering(20, 120, 630, 730, Mouse.x, Mouse.y): pygame.draw.rect(screen, WHITE, (15, 625, 100, 100), 3)
            if is_hovering(130, 230, 630, 730, Mouse.x, Mouse.y): pygame.draw.rect(screen, WHITE, (125, 625, 100, 100), 3)
            if is_hovering(240, 340, 630, 730, Mouse.x, Mouse.y): pygame.draw.rect(screen, WHITE, (235, 625, 100, 100), 3)
            pygame.draw.line(screen, BLACK, (0, 600), (1000, 600), 5)
            draw_color_text(screen, "技能點:" + str(Assassin.a_point), 20, 65, 600, WHITE)
            draw_color_text(screen, "技能點:" + str(Archer.a_point), 20, 175, 600, WHITE)
            draw_color_text(screen, "技能點:" + str(Mage.a_point), 20, 285, 600, WHITE)
            draw_color_text(screen, "1", 20, 65, 720, WHITE)
            draw_color_text(screen, "2", 20, 175, 720, WHITE)
            draw_color_text(screen, "3", 20, 285, 720, WHITE)
            draw_img(screen, ability_tree_arrow_right_img, 665, 300)
            draw_img(screen, ability_tree_arrow_left_img, 5, 300)
            draw_img(screen, ability_tree_arrow_top_img, 350, 5)
            draw_img(screen, button_close_img, 910, 30)
            hovering_close_button = is_hovering(910, 980, 30, 100, mouse_x, mouse_y)
            #檢測技能是否有已裝備的技能未學習
            for i in range(3):
                if i == 0: tree = A_tree.rogue
                if i == 1: tree = A_tree.archer
                if i == 2: tree = A_tree.mage
                for _, abilities in A_tree.keybind[i].items():
                    if abilities:
                        if tree[abilities] == 0:
                            A_tree.keybind[i][_] = ""
            A_tree.lclick = False
            pygame.display.update()
            def switch_cate(cate):
                A_tree.cate = cate
                if cate == 1: A_tree.showing_info = ["刺客(Rouge)", "刺客是一個狡詐的職業，", "擅長使用詭計來偷襲敵人。", "永久被動技能 - 激流:", "觸發:使用技能後下一次普通攻擊", "消耗:無消耗", "效果:獲得持續5秒的激流狀態。","冷卻時間:0秒", "激流狀態", "激流狀態可強化終結技，","並決定使用次數。", "永久解鎖", 300, 480, 50, "職業"]
                if cate == 2: A_tree.showing_info = ["弓箭手(Archer)", "弓箭手是一個善於遠程攻擊的職業，", "連續命中敵人能造成大量傷害。", "永久被動技能 - 專注力:", "觸發:使用普通攻擊", "消耗:無消耗", "效果:命中時獲得1點專注力，每3秒降低1點。", "冷卻:0秒", "專注力", "專注力可強化技能，", "使下一擊造成更多傷害。", "永久解鎖", 300, 480, 50, "職業"]
                if cate == 3: A_tree.showing_info = ["法師(Mage)", "法師是一個善於法術攻擊的職業，", "適當控管魔力的使用能在戰鬥中獲得優勢。", "永久被動技能 - 魔力:", "觸發:使用能力", "消耗:根據技能消耗量", "效果:無", "冷卻:0秒", "魔力", "魔力隨時間恢復。", "", "永久解鎖", 300, 480, 50, "職業"]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        A_tree.open = False
                        waiting = False
                        return False
                    if A_tree.showing_info[2].startswith("技能 -"):
                        if event.key == pygame.K_w:tweak_keybind("W" + str(A_tree.row), A_tree.showing_info[0])
                        if event.key == pygame.K_e:tweak_keybind("E" + str(A_tree.row), A_tree.showing_info[0])
                        if event.key == pygame.K_r:tweak_keybind("R" + str(A_tree.row), A_tree.showing_info[0])
                    if event.key == pygame.K_1:switch_cate(1)
                    if event.key == pygame.K_2:switch_cate(2)
                    if event.key == pygame.K_3:switch_cate(3)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if is_hovering(364, 414, 650, 700, Mouse.x, Mouse.y): A_tree.row = 3 - A_tree.row
                        A_tree.lclick = True
                        A_tree.mouse_temp_x = Mouse.x
                        A_tree.mouse_temp_y = Mouse.y
                    if event.button == 2: A_tree.row = 3 - A_tree.row
                    if event.button == 4: A_tree.gui_location_y += 30
                    if event.button == 5: A_tree.gui_location_y -= 30
            press_button = pygame.mouse.get_pressed()
            if (press_button[0]):
                if is_hovering(20, 120, 630, 730, mouse_x, mouse_y): switch_cate(1)
                if is_hovering(130, 230, 630, 730, mouse_x, mouse_y): switch_cate(2)
                if is_hovering(240, 340, 630, 730, mouse_x, mouse_y): switch_cate(3)
                if is_hovering(0, 1000, 0, 600, mouse_x, mouse_y):
                    if Mouse.x < 700:
                        A_tree.gui_location_x += Mouse.x - A_tree.mouse_temp_x
                        A_tree.gui_location_y += Mouse.y - A_tree.mouse_temp_y
                        A_tree.mouse_temp_x = Mouse.x
                        A_tree.mouse_temp_y = Mouse.y
                if hovering_close_button:
                    A_tree.open = False
                    waiting = False
                    return False
        if menu == 10:#存檔/讀檔
            pygame.display.set_caption("Finding The Light - Saves")
            draw_img(screen, save_ui_img, 30, 50)
            draw_img(screen, button_close_img, 900, 80)
            selected_save_img.set_colorkey(WHITE)
            draw_img(screen, selected_save_img, 100, -10 + Save_load.selected * 100)
            re = inv_preload(Save_load.selected)
            try:
                if re == False:
                    draw_color_text(screen, "玩家名稱:" + str(Save_load.player_name), 20, 570, 120, WHITE)
                    draw_color_text(screen, str(Save_load.time_preview), 20, 630, 150, WHITE)
                    draw_color_text(screen, "角色血量: " + str(Save_load.health_preview), 20, 550, 180, WHITE)
                    draw_color_text(screen, "所在區域: " + str(Save_load.area_preview), 20, 550, 210, WHITE)
                    draw_color_text(screen, "刺客等級: Lv." + str(Save_load.assassin_level_preview) + " [ " + str(Save_load.assassin_xp_preview) + "/" + str(Save_load.assassin_level_preview * 10 + 10) + " ]", 20, 600, 240, WHITE)
                    draw_color_text(screen, "弓箭手等級: Lv." + str(Save_load.archer_level_preview) + " [ " + str(Save_load.archer_xp_preview) + "/" + str(Save_load.archer_level_preview * 10 + 10) + " ]", 20, 600, 270, WHITE)
                    draw_color_text(screen, "法師等級: Lv." + str(Save_load.mage_level_preview) + " [ " + str(Save_load.mage_xp_preview) + "/" + str(Save_load.mage_level_preview * 10 + 10) + " ]", 20, 600, 300, WHITE)
                else:
                    draw_color_text(screen, "找不到存檔!", 30, 720, 250, WHITE)
            except:
                None
            if Save_load.warning == 1:
                draw_img(screen, load_warning_img, 250, 200)
            if Save_load.warning == 2:
                draw_img(screen, save_warning_img, 250, 200)
            pygame.display.update()
            hovering_save1_button = is_hovering(30, 430, 50, 150, mouse_x, mouse_y)
            hovering_save2_button = is_hovering(30, 430, 150, 250, mouse_x, mouse_y)
            hovering_save3_button = is_hovering(30, 430, 250, 350, mouse_x, mouse_y)
            hovering_save4_button = is_hovering(30, 430, 350, 450, mouse_x, mouse_y)
            hovering_save5_button = is_hovering(30, 430, 450, 550, mouse_x, mouse_y)
            hovering_check_inv = is_hovering(450, 520, 440, 510, mouse_x, mouse_y)
            hovering_load_button = is_hovering(540, 690, 440, 510, mouse_x, mouse_y)
            hovering_save_button = is_hovering(800, 950, 440, 510, mouse_x, mouse_y)
            hovering_confirm_button = is_hovering(325, 445, 400, 460, mouse_x, mouse_y)
            hovering_cancel_button = is_hovering(550, 670, 400, 460, mouse_x, mouse_y)
            hovering_close_button = is_hovering(900, 970, 80, 150, mouse_x, mouse_y)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Save_load.warning = 0
                        waiting = False
                        return False
                press_button = pygame.mouse.get_pressed()
                if (press_button[0]):
                    if Save_load.warning == 0:
                        if hovering_save1_button and Save_load.selected != 1:
                            Save_load.selected = 1
                        if hovering_save2_button and Save_load.selected != 2:
                            Save_load.selected = 2
                        if hovering_save3_button and Save_load.selected != 3:
                            Save_load.selected = 3
                        if hovering_save4_button and Save_load.selected != 4:
                            Save_load.selected = 4
                        if hovering_save5_button and Save_load.selected != 5:
                            Save_load.selected = 5
                        if hovering_check_inv:
                            re = inv_preload(Save_load.selected)
                            if re == False:
                                menu = 5
                                Inv.open = True
                                Inv.type = "load"
                        if hovering_load_button and re == False:
                            Save_load.warning = 1
                        if hovering_save_button:
                            if Areas.safe:
                                Save_load.warning = 2
                            if Areas.safe == False:
                                print("只能在城鎮內存檔")
                    if hovering_confirm_button:
                        if Save_load.warning == 1:
                            try:
                                Save_load.warning = 0
                                load(Save_load.selected)
                                title("讀檔成功!", "檔案名稱: Save" + str(Save_load.selected))
                                for item, count in Inv.invload.items():
                                    for i in range(len(Inv.inventory)):
                                        if Inv.inventory[i]["name"] == item: Inv.inventory[i]["count"] = count
                                if Inv.equip["sword"] and player.weapon == 1: Inv.equip["hotbar"][0] = Inv.equip["sword"]
                                elif Inv.equip["bow"] and player.weapon == 2: Inv.equip["hotbar"][0] = Inv.equip["bow"]
                                elif Inv.equip["wand"] and player.weapon == 3: Inv.equip["hotbar"][0] = Inv.equip["wand"]
                                else: Inv.equip["hotbar"][0] = ""
                                All_mobs.kill = True
                                waiting = False
                                return False
                            except:
                                None
                        if Save_load.warning == 2:
                            Save_load.warning = 0
                            save(Save_load.selected)
                            title("已存檔!", "檔案名稱: Save" + str(Save_load.selected))
                    if hovering_cancel_button:
                        Save_load.warning = 0
                    if hovering_close_button:
                        waiting = False
                        return False
                if (press_button[1]):
                    print(mouse_x, mouse_y)
        if menu == 11:#傳送門
            pygame.display.set_caption("Finding The Light - Portal")
            def portal_tp(info):
                for location_name, location_coord in info.items(): 
                    teleport(location_coord)
                    new_message("已傳送至" + location_name)
                    Areas.changed = True
            def portal_unlock(location):
                Portal.unlock[location] = True
                new_message("已解鎖" + location + "傳送門")
            portal_areas = {-2:{"曙光之城":-2900}, 11:{"一號路口":10000}, 17:{"天堂":16100}}
            draw_img(screen, portal_img, 30, 50)
            draw_img(screen, button_close_img, 900, 80)
            tp_info = {0:0}
            y_move = 0
            for location, unlock_stat in Portal.unlock.items():
                if button(35, 160 + y_move, "square", {"width":150, "height":50, "outlineWidth":5, "color":AGRAY, "outlineColor":BLACK}, location if unlock_stat else "???", 20, (75, 10)):
                    for area, location_info in portal_areas.items():
                        if list(location_info)[0] == location:
                            tp_info = location_info
                y_move += 45
            if Portal.unlock[list(portal_areas.get(Areas.area, False))[0]] == False: portal_unlock(list(portal_areas.get(Areas.area, False))[0])
            hovering_close_button = is_hovering(900, 970, 80, 150, mouse_x, mouse_y)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Portal.open = False
                        waiting = False
                        return False
                press_button = pygame.mouse.get_pressed()
                if (press_button[0]):
                    if Portal.unlock.get(list(tp_info)[0], False):
                        portal_tp(tp_info)
                        Portal.open = False
                        waiting = False
                        return False
                    if hovering_close_button:
                        Portal.open = False
                        waiting = False
                        return False
                if (press_button[1]):
                    print(mouse_x, mouse_y)
        if menu == 12:#深淵房間選擇
            Inv.info_loc_x = Mouse.x if mouse_x + 500 < WIDTH else Mouse.x - 500
            Inv.info_loc_y = Mouse.x if mouse_y - 500 > 0 else Mouse.y - 100
            if Mouse.y + 300 >= HEIGHT: Inv.info_loc_y = Mouse.y - 300
            draw_img(screen, depth_room_menu_img, 30, 50)
            if Depth.roll_room_type:
                current_room = {}
                room_types = {"戰鬥":40, "事件":40, "黑市":10, "挑戰":10}
                chosen_types = random.sample(list(room_types.keys()), 3)
                if chosen_types == []:
                    chosen_types = ["戰鬥"]
                #隨機抽取房間
                for i, rtype in enumerate(chosen_types):
                    event_name = rtype + ":" + random.choice(Depth.room_type[Depth.floor][rtype])
                    current_room[event_name] = i
                Depth.roll_room_type = False
            if Depth.room == 1 and Depth.floor == 1:
                draw_color_text(screen, "請選擇潛入城堡的方法", 40, 490, 80, WHITE)
                current_room = {"廢棄下水道":0, "假扮商隊":1, "攻擊守衛":2}
            elif Depth.room == 9:
                draw_color_text(screen, "魔王挑戰", 40, 490, 50, WHITE)
                current_room = {"魔王" + str(Depth.floor):1}
            else:
                draw_color_text(screen, "請選擇下個房間", 40, 490, 50, WHITE)
            hovering_room_info = ["", False]
            for room_type, idx in current_room.items():
                if button(100 + idx * 390, 250, "img", {"outlineWidth":5, "outlineColor":BLACK}, room_type if ":" not in room_type else room_type[3:], 25, (45, 90), depth_room_icon[room_type if ":" not in room_type else room_type[:2]]):
                    hovering_room_info = [room_type if ":" not in room_type else room_type[3:], True]
            #滑鼠懸停顯示房間資訊
            if hovering_room_info[1]:
                room_info_indicator(hovering_room_info[0])
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Depth.menu_open = False
                    pygame.quit()
                    return True
                press_button = pygame.mouse.get_pressed()
                if (press_button[0]):
                    if hovering_room_info[1]:
                        if hovering_room_info[0] in room_types:
                            Depth.current_room_name = random.choices(Depth.room_type[Depth.floor][hovering_room_info[0]])[0]
                        else:
                            Depth.current_room_name = hovering_room_info[0]
                        teleport(-7990)
                        Depth.get_room_reward = False
                        Depth.room += 1
                        Depth.spawn = True
                        Depth.menu_open = False
                        waiting = False
                        return False
                if (press_button[1]):
                    print(mouse_x, mouse_y)
        if menu == 13:#深淵祝福介面
            if Depth.menu_type == 0:
                pygame.draw.rect(screen, AGRAY, (30, 50, 800, 500))
                outline_text("祝福列表", 40, 770 / 2, 70, WHITE)
                for i in range(5):
                    pygame.draw.line(screen, BLACK, (35, 188 + 115 * i), (790, 188 + 115 * i), 4)
                    pygame.draw.line(screen, BLACK, (35, 282 + 115 * i), (790, 282 + 115 * i), 4)
                for i in range(9):
                    pygame.draw.line(screen, BLACK, (35 + i * 94, 188), (35 + i * 94, 532), 4)
                draw_img(screen, button_close_img, 740, 80)
            def roll_blessing_quality(type):
                r = random.randint(1, 100)
                if type == 1:
                    if r <= 40:
                        return 1
                    if 40 < r <= 70:
                        return 2
                    if 70 < r <= 90:
                        return 3
                    if 90 < r <= 100:
                        return 4
                    else: return 1
                if type == 2:
                    if r <= 50:
                        return 3
                    if 50 < r < 80:
                        return 4
                    if 80 < r < 100:
                        return 5
                    else: return 3
            if Depth.blessing_quality_roll > 0:
                random.shuffle(Depth.blessings_order)
                blessing1_tier = roll_blessing_quality(Depth.blessing_quality_roll)
                blessing2_tier = roll_blessing_quality(Depth.blessing_quality_roll)
                blessing3_tier = roll_blessing_quality(Depth.blessing_quality_roll)
                if len(Depth.blessings_order) < 2:
                    blessing2_tier = 0
                    Depth.blessing_reading2 = 0
                if len(Depth.blessings_order) < 3:
                    blessing3_tier = 0
                    Depth.blessing_reading3 = 0
                Depth.blessing_quality_roll = 0
            if Depth.menu_type == 0:
                idx = 0
                for blessing in Depth.blessings:
                    if blessing["rarity"] > 0:
                        draw_img(screen, blessing["img"][blessing["rarity"] - 1], 37 + (idx % 8 * 94), 191 + (idx // 8 * 115))
                        draw_color_text(screen, str(blessing["rarity"]), 15, 82 + (idx % 8 * 94), 282 + (idx // 8 * 115), WHITE)
                        idx += 1
            hovering_blessing_1 = False
            hovering_blessing_2 = False
            hovering_blessing_3 = False
            if Depth.menu_type == 1:
                draw_img(screen, depth_blessing_menu_img, 30, 50)
                if len(Depth.blessings_order) == 0:
                    Depth.menu_type = 0
                    Depth.blessing_menu = False
                    waiting = False
                    return False
                for blessing in Depth.blessings:
                    if blessing["name"] == Depth.blessings_order[0]: hovering_blessing_1 = button(255, 190, "img", {"outlineWidth":4, "outlineColor":BLACK}, "", 0, (0, 0), blessing["img"][blessing1_tier - 1])
                    if len(Depth.blessings_order) >= 2 and blessing["name"] == Depth.blessings_order[1]: hovering_blessing_2 = button(455, 190, "img", {"outlineWidth":4, "outlineColor":BLACK}, "", 0, (0, 0), blessing["img"][blessing2_tier - 1])
                    if len(Depth.blessings_order) >= 3 and blessing["name"] == Depth.blessings_order[2]: hovering_blessing_3 = button(655, 190, "img", {"outlineWidth":4, "outlineColor":BLACK}, "", 0, (0, 0), blessing["img"][blessing3_tier - 1])
                for blessing in Depth.blessings:
                    if blessing["name"] == Depth.blessings_order[0]:
                        if hovering_blessing_1: blessing_indicator(blessing["name"], blessing1_tier)
                    if len(Depth.blessings_order) >= 2 and blessing["name"] == Depth.blessings_order[1]:
                        if hovering_blessing_2: blessing_indicator(blessing["name"], blessing2_tier)
                    if len(Depth.blessings_order) >= 3 and blessing["name"] == Depth.blessings_order[2]:
                        if hovering_blessing_3: blessing_indicator(blessing["name"], blessing3_tier)
            if Depth.menu_type == 2:
                draw_img(screen, depth_blessing_menu_img, 30, 50)
                if Depth.blessing_upgrade_level > 0:
                    upgradable_blessings = [blessing for blessing in Depth.blessings if 0 < blessing["rarity"] < 5][:3]
                    upgrade_level = Depth.blessing_upgrade_level - 1
                    Depth.blessing_upgrade_level = 0
                if len(upgradable_blessings) == 0:
                    Depth.menu_type = 0
                    Depth.blessing_menu = False
                    waiting = False
                    return False
                if len(upgradable_blessings) > 0:
                    hovering_blessing_1 = button(255, 190, "img", {"outlineWidth":4, "outlineColor":BLACK}, "", 0, (0, 0), upgradable_blessings[0]["img"][min(upgradable_blessings[0]["rarity"] + upgrade_level, 4)])
                if len(upgradable_blessings) > 1:
                    hovering_blessing_2 = button(455, 190, "img", {"outlineWidth":4, "outlineColor":BLACK}, "", 0, (0, 0), upgradable_blessings[1]["img"][min(upgradable_blessings[1]["rarity"] + upgrade_level, 4)])
                if len(upgradable_blessings) > 2:
                    hovering_blessing_3 = button(655, 190, "img", {"outlineWidth":4, "outlineColor":BLACK}, "", 0, (0, 0), upgradable_blessings[2]["img"][min(upgradable_blessings[2]["rarity"] + upgrade_level, 4)])
                if hovering_blessing_1: blessing_indicator(upgradable_blessings[0]["name"], upgradable_blessings[0]["rarity"] + upgrade_level + 1)
                if hovering_blessing_2: blessing_indicator(upgradable_blessings[1]["name"], upgradable_blessings[1]["rarity"] + upgrade_level + 1)
                if hovering_blessing_3: blessing_indicator(upgradable_blessings[2]["name"], upgradable_blessings[2]["rarity"] + upgrade_level + 1)
            Inv.info_loc_x = Mouse.x if mouse_x + 500 < WIDTH else Mouse.x - 500
            Inv.info_loc_y = Mouse.x if mouse_y - 500 > 0 else Mouse.y - 100
            if Mouse.y + 300 >= HEIGHT: Inv.info_loc_y = Mouse.y - 300
            pygame.display.update()
            hovering_close_button = is_hovering(740, 810, 80, 150, mouse_x, mouse_y)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Depth.blessing_menu = False
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYDOWN and Depth.menu_type == 0:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_b:
                        Depth.blessing_menu = False
                        waiting = False
                        return False
                press_button = pygame.mouse.get_pressed()
                if (press_button[0]):
                    for i, hovering in enumerate([hovering_blessing_1, hovering_blessing_2, hovering_blessing_3]):
                        if hovering and Depth.menu_type == 1 and len(Depth.blessings_order) > i:
                            for blessing in Depth.blessings:
                                if blessing["name"] == Depth.blessings_order[i]:
                                    blessing["rarity"] = [blessing1_tier, blessing2_tier, blessing3_tier][i]
                                    Depth.blessings_order.pop(i)
                                    Depth.blessing_menu = False
                                    Depth.menu_type = 0
                                    waiting = False
                                    return False
                        if hovering and Depth.menu_type == 2:
                            upgrade_blessing(upgradable_blessings[i]["name"], upgrade_level)
                            upgradable_blessings = []
                            Depth.blessing_menu = False
                            Depth.menu_type = 0
                            waiting = False
                            return False
                    if hovering_close_button and Depth.menu_type == 0:
                        Depth.blessing_menu = False
                        waiting = False
                        return False
                if (press_button[1]):
                    print(mouse_x, mouse_y)
        if menu == 14:#交易
            #顯示介面
            pygame.draw.rect(screen, AGRAY, (30, 50, 800, 500))
            if Trade.show_info == False:
                pygame.draw.rect(screen, BLACK, (30, 150, 800, 400), 5)
                outline_text("交易", 40, 415, 75, WHITE)
                for i in range(4):
                    pygame.draw.line(screen, BLACK, (30, 230 + i * 100), (670, 230 + i * 100), 3)
                    pygame.draw.line(screen, BLACK, (30, 250 + i * 100), (670, 250 + i * 100), 3)
                for i in range(8):
                    pygame.draw.line(screen, BLACK, (110 + i * 80, 150), (110 + i * 80, 545), 3)
                #顯示交易選項
                shop = Trade.shops[Trade.items]
                for items in shop:
                    item_img = pygame.transform.scale(search_item(items["name"])["img"], (70, 70))
                    item_index = shop.index(items)
                    draw_img(screen, item_img, 36 + (item_index * 80 % 640), 156 + 100 * (item_index // 8))
                    draw_color_text(screen, str(items["count"]), 15, 73 + (item_index * 80 % 640), 230 + 100 * (item_index // 8), WHITE)
                    if is_hovering(36 + (item_index * 80 % 640), 116 + (item_index * 80 % 640), 156 + 100 * (item_index // 8), 256 + 100 * (item_index // 8), mouse_x, mouse_y):
                        if Trade.click:
                            Trade.sidebar = items
                            sidebar_item_index = item_index
                            current_value = 1
                            knob_x = 700
                            knob_dragging = False
            #檢查玩家能購買數量
            def check_player_can_buy(cost):
                player_can_buy = float("inf")
                for cost_items, cost_count in cost.items():
                    if search_item(cost_items)["count"] // cost_count < player_can_buy:
                        player_can_buy = search_item(cost_items)["count"] // cost_count
                return player_can_buy
            #商品資訊欄
            draw_img(screen, button_close_img, 740, 70)
            if Trade.sidebar != {} and Trade.show_info == False:
                pygame.draw.rect(screen, WHITE, (30 + (sidebar_item_index * 80 % 640), 150 + 100 * (sidebar_item_index // 8), 80, 80), 3)
                draw_img(screen, pygame.transform.scale(search_item(Trade.sidebar["name"])["img"], (50, 50)), 725, 170)
                pygame.draw.rect(screen, BLACK, (725, 170, 50, 50), 3)
                draw_color_text(screen, Trade.sidebar["name"], 25, 750, 230, search_item(Trade.sidebar["name"])["rarity"])
                draw_color_text(screen, "數量: " + str(Trade.sidebar["count"]), 20, 750, 260, WHITE)
                draw_color_text(screen, "所需物品:", 20, 750, 300, WHITE)
                #顯示所需物品
                y_move = 0
                for cost_items, cost_count in Trade.sidebar["cost"].items():
                    if y_move < 60:
                        draw_img(screen, pygame.transform.scale(search_item(cost_items)["img"], (30, 30)), 675, 330 + y_move)
                        draw_color_text(screen, cost_items + " x" + str(cost_count), 15, 765, 335 + y_move, search_item(cost_items)["rarity"])
                        y_move += 30
                if len(Trade.sidebar["cost"]) > 2: draw_color_text(screen, "...", 25, 750, 310 + y_move, WHITE)
                is_hovering(670, 820, 150, 400, mouse_x, mouse_y, "?")
                #數量選擇器(滑動條)
                bar_x, bar_y = 690, 410 + y_move
                draw_color_text(screen, "限購: " + (str(Trade.sidebar["limit"]) if Trade.sidebar["total_limit"] != -1 else "無"), 20, 750, 350 + y_move, WHITE)
                player_can_buy = check_player_can_buy(Trade.sidebar["cost"])
                #顯示購買按鈕
                if player_can_buy > 0 and Trade.sidebar["limit"]:
                    pygame.draw.rect(screen, GRAY, (bar_x, bar_y, 120, 10))
                    pygame.draw.rect(screen, BLACK, (bar_x, bar_y, 120, 10), 2)
                    pygame.draw.circle(screen, DGRAY, (knob_x, bar_y + 10 // 2), 10)
                    pygame.draw.circle(screen, BLACK, (knob_x, bar_y + 10 // 2), 10, 2)
                    draw_color_text(screen, "購買次數: " + str(current_value if player_can_buy > 0 else 0), 15, 750, 380 + y_move, WHITE)
                    pygame.draw.rect(screen, DGRAY, (690, 430 + y_move, 120, 40))
                    pygame.draw.rect(screen, BLACK, (690, 430 + y_move, 120, 40), 4)
                    draw_color_text(screen, "購買", 20, 750, 435 + y_move, WHITE)
                    if is_hovering(680, 810, 430 + y_move, 470 + y_move, mouse_x, mouse_y):
                        pygame.draw.rect(screen, WHITE, (690, 430 + y_move, 120, 40), 2)
                        if Trade.click:
                            player.gain_item(search_item(Trade.sidebar["name"])["name"], Trade.sidebar["count"] * current_value)
                            for cost_item, cost_count in Trade.sidebar["cost"].items():
                                total_cost = cost_count * current_value
                                player.gain_item(search_item(cost_item)["name"], -total_cost)
                            if Trade.sidebar["limit"] != -1 and Trade.sidebar["limit"] > 0: Trade.shops[Trade.items][sidebar_item_index]["limit"] -= 1
                            current_value = 1
                            knob_x = 700
                            knob_dragging = False
                elif player_can_buy == 0 and (Trade.sidebar["limit"] == -1 or Trade.sidebar["limit"]): outline_text("材料不足", 20, 710, 415 + y_move, RED)
                elif Trade.sidebar["limit"] == 0: outline_text("已達購買上限", 20, 690, 415 + y_move, RED)
                else: outline_text("無法購買", 20, 710, 415 + y_move, RED)
            if Trade.sidebar != {} and Trade.show_info:
                pygame.draw.rect(screen, BLACK, (30, 50, 800, 500), 5)
                pygame.draw.rect(screen, BLACK, (395, 100, 90, 120), 3)
                pygame.draw.line(screen, BLACK, (395, 190), (485, 190), 3)
                for i in range((len(Trade.sidebar["cost"]) // 2) + (len(Trade.sidebar["cost"]) % 2)):
                    if len(Trade.sidebar["cost"]) % 2 == 1:
                        if i == 0:
                            pygame.draw.rect(screen, BLACK, (395, 400, 90, 120), 3)
                            pygame.draw.line(screen, BLACK, (395, 490), (485, 490), 3)
                        else:
                            pygame.draw.rect(screen, BLACK, (395 + 50 + i * 50, 400, 90, 120), 3)
                            pygame.draw.rect(screen, BLACK, (395 - 50 - i * 50, 400, 90, 120), 3)
                            pygame.draw.line(screen, BLACK, (395 + 50 + i * 50, 490), (395 + 50 + i * 50 + 90, 490), 3)
                            pygame.draw.line(screen, BLACK, (395 - 50 - i * 50, 490), (395 - 50 - i * 50 + 90, 490), 3)
                    else:
                        pygame.draw.rect(screen, BLACK, (395 - 50 - i * 50, 400, 90, 120), 3)
                        pygame.draw.rect(screen, BLACK, (395 + 50 + i * 50, 400, 90, 120), 3)
                draw_img(screen, trade_arrow_img, 415, 250)
                draw_img(screen, pygame.transform.scale(search_item(Trade.sidebar["name"])["img"], (84, 84)), 398, 103)
                draw_color_text(screen, str(Trade.sidebar["count"]), 20, 438, 190, WHITE)
                x_location = 398 - (len(Trade.sidebar["cost"]) // 2) * 100 if len(Trade.sidebar["cost"]) % 2 == 1 else 398 - (len(Trade.sidebar["cost"]) // 2) * 100 + 50
                for items, count in Trade.sidebar["cost"].items():
                    draw_color_text(screen, str(count), 20, x_location + 45, 488, WHITE)
                    item_img = pygame.transform.scale(search_item(items)["img"], (84, 84))
                    draw_img(screen, item_img, x_location, 403)
                    x_location += 100
                if is_hovering(398, 398 + 90, 103, 103 + 90, mouse_x, mouse_y): inv_item_text(Trade.sidebar["name"])
                x_location = 398 - (len(Trade.sidebar["cost"]) // 2) * 100 if len(Trade.sidebar["cost"]) % 2 == 1 else 398 - (len(Trade.sidebar["cost"]) // 2) * 100 + 50
                for items in Trade.sidebar["cost"]:
                    if is_hovering(x_location, x_location + 90, 400, 400 + 90, mouse_x, mouse_y): inv_item_text(items)
                    x_location += 100
            Trade.click = False
            Inv.info_loc_x = mouse_x if mouse_x + 500 < WIDTH else mouse_x - 500
            Inv.info_loc_y = mouse_y if mouse_y - 500 > 0 else mouse_y - 100
            if mouse_y + 300 >= HEIGHT: Inv.info_loc_y = mouse_y - 300
            for items in shop:
                item_index = shop.index(items)
                if is_hovering(36 + (item_index * 80 % 640), 116 + (item_index * 80 % 640), 156 + 100 * (item_index // 8), 256 + 100 * (item_index // 8), mouse_x, mouse_y): inv_item_text(items["name"])
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Trade.show_info = False
                        Trade.open = False
                        Trade.items = []
                        waiting = False
                        return False
                    if event.key == pygame.K_u:
                        Trade.show_info = not Trade.show_info
                #控制旋鈕
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    Trade.click = True
                    if event.button == 1:  # 左鍵點擊
                        if (knob_x - 10) <= mouse_x <= (knob_x + 10) and (bar_y - 10) <= mouse_y <= (bar_y + 10):
                            knob_dragging = True
                        if is_hovering(740, 810, 70, 140, mouse_x, mouse_y) and Trade.show_info == False:
                            Trade.open = False
                            Trade.items = []
                            waiting = False
                            return False
                        elif is_hovering(740, 810, 70, 140, mouse_x, mouse_y) and Trade.show_info: Trade.show_info = False
                        elif is_hovering(670, 820, 150, 400, mouse_x, mouse_y) and Trade.show_info == False: Trade.show_info = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # 左鍵釋放
                        knob_dragging = False
                elif event.type == pygame.MOUSEMOTION:
                    if knob_dragging:
                        knob_x = max(bar_x, min(mouse_x, bar_x + 120))
                        #選擇購買數量
                        current_value = round((knob_x - bar_x) / 120 * (min(player_can_buy, (float("inf") if Trade.sidebar["limit"] == -1 else Trade.sidebar["limit"])) - 1)) + 1
#玩家
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.name = player_name
        self.image = player_right_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = GROUND - 50
        self.health = 100
        self.health_limit = 100
        self.speed = 10
        self.jump_time = 0
        self.jump_height = 0
        self.fall_speed = 1
        self.velocity = 0
        self.weapon = 1
        self.facing = 1
        self.holding = {"wings":0, "jump_wings":0, "sword":0, "rise_sword":0, "air_strike":0, "bow":0, "fire_bow":0, "wand":0, "food":0}
        self.action = "normal"
        self.cooldowns = {}
        self.skill_cooldowns = {}
        self.effects = []
        self.attacks = []
        self.attack_code = 0
        self.flying = False
        self.blight = 0
        self.crimson_harvest = 0
        self.eating_food = {"img":"", "rotate":0}
        self.sword_img = ""
    
    def update(self):
        #受到傷害 // 防禦力計算公式 : 最終傷害 = 原始傷害 / (1 + 防禦力 * 0.01 * (1 + 防禦力百分比))
        Damage_to_player.damage = Damage_to_player.damage / (1 + Stats.total["防禦力"] * 0.01 * (1 + Stats.total["防禦力%"] / 100))
        self.health -= Damage_to_player.damage
        Damage_to_player.damage = 0
        #控制效果持續時間
        for existing_effect in self.effects:
            existing_effect["tick"] = max(0, existing_effect["tick"] - 1)
            if existing_effect["tick"] <= 0:
                if existing_effect["name"] == "腥紅收割": player.crimson_harvest = 0
                self.effects.remove(existing_effect)
        #攻擊動畫
        for hold in self.holding:
            self.holding[hold] = max(0, self.holding[hold] - 1)
        if self.holding["jump_wings"] >= 7: draw_img(screen, player_wings_2_img, self.rect.x - 30, self.rect.y + 25)
        if 0 < self.holding["jump_wings"] < 7: draw_img(screen, player_wings_1_img, self.rect.x - 33, self.rect.y)
        if self.holding["wings"] >= 15: draw_img(screen, player_wings_2_img, self.rect.x - 30, self.rect.y + 25)
        if 0 < self.holding["wings"] < 15: draw_img(screen, player_wings_1_img, self.rect.x - 33, self.rect.y)
        if self.holding["wings"] == 0 and player.flying: self.holding["wings"] = 30
        if self.holding["air_strike"] > 10: self.holding["sword"] = self.holding["air_strike"] - 10
        #進食
        if self.holding["food"]:
            player.action = "rise_hand"
            eat_progress = self.holding["food"] / 60
            food_length = (1 - eat_progress) // 0.33 * (self.eating_food["img"].get_width() / 3)
            if player.facing == 1:  # 面向右方
                visible_part = self.eating_food["img"].subsurface((food_length, 0, self.eating_food["img"].get_width() - food_length, self.eating_food["img"].get_height()))
            else:  # 面向左方
                visible_part = self.eating_food["img"].subsurface((food_length, 0, self.eating_food["img"].get_width() - food_length, self.eating_food["img"].get_height()))
                visible_part = pygame.transform.flip(visible_part, True, False)  # 水平翻轉
            if player.facing == 1: draw_img(screen, visible_part, self.rect.centerx + 28, self.rect.top + 20)
            else: draw_img(screen, visible_part, self.rect.centerx - 78 + food_length, self.rect.top + 20)
            if self.holding["food"] == 1: self.action = "normal"
        #揮劍圖片
        if Inv.equip["hotbar"][0] != "":
            sword_info = search_item(Inv.equip["hotbar"][0])
            self.sword_img = sword_info["img"].copy()
            self.sword_img.set_colorkey(sword_info["rarity"])
        else:
            self.sword_img = item_iron_sword_img.copy()
            self.sword_img.set_colorkey(RARE)
        self.sword_img = self.sword_img.subsurface(self.sword_img.get_bounding_rect()).copy()
        self.sword_img = pygame.transform.scale(self.sword_img, (90, 90))
        #調整方向
        visual_sword = self.sword_img
        if self.action == "normal": self.image = pygame.transform.flip(player_right_img, self.facing == -1, False)
        if self.action == "rise_hand": self.image = pygame.transform.flip(player_rise_hand_right_img, self.facing == -1, False)
        #劍
        if self.holding["rise_sword"] and player.weapon == 1: draw_img(screen, pygame.transform.flip(pygame.transform.rotate(visual_sword, 45), self.facing == 1, False), self.rect.centerx - 20 - int(self.facing == -1) * 90, self.rect.y - 35)
        if self.holding["sword"] >= 10 and player.weapon == 1: draw_img(screen, pygame.transform.flip(pygame.transform.rotate(visual_sword, 60), self.facing == 1, False), self.rect.centerx - 40 - int(self.facing == -1) * 50, self.rect.y + 10)
        if 0 < self.holding["sword"] <= 9 and player.weapon == 1: draw_img(screen, pygame.transform.flip(pygame.transform.rotate(visual_sword, 105), self.facing == 1, False), self.rect.centerx - int(self.facing == -1) * 100, self.rect.y + 30)
        if 9 > self.holding["sword"] > 0 and player.weapon == 1: draw_img(screen, pygame.transform.flip(slash_right_1_img, self.facing == -1, False), self.rect.centerx + 50 - int(self.facing == -1) * 150, self.rect.y + 35)
        if 0 < self.holding["air_strike"] < 10:
            draw_img(screen, pygame.transform.flip(pygame.transform.rotate(visual_sword, 120), self.facing == 1, False), self.rect.centerx + 10 - int(self.facing == -1) * 100, self.rect.y + 35)
            draw_img(screen, pygame.transform.flip(slash_right_2_img, self.facing == -1, False), self.rect.centerx + 20 - int(self.facing == -1) * 150, self.rect.y - 35)
        if Player.cooldowns.get("刀舞", False):
            draw_img(screen, slash_blade_dance_right_img, self.rect.centerx - 80 + 50, self.rect.y + 30)
            draw_img(screen, slash_blade_dance_left_img, self.rect.centerx - 80 - 50, self.rect.y + 30)
        #弓
        if (20 >= self.holding["bow"] >= 10 or 30 >= self.holding["fire_bow"] >= 15) and player.weapon == 2: draw_img(screen, pygame.transform.flip(bow_right_1_img, self.facing == -1, False), self.rect.centerx + 5 - int(self.facing == -1) * 100, self.rect.y + 55)
        if (10 > self.holding["bow"] >= 2 or 15 > self.holding["fire_bow"] >= 2) and player.weapon == 2: draw_img(screen, pygame.transform.flip(bow_right_2_img, self.facing == -1, False), self.rect.centerx + 5 - int(self.facing == -1) * 100, self.rect.y + 55)
        #法杖
        if self.holding["wand"] >= 10 and player.weapon == 3 or Mage.ultimate: draw_img(screen, pygame.transform.flip(wand_right_1_img, self.facing == -1, False), self.rect.centerx + 10 - int(self.facing == -1) * 110, self.rect.y + 40)
        if 1 <= self.holding["wand"] <= 9 and player.weapon == 3: draw_img(screen, pygame.transform.flip(wand_right_2_img, self.facing == -1, False), self.rect.centerx + 20 - int(self.facing == -1) * 120, self.rect.y + 40)
        #施放技能
        #破空突擊
        if self.holding["rise_sword"]: player.attack(self.rect.centerx + (70 * self.facing), self.rect.y + 200, 50, Stats.total["攻擊力"] * (1 + Stats.total["攻擊力%"] / 100) * 3 * ((100 + Stats.charm["破空突擊傷害%"]) / 100), 0, self.attack_code, "破空突擊", 2, [60, 20, player.facing], [None], [0])
        #拉弓結束
        if self.holding["bow"] == 1: shoot_arrow(self.rect.centerx + 60, self.rect.centery + 40, self.facing, "normal")
        if self.holding["fire_bow"] == 1: shoot_arrow(self.rect.centerx + 60, self.rect.centery + 40, self.facing, "fire")
        Player_location.x = self.rect.x
        Player_location.y = self.rect.y
        #移動速度
        self.speed = round((10) * (1 + Stats.total["移動速度"] / 100))
        #生命值
        self.health_limit = round((Stats.total["生命上限"]) * (1 + (Stats.total["生命上限%"] / 100)))
        key_pressed = pygame.key.get_pressed()
        #移動
        self.move_distant = max(self.speed, 0)
        if key_pressed[pygame.K_d] and Player_location.disable_move == False and Player_location.dash_distance == 0:
            self.facing = 1
            if Player_location.player_move: player.rect.x += self.move_distant
            else: All_mobs.coord_x -= self.move_distant
            Player_location.coord_x += self.move_distant
            if player.rect.right + self.move_distant > WIDTH - 1:
                player.rect.right = WIDTH - 1
                Player_location.coord_x = Areas.area * 1000 - 1
        if key_pressed[pygame.K_a] and Player_location.disable_move == False and Player_location.dash_distance == 0:
            self.facing = -1
            if Player_location.player_move: player.rect.x -= self.move_distant
            else: All_mobs.coord_x += self.move_distant
            Player_location.coord_x -= self.move_distant
            if player.rect.left - self.move_distant < 0:
                player.rect.left = 0
                Player_location.coord_x = (Areas.area - 1) * 1000
        if self.rect.right > WIDTH: self.rect.right = WIDTH
        if self.rect.left < 0: self.rect.left = 0
        #11區移動
        if Area11.x_velocity > 1:
            if Player_location.player_move:
                player.rect.x += 10
            else: All_mobs.coord_x -= 10
            Player_location.coord_x += 10
            player.rect.x += 10
            Area11.x_velocity -= 10
        if Area11.y_velocity > 1:
            Player_location.anti_gravity = True
            player.rect.y -= 20
            Area11.y_velocity -= 20
        if Area11.y_velocity == 20:
            Player_location.disable_move = False
            Player_location.anti_gravity = False
            teleport(11500)
            Area11.y_velocity = 0
        if Area11.y_velocity == 0: Player_location.disable_move = False
        #跳躍
        if key_pressed[pygame.K_SPACE] and Player_location.disable_jump == False and player.jump_time > 0:
            if player.rect.y < GROUND - 50 and player.jump_height == 0: player.holding["jump_wings"] = 15
            if player.jump_height <= Stats.total["跳躍高度"]:
                player.rect.y -= 20
                player.jump_height += 20
        #重製跳躍次數
        if self.rect.y == GROUND - 50:
            self.jump_time = Stats.total["跳躍次數"]
            Player_location.midair_dash = 1
        #重力加速度
        if self.rect.y < GROUND - 50 and Player_location.anti_gravity == False and not 0 < self.jump_height < 150 and Player_location.dash_distance == 0 or Player_location.disable_ground:
            self.velocity += (GRAVITY * 1 / 20) * self.fall_speed
            self.rect.y += round(self.velocity)
        if self.rect.y >= GROUND - 50 and Player_location.disable_ground == False:
            if self.holding["rise_sword"]:
                Player.cooldowns["破空突擊"] = 60
                self.action = "normal"
                self.fall_speed = 1
                self.holding["rise_sword"] = 0
            self.rect.y = GROUND - 50
            self.velocity = 0
            self.jump_height = 0
        #隱身
        if Player.cooldowns["隱身"] > 1: self.image.set_alpha(128)
        elif Player.cooldowns["隱身"] == 1: self.image.set_alpha(256)
    #生成攻擊
    def attack(self, x, y, radius, damage, element, code, source, duration, kb, effect, effect_duration):
        self.attacks.append([x, y, radius, damage, element, code, source, duration, kb, effect, effect_duration])
    #攻擊反饋
    def attack_feedback(self, skill):
        if skill == "rogue_main_attack" and Assassin.smite and Assassin.ultimate_time > 0:
            Assassin.ultimate_time = max(0, Assassin.ultimate_time - 1)
            if Assassin.ultimate_time == 0: Player.cooldowns["暗影襲擊剩餘時間"] = 0
        elif skill == "rogue_main_attack" and Assassin.ultimate_time == 0 and Assassin.smite:
            Player.cooldowns["rogue_riptide"] = 300
            Assassin.smite = False
        if skill == "破空突擊":
            self.holding["air_strike"] = 15
            self.action = "normal"
            self.holding["rise_sword"] = 0
        if skill == "混沌匕首":
            Assassin.remove_chaos_dagger = True
        if skill == "archer_main_attack" or skill == "苦無": Archer.focus = min(Archer.focus + 1, Archer.focus_limit)
        if skill == "火焰箭矢": Archer.focus = 0
        if skill == "mage_ultimate_target":
            tp_location = Mouse.x - player.rect.x
            teleport(Player_location.coord_x + tp_location)
            self.rect.y = Mouse.y
            Player.cooldowns["mage_water_burst"] = 120 + A_tree.mage["水爆延長"] * 120
            Mage.mana = min(Mage.mana + 30, Mage.mana_limit)
            Mage.ultimate = False
            self.weapon = 1
            Assassin.magic_enchant = 1.2
            self.attack_code = -~ self.attack_code
            water_burst = Water_burst(player.rect.x, Mouse.y + 200, self.attack_code)
            all_sprites.add(water_burst)
            water_bursts.add(water_burst)
    #普通攻擊
    def main_attack(self):
        self.main_attack_element = 0
        if Assassin.smite and Assassin.ultimate_time == 0 and Assassin.magic_enchant == 1: self.main_attack_element = 4
        if Assassin.ultimate_time > 0 and Assassin.magic_enchant == 1: self.main_attack_element = 1
        if Assassin.ultimate_time == 0 and Assassin.magic_enchant > 1: self.main_attack_element = 2
        if Assassin.ultimate_time > 0 and Assassin.magic_enchant > 1: self.main_attack_element = 7
        if player.weapon == 1 and Player.cooldowns["rogue_main"] == 0:
            Player.cooldowns["rogue_main"] = 20
            self.holding["sword"] = 15
            self.attack_code = -~ self.attack_code
            player.attack(
                self.rect.centerx + (70 * self.facing),
                self.rect.y + 70,
                50,
                Stats.total["攻擊力"] * (1 + Stats.total["攻擊力%"] / 100) * Assassin.magic_enchant *
                (1 + int(Assassin.smite) * (1 + A_tree.rogue["重擊強化"])) * (1 + int(Assassin.smite) * Stats.charm["重擊傷害%"] / 100),  # 傷害計算
                self.main_attack_element,
                self.attack_code,
                "rogue_main_attack",
                15,
                [60, 20, player.facing],
                [None],
                [0]
                )
        if player.weapon == 2 and Player.cooldowns["archer_main"] == 0 and self.holding["fire_bow"] == 0:
            Player.cooldowns["archer_main"] = 40
            self.holding["bow"] = 20
        if player.weapon == 3 and Player.cooldowns["mage_main"] == 0:
            Player.cooldowns["mage_main"] = 50
            self.holding["wand"] = 15
            self.attack_code = -~ self.attack_code 
            magic_orb = Magic_orb(self.rect.centerx + self.facing * 50, self.rect.top + 100, Mouse.x, Mouse.y, self.attack_code)
            all_sprites.add(magic_orb)
            magic_orbs.add(magic_orb)
    #技能
    def skill(self, skill):
        #刺客
        if skill == "暗影脈衝" and Assassin.ultimate_time == 0 and A_tree.rogue["暗影脈衝"] > 0 and Player.cooldowns["暗影脈衝"] == 0:
            Player.cooldowns["暗影脈衝"] = 600
            Player.cooldowns["rogue_skill_time"] = 300
            player.gain_effect("移動速度", 50, 300)
            Assassin.smite = True
        if skill == "破空突擊" and A_tree.rogue["破空突擊"] and Player.cooldowns["破空突擊"] == 0 and self.rect.y < GROUND - 120:
            Player.cooldowns["破空突擊"] = 300
            self.jump_height = Stats.total["跳躍高度"]
            self.fall_speed = 1.5
            self.action = "rise_hand"
            self.holding["rise_sword"] = float("inf")
            self.attack_code = -~ self.attack_code
        if skill == "混沌匕首" and A_tree.rogue["混沌匕首"] and Player.cooldowns["混沌匕首"] == 0:
            summon_skill(self.rect.centerx + self.facing * 100, self.rect.centery, self.facing, "chaos_dagger", False, 120)
            Player.cooldowns["混沌匕首"] = 600
        #流放者
        if skill == "幻影分身" and A_tree.rogue["幻影分身"]:
            #放置分身
            if Player.cooldowns["幻影分身"] == 0:
                if Areas.lock_left and current_coord_x < 300 and self.facing == -1:
                    summon_coord = 60
                elif Areas.lock_right and current_coord_x > 700 and self.facing == 1:
                    summon_coord = 940
                else:
                    summon_coord = self.rect.x + self.facing * 300
                summon_skill(summon_coord, self.rect.centery, self.facing, "shadow_clone", False, 180)
                Player.cooldowns["幻影分身持續時間"] = 180
                Player.cooldowns["幻影分身"] = 420
            #傳送至分身
            if Assassin.shadow_clone_location != (False, False) and Player.cooldowns["rogue_riptide"] >= 180:
                Player.cooldowns["rogue_riptide"] -= 180
                Player.cooldowns["隱身"] = 120
                self.attack_code = -~ self.attack_code
                if A_tree.rogue["刀舞"]:
                    Player.cooldowns["刀舞"] = 30
                    player.attack(
                        self.rect.centerx - 20,
                        self.rect.y + 70,
                        140,
                        Stats.total["攻擊力"] * (1 + Stats.total["攻擊力%"] / 100) * 3,
                        7,
                        self.attack_code,
                        "rogue_shadow_clone",
                        15,
                        [60, 20, player.facing],
                        [None],
                        [0]
                        )
                else:
                    Player.cooldowns["rogue_main"] = 20
                    self.holding["sword"] = 15
                    player.attack(
                        self.rect.centerx + (70 * self.facing),
                        self.rect.y + 70,
                        70,
                        Stats.total["攻擊力"] * (1 + Stats.total["攻擊力%"] / 100) * 3,
                        7,
                        self.attack_code,
                        "rogue_shadow_clone",
                        15,
                        [60, 20, player.facing],
                        [None],
                        [0]
                        )
                teleport(Assassin.shadow_clone_location[0] - self.rect.x + Player_location.coord_x)
                player.rect.y = Assassin.shadow_clone_location[1]
                Player.cooldowns["幻影分身持續時間"] = 0
        if skill == "煙霧彈" and A_tree.rogue["煙霧彈"] and Player.cooldowns["煙霧彈"] == 0:
            Player.cooldowns["煙霧彈"] = 420
            summon_skill(self.rect.x + 50 + self.facing * 30, self.rect.y + 70, self.facing, "rogue_smoke_bomb", False, 300)
        #射手
        if skill == "火焰箭矢" and A_tree.archer["火焰箭矢"] > 0 and Player.cooldowns["火焰箭矢"] == 0 and self.holding["bow"] == 0:
            Player.cooldowns["火焰箭矢"] = 600
            self.holding["fire_bow"] = 30
        #法師
        if skill == "隕石" and A_tree.mage["隕石"] > 0 and Mage.mana >= 30 and Mage.mana >= 30 and Player.cooldowns["隕石"] == 0:
            Player.cooldowns["隕石"] = 600
            self.holding["wand"] = 15
            Mage.mana -= 30
            self.attack_code = -~ self.attack_code 
            meteor = Meteor(self.rect.centerx + 150 * self.facing, self.rect.top - 500, self.attack_code)
            all_sprites.add(meteor)
            meteors.add(meteor)
    #使用物品
    def use_item(self, item):
        if item["itemType"] == "consumable" and item["count"] > 0 and Player.skill_cooldowns.get(item["name"], False) == 0:
            player.holding["food"] = 60
            self.eating_food["img"] = item["img"].copy()
            self.eating_food["img"].set_colorkey(item["rarity"])
            self.eating_food["rotate"] = item["eatRotate"]
            self.eating_food["img"] = self.eating_food["img"].subsurface(self.eating_food["img"].get_bounding_rect()).copy()
            self.eating_food["img"] = pygame.transform.rotate(self.eating_food["img"], self.eating_food["rotate"])
            self.eating_food["img"] = pygame.transform.scale(self.eating_food["img"], (50, 50))
            for effect, time in item["attribute"].items():
                if "生命回復" in effect: player.gain_effect(effect[:4], 1, time_to_ticks(time[1:-1]))
                if "移動速度" in effect: player.gain_effect(effect[:4], effect[7:9], time_to_ticks(time[1:-1]))
            if "無限使用t" not in item["attribute"]: player.gain_item(item["name"], -1, True)
            if "冷卻時間t" in item["attribute"]: Player.skill_cooldowns[item["name"]] = time_to_ticks(item["attribute"]["冷卻時間t"][1:-1])
        if "skill" in item and item["skill"].get("skillCD", False) and Player.skill_cooldowns[item["name"]] == 0: Player.skill_cooldowns[item["name"]] = item["skill"]["skillCD"] * 60
    #終結技
    def ultimate(self):
        if Mage.ultimate == True: self.attack_feedback("mage_ultimate_target")
        if self.weapon == 1 and Mage.ultimate == False and A_tree.rogue["暗影襲擊"] > 0 and Player.cooldowns["rogue_riptide"] > 0 and Player.cooldowns["暗影襲擊"] == 0 and Assassin.ultimate_time == 0 and All_mobs.nearest_x != -1:#暗影襲擊:激流狀態下才可使用，傳送到最近敵人，角色獲得重擊狀態(次數=激流狀態剩餘秒數、傷害=20)
            Player.cooldowns["暗影襲擊"] = 600 + A_tree.rogue["暗影襲擊降低冷卻"] * 300
            teleport(All_mobs.nearest_x)
            Player.cooldowns["rogue_skill_time"] = 0
            Assassin.smite = True
            Assassin.ultimate_time = math.ceil(Player.cooldowns["rogue_riptide"] / 60) + 3 * A_tree.rogue["激流強化"]
            Player.cooldowns["rogue_riptide"] = 0
            player.main_attack()
            Player.cooldowns["暗影襲擊剩餘時間"] = 600
        if self.weapon == 2 and A_tree.archer["苦無"] > 0 and Mage.ultimate == False:
            if Archer.kunai_amount > 0 and Player.cooldowns["苦無"] != 0:
                self.attack_code = -~ self.attack_code
                shoot_arrow(self.rect.centerx, self.rect.centery + 20, self.facing, "kunai")
                Archer.kunai_amount -= 1
            if A_tree.archer["雙向苦無"] > 0 and Archer.kunai_amount >= 1 and Player.cooldowns["苦無"] != 0:
                self.attack_code = -~ self.attack_code
                shoot_arrow(self.rect.centerx, self.rect.centery + 20, -self.facing, "kunai")
                Archer.kunai_amount -= 1
            if Player.cooldowns["苦無"] == 0:
                Player.cooldowns["苦無"] = 1200
                Player.cooldowns["苦無剩餘時間"] = 600
                Archer.kunai_amount = math.ceil(Archer.focus) + 1
                Archer.focus = 0
            if Archer.kunai_amount == 0: Player.cooldowns["苦無剩餘時間"] = 0
        if self.weapon == 3 and A_tree.mage["瞬水爆"] > 0 and Mage.ultimate == False and Player.cooldowns["瞬水爆"] == 0 and Mage.mana > Stats.total["魔力上限"] / 2 and Mage.ultimate == False: #瞬水爆:傳送到滑鼠位置，造成水爆領域，持續2秒，切換成近戰狀態，魔力+30，每秒燒10魔力(燒完或切武器停止)，魔力消耗:50
            Mage.mana -= Stats.total["魔力上限"] // 2
            Player.cooldowns["瞬水爆"] = 1800
            Mage.ultimate = True
            target = Target(self.rect.centerx - 150, self.rect.top + 75)
            all_sprites.add(target)
            targets.add(target)
    #獲得效果
    def gain_effect(self, effect, level, tick, replace_old = False):
        replaced_effect = False
        #判斷是否已經有同等級效果
        for effect_info in self.effects:
            if effect_info.get("name", False) == effect and (effect_info.get("level", False) == int(level) and int(effect_info.get("tick", False)) < tick or replace_old):
                effect_info["tick"] = tick
                effect_info["level"] = int(level)
                replaced_effect = True
        if replaced_effect == False:
            self.effects.append({"name":effect, "level":int(level), "tick":tick})
    #獲得經驗值
    def gain_exp(self, exp):
        if self.weapon == 1:
            Assassin.xp += exp
            new_message("刺客經驗 + " + str(exp))
        if self.weapon == 2:
            Archer.xp += 10
            new_message("弓箭手經驗 + " + str(exp))
        if self.weapon == 3:
            Mage.xp += 10
            new_message("法師經驗 + " + str(exp))
    #獲得物品
    def gain_item(self, item, amount, hide_msg = False):
        if amount != 0:
            for i in range(len(Inv.inventory)):
                if Inv.inventory[i]["name"] == item: Inv.inventory[i]["count"] += amount
            if search_item(item)["special"]: title("重要物品", search_item(item)["name"] + ("+" if amount > 0 else "-") + str(amount))
            if hide_msg == False: new_message((search_item(item)["name"]) + ("+" if amount > 0 else "") + str(amount))
#玩家位置
class Player_location:
    def __init__(self):
        self.disable_move = False
        self.disable_jump = False
        self.disable_ground = False
        self.x = 0
        self.y = 0
        self.coord_x = 0
        self.coord_y = 0
        self.anti_gravity = False
        self.dash_distance = 0
        self.midair_dash = 0
        self.mouse = False
        self.background_moving = 0
        self.player_move = False
#遊戲時間
class Game_time:
    def __init__(self):
        self.minute = 0
        self.hour = 0
#除錯資訊
class Info():
    def __init__(self):
        self.open = False
#刺客
class Assassin:
    def __init__(self):
        self.remove_chaos_dagger = False
        self.magic_enchant = 0
        self.smite = False
        self.ultimate_time = 0
        self.shadow_clone_location = (0, 0)
        self.level = 1
        self.xp = 0
        self.xp_req = 0
        self.a_point = 1
#弓箭手
class Archer:
    def __init__(self):
        self.focus = 0
        self.focus_limit = 0
        self.kunai_amount = 0
        self.level = 1
        self.xp = 0
        self.xp_req = 0
        self.a_point = 1
#法師
class Mage:
    def __init__(self):
        self.mana = 0
        self.mana_limit = 0
        self.ultimate = False
        self.magic_orb_hit = False
        self.level = 1
        self.xp = 0
        self.xp_req = 0
        self.a_point = 1
#所有怪物
class All_mobs:
    def __init__(self):
        self.count = 0
        self.kill = False
        self.in_area = 0
        self.remove_lootchest = False
        self.coord_x = 0
        self.nearest_x = 0
        self.boss_fight_active = False
        self.crack_wall_broken = False
#敵對生物
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, level, area, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        def base_stats(name, image, radius, color_key, health_limit, speedx, tracking_range, attack_range, base_damage, ground, can_fly, weakness, defense, rank, can_skill, skills = None, skill_cd_min = 0, skill_cd_max = 0):
            self.name = name
            self.image = image
            self.radius = radius
            self.image.set_colorkey(color_key)
            self.health_limit = health_limit
            self.health = self.health_limit
            self.speedx = speedx
            self.tracking_range = tracking_range
            self.attack_range = attack_range
            self.base_damage = base_damage
            self.ground = ground
            self.fly = can_fly
            self.weakness = weakness
            self.defense = defense
            self.rank = rank
            self.can_skill = can_skill
            self.knockback_resistance = 0
            if can_skill:
                self.skill_load = 0
                self.skills = skills
                self.skill_cooldown = 0
                self.casting_skill = ""
                self.skill_cd_min = skill_cd_min
                self.skill_cd_max = skill_cd_max
            else:
                self.skill_cooldown = 1
                self.skill_load = 0
        if self.type == "slime":
            base_stats("水史萊姆", slime_img, 65, GREEN, 20 + level * 10, 3, 300, 150, 5 + (5 * level), GROUND + 10, False, [2], [1], "normal", False)
            self.jumping = 0
        if self.type == "skeleton": base_stats("骷髏", skeleton_left_img, 65, GREEN, 20 + level * 5, 5, 400, 150, 8 + (5 * level), GROUND - 40, False, [0], [2], "normal", False)
        if self.type == "tree_monster": base_stats("樹妖", tree_monster_img, 65, WHITE, 20 + level * 10, 3, 500, 150, 5 + (5 * level), GROUND - 50, False, [2], [0, 1], "elite", False)
        if self.type == "crack_wall":
            base_stats("脆弱牆壁", crack_wall_img, 100, WHITE, 100, 0, 0, 0, 0, GROUND - 235, False, [0, 4], [2], "elite", False)
            self.knockback_resistance = 1
        if self.type == "zombie": base_stats("殭屍", zombie_left_img, 65, YELLOW, 10 + level * 13, 3, 800, 150, 5 + (3 * level), GROUND - 30, False, [2, 6], [0], "normal", False)
        if self.type == "xerath":
            base_stats("Xerath", xerath_img, 65, WHITE, level * 50, 7, 1000, 150, 3 + level * 1, GROUND - 100, False, [2, 6], [0, 7], "boss", False)
            self.sub_name = "墓穴守護者"
            self.hp_lower_250 = False
            self.hp_lower_150 = False
            self.y_weight = 0
        if self.type == "skywing_beast":
            base_stats("飛翼獸", skywing_beast_1_img, 65, GREEN, level * 15, 3, 500, 150, 10 + (4 * level), GROUND - 400, True, [2], [3], "normal", True, {"俯衝":70, "風暴":30}, 300, 420)
            self.change_img = 15
            self.rush_time = 60
        if self.type == "storm":
            base_stats("風暴", storm_img, 1, GREEN, 1, 3, 500, 100, level * 5, GROUND - 200, False, [], [], "skill", False)
            self.exist_duration = 180
        if self.type == "cursed_silver_knight":
            base_stats("被詛咒的銀騎士", cursed_silver_knight_img, 65, GREEN, level * 20, 2, 300, 100, 10 + (2 * level), GROUND - 100, False, [7], [4], "elite", True, {"長槍投射":50, "格擋":50}, 360, 480)
            self.defend_time = 120
        if self.type == "silver_knight_spear":
            base_stats("銀騎士長槍", silver_knight_spear_right_img, 1, GREEN, 1, 5, 0, 100, level * 8, GROUND - 50, True, [], [], "skill", False)
            self.detect_facing = True
        if self.type == "thunder_cloud":
            base_stats("烏雲", thunder_cloud_img, 65, GREEN, 30 + level * 5, 5, 400, 150, 0, GROUND - 400, True, [4], [1], "normal", True, {"落雷":80, "風暴":20}, 120, 150)
            self.lightning_last_time = 30
        if self.type == "thunder_dragon":
            base_stats("雷電飛龍", thunder_dragon_right_img, 100, GREEN, 50 + level * 10, 3, 700, 150, 0, GROUND - 400, True, [2], [1, 5, 3], "elite", True, {"落雷":60, "風暴":40}, 180, 240)
            self.lightning_last_time = 30
        if self.type == "cloud":
            base_stats("", cloud_images[random.randint(0, 4)], 1, GREEN, 1, random.randint(0, 2), 0, 0, 0, GROUND, True, [], [], "skill", False)
            self.facing = random.choice(["left", "right"])
        if self.type == "falling_rock": base_stats("", falling_rock_img, 50, GREEN, 1, 0, 0, 50, 50, GROUND + 500, False, [], [], "skill", False)
        if self.type == "falling_stick": base_stats("", falling_stick_img, 50, GREEN, 1, 0, 0, 50, 40, GROUND + 500, False, [], [], "skill", False)
        if self.type == "falling_brick": base_stats("", falling_brick_img, 70, GREEN, 1, 0, 0, 70, 60, GROUND + 500, False, [], [], "skill", False)
        if self.type == "falling_star_raindrop": base_stats("", falling_star_raindrop_img, 30, GREEN, 1, 0, 0, 30, 40, GROUND + 500, False, [], [], "skill", False)
        if self.type == "falling_meteor": base_stats("", falling_meteor_img, 50, GREEN, 1, 0, 0, 50, 70, GROUND + 500, False, [], [], "skill", False)
        if self.type == "falling_log": base_stats("", falling_log_img, 80, GREEN, 1, 0, 0, 80, 60, GROUND + 500, False, [], [], "skill", False)
        if self.type == "falling_pillar": base_stats("", falling_pillar_img, 70, GREEN, 1, 0, 0, 50, 80, GROUND + 500, False, [], [], "skill", False)
        if self.type == "falling_star_frag": base_stats("", falling_star_frag_img, 50, GREEN, 1, 0, 50, 60, 0, GROUND + 500, False, [], [], "skill", False)
        if self.type == "Stellaris":
            base_stats("Stellaris", stellaris_1_img, 150, GREEN, 500, 0, 2000, 0, 0, GROUND - 250, False, [2, 6], [3, 4], "boss", True, {"星疫蔓延":100, "星界降臨":0, "星疫孵化":0, "星疫雷射":0, "殞命刺擊":0, "星疫隕石":0, "逆轉命運":0, "核心暴露":0, "收集星輝":0, "守護Tuleen":0}, 300, 420)
            self.falling = True
            self.knockback_resistance = 1
            self.health_temp = self.health
            self.time = 0
            self.can_skill = False
            #技能測試
            self.skills = {"星疫蔓延":100, "星界降臨":0, "星疫孵化":0, "星疫雷射":0, "殞命刺擊":0, "星疫隕石":0, "逆轉命運":0, "核心暴露":0, "收集星輝":0, "守護Tuleen":0}
            self.skill_priority = 0
            #星疫擴散
            self.blight_spread_time = 0
            self.blight_spread_distant = 0 
            self.blight_cd = 120
            #星界降臨
            self.from_the_star_time = 0
            #星疫孵化
            self.blight_pod_time = 0
            #星疫雷射
            self.blight_laser_time = 0
            #殞命刺擊
            self.impaling_doom_time = 0
            self.impaling_doom_location = 0
            #星疫隕石
            self.blight_meteor_time = 0
            self.blight_meteor_cd = 30
            #逆轉命運
            self.distorting_fate_time = 0
            #核心暴露
            self.core_expose_time = 600
            self.core_health = 200
            self.core_open_by_npc_ability = False
            #收集星輝
            self.stardust_collect_time = 300
            #守護Tuleen
            self.defend_tuleen_time = 300
            self.tuleen_weapon = []
            self.weapon_speedx = 0
            #感染同伴
            self.corrupt_npc_time = 900
        if self.type == "from_the_star_wave": base_stats("", from_the_star_wave_img, 50, GREEN, 1, 0, 0, 50, 100, GROUND - 60, False, [], [], "skill", False)
        if self.type == "blight_pod":
            base_stats("", blight_pod_img, 50, GREEN, 100, 0, 0, 0, 0, GROUND, False, [2], [7], "normal", False)
            self.explode_time = 0
            self.knockback_resistance = 1
        if self.type == "blight_slime":
            base_stats("星疫史萊姆", blight_slime_img, 120, GREEN, 200, 3, 600, 120, 10 + level, GROUND - 100, False, [2], [1], "elite", False)
            self.jumping = 0
            Area18.boss_claim_area += 100
        if self.type == "stardust": base_stats("星輝", aurora_star_img, 50, GREEN, 1, 0, 0, 0, 0, 150, True, [], [], "normal", False)
        if self.type == "aurora_attack":
            base_stats("", dmg_indicator_img, 0, BLACK, 1, 0, 0, 0, 0, 100, True, [], [], "skill", False)
            Area18.aurora_attack = 50
        if self.type == "blight_bomb":
            base_stats("星疫炸彈", blight_bomb_img, 50, GREEN, 50, 0, 0, 0, 0, 500, False, [], [], "normal", False)
            self.explode_time = 280
            self.knockback_resistance = 1
        if self.type == "blight_meteor": base_stats("", blight_meteor_img, 70, GREEN, 1, 0, 0, 70, 70, GROUND + 100, False, [], [], "skill", False)
        if self.type == "毒霧":
            base_stats("毒霧", dmg_indicator_img, 50, BLACK, 150, 0, 0, 50, 0, 450, True, [], [], "skill", False)
            self.knockback_resistance = 1
        if self.type == "poison_gas_particle":
            base_stats("", dmg_indicator_img, 50, BLACK, 999, 0, 0, 50, 1, GROUND, True, [], [], "skill", False)
            self.alpha = 255
            self.radius = random.randint(5, 10)
            self.vector_x = random.randint(-2, 2)
            self.vector_y = random.randint(-2, 2)
        if self.type == "大老鼠": base_stats("大老鼠", giant_rat_left_img, 200, GREEN, 120 * Depth.multiplier["生命值%"], 3, 500, 220, 50 * Depth.multiplier["攻擊力%"], 400, False, [2, 5], [0], "normal", False)
        if self.type == "城門守衛":
            base_stats("城門守衛", castle_guardian_img, 80, GREEN, 200 * Depth.multiplier["生命值%"], 2, 800, 120, 40 * Depth.multiplier["攻擊力%"], 400, False, [7], [0, 4], "elite", False)
            self.knockback_resistance = 0.8
        if self.type == "Samwell Calder":
            base_stats("Samwell Calder", dmg_indicator_img, 200, BLACK, 5000, 0, 1000, 0, 0, 480, False, [], [], "boss", True, {"暗影飛刀":20, "黑淵之爪":20, "黑淵之影":10, "腥紅牢籠":20, "深淵凝視":10, "增援":20}, 180, 240)
            self.p1_DepthBossShield = True
            self.p2_DepthBossSheild = True
            self.p1_ShieldBreakAttack = False
            self.p2_ShieldBreakAttack = False
            self.knockback_resistance = 1
            self.sub_name = "深淵統治者"
            self.shadow_daggers_cast_time = 90
            self.grasp_of_the_depth_cast_time = 0
            self.shadow_of_the_depth_cast_time = 0
            self.gaze_of_the_depth_cast_time = 0
            self.cage_of_darkness_cast_time = 0
            self.crimson_harvest_stack_temp = player.crimson_harvest
            self.bladeCraftProgress = 0
            self.phrase = 1
            depth_room_background_img["魔王1"] = dd_boss_challenge_1_img
            #self.skills = {"熔岩噴發":0, "腐蝕之雨":0, "原初風暴":0, "天地崩解":0, "雷霆審判":0, "腥紅終焉":0, "深淵凝視":0}
            self.lava_eruption_cast_time = 0
            self.corrupted_rain_cast_time = 0
            self.primal_storm_cast_time = 0
            self.earth_rift_cast_time = 0
            self.thunder_judgement_cast_time = 180
            self.crimson_fianle_cast_time = 0
            #self.health = 1
            All_mobs.boss_fight_active = True
        if self.type == "暗影飛刀":
            base_stats("暗影匕首", shadow_dagger_img, 50, GREEN, 999, 0, 0, 5, 50, 100, True, [], [], "skill", False)
            # 使匕首面朝玩家
            middle_pos = (250 if 500 <= player.rect.x < 1000 else 750, 100)
            dx = player.rect.x - middle_pos[0]
            dy = player.rect.y - middle_pos[1]
            distance = math.hypot(dx, dy)
            if distance == 0:
                distance = 0.0001  # 避免除以0
            self.vx = dx / distance * 15
            self.vy = dy / distance * 15
            angle_deg = math.degrees(math.atan2(dy, dx))
            self.image = pygame.transform.rotate(shadow_dagger_img, -angle_deg)
        if self.type == "黑淵之影":
            base_stats("黑淵之影", shadow_of_the_depth_img, 10, GREEN, 1, 0, 1000, 50, 120, GROUND - 100, False, [], [], "skill", False)
            self.last_time = 60
        if self.type == "腥紅牢籠":
            base_stats("腥紅牢籠", cage_of_darkness_img, 300, GREEN, 100, 0, 0, 0, 0, 400, False, [], [], "normal", False)
            self.knockback_resistance = 1
            self.last_time = 120
        if self.type == "腐蝕雨滴": base_stats("腐蝕雨滴", corrupted_raindrop_img, 50, GREEN, 1, 0, 0, 50, 30, 700, False, [], [], "skill", False)
        if self.type == "腥紅終焉":
            base_stats("腥紅終焉", crimson_finale_img[1 - x // 250 % 2], 200, GREEN, 1, 0, 0, 100, 200, 500, True, [], [], "skill", False)
            self.last_time = (4 - x // 250) * 45
        self.resistance = 1
        self.y_weight = 1
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.level = level
        self.area = area
        self.damage_boost = 1
        self.coord_x = 0
        self.damage_taken_cd = []
        self.attack_cd = 0
        self.active_skills = {"俯衝":0, "風暴":0, "長槍投射":0, "格擋":0, "落雷":0, "星疫蔓延":0, "星界降臨":0, "星疫孵化":0, "星疫雷射":0, "殞命刺擊":0, "星疫隕石":0, "逆轉命運":0, "核心暴露":0, "收集星輝":0, "守護Tuleen":0, "暗影飛刀":0, "黑淵之爪":0, "黑淵之影":0, "腥紅牢籠":0, "深淵凝視":0, "增援":0, "熔岩噴發":0, "腐蝕之雨":0, "原初風暴":0, "天地崩解":0, "雷霆審判":0, "腥紅終焉":0}
        #力量/虛弱/燃燒
        self.effect = {None:0, "strength":0, "weakness":0, "burn":0, "vulnerable":0, "slowness":0}
    def update(self):
        if Info.open: pygame.draw.circle(screen, GREEN, (self.rect.centerx, self.rect.centery), self.radius)
        self.rect.x += All_mobs.coord_x
        self.coord_x = Player_location.coord_x + (self.rect.x - player.rect.x)
        #掉落
        if self.fly == False and self.rect.y < self.ground: self.rect.y = min(self.rect.y + 5, self.ground)
        #怪物傳送(座標)
        def mob_teleport(coord_x):
            if self.rect.x > player.rect.x: fix = 395
            else: fix = 0
            self.rect.x += (coord_x - Player_location.coord_x) + player.rect.x - self.rect.x + fix
        #獲得狀態
        def get_effect(effect, tick):
            if self.effect[effect] < tick and self.rank != "skill": self.effect[effect] = tick
        #承受傷害
        def deal_damage(damage, type, sourece = ""):
            if self.rank != "skill":
                if type in self.weakness: total = damage * 1.2 / self.resistance
                elif type in self.defense: total = damage * 0.8 / self.resistance
                else: total = damage / self.resistance
                #Samwell Calder護盾
                if self.type == "Samwell Calder" and ((self.p1_DepthBossShield and self.phrase == 1) or (self.p2_DepthBossSheild and self.phrase == 2)):
                    total = 0
                    if self.p1_ShieldBreakAttack:
                        self.p1_DepthBossShield = False
                        self.p1_ShieldBreakAttack = False
                        new_dialogue("水晶之力已被減弱，現在乘勝追擊!", "", "鐵匠名稱", "鐵匠")
                    if self.p2_ShieldBreakAttack:
                        self.p2_DepthBossShield = False
                        self.p2_ShieldBreakAttack = False
                        new_dialogue("水晶之力已被減弱，現在乘勝追擊!", "", "鐵匠名稱", "鐵匠")
                #破空突擊回復生命
                if self.health - total <= 0 and sourece == "破空突擊" and self.rank == "normal" and A_tree.rogue["破空突擊強化"]: player.health = min(player.health + player.health_limit * 0.15, player.health_limit)
                if self.health - total <= 0 and sourece == "破空突擊" and (self.rank == "elite" or self.rank == "boss") and A_tree.rogue["破空突擊強化"]: player.health = min(player.health + player.health_limit * 0.25, player.health_limit)
                #星辰令使核心暴露
                if self.active_skills["核心暴露"] and self.type == "Stellaris":
                    self.core_health -= total
                elif self.type != "Stellaris" or Area18.stellaris_phase == 2 :
                    self.health -= total
                    self.tracking_range = 1000
                if total != 0 and (self.active_skills["核心暴露"] or self.type != "Stellaris"): summon_dmg_indicator(self.rect.x, self.rect.y, type, (total))
        #擊退
        def knockback(distance):
            if self.rank != "skill":
                self.rect.x += round(distance[0] * distance[2] * (1 - self.knockback_resistance))
                self.rect.y -= round(distance[1] * (1 - self.knockback_resistance))
        #施放技能
        if self.active_skills["俯衝"]:
            self.rush_time -= 1
            if 30 < self.rush_time < 60:
                self.rect.y += 10
            if 1 <= self.rush_time < 30:
                self.rect.y -= 10
            if self.rush_time == 0:
                self.rect.y = 150
                self.active_skills["俯衝"] = False
                self.rush_time = 60
        if self.active_skills["風暴"]:
            summon_mob(self.rect.centerx, GROUND - 200, 5, Areas.area, "storm", False)
            self.active_skills["風暴"] = False
        if self.active_skills["長槍投射"]:
            summon_mob(self.rect.centerx, 500, 10, Areas.area, "silver_knight_spear", False)
            self.active_skills["長槍投射"] = False
        if self.active_skills["格擋"]:
            self.defend_time -= 1
            self.knockback_resistance = 1
            draw_img(screen, silver_knight_shield_img, self.rect.centerx - 50, self.rect.y)
            if self.defend_time < 0:
                self.knockback_resistance = 0
                self.active_skills["格擋"] = False
                self.defend_time = 120
        if self.active_skills["落雷"]:
            self.lightning_last_time -= 1
            draw_img(screen, lightning_img, self.rect.centerx - 50, self.rect.bottom)
            if abs(self.rect.centerx - player.rect.centerx) <= 150:
                Damage_to_player.damage += (5 * self.level * self.damage_boost) / 30
            if self.lightning_last_time == 0:
                self.active_skills["落雷"] = False
                self.lightning_last_time = 30
        if self.active_skills["星疫蔓延"]:
            new_boss_skill_bar("星疫蔓延", self.blight_spread_time, 180)
            self.blight_spread_time += 1
            draw_img(screen, aurora_skill_1, player.rect.x - (Player_location.coord_x - 17010), 470)
            if self.blight_spread_time == 1: new_dialogue("星疫無所不在，你們將葬身於此!", "", "Stellaris", "星辰令使")
            if self.blight_spread_time < 120: self.blight_spread_distant = min(self.blight_spread_distant + 10, (1000 - self.health))
            if self.blight_spread_time == 120: new_dialogue("星疫擴散了，別慌!站在魔法陣裡並接受治癒!", "", "Aurora", "魔法師")
            if self.blight_spread_time >= 180:
                if Player_location.coord_x <= 17200:
                    player.blight = max(0, player.blight - 20)
                    self.health -= 25
                else: self.health += 100
                self.active_skills["星疫蔓延"] = False
                self.blight_spread_time = 0
                self.blight_spread_distant = 0
        if self.active_skills["星界降臨"]:
            self.from_the_star_time += 1
            new_boss_skill_bar("星界降臨", self.from_the_star_time, 45)
            if self.from_the_star_time < 10: self.rect.y -= 100
            if self.from_the_star_time >= 45:
                summon_mob(self.rect.x + 20, GROUND - 60, 20, self.area, "from_the_star_wave", False)
                self.from_the_star_time = 0
                self.active_skills["星界降臨"] = False
        if self.active_skills["星疫孵化"]:
            self.blight_pod_time += 1
            if self.blight_pod_time == 1: summon_mob(random.randint(300, 600), GROUND, 1, self.area, "blight_pod", False)
            if self.blight_pod_time == 300:
                self.active_skills["星疫孵化"] = False
                self.blight_pod_time = 0
        if self.active_skills["星疫雷射"]:
            self.blight_laser_time += 1
            if self.blight_laser_time == 1:
                global laser_1, laser_2, laser_3, laser_4, laser_5
                laser_1 = random.randint(100, 200)
                laser_2 = random.randint(300, 400)
                laser_3 = random.randint(500, 600)
                laser_4 = random.randint(600, 700)
            if self.blight_laser_time < 120 and self.blight_laser_time % 60 < 30:
                draw_img(screen, blight_laser_1_img, self.rect.x - laser_1, 0)
                draw_img(screen, blight_laser_1_img, self.rect.x - laser_2, 0)
                draw_img(screen, blight_laser_1_img, self.rect.x - laser_3, 0)
                draw_img(screen, blight_laser_1_img, self.rect.x - laser_4, 0)
            if self.blight_laser_time > 120:
                draw_img(screen, blight_laser_2_img, self.rect.x - laser_1, 0)
                draw_img(screen, blight_laser_2_img, self.rect.x - laser_2, 0)
                draw_img(screen, blight_laser_2_img, self.rect.x - laser_3, 0)
                draw_img(screen, blight_laser_2_img, self.rect.x - laser_4, 0)
                if abs(player.rect.x - (self.rect.x - laser_1)) < 60 or abs(player.rect.x - (self.rect.x - laser_2)) < 60 or abs(player.rect.x - (self.rect.x - laser_3)) < 60 or abs(player.rect.x - (self.rect.x - laser_4)) < 60: Damage_to_player.damage += 2
            if self.blight_laser_time > 240:
                self.blight_laser_time = 0
                self.active_skills["星疫雷射"] = False
        if self.active_skills["殞命刺擊"]:
            self.impaling_doom_time += 1
            new_boss_skill_bar("殞命刺擊", self.impaling_doom_time, 480)
            if self.impaling_doom_time % 30 == 1 and self.impaling_doom_time % 60 < 30:
                self.impaling_doom_location = Player_location.coord_x
            if self.impaling_doom_time % 60 < 30: draw_img(screen, impaling_doom_1_img, player.rect.x - Player_location.coord_x + self.impaling_doom_location, 500)
            if 30 < self.impaling_doom_time % 60 < 60:
                draw_img(screen, impaling_doom_2_img, player.rect.x - Player_location.coord_x + self.impaling_doom_location, 700 - (self.impaling_doom_time % 60 - 30) * 10)
            if self.impaling_doom_time % 60 == 40:
                if abs(Player_location.coord_x - self.impaling_doom_location) < 50:
                    Damage_to_player.damage += 70
                    self.health += 10
                else: self.health -= 5
            if self.impaling_doom_time >= 480:
                self.impaling_doom_time = 0
                self.active_skills["殞命刺擊"] = False
        if self.active_skills["星疫隕石"]:
            new_boss_skill_bar("星疫隕石", self.blight_meteor_time, 300)
            self.blight_meteor_time += 1
            self.blight_meteor_cd -= 1
            if self.blight_meteor_cd == 0:
                self.blight_meteor_cd = random.randint(30, 50)
                summon_mob(random.randint(player.rect.x - 50, player.rect.x + 50), -100 , 1, Areas.area, "blight_meteor", False)
            if self.blight_meteor_time >= 300:
                self.blight_meteor_time = 0
                self.active_skills["星疫隕石"] = False
        if self.active_skills["逆轉命運"]:
            self.distorting_fate_time += 1
            if self.distorting_fate_time < 30:
                new_boss_skill_bar("逆轉命運", self.distorting_fate_time, 30)
                Player_location.disable_move = True
            if self.distorting_fate_time == 30:
                new_dialogue("你，加入我的行列!", "", "Stellaris", "星辰令使")
                teleport(18150)
                mob_teleport(17690 + 500 - Area18.blight_area)
            if self.distorting_fate_time > 30:
                draw_img(screen, aurora_skill_1, player.rect.x - (Player_location.coord_x - 17010), 470)
                new_boss_skill_bar("前往NPC處並接受淨化", self.distorting_fate_time, 210)
            if self.distorting_fate_time == 90: new_dialogue("沒時間了，冒險者，快過來接受淨化!", "", "Tuleen", "銀騎士")
            if self.distorting_fate_time == 210:
                if Player_location.coord_x <= 17200:
                    player.blight = max(0, player.blight - 40)
                    self.health -= 25
                else: self.health += 100
                self.distorting_fate_time = 0
                self.active_skills["逆轉命運"] = False
        if self.active_skills["核心暴露"]:
            self.core_expose_time -= 1
            new_boss_skill_bar("核心暴露剩餘時間", self.core_expose_time, 600)
            new_boss_skill_bar("核心生命值", self.core_health, 200)
            self.image = stellaris_2_img
            if self.core_open_by_npc_ability == False: new_dialogue("無垠的象徵，於虛空中顯現!", "星疫必須擴散!", "Stellaris", "星辰令使")
            def core_close(health):
                if self.core_open_by_npc_ability and health > 0: health = 0
                self.health += health
                self.core_health = 200
                self.core_expose_time = 600
                self.core_open_by_npc_ability = False
                self.image = stellaris_1_img
                self.active_skills["核心暴露"] = False
            if self.core_health <= 0:
                new_dialogue("做得好，冒險家! 令使後退了! 你的攻擊卓有成效!", "", "Tuleen", "銀騎士")
                core_close(-100)
            if self.core_expose_time == 0:
                new_dialogue("你的攻擊不夠強大!", "", "Tuleen", "銀騎士")
                core_close(200)
        if self.active_skills["收集星輝"]:
            self.stardust_collect_time -= 1
            new_boss_skill_bar("星輝剩餘數量: " + str(Area18.stardust_remain), self.stardust_collect_time, 300)
            if self.stardust_collect_time == 299:
                new_dialogue("我已召喚宇宙中的星輝，在它們消散之前將其摘下!", "", "Aurora", "魔法師")
                summon_mob(random.randint(self.rect.x - 400, self.rect.x - 300), random.randint(100, 200), 1, self.area, "stardust")
                summon_mob(random.randint(self.rect.x - 300, self.rect.x - 200), random.randint(100, 200), 1, self.area, "stardust")
                summon_mob(random.randint(self.rect.x - 200, self.rect.x - 100), random.randint(100, 200), 1, self.area, "stardust")
                Area18.stardust_remain = 3
            if Area18.stardust_remain == 0:
                new_dialogue("星輝足夠了!讓我將摘下的星輝，塑造成強力的武器...", "星輝的力量已穿透他的外殼，趁現在攻擊核心!", "Aurora", "魔法師")
                summon_mob(self.rect.x + 70, 100, 1, self.area, "aurora_attack")
                Area18.stardust_remain = 0
                self.stardust_collect_time = 300
                self.active_skills["收集星輝"] = False
            if self.stardust_collect_time == 0:
                new_dialogue("我需要更多星輝!", "", "Aurora", "魔法師")
                Area18.stardust_remain = 0
                self.stardust_collect_time = 300
                self.active_skills["收集星輝"] = False
        if self.active_skills["守護Tuleen"]:
            self.defend_tuleen_time -= 1
            new_boss_skill_bar("守護Tuleen", self.defend_tuleen_time, 300)
            def random_weapon():
                if random.randint(0, 1): self.tuleen_weapon.append(silver_knight_spear_right_img)
                else: self.tuleen_weapon.append(tuleen_skill_1_1_img)
            for i in range(len(self.tuleen_weapon)): draw_img(screen, self.tuleen_weapon[i], player.rect.x - (Player_location.coord_x - 17320) + self.weapon_speedx, 500 - i * 55)
            if self.defend_tuleen_time == 299:
                random_weapon()
                new_dialogue("令使將目光看向了我，在我準備發動攻擊時守護我!", "", "Tuleen", "銀騎士")
                for i in range(5): summon_mob(player.rect.x - (Player_location.coord_x - 17150 - (i * 80)), 500, 20, 18, "blight_bomb")
            if self.defend_tuleen_time == 240: random_weapon()
            if self.defend_tuleen_time == 180: random_weapon()
            if self.defend_tuleen_time == 120: random_weapon()
            if self.defend_tuleen_time == 60: random_weapon()
            if self.defend_tuleen_time <= 25: self.weapon_speedx += 15
            if self.defend_tuleen_time == 0:
                new_dialogue("將憤怒宣洩於令使之上!", "", "Tuleen", "銀騎士")
                self.active_skills["核心暴露"] = True
                self.core_open_by_npc_ability = True
                self.defend_tuleen_time = 300
                self.weapon_speedx = 0
                self.tuleen_weapon = []
                self.active_skills["守護Tuleen"] = False
            if Area18.blight_bomb_explode:
                Area18.blight_bomb_explode = False
                self.weapon_speedx = 0
                self.tuleen_weapon = []
                self.defend_tuleen_time == 300
                self.active_skills["守護Tuleen"] = False
        if self.active_skills["暗影飛刀"]:
            self.shadow_daggers_cast_time -= 1
            new_boss_skill_bar("暗影飛刀", self.shadow_daggers_cast_time, 90, YELLOW)
            if self.shadow_daggers_cast_time % 30 == 1:
                px, py = player.rect.x, player.rect.y
                if px <= 500: summon_x = 750
                else: summon_x = 250
                # 生成三把匕首
                for offset in [-75, 0, 75]:
                    start_pos = (summon_x + offset, 100)
                    summon_mob(start_pos[0], start_pos[1], 1, -7, "暗影飛刀", False)
            if self.shadow_daggers_cast_time == 0:
                self.shadow_daggers_cast_time = 90
                self.active_skills["暗影飛刀"] = False
        if self.active_skills["黑淵之爪"]:
            self.grasp_of_the_depth_cast_time += 1
            if self.grasp_of_the_depth_cast_time < 120:
                new_boss_skill_bar("黑淵之爪", self.grasp_of_the_depth_cast_time, 120, PURPLE)
            #橢圓的出現/放大
            if self.grasp_of_the_depth_cast_time <= 60:
                self.oval_position = (player.rect.centerx, 550)
                self.oval_growth_ratio = self.grasp_of_the_depth_cast_time / 60
                self.oval_size = 10 + (200 - 10) * self.oval_growth_ratio

            # 畫出橢圓
            out_oval_rect = pygame.Rect(self.oval_position[0], self.oval_position[1], self.oval_size * 2, self.oval_size * 0.5)
            out_oval_rect.center = self.oval_position
            inner_oval_rect = pygame.Rect(self.oval_position[0], self.oval_position[1], self.oval_size * 2 - 10, self.oval_size * 0.5 - 10)
            inner_oval_rect.center = self.oval_position
            pygame.draw.ellipse(screen, PURPLE, out_oval_rect, 20)
            pygame.draw.ellipse(screen, BLACK, inner_oval_rect)
            if 120 < self.grasp_of_the_depth_cast_time <= 180:
                draw_img(screen, pygame.transform.scale(grasp_of_the_depth_img, (200, 140)), self.oval_position[0] - 90, 420)
            # 造成傷害
            if self.grasp_of_the_depth_cast_time == 120:
                if self.oval_position[0] - 200 <= player.rect.x <= self.oval_position[0] + 200 and 600 > player.rect.y > 245:
                    Damage_to_player.damage = 120
                    player.crimson_harvest = min(5, player.crimson_harvest + 2)
            if self.grasp_of_the_depth_cast_time == 180:
                self.grasp_of_the_depth_cast_time = 0
                self.active_skills["黑淵之爪"] = False
        if self.active_skills["黑淵之影"]:
            self.shadow_of_the_depth_cast_time += 1
            new_boss_skill_bar("黑淵之影", self.shadow_of_the_depth_cast_time, 120, BLACK)
            if self.shadow_of_the_depth_cast_time < 90:
                self.shadow_summon_position_x = player.facing * (-150) + player.rect.centerx
            for i in range(3):
                summon_skill(self.shadow_summon_position_x, player.rect.centery, 1, "rogue_black_hole_particle", True, 30)
            if self.shadow_of_the_depth_cast_time == 120:
                summon_mob(self.shadow_summon_position_x, GROUND - 100, 1, -7, "黑淵之影", False)
                self.shadow_of_the_depth_cast_time = 0
                self.active_skills["黑淵之影"] = False
        if self.active_skills["腥紅牢籠"]:
            self.cage_of_darkness_cast_time += 1
            new_boss_skill_bar("腥紅牢籠", self.cage_of_darkness_cast_time, 30, (194, 24, 7))
            if self.cage_of_darkness_cast_time == 30:
                summon_mob(player.rect.x - 100, 100, 1, -7, "腥紅牢籠", True)
                self.cage_of_darkness_cast_time = 0
                self.active_skills["腥紅牢籠"] = False
        if self.active_skills["深淵凝視"]:
            self.gaze_of_the_depth_cast_time += 1
            new_boss_skill_bar("深淵凝視", self.gaze_of_the_depth_cast_time, 60, (194, 24, 7))
            if self.gaze_of_the_depth_cast_time >= 45:
                draw_img(screen, gaze_of_the_depth_img[(self.gaze_of_the_depth_cast_time - 45) // 5], 350, 120)
            if self.gaze_of_the_depth_cast_time == 60:
                player.crimson_harvest = min(5, player.crimson_harvest + 2)
                self.gaze_of_the_depth_cast_time = 0
                self.active_skills["深淵凝視"] = False
        if self.active_skills["增援"]:
            summon_mob(350, 400, 20, -7, "城門守衛")
            summon_mob(650, 400, 20, -7, "城門守衛")
            self.active_skills["增援"] = False
        if self.active_skills["熔岩噴發"]:
            self.lava_eruption_cast_time += 1
            new_boss_skill_bar("熔岩噴發", self.lava_eruption_cast_time, 139, (255, 127, 39))
            if self.lava_eruption_cast_time % 20 <= 14:
                lava_pos_x = self.lava_eruption_cast_time // 20 * 140
                for i in range(1, 4):
                    draw_img(screen, lava_eruption_img[self.lava_eruption_cast_time % 20 // 2], 10 + lava_pos_x, 160 * i)
                if 10 + lava_pos_x < player.rect.x < 150 + lava_pos_x and self.lava_eruption_cast_time % 20 == 0:
                    Damage_to_player.damage = 100
            if self.lava_eruption_cast_time >= 139:
                self.lava_eruption_cast_time = 0
                self.active_skills["熔岩噴發"] = False
        if self.active_skills["腐蝕之雨"]:
            self.corrupted_rain_cast_time += 1
            new_boss_skill_bar("腐蝕之雨", self.corrupted_rain_cast_time, 180, LBLUE)
            if self.corrupted_rain_cast_time % 10 == 0:
                summon_mob(random.randint(0, 1000), random.randint(30, 100), 1, -7, "腐蝕雨滴")
            if self.corrupted_rain_cast_time >= 180:
                self.corrupted_rain_cast_time = 0
                self.active_skills["腐蝕之雨"] = False
        if self.active_skills["原初風暴"]:
            self.primal_storm_cast_time += 1
            new_boss_skill_bar("原初風暴", self.primal_storm_cast_time, 60, WHITE)
            if self.primal_storm_cast_time <= 1:
                self.primal_storm_facing = random.choice((1, -1))
                self.primal_storm_pos_x = 0 if self.primal_storm_facing == 1 else 1000
            self.primal_storm_pos_x += 15 * self.primal_storm_facing
            storm_img.set_colorkey(GREEN)
            draw_img(screen, storm_img, self.primal_storm_pos_x - (storm_img.get_width() / 2), 300)
            self.storm_pull_speed = round((1000 - abs(self.primal_storm_pos_x - player.rect.x)) / 1000 * 15)
            if 13 <= self.storm_pull_speed <= 15:
                Damage_to_player.damage = 2
            if self.primal_storm_pos_x - player.rect.x > 0:
                teleport(min(Player_location.coord_x + self.storm_pull_speed, -7080))
            elif self.primal_storm_pos_x - player.rect.x < 0:
                teleport(max(Player_location.coord_x - self.storm_pull_speed, -7920))
            if self.primal_storm_cast_time >= 60:
                self.primal_storm_cast_time = 0
                self.active_skills["原初風暴"] = False
        if self.active_skills["天地崩解"]:
            self.earth_rift_cast_time += 1
            if self.earth_rift_cast_time <= 45:
                new_boss_skill_bar("天地崩解", self.earth_rift_cast_time, 45, (0, 100, 0))
                if self.earth_rift_cast_time == 1:
                    self.earth_rift_area = random.randint(0, 500)
            draw_img(screen, giant_rock_img, self.earth_rift_area + giant_rock_img.get_width() / 2, 0.5 * 10 * (self.earth_rift_cast_time / 4) ** 2)
            #石頭砸洞動畫
            if self.earth_rift_cast_time >= 35:
                draw_img(screen, earth_rift_img[min(max(self.earth_rift_cast_time - 30, 0) // 5, 2)], self.earth_rift_area, 400)
            if 45 < self.earth_rift_cast_time <= 345:
                new_boss_skill_bar("天地崩解", abs(self.earth_rift_cast_time - 345), 300, (0, 100, 0))
                #玩家掉入坑洞
                if self.earth_rift_area <= player.rect.x <= self.earth_rift_area + 500:
                    Player_location.disable_ground = True
                else:
                    Player_location.disable_ground = False
                if player.rect.y >= 600:
                    Damage_to_player.damage = 150
                    player.rect.y = 100
                    self.earth_rift_cast_time = 360
            #地板裂開圖像
            if self.earth_rift_cast_time >= 360:
                self.active_skills["天地崩解"] = False
                Player_location.disable_ground = False
                self.earth_rift_cast_time = 0
        if self.active_skills["雷霆審判"]:
            self.thunder_judgement_cast_time -= 1
            new_boss_skill_bar("雷霆審判", self.thunder_judgement_cast_time, 180, YELLOW)
            if self.thunder_judgement_cast_time % 60 == 59:
                self.thunder_judgement_pos = (random.randint(30, 250), random.randint(259, 500), random.randint(500, 750), random.randint(750, 970), random.randint(30, 970))
            #提示施放位置
            if 20 < self.thunder_judgement_cast_time % 60 < 59 and self.thunder_judgement_cast_time % 8 == 0:
                for i in range(4):
                    draw_img(screen, thunder_judgement_img[4], self.thunder_judgement_pos[i], 100)
            #施放技能
            elif self.thunder_judgement_cast_time % 60 <= 20:
                for i in range(4):
                    draw_img(screen, thunder_judgement_img[(20 - self.thunder_judgement_cast_time % 60) // 5], self.thunder_judgement_pos[i], 100)
                    if self.thunder_judgement_pos[i] <= player.rect.x <= self.thunder_judgement_pos[i] + 100 and self.thunder_judgement_cast_time % 60 == 19:
                        Damage_to_player.damage = 100
            if self.thunder_judgement_cast_time <= 0:
                self.thunder_judgement_cast_time = 180
                self.active_skills["雷霆審判"] = False
        if self.active_skills["腥紅終焉"]:
            self.crimson_fianle_cast_time += 1
            new_boss_skill_bar("腥紅終焉", self.crimson_fianle_cast_time, 180, RED)
            if self.crimson_fianle_cast_time % 45 == 1:
                self.crimson_spike = self.crimson_fianle_cast_time // 45
                summon_mob(self.crimson_spike * 250, 600 if self.crimson_spike % 2 == 1 else -500, 1, -7, "腥紅終焉")
            if self.crimson_fianle_cast_time >= 180:
                self.crimson_fianle_cast_time = 0
                self.active_skills["腥紅終焉"] = False
        #選擇技能
        def choose_skill(skills_probabilities):
            skills = list(skills_probabilities.keys())
            probabilities = list(skills_probabilities.values())
            chosen_skill = random.choices(skills, probabilities, k=1)[0]
            return chosen_skill
        #準備技能
        if (self.rect.centerx - player.rect.centerx + 100 > 0 and self.rect.centerx - player.rect.centerx < self.tracking_range and self.can_skill) or (self.rect.centerx - player.rect.centerx - 100 < 0 and self.rect.centerx - player.rect.centerx < self.tracking_range and self.can_skill):
            self.skill_cooldown -= 1
            if self.skill_cooldown <= 0:
                self.skill_load = 50
                self.casting_skill = choose_skill(self.skills)
                self.skill_cooldown = random.randint(self.skill_cd_min, self.skill_cd_max)
            if self.skill_load > 0:
                if self.rank != "boss": mob_skill_bar(self.rect.centerx - 40, self.rect.top - 110, self.casting_skill, self.skill_load, 50)
                self.skill_load -= 1
                if self.skill_load == 0: self.active_skills[self.casting_skill] = True
        for cd_atk in self.damage_taken_cd:
            cd_atk[1] -= 1
            if cd_atk[1] == 0:
                self.damage_taken_cd.remove(cd_atk)
                if player.attacks == [] and player.attack_code != 0: player.attack_code = 0
        #受到攻擊判定
        for attack in player.attacks:
            x, y, radius, damage, element, code, source, duration, kb, effect, effect_duration = attack
            #檢測是否在攻擊範圍內
            if are_circles_intersecting(x, y, radius, self.rect.centerx, self.rect.centery, self.radius) and all(cd[0] != code for cd in self.damage_taken_cd):
                self.damage_taken_cd.append([code, 60])
                player.attack_feedback(source)
                deal_damage(damage, element, source)
                knockback(kb)
                for effects in effect:
                    for effects_duration in effect_duration:
                        get_effect(effects, effects_duration)
                if Info.open: mob_debug_info(self.name, x, y, radius, damage, element, code, source, Player.name, duration, kb, effect, effect_duration, self.health, self.health_limit)
        no_health_bar = ["blight_bomb", "stardust", "Stellaris"]
        if (self.rank == "normal" or self.rank == "elite") and self.type not in no_health_bar: draw_mob_health(self.health, self.health_limit, self.rect.centerx - 80, self.rect.top - 30, self.name, self.level, self.effect, self.weakness, self.defense, self.rank)
        elif self.rank == "boss" and self.type not in no_health_bar: draw_boss_health(screen, self.health, self.health_limit, RED, self.name, self.sub_name, self.effect, self.weakness, self.defense)
        #觸發狀態
        self.damage_boost = 1
        self.resistance = 1
        for effect_time in self.effect:
            self.effect[effect_time] = max(0, self.effect[effect_time] - 1)
        if self.effect["strength"]: self.damage_boost += 0.2
        if self.effect["weakness"]: self.damage_boost -= 0.2
        if self.effect["burn"] % 60 == 1: deal_damage(0.8 * Stats.total["攻擊力"] * (1 + Stats.total["攻擊力%"] / 100), 2)
        if self.effect["vulnerable"]: self.resistance -= 0.2
        #離玩家最近距離
        if abs(self.coord_x - Player_location.coord_x) < abs(All_mobs.nearest_x - Player_location.coord_x): All_mobs.nearest_x = self.coord_x
        #特殊能力
        if self.type == "slime":
            self.jumping += 1
            if self.jumping >= 60:
                self.rect.y -= 20
                if self.rect.y <= GROUND - 40:
                    self.jumping = 0
        if self.type == "skeleton":
            if (self.rect.left - player.rect.centerx) + 50 < 0 and (self.rect.centerx - player.rect.centerx) < self.tracking_range: self.image = skeleton_right_img
            if (self.rect.right - player.rect.centerx) - 50 > 0 and (self.rect.centerx - player.rect.centerx) < self.tracking_range: self.image = skeleton_left_img
        if self.type == "crack_wall": All_mobs.crack_wall_broken = False
        if self.type == "zombie":
            if (self.rect.left - player.rect.centerx) + 50 < 0 and (self.rect.centerx - player.rect.centerx) < self.tracking_range: self.image = zombie_right_img
            if (self.rect.right - player.rect.centerx) - 50 > 0 and (self.rect.centerx - player.rect.centerx) < self.tracking_range: self.image = zombie_left_img
        if self.type == "xerath":
            if 150 < self.health < 250 and self.hp_lower_250 == False:
                new_dialogue("你的抵抗是徒勞的，凡人?但你仍有時間放棄，", "不然將面臨更深的黑暗。", "Xerath", "暗影統治者")
                self.hp_lower_250 = True
            if 50 < self.health < 150 and self.hp_lower_150 == False:
                new_dialogue("我已經厭倦了你的挑戰，凡人。", "黑暗將吞噬一切，包括你。", "Xerath", "暗影統治者")
                self.hp_lower_150 = True
        if self.type == "skywing_beast":
            self.change_img -= 1
            if self.change_img == 0:
                if self.image == skywing_beast_1_img:
                    self.image = skywing_beast_2_img
                elif self.image == skywing_beast_2_img:
                    self.image = skywing_beast_1_img
                self.image.set_colorkey(GREEN)
                if self.casting_skill == "俯衝" or self.active_skills["俯衝"]:
                    self.change_img = 8
                else: self.change_img = 15
        if self.type == "storm":
            self.exist_duration -= 1
            if self.exist_duration == 0:
                self.kill()
                All_mobs.count -= 1
        if self.type == "silver_knight_spear":
            if self.rect.centerx - player.rect.centerx > 0 and self.detect_facing:
                self.image = silver_knight_spear_left_img
            self.detect_facing = False
            if self.image == silver_knight_spear_right_img: self.rect.x += 20
            else: self.rect.x -= 20
        if self.type == "thunder_dragon":
            if (self.rect.left - player.rect.centerx) + 100 < 0 and (self.rect.centerx - player.rect.centerx) < self.tracking_range: self.image = thunder_dragon_right_img
            if (self.rect.right - player.rect.centerx) - 100 > 0 and (self.rect.centerx - player.rect.centerx) < self.tracking_range: self.image = thunder_dragon_left_img
        if self.type == "cloud":
            self.rect.y += 10
            if self.facing == "left": self.rect.x -= self.speedx
            else: self.rect.x += self.speedx
        if self.type.startswith("falling"):
            self.rect.y += 10
        if self.type == "Stellaris":
            #前進/後退
            self.health += Area18.boss_claim_area
            Area18.boss_claim_area = 0
            if Area18.stellaris_phase != 2:
                self.rect.x += ((self.health_temp - self.health))
            self.health_temp = self.health
            blight = int(Area18.blight_area // 50)
            for i in range(blight):
                draw_img(screen, blight_path_img, self.rect.x + (i * 50) + 80, 479)
            spread_blight = self.blight_spread_distant // 50
            for k in range(spread_blight):
                draw_img(screen, blight_path_img, self.rect.x - (k * 50) + 80, 479)
            Area18.blight_area = self.health
            #星疫感染
            if (player.rect.x - self.rect.x + self.blight_spread_distant - 50) > 0 and self.blight_cd == 0:
                player.blight += 10
                self.blight_cd = 120
            self.blight_cd = max(0, self.blight_cd - 1)
            #墜落
            if self.falling and self.rect.y < self.ground: self.rect.y = min(self.rect.y + 15, self.ground)
            #時間
            self.time += 1
            if self.time == 1: teleport(17500)
            #開核心
            if Area18.aurora_attack == 2:
                self.active_skills["核心暴露"] = True
                self.core_open_by_npc_ability = True
            #第0階段:
            if Area18.stellaris_phase == 0 and self.time == 180:
                self.can_skill = True
                Area18.stellaris_phase = 1
            #第1階段
            if Area18.stellaris_phase == 1 and self.time > 180:
                if self.active_skills["逆轉命運"] or self.active_skills["星疫蔓延"] or self.active_skills["收集星輝"] or self.active_skills["守護Tuleen"] or self.active_skills["核心暴露"] or self.active_skills["星疫雷射"]: self.skills = {"星疫蔓延":0, "星界降臨":25, "星疫孵化":25, "星疫雷射":25, "殞命刺擊":0, "星疫隕石":25, "逆轉命運":0, "核心暴露":0}
                else: self.skills = {"星疫蔓延":10, "星界降臨":15, "星疫孵化":10, "星疫雷射":10, "殞命刺擊":10, "星疫隕石":15, "逆轉命運":10, "核心暴露":10, "收集星輝":5, "守護Tuleen":5}
                if self.health <= 0:
                    new_dialogue("如果我快死了，我將帶上他們!", "", "Stellaris", "星辰令使")
                    self.image = stellaris_3_img
                    self.can_skill = False
                    Area18.stellaris_phase = 2
                    self.health = 250
                    self.rect.y = 450
                    for skills in self.active_skills:
                        self.active_skills[skills] = False
                    self.casting_skill = ""
                    self.rect.x += (self.coord_x - 18250)
            #第2階段
            if Area18.stellaris_phase == 2:
                self.corrupt_npc_time -= 1
                if 500 < self.corrupt_npc_time < 700: new_dialogue("這是什麼? 星疫在我周圍聚集! 冒險者，在這一切都太晚之前摧毀令使", "", "Tuleen", "銀騎士")
                if 300 < self.corrupt_npc_time < 500: new_dialogue("我...也快撐不住了!", "", "Aurora", "魔法師")
                new_boss_skill_bar("感染同伴", self.corrupt_npc_time, 900)
                draw_boss_health(screen, self.health, 250, TEAL, "Stellaris", "星辰令使", self.effect, self.weakness, self.defense)
                if self.corrupt_npc_time == 0: player.health = - 100
                if self.health <= 0:
                    title("Victory!", "Stellaris, 星辰令使")
                    Area18.stellaris_phase = 0
                    Area18.blight_area = 0
                    Area18.boss_claim_area = 0
                    All_mobs.boss_fight_active = False
                    if Area18.first_beat_boss:
                        Quest_03.stage += 1
                        Area18.first_beat_boss = False
        if self.type == "from_the_star_wave": self.rect.x -= 10
        if self.type == "blight_pod":
            self.explode_time += 1
            new_boss_skill_bar("星疫孵化", self.explode_time, 300)
            if self.explode_time == 300:
                summon_mob(self.rect.x, GROUND - 100, 20, self.area, "blight_slime")
                self.kill()
        if self.type == "blight_slime":
            self.jumping += 1
            if self.jumping >= 60:
                self.rect.y -= 40
                if self.rect.y <= GROUND - 180:
                    self.jumping = 0
        if self.type == "stardust":
            if Area18.stardust_remain == 0: self.kill()
        if self.type == "aurora_attack":
            #NPC事件:Aurora
            if Area18.aurora_attack > 0:
                self.image = aurora_skill_2_images[6 - (Area18.aurora_attack // 10)]
                Area18.aurora_attack -= 2
                if Area18.aurora_attack == 0: self.kill()
        if self.type == "blight_bomb":
            self.explode_time -= 1
            if self.explode_time < 15: self.image = blight_bomb_explode_img
            if self.explode_time == 0:
                new_dialogue("冒險者，下次保護好我!", "", "Tuleen", "銀騎士")
                Damage_to_player.damage = 50
                Area18.blight_bomb_explode = True
                self.kill()
        if self.type == "blight_meteor": self.rect.y += 10
        if self.type == "毒霧":
            summon_mob(self.rect.x + random.uniform(-20, 20), self.rect.y + random.uniform(-50, 50), 1, Areas.area, "poison_gas_particle", False)
        if self.type == "poison_gas_particle":
            self.alpha = max(0, self.alpha - 20)
            gas_particle = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(gas_particle, (0, 255, 0, self.alpha), (self.radius, self.radius), self.radius)
            draw_img(screen, gas_particle, self.rect.x - self.radius, self.rect.y - self.radius)
            self.rect.x += self.vector_x
            self.rect.y += self.vector_y
            if self.alpha <= 0: self.kill()
        if self.type == "大老鼠":
            if (self.rect.left - player.rect.centerx) + 50 < 0 and (self.rect.centerx - player.rect.centerx) < self.tracking_range: self.image = giant_rat_right_img
            if (self.rect.right - player.rect.centerx) - 50 > 0 and (self.rect.centerx - player.rect.centerx) < self.tracking_range: self.image = giant_rat_left_img
        if self.type == "Samwell Calder":
            #第一階段
            if self.phrase == 1:
                self.crimson_blade_count = search_item("腥紅刀片")["count"]
                if self.bladeCraftProgress == 0 and self.p1_DepthBossShield:
                    new_boss_skill_bar("腥紅刀片蒐集進度: " + str(self.crimson_blade_count) + "/ 10", min(10, self.crimson_blade_count), 10, (255, 74, 52))
                elif 1 <= self.bladeCraftProgress < 1800 and self.p1_DepthBossShield:
                    self.bladeCraftProgress += 1
                    new_boss_skill_bar("腥紅刀片修復進度 ", min(self.bladeCraftProgress, 1800) , 1800, (255, 74, 52))
                    if self.bladeCraftProgress == 1200: new_dialogue("快修好了，再幫我撐10秒!", "", "鐵匠名稱", "鐵匠")
                elif self.bladeCraftProgress >= 1800 and self.p1_DepthBossShield:
                    new_dialogue("腥紅之刃已修復完畢，使用這把鋒利的劍刃，", "貫穿國王的護盾!", "鐵匠名稱", "鐵匠")
                    self.p1_ShieldBreakAttack = True
                    self.bladeCraftProgress = 0
                if self.crimson_harvest_stack_temp < player.crimson_harvest:
                    player.gain_effect("腥紅收割", player.crimson_harvest, 600, True)
                self.crimson_harvest_stack_temp = player.crimson_harvest
                if self.bladeCraftProgress == 0 and self.p1_DepthBossShield and not self.p1_ShieldBreakAttack:
                    option = summon_npc(-7900, 400, {"修復刀片":"修復刀片"}, "鐵匠", kevin_1_img)
                    if option != None and option[0] == "修復刀片":
                        if search_item("腥紅刀片")["count"] >= 10:
                            player.gain_item("腥紅刀片", -10)
                            self.bladeCraftProgress = 1
                            new_dialogue("我已經開始修復刀片，這需要花費一些時間，請繼續戰鬥!", "", "鐵匠名稱", "鐵匠")
                        elif self.bladeCraftProgress == 0:
                            new_dialogue("冒險者，我們還需要" + str(10 - self.crimson_blade_count) + "個刀片就可以開剁了!", "", "鐵匠名稱", "鐵匠")
                else:
                    summon_npc(-7900, 400, {}, "鐵匠", kevin_1_img)
                if self.p1_ShieldBreakAttack:
                    new_boss_skill_bar("腥紅之刃已修復完畢", 1, 1, YELLOW)
                #轉換至第二階段
                if self.health <= 2500:
                    self.phrase = 2
                    self.health = 5000
                    depth_room_background_img["魔王1"] = dd_boss_challenge_2_img
                    self.skills = {"熔岩噴發":15, "腐蝕之雨":17, "原初風暴":17, "天地崩解":17, "雷霆審判":17, "腥紅終焉":15}
        if self.type == "暗影飛刀":
            self.rect.x += self.vx
            self.rect.y += self.vy
        if self.type == "黑淵之影":
            self.last_time -= 1
            if self.rect.x < player.rect.x: self.rect.x += 10
            else: self.rect.x -= 10
            if self.last_time <= 0:
                self.health = 0
        if self.type == "腥紅牢籠":
            self.last_time -= 1
            if self.rect.y == 400 and abs(player.rect.x - self.rect.centerx) < 150 and self.last_time > 0 and self.health > 0:
                Player_location.disable_move = True
                Player_location.disable_jump = True
                player.crimson_harvest = 5
            elif abs(player.rect.centerx - self.rect.centerx) > 150 or self.last_time <= 0 or self.health <= 0:
                Player_location.disable_move = False
                Player_location.disable_jump = False
                self.rect.y += 20
            else:
                self.rect.y = min(400, self.rect.y + 10)
            if self.rect.y >= 600:
                Player_location.disable_move = False
                Player_location.disable_jump = False
                self.health = 0
        if self.type == "腐蝕雨滴":
            self.rect.y += 10
        if self.type == "腥紅終焉":
            if self.rect.y <= -100:
                self.rect.y = min(-100, self.rect.y + 50)
            elif self.rect.y >= 200:
                self.rect.y = max(200, self.rect.y - 50)
            self.last_time -= 1
            if self.last_time == 0: self.kill()
        #追蹤玩家位置
        if (self.rect.centerx - player.rect.centerx) + 100 > 0 and (self.rect.centerx - player.rect.centerx) < self.tracking_range and Player.cooldowns["隱身"] == 0:
            self.rect.left -= self.speedx * (0.5 if self.effect["slowness"] else 1)
        if (self.rect.centerx - player.rect.centerx) - 100 < 0 and (self.rect.centerx - player.rect.centerx) < self.tracking_range and Player.cooldowns["隱身"] == 0:
            self.rect.right += self.speedx * (0.5 if self.effect["slowness"] else 1)
        #攻擊玩家
        self.attack_cd = max(0, self.attack_cd - 1)
        if abs(self.rect.centerx - player.rect.centerx) <= self.attack_range and abs(self.rect.centery - player.rect.centery) <= 150 and self.attack_cd == 0 and (Player.cooldowns["隱身"] == 0 or self.rank == "skill"):
            Damage_to_player.damage += self.base_damage * self.damage_boost
            self.attack_cd = 60
            if self.type == "falling_star_raindrop": player.blight += 10
            if self.type == "falling_star_frag": player.blight += 20
            if self.type == "暗影飛刀":
                player.crimson_harvest = min(5, player.crimson_harvest + 1)
            if self.type == "黑淵之影":
                if Player_location.dash_distance == 0: player.crimson_harvest = min(5, player.crimson_harvest + 2)
                self.health = 0
        #移除
        #不會因換區域移除的敵人
        keeping_monsters = ["Stellaris", "blight_pod", "blight_slime", "from_the_star_wave", "blight_bomb", "stardust", "Samwell Calder"]
        #刪除超出區域的敵人
        #非玩家擊敗
        if (self.type not in keeping_monsters and self.area != Areas.area) or All_mobs.kill:
            self.kill()
            if self.rank != "skill": All_mobs.count -= 1
        #被玩家擊敗
        if self.health <= 0 or (self.rank != "boss" and (self.health / self.health_limit <= 0.1) and A_tree.rogue["無聲絞喉"]):
            if (self.rank != "boss" and (0 < self.health / self.health_limit <= 0.1) and A_tree.rogue["無聲絞喉"] and player.weapon == 1):
                summon_dmg_indicator(self.rect.x, self.rect.y, 0, "Executed")
            self.kill()
            if self.rank != "skill": All_mobs.count -= 1
            All_mobs.nearest_x = -1
            #擊敗敵人觸發技能
            if A_tree.rogue["次元斬 I"] and player.weapon == 1:
                rogue_skills = ["暗影脈衝", "破空突擊", "混沌匕首", "暗影襲擊"]
                for i in range(len(rogue_skills)):
                    if self.rank == "normal": Player.cooldowns[rogue_skills[i]] = max(0, Player.cooldowns[rogue_skills[i]] - 60 - 60 * A_tree.rogue["次元斬 II"])
                    if self.rank == "elite" or self.rank == "boss": Player.cooldowns[rogue_skills[i]] = 0
                summon_skill(self.rect.centerx, self.rect.centery - 20, player.facing, "rogue_black_hole", False, 30)
            if A_tree.rogue["流放者"]: Player.cooldowns["rogue_riptide"] = min(300, Player.cooldowns["rogue_riptide"] + 60 + 60 * A_tree.rogue["隱身"])
            if self.type == "slime":
                spawn_item(self.rect.x, self.rect.y, "金幣", 1, "mob")
                spawn_item(self.rect.x, self.rect.y, "史萊姆黏液", 1, "mob")
                player.gain_exp(10)
            if self.type == "skeleton":
                spawn_item(self.rect.x, self.rect.y, "金幣", 3, "mob")
                spawn_item(self.rect.x, self.rect.y, "骨頭", 3, "mob")
                player.gain_exp(15)
            if self.type == "tree_monster":
                spawn_item(self.rect.x, self.rect.y, "金幣", 5, "mob")
                spawn_item(self.rect.x, self.rect.y, "樹枝", 2, "mob")
                spawn_item(self.rect.x, self.rect.y,"靈木碎片", random.randint(0, 1), "mob")
                player.gain_exp(20)
            if self.type == "crack_wall":All_mobs.crack_wall_broken = True
            if self.type == "zombie":
                spawn_item(self.rect.x, self.rect.y, "金幣", 3, "mob")
                spawn_item(self.rect.x, self.rect.y, "腐爛肉塊", 1, "mob")
                player.gain_exp(15)
            if self.type == "xerath":
                title("挑戰成功!", "暗影統治者 - Xerath")
                new_dialogue("哈哈...光明...你可能贏了這次，但黑暗會捲土重來...", " ", "Xerath", "暗影統治者")
                if Area9.first_beat_boss == True:
                    spawn_item(self.rect.x, self.rect.y, "死靈收割之鐮", 1, "mob")
                    Assassin.xp += 50
                    new_message("刺客經驗 + 50")
                    Archer.xp += 50
                    new_message("弓箭手經驗 + 50")
                    Mage.xp += 50
                    new_message("法師經驗 + 50")
                    Area9.first_beat_boss = False
            if self.type == "blight_pod": Area18.boss_claim_area -= 25
            if self.type == "stardust": Area18.stardust_remain -= 1
            if self.type == "城門守衛" and Depth.room == 10:
                spawn_item(self.rect.x, self.rect.y, "腥紅刀片", 1, "mob")
            if self.type == "Samwell Calder": All_mobs.boss_fight_active = False
#生成敵對生物
def summon_mob(x, y, level, area, type, count = True):
    if count: All_mobs.count += 1
    mob = Mob(x, y, level, area, type)
    all_sprites.add(mob)
    mobs.add(mob)
#造成玩家傷害
class Damage_to_player():
    def __init__(self):
        self.damage = 0
#技能特效
def summon_skill(x, y, facing, skill_type, is_particle, last_time):
    player.attack_code = -~ player.attack_code 
    player_skill = Player_skill(x, y, facing, player.attack_code, skill_type, is_particle, last_time)
    all_sprites.add(player_skill)
    mobs.add(player_skill)
#技能
class Player_skill(pygame.sprite.Sprite):
    def __init__(self, x, y, facing, code, skill_type, is_particle, last_time):
        pygame.sprite.Sprite.__init__(self)
        self.is_particle = is_particle
        self.skill_type = skill_type
        self.facing = facing
        if self.is_particle:
            #黑洞粒子
            if self.skill_type == "rogue_black_hole_particle":
                self.image = dmg_indicator_img
                self.radius = random.randint(2, 5)
                self.speed = random.uniform(2, 5)
                self.angle = random.uniform(0, 2 * math.pi)
                self.color = (223, 100, 224)
                self.alpha = 255
            #煙霧彈粒子
            if self.skill_type == "rogue_smoke_bomb_particle":
                self.x = x + random.randrange(-50, 50) * (1.5 if A_tree.rogue["煙霧範圍提升"] else 1)
                self.y = y + random.randrange(-50, 50) * (1.5 if A_tree.rogue["煙霧範圍提升"] else 1)
                self.size = random.randint(10, 30)
                self.lifetime = random.randint(40, 80)  # 粒子壽命
                self.alpha = 255
                self.color = (100, 100, 100)  # 煙霧為灰色
                self.vel_x = random.uniform(-2, 2) * 2  # 水平擴散
                self.vel_y = random.uniform(-2, -6)  # 向上移動
                self.image = dmg_indicator_img
        else:
            #黑洞
            if self.skill_type == "rogue_black_hole":
                self.image = pygame.transform.scale(black_hole_1_img, (20, 20))
                self.speedx = 0
                self.size = 20
                self.alpha = 255
            #混沌匕首
            if self.skill_type == "chaos_dagger":
                if self.facing == 1: self.image = chaos_dagger_right_img
                if self.facing == -1: self.image = chaos_dagger_left_img
                self.image = pygame.transform.scale(self.image, (120, 24))
                self.speedx = 15
            #幻影分身
            if self.skill_type == "shadow_clone":
                if self.facing == 1: self.image = shadow_clone_right_img
                if self.facing == -1: self.image = shadow_clone_left_img
                self.image.set_colorkey(BLACK)
                self.speedx = 0
            #煙霧彈
            if self.skill_type == "rogue_smoke_bomb":
                self.image = smoke_bomb_img
                self.angle = math.radians(70) #投擲角度
                self.v0x = 15 * math.cos(self.angle) * facing  #x初速度
                self.v0y = 15 * math.sin(self.angle)  #y初速度
                self.time = 0
                self.speedx = 0
                self.orign_x = x
                self.orign_y = y
                #self.rect.x = self.orign_x + self.v0x * self.time
                #self.rect.y = self.orign_y - (self.v0y * self.time) + (0.5 * 0.5 * self.time ** 2)
                #v0 - vt + 1/2*a*t^2
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.code = code
        self.last_time = last_time

    def update(self):
        self.rect.x += All_mobs.coord_x
        if self.is_particle == False:
            self.rect.x += self.speedx * self.facing
            self.last_time -= 1
        #非粒子
        if self.skill_type == "rogue_black_hole" and self.last_time < 60:
            self.image = pygame.transform.scale(black_hole_1_img, (self.size, self.size))
            self.image.set_alpha(self.alpha)
            if self.last_time < 20:
                self.size += 10
                self.rect.x -= 5
                self.rect.y -= 5
                self.alpha -= 5
                summon_skill(self.rect.right, self.rect.bottom + 30, self.facing, "rogue_black_hole_particle", True, 1)
        if self.skill_type == "chaos_dagger":
            player.attack(self.rect.centerx, self.rect.centery, 30, 0, 0, self.code, "混沌匕首", 2, [0, 0, self.facing], ["vulnerable"], [300])
            if Assassin.remove_chaos_dagger:
                Assassin.remove_chaos_dagger = False
                self.last_time = 5
        if self.skill_type == "shadow_clone":
            if Player.cooldowns["幻影分身持續時間"] == 0: self.last_time = 0
            Assassin.shadow_clone_location = (self.rect.x, self.rect.y)
            if Inv.equip["hotbar"][0] != "":
                sword_info = search_item(Inv.equip["hotbar"][0])
                self.sword_img = sword_info["img"].copy()
                self.sword_img.set_colorkey(sword_info["rarity"])
            else:
                self.sword_img = item_iron_sword_img.copy()
                self.sword_img.set_colorkey(RARE)
            self.sword_img = self.sword_img.subsurface(self.sword_img.get_bounding_rect()).copy()
            self.sword_img = pygame.transform.scale(self.sword_img, (90, 90))
            #調整方向
            if A_tree.rogue["刀舞"]:
                if self.last_time > 150:
                    draw_img(screen, slash_blade_dance_right_img, self.rect.centerx - 80 + 50, self.rect.y + 30)
                    draw_img(screen, slash_blade_dance_left_img, self.rect.centerx - 80 - 50, self.rect.y + 30)
                    player.attack(
                        self.rect.centerx - 20,
                        self.rect.y + 70,
                        140,
                        Stats.total["攻擊力"] * (1 + Stats.total["攻擊力%"] / 100) * 3,
                        7,
                        self.code,
                        "rogue_shadow_clone",
                        15,
                        [60, 20, player.facing],
                        [None],
                        [0]
                        )
            else:
                visual_sword = self.sword_img
                if self.last_time == 169: player.attack(self.rect.centerx + (70 * self.facing), self.rect.y + 70, 70, Stats.total["攻擊力"] * (1 + Stats.total["攻擊力%"] / 100) * 2, 7, self.code, "rogue_shadow_clone", 15, [60, 20, self.facing], [None], [0])
                if self.last_time > 165:
                    draw_img(screen, pygame.transform.flip(pygame.transform.rotate(visual_sword, 60), self.facing == 1, False), self.rect.centerx - 40 - int(self.facing == -1) * 50, self.rect.y + 10)
                    summon_skill(self.rect.right, self.rect.centery + 30, self.facing, "rogue_black_hole_particle", True, 1)
                if 155 < self.last_time <= 165: draw_img(screen, pygame.transform.flip(pygame.transform.rotate(visual_sword, 105), self.facing == 1, False), self.rect.centerx - int(self.facing == -1) * 100, self.rect.y + 30)
                if 155 < self.last_time <= 165: draw_img(screen, pygame.transform.flip(slash_right_2_img, self.facing == -1, False), self.rect.centerx + 20 - int(self.facing == -1) * 150, self.rect.y - 35)
                if self.last_time < 10: summon_skill(self.rect.right, self.rect.centery + 30, self.facing, "rogue_black_hole_particle", True, 1)
        if self.skill_type == "rogue_smoke_bomb":
            self.time += 1
            if self.rect.bottom >= 580:
                self.rect.bottom = 580
                player.attack(self.rect.centerx, self.rect.centery, 100 * (1.5 if A_tree.rogue["煙霧範圍提升"] else 1), 
                    Stats.total["攻擊力"] * (1 + Stats.total["攻擊力%"] / 100) * 0.5,
                    7,
                    self.code,
                    "rogue_smoke_bomb",
                    2,
                    [0, 0, player.facing],
                    ["slowness"],
                    [300]
                    )
                if self.last_time % 3 == 0:
                    summon_skill(self.rect.x, self.rect.y, self.facing, "rogue_smoke_bomb_particle", True, 60)
            else:
                self.rect.x = self.orign_x + self.v0x * self.time
                self.rect.y = self.orign_y - (self.v0y * self.time) + (0.5 * 0.5 * self.time ** 2) #v0 - vt + 1/2*a*t^2
        #粒子
        if self.skill_type == "rogue_black_hole_particle":
            # 更新位置
            self.rect.x += self.speed * math.cos(self.angle)
            self.rect.y += self.speed * math.sin(self.angle)
            # 透明度減少
            self.alpha -= 5
            self.alpha = max(self.alpha, 0)
            if self.alpha > 0:
                s = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*self.color, self.alpha), (self.radius, self.radius), self.radius)
                screen.blit(s, (self.rect.x - self.radius, self.rect.y - self.radius))
                if self.alpha <= 0 :self.kill()
        if self.skill_type == "rogue_smoke_bomb_particle":
            self.x += self.vel_x
            self.y += self.vel_y
            self.size *= 0.98  # 粒子慢慢縮小
            self.alpha -= 4  # 逐漸透明
            self.lifetime -= 1
            if self.alpha > 0:
                smoke_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
                pygame.draw.circle(smoke_surface, (100, 100, 100, self.alpha), (self.size, self.size), self.size)
                screen.blit(smoke_surface, (self.x - self.size, self.y - self.size))
            else :self.kill()
        if self.last_time <= 0:
            if self.skill_type == "shadow_clone": Assassin.shadow_clone_location = (False, False)
            self.kill()
#射箭
def shoot_arrow(x, y, facing, type):
    player.attack_code = -~ player.attack_code 
    arrow = Arrow(x, y, facing, player.attack_code, type)
    all_sprites.add(arrow)
    arrows.add(arrow)
#箭矢(所有種類)
class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, facing, code, arrow_type):
        pygame.sprite.Sprite.__init__(self)
        self.facing = facing
        self.arrow_type = arrow_type
        self.focus = math.ceil(Archer.focus)
        if self.arrow_type == "normal":
            if self.facing == 1: self.image = arrow_right_img
            if self.facing == -1: self.image = arrow_left_img
        elif self.arrow_type == "fire":
            if self.facing == 1: self.image = fire_arrow_right_img
            if self.facing == -1: self.image = fire_arrow_left_img
        elif self.arrow_type == "kunai":
            if self.facing == 1: self.image = kunai_right_img
            if self.facing == -1: self.image = kunai_left_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.code = code
        self.speedx = 20

    def update(self):
        self.rect.x += All_mobs.coord_x
        self.rect.x += self.speedx * self.facing
        if self.arrow_type == "normal": player.attack(self.rect.centerx + 20 * self.facing, self.rect.centery, 20, Stats.total["攻擊力"] * (1 + Stats.total["攻擊力%"] / 100) * (1 + self.focus * 0.2), 0, self.code, "archer_main_attack", 2, [30, 0, self.facing], [None], [0])
        if self.arrow_type == "fire": player.attack(self.rect.centerx + 20 * self.facing, self.rect.centery, 20, Stats.total["攻擊力"] * (1 + Stats.total["攻擊力%"] / 100) * (1 + self.focus), 2, self.code, "火焰箭矢", 2, [40, 0, self.facing], ["burn"] if A_tree.archer["點燃"] else [None], [180])
        if self.arrow_type == "kunai": player.attack(self.rect.centerx + 20 * self.facing, self.rect.centery, 20, Stats.total["攻擊力"] * (4 + Stats.total["攻擊力%"] / 100), 5, self.code, "苦無", 2, [40, 0, self.facing], [None], [0])
        if self.rect.x > WIDTH:
            self.kill()
        if self.rect.x <= 0:
            self.kill()
#魔法光線
class Magic_orb(pygame.sprite.Sprite):
    def __init__(self, x, y, mouse_x, mouse_y, code):
        pygame.sprite.Sprite.__init__(self)
        self.image = dmg_indicator_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.start_x = x
        self.start_y = y
        self.time = 60
        self.code = code
        self.facing = player.facing
    def update(self):
        self.rect.x += All_mobs.coord_x
        # 計算從玩家方塊到滑鼠的方向
        direction_x = self.mouse_x - (player.rect.centerx)
        direction_y = self.mouse_y - (player.rect.centery)
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
        # 規範化方向
        max_distance = 400
        direction_x /= distance
        direction_y /= distance
        self.rect.centerx += direction_x * 20
        self.rect.centery += direction_y * 20
        distance_travelled = math.sqrt((self.start_x - self.rect.x) ** 2 + (self.start_y - self.rect.y) ** 2)
        line_end_x = self.start_x + direction_x * 400
        line_end_y = self.start_y + direction_y * 400
        if 9 >= player.holding["wand"]:
            pygame.draw.line(screen, BLACK, (self.start_x + 50 * self.facing, self.start_y - 18), (line_end_x, line_end_y), 40)
            pygame.draw.line(screen, PURPLE, (self.start_x + 50 * self.facing, self.start_y - 18), (line_end_x, line_end_y), 30)
        player.attack(self.rect.centerx, self.rect.centery + 40, 20, 2 * Stats.total["攻擊力"] * (1 + Stats.total["攻擊力%"] / 100), 0, self.code, "mage_main_attack", 2, [0, 0, self.facing], [None], [0])
        if self.rect.x > WIDTH or self.rect.x <= 0 or distance_travelled >= max_distance:
            self.kill()
#隕石
class Meteor(pygame.sprite.Sprite):
    def __init__(self, x, y, code):
        pygame.sprite.Sprite.__init__(self)
        self.image = meteor_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = 20
        self.code = code
        self.facing = player.facing

    def update(self):
        player.attack(self.rect.centerx, self.rect.centery + 45, 70, Stats.total["攻擊力"] * (4 + A_tree.mage["隕石增加傷害"] + (1 + Stats.total["攻擊力%"] / 100)), 2, self.code, "隕石", 2, [30, 50, self.facing], [None], [0])
        self.rect.x += All_mobs.coord_x
        self.rect.y += self.speedy
        if self.rect.y > GROUND:
            self.kill()
#準心
class Target(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = target_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.centerx = x
        self.rect.bottom = y
    def update(self):
        self.rect.x = Mouse.x - 30
        self.rect.y = Mouse.y - 30
        if Mage.ultimate == False:
            self.kill()
#水爆領域
class Water_burst(pygame.sprite.Sprite):
    def __init__(self, x, y, code):
        pygame.sprite.Sprite.__init__(self)
        self.image = water_burst_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.code = code
        self.rect.centerx = x
        self.rect.bottom = y
    def update(self):
        self.rect.x += All_mobs.coord_x
        player.attack(self.rect.centerx, self.rect.centery, 150, 2 * Stats.total["攻擊力"] * (1 + Stats.total["攻擊力%"] / 100), 1, self.code, "mage_ultimate_water_burst", 5, [0, 0, 0], [None], [0])
        if Player.cooldowns["mage_water_burst"] == 0:
            self.kill()
#傷害顯示器
#物理:0 灰
#水屬性:1 藍
#火屬性:2 紅
#風屬性:3 白
#地屬性:4 綠
#雷屬性:5 黃
#光屬性:6 金
#暗屬性:7 紫
class Dmg_indicator(pygame.sprite.Sprite):
    def __init__(self, x, y, element, damage):
        pygame.sprite.Sprite.__init__(self)
        self.image = dmg_indicator_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.element = element
        if damage != "Executed":
            self.damage = round(damage, 1)
        else:
            self.damage = damage
        self.rand_x = random.randint(-30, 30)
        self.rand_y = random.randint(-60, -50)
    def update(self):
        def draw_damage(text_color):
            font = pygame.font.Font(text_font_2, 72)
            base = font.render(str(self.damage), True, BLACK)  # 渲染外框
            outline = pygame.Surface((base.get_width() + 4, base.get_height() + 4), pygame.SRCALPHA)
            text_surface = font.render(str(self.damage), True, text_color)  # 渲染主文字
            # 繪製外框 (上下左右四個方向)
            for dx in [-2, 2]:
                for dy in [-2, 2]:
                    outline.blit(base, (dx + 2, dy + 2))
            # 中心繪製主文字
            outline.blit(text_surface, (2, 2))
            screen.blit(outline, (self.rect.x + self.rand_x, self.rect.y + self.rand_y))
        if self.element == 0: draw_damage(GRAY)
        if self.element == 1: draw_damage(LBLUE)
        if self.element == 2: draw_damage(RED)
        if self.element == 3: draw_damage(WHITE)
        if self.element == 4: draw_damage(DGREEN)
        if self.element == 5: draw_damage(YELLOW)
        if self.element == 6: draw_damage(GOLD)
        if self.element == 7: draw_damage(PURPLE)
        self.rect.y += 10
        if self.rect.y > HEIGHT:
            self.kill()
#顯示傷害
def summon_dmg_indicator(x, y, element, damage):
    dmg_indicator = Dmg_indicator(x, y, element, damage)
    all_sprites.add(dmg_indicator)
    dmg_indicators.add(dmg_indicator)
#掉落物品
class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, count, drop_type):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.drop_type = drop_type
        self.image = pygame.transform.scale(search_item(item_type)["img"], (50, 50))
        self.image.set_colorkey(search_item(item_type)["rarity"])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedx = 0
        self.speedy = 0
        self.ground = GROUND + 100 + random.randint(-10, 10)
        self.gravity = 0.5
        self.count = count
        if self.drop_type == "chest":
            self.speedx = random.uniform(-5, 5)
            self.speedy = random.uniform(-10, -5)
        if self.drop_type == "mob": self.speedx = random.uniform(-5, 5)
        self.pick_up_time = 0
    def update(self):
        outline_text(search_item(self.item_type)["name"] + " * " + str(self.count), 25, self.rect.x - (len(search_item(self.item_type)["name"]) * 20 // 2 if len(search_item(self.item_type)["name"]) > 2 else 0), self.rect.top - 30, search_item(self.item_type)["rarity"])
        self.rect.x += All_mobs.coord_x
        self.rect.x += self.speedx
        self.speedy += self.gravity
        self.rect.y += self.speedy
        if self.rect.x > 960 and Areas.lock_right: self.rect.x = 960
        if self.rect.x < 0 and Areas.lock_left: self.rect.x = 0
        if self.rect.bottom >= self.ground:
            self.rect.bottom = self.ground
            self.speedy = 0
            if self.drop_type == "chest" or self.drop_type == "mob": self.speedx *= 0.9
            if abs(self.rect.centerx - player.rect.centerx) < 40: self.pick_up_time += 1
            else: self.pick_up_time = 0
            if self.pick_up_time >= 20:
                self.kill()
                player.gain_item(self.item_type, self.count)
        if abs(self.rect.x - player.rect.x) > 1000 or self.count <= 0:
            if search_item(self.item_type)["special"]: player.gain_item(self.item_type, self.count)
            self.kill()
#定義 生成掉落物品
def spawn_item(x, y, item_type, count, drop_type):
    item = Item(x, y, item_type, count, drop_type)
    all_sprites.add(item)
    items.add(item)
#寶箱資訊
class Lootchest_info():
    def __init__(self):
        self.exist = False
        self.claimed = 0
#寶箱
class Lootchest(pygame.sprite.Sprite):
    def __init__(self, x, y, tier, area, contain_items):
        pygame.sprite.Sprite.__init__(self)
        self.tier = tier
        self.image = dmg_indicator_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.centerx = x - 78
        self.rect.bottom = y - 73
        self.area = area
        self.items = contain_items if contain_items != "none" else []
    def update(self):
        lootchest_imgs = {1:t1_lootchest_img, 2:t2_lootchest_img, 3:t3_lootchest_img, 4:t4_lootchest_img}
        draw_img(screen, lootchest_imgs[self.tier], self.rect.x, self.rect.top)
        self.rect.x += All_mobs.coord_x
        if self.alive: Lootchest_info.exist = True
        if self.rect.left <= player.rect.x <= self.rect.right and All_mobs.count == 0:
            draw_img(screen, button_use_img, self.rect.centerx, 300)
            #寶箱獎勵
            if Areas.use:
                Areas.lootchest[Areas.area] -= 1
                #T1
                if self.tier == 1:
                    self.random_coin(1, 3)
                #T2
                if self.tier == 2:
                    self.random_coin(5, 10)
                    self.random_ore(3, 4)
                #T3
                if self.tier == 3:
                    self.random_coin(15, 20)
                    self.random_ore(5, 8)
                #T4
                if self.tier == 4:
                    self.random_coin(20, 30)
                #產生物品
                for item in self.items:
                    spawn_item(self.rect.x, self.rect.y, item["index"], item["count"], "chest")
                Areas.use = False
                self.kill()
        if All_mobs.remove_lootchest:
            All_mobs.remove_lootchest = False
            self.kill()
        if ((self.rect.left < 0 or self.rect.right > WIDTH) and self.area != Areas.area):
            self.kill()
    def random_coin(self, range1, range2):
        self.items.append({"index":"金幣", "count":random.randint(range1, range2)})
    def random_ore(self, range1, range2):
        self.items.append({"index":"基礎礦石", "count":random.randint(range1, range2)})
#定義 生成寶箱
def spawn_lootchest(x, y, tier, area, items = []):
    if items == []: items = "none"
    lootchest = Lootchest(x, y, tier, area, items)
    all_sprites.add(lootchest)
    lootchests.add(lootchest)
#音樂
class Music():
    def __init__(self):
        self.music = True
#訊息
class Messages():
    def __init__(self):
        self.text = []
#定義 新訊息
def new_message(message):
    Player.cooldowns["message"] = 100
    Messages.text.pop()
    Messages.text.insert(0, message)
#無框對話
class Dialogue():
    def __init__(self):
        self.text = []
        self.name = []
#定義 新對話
def new_dialogue(dialogue, dialogue2, name, subname):
    Player.cooldowns["dialogue"] = 300
    Dialogue.text = []
    Dialogue.text.insert(0, dialogue)
    Dialogue.text.insert(0, dialogue2)
    Dialogue.name[0] = str(name)
    Dialogue.name[1] = str(subname)
#標題
class Title():
    def __init__(self):
        self.text = [" ", " "]
#定義 新標題
def title(title, subtitle):
    Player.cooldowns["title"] = 120
    Title.text[0] = title
    Title.text[1] = subtitle
#魔王技能條
class Boss_skill_bar():
    def __init__(self):
        self.bars = []
#定義 新魔王技能條
def new_boss_skill_bar(name, time, total_time, color = TEAL):
    Boss_skill_bar.bars.append([name, time, total_time, color])
#提示
class Hint():
    def __init__(self):
        self.open = False
#物品欄
class Inv():
    def __init__(self):
        self.open = False
        self.cate = 1
        self.use = False
        self.equip = {"sword":0, "bow":0, "wand":0, "helmet":0, "armor":0, "legs":0, "boots":0, "charms":[]}
        self.charm_slot = []
        self.charm_slot_preview = []
        self.showing_charm = {}
        self.invload = []
        self.preview = []
        self.equip_preview = {"sword":0, "bow":0, "wand":0, "helmet":0, "armor":0, "legs":0, "boots":0, "charms":[]}
        self.info_loc_x = 0
        self.info_loc_y = 0
        self.hovering_item = False
        self.type = "normal"
        self.inventory = []
        self.hotbar_index = 0
        self.hotbar_selecting = False
        self.hotbar_selection_timer = 0
        self.selected_item = ""
#角色屬性
class Stats():
    def __init__(self):
        self.open = False
        self.cate = 1
        self.info = {}
        self.basic = 0
        self.bonus = 0
        self.total = 0
        self.charm = {}
#解謎
class Puzzle():
    def __init__(self):
        self.open = False
#鍛造
class Forge():
    def __init__(self):
        self.open = False
        self.cate = 1
        self.selected = 1
        self.working = 0
        self.last_time = 0
        self.max_last_time = 0
#天賦樹
class A_tree():
    def __init__(self):
        self.open = False
        self.cate = 1
        self.gui_location_x = 0
        self.gui_location_y = 0
        self.info_loc_x = 0
        self.info_loc_y = 0
        self.showing_info = 0
        self.node_img = 0
        self.moving = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_temp_x = 0
        self.mouse_temp_y = 0
        self.lclick = False
        self.rogue = {}
        self.archer = {}
        self.mage = {}
        self.keybind = [{}, {}, {}]
        self.row = 1
        self.skill_img = {}
        self.specialization_unlock = {}
#任務
class Quest():
    def __init__(self):
        self.open = False
        self.next_stage = False
        self.skippable = False
        self.tracking = 0
#任務01 - 藥水實驗
class Quest_01():
    def __init__(self):
        self.progressing = False
        self.complete = False
        self.stage = 0
        self.dialogue = []
#任務02 - 黑暗勢力的威脅
class Quest_02():
    def __init__(self):
        self.progressing = False
        self.complete = False
        self.stage = 0
        self.dialogue = []
#任務03 - 星疫之災
class Quest_03():
    def __init__(self):
        self.progressing = False
        self.complete = False
        self.stage = 0
#任務04 - 黑暗王座的終焉
class Quest_04():
    def __init__(self):
        self.progressing = False
        self.complete = False
        self.stage = 0
#存檔/讀檔
class Save_load():
    def __init__(self):
        self.selected = 1
        self.warning = 0
        self.empty = ""
        self.name = ""
        self.time_preview = ""
        self.health_preview = 0
        self.area_preview = 0
        self.assassin_level_preview = 0
        self.assassin_xp_preview = 0
        self.archer_level_preview = 0
        self.archer_xp_preview = 0
        self.mage_level_preview = 0
        self.mage_xp_preview = 0
#傳送門
class Portal():
    def __init__(self):
        self.open = False
        self.unlock = {}
#至黑深淵
class Depth():
    def __init__(self):
        self.floor = 1
        self.room = 1
        self.start = True
        self.room_type = {}
        self.menu_open = False
        self.blessing_menu = False
        self.menu_type = 0
        self.score = 0
        self.spawn = False
        self.blessings = []
        self.blessings_order = []
        self.blessing_quality_roll = 0
        self.blessing_upgrade_level = 0
        self.blessing_reading1 = 0
        self.blessing_reading2 = 0
        self.blessing_reading3 = 0
        self.current_room_name = ""
        self.roll_room_type = False
        self.room_info = []
        self.stats = {}
        self.get_room_reward = False

        self.multiplier = {}
#交易
class Trade():
    def __init__(self):
        self.open = False
        self.items = []
        self.sidebar = {}
        self.show_info = False
        self.click = True
        self.shops = {}
#區域
class Areas():
    def __init__(self):
        self.area = 0
        self.areas = 0
        self.spawnpoint = 0
        self.switch = False
        self.spawn = False
        self.use = False
        self.cleared = {}
        self.first = {}
        self.lootchest = {}
        self.mob_killed = {}
        self.lock_right = False
        self.lock_left = False
        self.regen_lock = False
        self.safe = False
        self.changed = True
        self.special_area = ""
#區域6 - 墓園
class Area6():
    def __init__(self):
        self.first = True
        self.clear = False
        self.cata_open = False
#區域7 - 地下墓穴大廳
class Area7():
    def __init__(self):
        self.wave = 1
        self.wave_clear = False
        self.w_clock = 0
#區域8 - 地下墓穴機關房
class Area8():
    def __init__(self):
        self.puzzle_complete = False
        self.puzzle_rune_holding = 0
        self.rune_slot = [0, 0, 0, 0, 0]
        self.old_holding = 0
#區域9 - 地下墓穴魔王房
class Area9():
    def __init__(self):
        self.boss_summoned = False
        self.first_beat_boss = False
#區域11 - 一號路口
class Area11():
    def __init__(self):
        self.x_velocity = 0
        self.y_velocity = 0
#區域12 - 天空群島1
class Area12():
    def __init__(self):
        self.falling = False
#區域16 - 天空群島5
class Area16():
    def __init__(self):
        self.ascension_distant = 0
        self.max_ascension_distant = 1500
        self.ascension_time = 0
        self.ascension_phase = ""
#區域18 - 星界聖所1
class Area18():
    def __init__(self):
        self.boss_summoned = False
        self.first_beat_boss = False
        #開場/~50%血量/~30%血量/0%血量
        self.stellaris_phase = 0
        self.blight_area = 0
        self.boss_claim_area = 0
        self.stardust_remain = 0
        self.aurora_attack = 0
        self.blight_bomb_explode = False
#滑鼠
class Mouse():
    def __init__(self):
        self.x = 0
        self.y = 0
#存檔
def save(file):
    with open("Save" + str(file) + ".txt", mode = "w", encoding = "utf-8") as file:
        #儲存玩家數據
        file.write("===FTL遊戲進度存檔===\n")
        file.write("存檔時間: 20" + now.strftime("%y-%m-%d %H:%M:%S\n"))
        file.write(str(Player.name) + "\n")
        file.write(str(player.health) + "\n")
        file.write(str(Player_location.coord_x) + "\n")
        file.write(str(Player_location.y) + "\n")
        file.write(str(Areas.lock_left) + "\n")
        file.write(str(Areas.lock_right) + "\n")
        save_data = {item["name"]: item["count"] for item in Inv.inventory}
        file.write(str(save_data) + "\n")
        file.write(str(Inv.equip) + "\n")
        file.write(str(Inv.charm_slot) + "\n")
        file.write(str(Areas.area) + "\n")
        file.write(str(Areas.spawnpoint) + "\n")
        #儲存冷卻
        file.write(str(Player.cooldowns) + "\n")
        file.write(str(Player.skill_cooldowns) + "\n")
        #儲存刺客數據
        file.write(str(Assassin.level) + "\n")
        file.write(str(Assassin.xp) + "\n")
        file.write(str(Assassin.a_point) + "\n")
        #儲存弓箭手數據
        file.write(str(Archer.level) + "\n")
        file.write(str(Archer.xp) + "\n")
        file.write(str(Archer.a_point) + "\n")
        #儲存法師數據
        file.write(str(Mage.mana) + "\n")
        file.write(str(Mage.level) + "\n")
        file.write(str(Mage.xp) + "\n")
        file.write(str(Mage.a_point) + "\n")
        #儲存其他數據
        file.write(str(Forge.working) + "\n")
        file.write(str(Forge.max_last_time) + "\n")
        file.write(str(A_tree.rogue) + "\n")
        file.write(str(A_tree.archer) + "\n")
        file.write(str(A_tree.mage) + "\n")
        file.write(str(A_tree.keybind) + "\n")
        file.write(str(A_tree.specialization_unlock) + "\n")
        file.write(str(Portal.unlock) + "\n")
        file.write(str(Quest.tracking) + "\n")
        file.write(str(Quest_01.stage) + "\n")
        file.write(str(Quest_01.progressing) + "\n")#BOOL
        file.write(str(Quest_01.complete) + "\n")#BOOL
        file.write(str(Quest_02.stage) + "\n")
        file.write(str(Quest_02.progressing) + "\n") #BOOL
        file.write(str(Quest_02.complete) + "\n") #BOOL
        file.write(str(Quest_03.stage) + "\n")
        file.write(str(Quest_03.progressing) + "\n") #BOOL
        file.write(str(Quest_03.complete) + "\n") #BOOL
        file.write(str(Areas.cleared) + "\n")
        file.write(str(Areas.lootchest) + "\n")
        file.write(str(Areas.first) + "\n")
        file.write(str(All_mobs.crack_wall_broken) + "\n")
        file.write(str(Area6.cata_open) + "\n")
        file.write(str(Area8.puzzle_complete) + "\n")
        file.write(str(Area9.first_beat_boss) + "\n")
        file.write(str(Area18.first_beat_boss) + "\n")
def load(file):
    with open("Save" + str(file) + ".txt", mode = "r", encoding = "utf-8") as file:
        #讀取玩家數據
        file.readline()
        print(file.readline()[:-1])
        Player.name = file.readline()[:-1]
        player.health = eval(file.readline())
        player_location_temp = eval(file.readline())
        teleport(player_location_temp)
        player.rect.y = eval(file.readline())
        Areas.lock_left = eval(file.readline())
        Areas.lock_right = eval(file.readline())
        Inv.invload = eval(file.readline())
        Inv.equip = eval(file.readline())
        Inv.charm_slot = eval(file.readline())
        Areas.area = eval(file.readline())
        Areas.spawnpoint = eval(file.readline())
        #讀取冷卻
        Player.cooldowns = eval(file.readline())
        Player.skill_cooldowns = eval(file.readline())
        #讀取刺客數據
        Assassin.level = eval(file.readline())
        Assassin.xp = eval(file.readline())
        Assassin.a_point = eval(file.readline())
        #讀取弓箭手數據
        Archer.level = eval(file.readline())
        Archer.xp = eval(file.readline())
        Archer.a_point = eval(file.readline())
        #讀取法師數據
        Mage.mana = eval(file.readline())
        Mage.level = eval(file.readline())
        Mage.xp = eval(file.readline())
        Mage.a_point = eval(file.readline())
        #讀取其他數據
        Forge.working = eval(file.readline())
        Forge.max_last_time = eval(file.readline())
        A_tree.rogue = eval(file.readline())
        A_tree.archer = eval(file.readline())
        A_tree.mage = eval(file.readline())
        A_tree.keybind = eval(file.readline())
        A_tree.specialization_unlock = eval(file.readline())
        Portal.unlock = eval(file.readline())
        Quest.tracking = eval(file.readline())
        Quest_01.stage = eval(file.readline())
        Quest_01.progressing = eval(file.readline())
        Quest_01.complete = eval(file.readline())
        Quest_02.stage = eval(file.readline())
        Quest_02.progressing = eval(file.readline())
        Quest_02.complete = eval(file.readline())
        Quest_03.stage = eval(file.readline())
        Quest_03.progressing = eval(file.readline())
        Quest_03.complete = eval(file.readline())
        Areas.cleared = eval(file.readline())
        Areas.lootchest = eval(file.readline())
        Areas.first = eval(file.readline())
        All_mobs.crack_wall_broken = eval(file.readline())
        Area6.cata_open = eval(file.readline())
        Area8.puzzle_complete = eval(file.readline())
        Area9.first_beat_boss = eval(file.readline())
        Area18.first_beat_boss = eval(file.readline())
        All_mobs.remove_lootchest = True
        Areas.changed = True
def inv_preload(file):
    try:
        with open("Save" + str(file) + ".txt", mode = "r", encoding = "utf-8") as file:
            file.readline()
            Save_load.time_preview = str(file.readline())[:-1]
            Save_load.player_name = file.readline()[:-1]
            Save_load.health_preview = eval(file.readline())
            file.readline()
            file.readline()
            file.readline()
            file.readline()
            inv_preview_temp = eval(file.readline())
            Inv.equip_preview = eval(file.readline())
            Inv.charm_slot_preview = eval(file.readline())
            Save_load.area_preview = eval(file.readline())
            file.readline()
            file.readline()
            file.readline()
            Save_load.assassin_level_preview = eval(file.readline())
            Save_load.assassin_xp_preview = eval(file.readline())
            file.readline()
            Save_load.archer_level_preview = eval(file.readline())
            Save_load.archer_xp_preview = eval(file.readline())
            file.readline()
            file.readline()
            Save_load.mage_level_preview = eval(file.readline())
            Save_load.mage_xp_preview = eval(file.readline())
            for item, count in inv_preview_temp.items():
                for i in range(len(Inv.preview)):
                    if Inv.preview[i]["name"] == item: Inv.preview[i]["count"] = count
            return False
    except:
        return True
#將角色加入群組
all_sprites = pygame.sprite.Group()
dmg_indicators = pygame.sprite.Group()
player_skills = pygame.sprite.Group()
arrows = pygame.sprite.Group()
magic_orbs = pygame.sprite.Group()
meteors = pygame.sprite.Group()
targets = pygame.sprite.Group()
water_bursts = pygame.sprite.Group()
mobs = pygame.sprite.Group()
items = pygame.sprite.Group()
lootchests = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
Areas.area = 1
Areas.areas = 20
Areas.spawn = True
Areas.cleared = {-7:False, -6:False, -5:False, -4:False, -3:False, -2:False, -1:False, 1:False, 2:False, 3:False, 4:False, 5:False, 6:False, 7:False, 8:False, 9:False, 10:False,
                    11:False, 12:False, 13:False, 14:False, 15:False, 16:False, 17:False, 18: False, 19: False}
Areas.first = {"破曉平原":False, "天空群島":False, "至黑深淵":False}
Areas.lootchest = {-7:0, -6:0, -5:1, -4:0, -2:0, -1:0, 1:1, 2:1, 3:0, 4:0, 5:0, 6:1, 7:0, 8:0, 9:0, 10:1,
                   11:0, 12:1, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0}
Areas.mob_killed = {-7:False, -6:False, -5:False, -4:False, -2:False, -1:False, 1:False, 2:False, 3:False, 4:False, 5:False, 6:False, 10:False,
                    11:False, 12:False, 13:False, 14:False, 15:False, 16:False, 17:False, 18:False, 19:False}
Areas.spawnpoint = 0
Areas.use = False
Areas.lock_right = False
Areas.lock_left = True
Areas.regen_lock = False
Areas.safe = False
Areas.changed = True
Areas.special_area = ""
Area6.cata_open = False
Area7.wave = 1
Area7.wave_clear = False
Area7.w_clock = 0
Area8.puzzle_complete = False
Area8.puzzle_rune_holding = 0
Area8.rune_slot = [0, 0, 0, 0, 0]
Area8.old_holding = 0
Area9.boss_summoned = False
Area9.first_beat_boss = True
Area11.x_velocity = 0
Area11.y_velocity = 0
Area12.falling = False
Area16.ascension_distant = 0
Area16.max_ascension_distant = 1500
Area16.ascension_time = 0
Area16.ascension_phase = ""
Area18.first_beat_boss = True
Area18.boss_summoned = False
Area18.stellaris_phase = 0
Area18.blight_area = 0
Area18.boss_claim_area = 0
Area18.stardust_remain = 0
Area18.aurora_attack = 0
Area18.blight_bomb_explode = False
Music.music = False
Stats.open = False
Stats.cate = 1
#玩家數據
Stats.basic = {}
Stats.bonus = {}
Stats.total = {}
Stats.charm = {}
Stats.info = "攻擊力"
A_tree.open = False
A_tree.cate = 1
A_tree.showing_info = ["刺客(Rouge)", "刺客是一個狡詐的職業，", "擅長使用詭計來偷襲敵人。", "永久被動技能 - 激流:", "觸發:使用技能後下一次普通攻擊", "消耗:無消耗", "效果:獲得持續5秒的激流狀態。","冷卻:0秒", "激流狀態", "激流狀態可強化終結技，","並決定使用次數。", "永久解鎖", 300, 480, 50, "職業"]
A_tree.node_img = ability_tree_rogue_node[0]
A_tree.moving = False
A_tree.gui_location_x = 0
A_tree.gui_location_y = 0
A_tree.mouse_temp_x = 0
A_tree.mouse_temp_y = 0
A_tree.lclick = False
A_tree.rogue = {"被動":1, "暗影脈衝":0, "重擊強化":0, "暗影襲擊":0, "暗影襲擊降低冷卻":0, "激流強化":0, "破空突擊":0, "次元斬 I":0, "破空突擊強化":0, "混沌匕首":0, "混沌匕首強化":0, "次元斬 II":0, "流放者":0, "聖騎士":0, "疾風行者":0, "幻影分身":0, "隱身":0, "刀舞":0, "無聲絞喉":0, "煙霧彈":0, "煙霧範圍提升":0}
A_tree.archer = {"被動":1, "火焰箭矢":0, "點燃":0, "苦無":0, "雙向苦無":0, "專注力強化":0}
A_tree.mage = {"被動":1, "隕石":0, "隕石增加傷害":0, "瞬水爆":0, "水爆延長":0, "水爆節省魔力":0}
A_tree.keybind = [{"W1":"", "E1":"", "R1":"", "W2":"", "E2":"", "R2":"", "Q":""}, {"W1":"", "E1":"", "R1":"", "W2":"", "E2":"", "R2":"", "Q":""}, {"W1":"", "E1":"", "R1":"", "W2":"", "E2":"", "R2":"", "Q":""}]
A_tree.row = 1
A_tree.skill_img = [
    {"暗影脈衝":rogue_skill1_img, "破空突擊":rogue_skill2_img, "次元斬 I":rogue_skill3_img, "混沌匕首":rogue_skill4_img, "幻影分身":rogue_skill5_img, "煙霧彈":rogue_skill6_img, "暗影襲擊":rogue_ultimate_img},
    {"火焰箭矢":archer_skill1_img, "苦無":archer_ultimate_img},
    {"隕石":mage_skill1_img, "瞬水爆":mage_ultimate_img}]
A_tree.specialization_unlock = {"rogue":{"流放者":False, "聖騎士":False, "疾風行者":False}, "archer":{"鷹眼":False, "魔箭手":False}, "mage":{"奧術師":False, "牧師":False}}
Save_load.selected = 1
Save_load.warning = 0
Save_load.health_preview = 0
Save_load.time_preview = ""
Save_load.area_preview = 0
Save_load.assassin_level_preview = 0
Save_load.assassin_xp_preview = 0
Save_load.archer_level_preview = 0
Save_load.archer_xp_preview = 0
Save_load.mage_level_preview = 0
Save_load.mage_xp_preview = 0
Player_location.disable_move = False
Player_location.disable_jump = False
Player_location.anti_gravity = False
Player_location.disable_ground = False
Player_location.dash_distance = 0
Player_location.midair_dash = 0
Player_location.x = 0
Player_location.y = 0
Player_location.coord_x = 0
Player_location.coord_y = 0
Player_location.background_moving = 0
Player_location.player_move = False
#冷卻
Player.cooldowns = {"health":0, "dash":0,
                    "rogue_riptide":0, "rogue_main":0, "暗影脈衝":0, "破空突擊":0, "rogue_skill_time":0, "次元斬 I":0, "混沌匕首":0, "幻影分身":0, "幻影分身持續時間":0, "隱身":0, "刀舞持續時間":0, "煙霧彈":0, "暗影襲擊":0, "暗影襲擊剩餘時間":0,
                    "archer_focus":0, "archer_main":0 ,"火焰箭矢":0, "苦無":0, "苦無剩餘時間":0,
                    "mage_mana":0, "mage_main":0, "隕石":0, "瞬水爆":0, "mage_water_burst":0,
                    "message":0, "title":0, "dialogue":0, "forge":0}
Player.skill_cooldowns = {"粗鐵劍":0, "木製弓":0, "基礎魔杖":0, "死靈收割之鐮":0, "銀月之刃":0, "秋日餽贈":0}
Game_time.minute = 0
Game_time.hour = 10
Info.open = False
Damage_to_player.damage = 0
Assassin.remove_chaos_dagger = False
Assassin.magic_enchant = 1
Assassin.ultimate_time = 0
Assassin.shadow_clone_location = (False, False)
Assassin.smite = False
Assassin.level = 1
Assassin.xp = 0
Assassin.xp_req = 0
Assassin.a_point = 0
Archer.focus = 0
Archer.focus_limit = 5
Archer.kunai_amount = 0
Archer.level = 1
Archer.xp = 0
Archer.xp_req = 0
Archer.a_point = 0
Mage.mana_limit = 100
Mage.mana = Mage.mana_limit
Mage.ultimate = False
Mage.level = 1
Mage.xp = 0
Mage.xp_req = 0
Mage.a_point = 0
All_mobs.kill = False
All_mobs.count = 0
All_mobs.remove_lootchest = False
All_mobs.coord_x = 0
All_mobs.nearest_x = -1
All_mobs.boss_fight_active = False
All_mobs.crack_wall_broken = False
Messages.text = [" ", " ", " ", " ", " "]
Title.text = [" ", " "]
Dialogue.text = [" ", " "]
Dialogue.name = [" ", " "]
Boss_skill_bar.bars = []
Hint.open = True
Quest.open = False
Quest.next_stage = False
Quest.skippable = False
Quest.tracking = 0
Player.name = "Player"
Inv.open = False
Inv.cate = 1
Inv.use = False
Inv.equip = {"sword":"", "bow":"", "wand":"", "helmet":"", "armor":"", "legs":"", "boots":"", "charm":[], "questItem":[], "hotbar":[""]}
Inv.charm_slot = [0, 3]
Inv.showing_charm = {"name":[], "img":[], "count":[]}
Inv.invload = []
Inv.equip_preview = copy.deepcopy(Inv.equip)
Inv.info_loc_x = 0
Inv.info_loc_y = 0
Inv.type = "normal"
Inv.inventory = [
    #武器
    {"name":"粗鐵劍", "itemType":"sword", "rarity":RARE, "img":item_iron_sword_img, "special":False, "count":1, "location":{"locationName":"鍛造 劍", "locationColor":GRAY}, "attribute":{"攻擊力":5}, "skill":{"skillName":"殘暴", "skillType":"主動技能", "skillTrigger":"S","skillCost":"無", "skillCD":10, "skillEffect":["立即使用普通攻擊", "並額外造成10點傷害"]}, "itemLore":[], "equip":True},
    {"name":"木製弓", "itemType":"bow", "rarity":RARE, "img":item_wooden_bow_img, "special":False, "count":1, "location":{"locationName":"鍛造 弓", "locationColor":GRAY}, "attribute":{"攻擊力":7}, "skill":{"skillName":"精準射擊", "skillType":"主動技能", "skillTrigger":"S","skillCost":"無", "skillCD":10, "skillEffect":["立即使用普通攻擊", "命中後獲得3點專注力"]}, "itemLore":[], "equip":True},
    {"name":"基礎魔杖", "itemType":"wand", "rarity":RARE, "img":item_wand_img, "special":False, "count":1, "location":{"locationName":"鍛造 魔杖", "locationColor":GRAY}, "attribute":{"攻擊力":8}, "skill":{"skillName":"治癒", "skillType":"主動技能", "skillTrigger":"S","skillCost":"30魔力", "skillCD":15, "skillEffect":["治癒30%最大生命"]}, "itemLore":[], "equip":True},
    {"name":"死靈收割之鐮", "itemType":"sword", "rarity":EPIC, "img":item_spirit_harvester_img, "special":True, "count":0, "location":{"locationName":"地下墓穴 鐮刀", "locationColor":GRAY}, "attribute":{"攻擊力":10}, "skill":{"skillName":"收割", "skillType":"主動技能", "skillTrigger":"S","skillCost":"無", "skillCD":15, "skillEffect":["10秒內的普通攻擊", "附帶10%吸血"]}, "itemLore":[], "equip":True},
    {"name":"銀月之刃", "itemType":"sword", "rarity":EPIC, "img":item_silvermoon_blade_img, "special":False, "count":0, "count":0, "location":{"locationName":"星界聖域 劍", "locationColor":TEAL}, "attribute":{"攻擊力":15, "防禦力":10}, "skill":{"skillName":"銀月之誓", "skillType":"主動技能", "skillTrigger":"S","skillCost":"無", "skillCD":15, "skillEffect":["隨機召喚5把銀騎士武器攻擊目標，", "每把造成10點傷害"]}, "itemLore":["這把長劍是銀騎士的象徵，", "代表著榮耀與正義。"], "equip":True},
    #護符
    {"name":"初階影脈護符", "itemType":"charm", "rarity":COMMON, "img":item_basic_shadow_charm, "special":False, "count":0, "location":{"locationName":"護符", "locationColor":YELLOW}, "attribute":{"重擊傷害%":10}, "charmSlot":1, "equip":True},
    {"name":"中階影脈護符", "itemType":"charm", "rarity":UNCOMMON, "img":item_intermediate_shadow_charm, "special":False, "count":0, "location":{"locationName":"護符", "locationColor":YELLOW}, "attribute":{"重擊傷害%":20}, "charmSlot":2, "equip":True},
    {"name":"高階影脈護符", "itemType":"charm", "rarity":RARE, "img":item_advanced_shadow_charm, "special":False, "count":0, "location":{"locationName":"護符", "locationColor":YELLOW}, "attribute":{"重擊傷害%":30}, "charmSlot":3, "equip":True},
    {"name":"初階空刃護符", "itemType":"charm", "rarity":COMMON, "img":item_basic_air_blade_charm, "special":False, "count":0, "location":{"locationName":"護符", "locationColor":YELLOW}, "attribute":{"破空突擊傷害%":10}, "charmSlot":1, "equip":True},
    {"name":"中階空刃護符", "itemType":"charm", "rarity":UNCOMMON, "img":item_intermediate_air_blade_charm, "special":False, "count":0, "location":{"locationName":"護符", "locationColor":YELLOW}, "attribute":{"破空突擊傷害%":20}, "charmSlot":2, "equip":True},
    {"name":"高階空刃護符", "itemType":"charm", "rarity":RARE, "img":item_advanced_air_blade_charm, "special":False, "count":0, "location":{"locationName":"護符", "locationColor":YELLOW}, "attribute":{"破空突擊傷害%":30}, "charmSlot":3, "equip":True},
    #貨幣
    {"name":"金幣", "itemType":"currency", "rarity":RARE, "img":item_coin_img, "special":False, "count":0, "location":{"locationName":"貨幣", "locationColor":GOLD}, "itemLore":["金幣是遊戲中最常見的貨幣", "這些閃亮的金幣被廣泛接受，", "可用於購買各種物品。"]},
    #戰利品
    {"name":"史萊姆黏液", "itemType":"loot", "rarity":COMMON, "img":item_slime_glue_img, "special":False, "count":0, "location":{"locationName":"戰利品", "locationColor":GRAY}, "itemLore":["透明而黏糊糊的物質"]},
    {"name":"骨頭", "itemType":"loot", "rarity":COMMON, "img":item_bone_img, "special":False, "count":0, "location":{"locationName":"戰利品", "locationColor":GRAY}, "itemLore":["乾燥且堅固的遺物"]},
    {"name":"樹枝", "itemType":"loot", "rarity":COMMON, "img":item_stick_img, "special":False, "count":0, "location":{"locationName":"戰利品", "locationColor":GRAY}, "itemLore":["適合用來製作武器手柄"]},
    {"name":"靈木碎片", "itemType":"loot", "rarity":UNCOMMON, "img":item_tree_frag_img, "special":False, "count":0, "location":{"locationName":"戰利品", "locationColor":GRAY}, "itemLore":["蘊含了大自然的靈氣和魔法能量"]},
    {"name":"腐爛肉塊", "itemType":"loot", "rarity":COMMON, "img":item_rotten_flesh_img, "special":False, "count":0, "location":{"locationName":"戰利品", "locationColor":GRAY}, "itemLore":["充斥著腐朽和死亡的氣息"]},
    {"name":"基礎礦石", "itemType":"loot", "rarity":UNCOMMON, "img":item_basic_ore_img, "special":False, "count":0, "location":{"locationName":"戰利品", "locationColor":GRAY}, "itemLore":["常見的礦物，加工後可製成武器和裝備"]},
    {"name":"鐵塊", "itemType":"loot", "rarity":UNCOMMON, "img":item_iron_ingot_img, "special":False, "count":0, "location":{"locationName":"戰利品", "locationColor":GRAY}, "itemLore":["由礦石精煉而成的金屬材料，用於打造基礎的武器和裝備"]},
    #消耗品
    {"name":"蜂蜜麵包", "itemType":"consumable", "rarity":UNCOMMON, "img":item_honey_bread_img, "special":False, "count":0, "location":{"locationName":"消耗品", "locationColor":YELLOW}, "attribute":{"生命回復t":"(0:03)"}, "itemLore":["柔軟的麵包淋上濃郁蜂蜜，吃下後可短暫回復生命。"], "eatRotate":315 ,"equip":True},
    {"name":"微風薄餅", "itemType":"consumable", "rarity":UNCOMMON, "img":item_breeze_cookie_img, "special":False, "count":0, "location":{"locationName":"消耗品", "locationColor":YELLOW}, "attribute":{"移動速度 + 20%t":"(1:00)"}, "itemLore":["酥脆的餅乾，一入口便化作微風般的清爽甜味。", "吃下它的人，腳步會變得如疾風般迅捷。 "], "eatRotate":0 ,"equip":True},
    {"name":"秋日餽贈", "itemType":"consumable", "rarity":RARE, "img":item_autumn_delicacy_img, "special":False, "count":0, "location":{"locationName":"消耗品", "locationColor":YELLOW}, "attribute":{"生命回復t":"(0:02)", "無限使用t":"", "冷卻時間t":"(0:05)"}, "itemLore":["以豐收的南瓜製成，帶有微妙的香料氣息，", "每一口都能感受到秋天的溫暖。"], "eatRotate":0 ,"equip":True},
    #任務道具
    {"name":"靈魂碎片", "itemType":"questItem", "rarity":EPIC, "img":item_soul_frag_img, "special":True, "count":0, "location":{"locationName":"黑暗勢力的威脅 任務道具", "locationColor":PURPLE}, "itemLore":["靈魂碎片擁有強大的靈魂能量，", "可以用來開啟地下墓穴的門，揭示著古老的秘密和寶藏。"]},
    {"name":"生命水晶", "itemType":"questItem", "rarity":LEGENDARY, "img":item_crystal_of_life_img, "special":True, "count":0, "location":{"locationName":"黑暗勢力的威脅 任務道具", "locationColor":PURPLE}, "attribute":{"生命上限%":30}, "itemLore":["紀念碑物品 1/7"], "equip":True},
    {"name":"力量水晶", "itemType":"questItem", "rarity":LEGENDARY, "img":item_crystal_of_strength_img, "special":True, "count":0, "location":{"locationName":"星疫之災 任務道具", "locationColor":TEAL}, "attribute":{"攻擊力%":30}, "itemLore":["紀念碑物品 2/7"], "equip":True},
    {"name":"極光之翼", "itemType":"questItem", "rarity":LEGENDARY, "img":item_aurora_wing_img, "special":True, "count":0, "location":{"locationName":"星疫之災 任務道具", "locationColor":TEAL}, "attribute":{"跳躍次數":1}, "itemLore":["蘊含天堂之力的光輝之翼", "當你展開它，七彩的光芒將照亮前方的道路", "引領你飛向更高的境界"], "equip":True},
    {"name":"腥紅刀片", "itemType":"questItem", "rarity":RARE, "img":item_crimson_blade_img, "special":False, "count":0, "location":{"locationName":"黑暗王座的終焉 任務道具", "locationColor":RED}, "itemLore":["將十個刀片交給鐵匠即可復原..."], "equip":False}
]
Inv.preview = [{k: (v.copy() if isinstance(v, pygame.Surface) else copy.deepcopy(v)) for k, v in item.items()} for item in Inv.inventory]
Inv.hotbar_index = 0
Inv.hotbar_selecting = False
Inv.hotbar_selection_timer = 0
Inv.selected_item = ""
Puzzle.open = False
Forge.open = False
Forge.cate = 1
Forge.selected = 1
Forge.working = 0
Forge.max_last_time = 0
Quest_01.progressing = False
Quest_01.complete = False
Quest_01.stage = 0
Quest_02.progressing = False
Quest_02.complete = False
Quest_02.dialogue = ["噢，你來了。我有一個重要的任務，你是否願意接受", "是否開啟主線任務:黑暗勢力的威脅?", "當然，市長。我願意幫助城鎮。", "很好。在城鎮之外，穿越森林，你將找到一片廢墟，而廢墟後有一座墓園", "那個廢墟是這個城鎮的前身，曾經遭受黑暗勢力的襲擊，現在變成了廢墟。", "墓園？那裡有什麼重要的事情嗎?", "在墓園內，有一個古老的地下墓穴，而裡面有一扇門，只有特殊的鑰匙才能打開。", "那鑰匙是什麼?", "這就是你的任務。你需要在廢墟中找到靈魂碎片，它是打開地下墓穴門的鑰匙。", "了解。還有別的嗎?", "當你進入地下墓穴，你會面對一些棘手的敵人。你的目標是討伐他們，取得生命水晶。", "生命水晶?", "是的，我們需要生命水晶來恢復這個城鎮的生機", "而且，我聽說，那些黑暗勢力的領袖持有一把古老但強力的武器。", "也許你能夠得到它。", "好的，我會嘗試的。", "勇者，城鎮的希望寄託在你身上。", "遇到困難不要怕，堅持微笑面對他!", "你帶著生命水晶回來了!這些怪物會不會很強大?", "「下次還填非常簡單!」", "好吧。總之，在你前往下個區域之前，曙光之城永遠歡迎你回來。", "這些金幣是作為你完成任務的獎勵。", "向著旅途的下一站前進!"]
Quest_02.stage = 0
Quest_03.progressing = False
Quest_03.complete = False
Quest_03.stage = 0
Quest_04.progressing = False
Quest_04.complete = False
Quest_04.stage = 0
Portal.open = False
Portal.unlock = {"曙光之城":True, "一號路口":False, "天堂":False}
Depth.floor = 1
Depth.room = 1
Depth.start = True
Depth.menu_open = False
Depth.blessing_menu = False
Depth.menu_type = 0
Depth.score = 0
Depth.spawn = False
Depth.current_room_name = ""
Depth.roll_room_type = False
Depth.room_info = {
    #起始房間
    "起始房間1":{"type":"開場事件", "floor":{1}, "effect":{}},
    #開場事件
    "廢棄下水道":{"type":"開場事件", "floor":{1}, "effect":{"民心值%":10, "警戒值%":10, "寶藏分":30, "祝福":1}, "enemy":[{"name":"大老鼠", "pos":(300, 400)}, {"name":"毒霧", "pos":(500, 450)}, {"name":"大老鼠", "pos":(800, 400)}], "info":"潛入充滿老鼠與毒霧的陰暗下水道，可以有效避免守衛以及發現寶藏"},
    "假扮商隊":{"type":"開場事件", "floor":{1}, "effect":{"民心值%":30, "警戒值%":20, "寶藏分":10, "情報值%":10}, "info":"偽裝成黑市的商人混入城內，雖有一些風險，但能獲得部分商人信任"},
    "攻擊守衛":{"type":"開場事件", "floor":{1}, "effect":{"民心值%":40, "警戒值%":50, "寶藏分":20, "情報值%":5}, "enemy":[{"name":"城門守衛", "pos":(700, 400)}, {"name":"城門守衛", "pos":(800, 400)}], "info":"直接與城門守衛交戰，可能使國王更加警戒，並大幅提振居民士氣"},
    #戰鬥
    "武器庫哨站":{"type":"戰鬥", "floor":{1, 2}, "effect":{"警戒值%":5, "寶藏分":10, "情報值%":5}, "enemy":[{"name":"城衛巡邏兵", "pos":(400, 500)}, {"name":"警戒槍兵", "pos":(700, 500)}, {"name":"爆破師", "pos":(600, 500)}], "info":"被守衛改建成防禦據點，敵人數量不多但裝備精良。"},
    "下層檢查站":{"type": "戰鬥","floor":{1, 2}, "effect": {"警戒值%": 3, "情報值%": 7},"enemy":[{"name":"城衛巡邏兵", "pos":(500, 500)}, {"name":"監督官", "pos":(600, 400)}], "info": "原為通行檢查哨，如今變成盤查反抗者的據點，監督官會優先呼叫援軍。"},
    "舊倉庫區": {"type": "戰鬥", "floor": {1, 2, 3}, "effect": {"寶藏分": 15, "警戒值%": 4}, "enemy": [{"name":"爆破師", "pos":(400, 550)}, {"name":"城衛巡邏兵", "pos":(600, 500)}, {"name":"城衛巡邏兵", "pos":(300, 520)}], "info": "封鎖的儲藏區藏有不少補給，守衛為防竊盜設下陷阱。"},
    "高架橋哨塔": {"type": "戰鬥", "floor": {2, 3}, "effect": {"情報值%": 10, "警戒值%": 5}, "enemy": [{"name":"警戒槍兵", "pos":(450, 300)}, {"name":"警械槍兵", "pos":(550, 250)}], "info": "哨塔提供絕佳視野，擊敗守軍可掌握周遭布局。"},
    "市集遺址": {"type": "戰鬥", "floor": {1, 2}, "effect": {"民心值%": 8, "寶藏分": 8}, "enemy": [{"name":"城衛巡邏兵", "pos":(500, 520)}, {"name":"流亡傭兵", "pos":(650, 540)}], "info": "曾經繁榮的市集如今被掌控，擊敗他們可贏得居民信任。"},
    "武裝儲藏通道": {"type": "戰鬥", "floor": {2, 3}, "effect": {"寶藏分": 12, "警戒值%": 6}, "enemy": [{"name":"城衛巡邏兵", "pos":(400, 500)}, {"name":"爆破師", "pos":(700, 550)}], "info": "通道內藏有軍火，敵人裝備沉重但動作緩慢。"},
    #事件
    "暗巷中的情報":{"type":"事件", "floor":{1, 2, 3}, "effect":{"民心值%":5, "警戒值%":5, "情報值%":10}, "info":"一位神秘居民在暗巷中向你透露王城的祕密"},
    "走失的小孩":{"type":"事件", "floor":{1, 2, 3}, "choice":{"幫助":{"民心值%":10, "警戒值%":5}, "離開":{"民心值%":-5}}, "info":"一名走失的孩子正在尋找家人，你願意幫助他嗎?"},
    "叛變守衛的交易":{"type":"事件", "floor":{1, 2, 3}, "choice":{"同意":{"警戒值%":-10, "寶藏分":-10, "情報值%":10}, "拒絕":{"警戒值%":10}}, "info":"一名守衛提出秘密交易，你可以用資金換取他關鍵的情報"},
    "提供居民資源":{"type":"事件", "floor":{1, 2, 3}, "effect":{"民心值%":15, "寶藏分":-5, "祝福":1}, "info":"提供居民必要的食物與資金"},
    "黑市商人的宣傳":{"type":"事件", "floor":{1, 2, 3}, "effect":{"民心值%":5, "寶藏分":5, "黑市%":100}, "info":"一名黑市商人塞給你一張帶有神秘的地點的紙條，希望與你交換秘寶"},
    #挑戰
    "燃燒試煉": {"type": "挑戰", "floor": {2, 3}, "effect": {"寶藏分": 10, "情報值%": 5}, "info": "火焰每十秒會蔓延一次，在限制時間內完成全部跳躍才能逃出。"},
    "隱形獵殺": {"type": "挑戰", "floor": {1, 2}, "effect": {"情報值%": 10, "警戒值%": -5}, "info": "房間中有一名潛伏敵人，需靠聲音與干擾物引誘其現身後擊殺，不能被其他守衛發現。"},
    "連擊試煉": {"type": "挑戰", "floor": {1, 2, 3}, "effect": {"寶藏分": 5, "民心值%": 5}, "info": "在不被擊中的狀況下完成10連擊，成功可讓居民相信你的力量。"},
    "禁技空間": {"type": "挑戰", "floor": {2, 3}, "effect": {"情報值%": -5, "民心值%":5}, "info": "該房間封鎖了技能，只能靠普攻與單體技作戰。"},
    "守衛時限": {"type": "挑戰", "floor": {1, 2, 3}, "effect": {"警戒值%": -5, "情報值%": 5}, "info": "房間中的鐘會在60秒內敲響，須在之前擊敗信使守衛阻止通報。"},
    #黑市
    "黑市": {"type": "黑市", "floor": {1, 2, 3}, "info": "機密情報、裝備的交易所，也可以購買籌碼抽取強大道具，其中不乏許多神秘的商人"},
    #魔王挑戰
    "魔王1":{"type":"魔王挑戰", "floor":{1}, "effect":{"民心值%":30, "警戒值%":30, "寶藏分":30}, "info":"與魔王1戰鬥"},
    "魔王2":{"type":"魔王挑戰", "floor":{2}, "effect":{"民心值%":40, "警戒值%":40, "寶藏分":40}, "info":"與魔王2戰鬥"},
    "魔王3":{"type":"魔王挑戰", "floor":{3}, "effect":{"寶藏分":50}, "info":"與魔王3戰鬥"},
}
Depth.room_type = {1:{}, 2:{}, 3:{}}
room_types = {"開場事件", "戰鬥", "事件", "挑戰", "黑市", "魔王挑戰"}
for i in range(1, 4):
    for types in room_types:
        Depth.room_type[i].update({types:[key for key, value in Depth.room_info.items() if isinstance(value, dict) and value.get("type") == types and i in value.get("floor")]})
#主動能力 [施放3次普通攻擊:0攻擊+10%/1防禦+10%/2生命+5%/3速度提升+10%/4冷卻-1秒/5魔力+5/6敵人抗性-10%/7護盾5% | 施放技能後:8物理傷+10%/9水傷加成+10%/10火傷加成+10%/11攻擊力100%範圍傷害/12提供護盾10%生命上限| 施放大招後:13冷卻-5秒/14攻擊力+30%/15生命+30%/16緩速3秒] 被動能力 [生命值低於20%:17產生爆炸每炸死1個敵人+10%生命/18無敵1秒+速度提升20%/18冷卻-80%/20獲得護盾80% | 被攻擊:21反彈20%傷害 | 怪物死亡:22攻擊力200%傷害範圍] 常駐能力 [23生命回復+10%/24護盾+10%/25掉落+20%/26掉落品質+10%]
Depth.blessings = [
    #三下普通攻擊觸發
    {"name":"毀滅之勢", "img":dd_blessing_atk, "trigger":"tripleMainAttack", "effects":{"攻擊力%":10}, "effectDuration":120 ,"rarity":0},
    {"name":"鋼鐵防線", "img":dd_blessing_def, "trigger":"tripleMainAttack", "effects":{"防禦力%":10}, "effectDuration":120, "rarity":0},
    {"name":"疾風行者", "img":dd_blessing_spd, "trigger":"tripleMainAttack", "effects":{"移動速度%":10}, "effectDuration":120, "rarity":0},
    #施放技能觸發
    {"name":"殘暴打擊", "img":dd_blessing_physical, "trigger":"castSkill", "effects":{"物理屬性傷害%":10}, "effectDuration":180, "rarity":0},
    {"name":"潮汐之怒", "img":dd_blessing_water, "trigger":"castSkill", "effects":{"水屬性傷害%":10}, "effectDuration":180, "rarity":0},
    {"name":"熾焰之舞", "img":dd_blessing_fire, "trigger":"castSkill", "effects":{"火屬性傷害%":10}, "effectDuration":180, "rarity":0},
    #施放終結技
    {"name":"扭曲時空", "img":dd_blessing_cd, "trigger":"castUltimate", "effects":{"回復冷卻回復":1}, "effectDuration":1, "rarity":0},
    {"name":"王者之怒", "img":dd_blessing_atk, "trigger":"castUltimate", "effects":{"攻擊力%":30}, "effectDuration":240, "rarity":0},
    {"name":"鋼鐵壁壘", "img":dd_blessing_def, "trigger":"castUltimate", "effects":{"防禦力%":30}, "effectDuration":240, "rarity":0},
    {"name":"毀滅震盪", "img":dd_blessing_explode, "trigger":"castUltimate", "effects":{"範圍傷害":100}, "effectDuration":1, "rarity":0},
    #生命低於20%
    {"name":"絕地反擊", "img":dd_blessing_atk, "trigger":"healthLow", "effects":{"範圍傷害":200}, "effectDuration":1, "rarity":0},
    {"name":"逃脫藝術", "img":dd_blessing_def, "trigger":"healthLow", "effects":{"防禦力%":float("inf")}, "effectDuration":60, "rarity":0},
    {"name":"逆轉命運", "img":dd_blessing_hpr, "trigger":"healthLow", "effects":{"冷卻回復":5}, "effectDuration":1, "rarity":0},
    #擊敗怪物
    {"name":"靈魂尖嘯", "img":dd_blessing_atk, "trigger":"killMob", "effects":{"攻擊力%":10}, "effectDuration":120, "rarity":0},
    {"name":"靈魂屏障", "img":dd_blessing_def, "trigger":"killMob", "effects":{"防禦力%":10}, "effectDuration":120, "rarity":0},
    #常駐能力
    {"name":"復甦之力", "img":dd_blessing_hpr, "trigger":"passive", "effects":{"生命回復":10}, "effectDuration":1, "rarity":0},
    {"name":"永恆壁障", "img":dd_blessing_def, "trigger":"passive", "effects":{"防禦力%":5}, "effectDuration":1, "rarity":0},
    {"name":"貪婪之爪", "img":dd_blessing_lbonus, "trigger":"passive", "effects":{"戰利品掉落%":20}, "effectDuration":1, "rarity":0},
    {"name":"命運餽贈", "img":dd_blessing_lquality, "trigger":"passive", "effects":{"戰利品品質%":10}, "effectDuration":1, "rarity":0}
]
Depth.blessings_order = [i["name"] for i in Depth.blessings]
Depth.blessing_quality_roll = 0
Depth.blessing_upgrade_level = 0
Depth.blessing_reading1 = 0
Depth.blessing_reading2 = 1
Depth.blessing_reading3 = 2
Depth.stats = {"民心值%":0, "警戒值%":0, "情報值%":0, "寶藏分":0, "黑市%":0, "祝福":0}
Depth.get_room_reward = False
Depth.multiplier = {"攻擊力%":0, "生命值%":0}
Trade.open = False
Trade.items = []
Trade.sidebar = {}
Trade.show_info = False
Trade.click = False
#商店
Trade.shops = {
            "刺客護符商人":
                [{"name":"中階影脈護符", "count":1, "cost":{"初階影脈護符": 2, "金幣": 30, "骨頭":5}, "total_limit":-1, "limit":-1}, 
                {"name":"高階影脈護符", "count":1, "cost":{"中階影脈護符":2, "金幣":50, "骨頭":10}, "total_limit":-1, "limit":-1},
                {"name":"中階空刃護符", "count":1, "cost":{"初階空刃護符": 2, "金幣": 30, "樹枝":5}, "total_limit":-1, "limit":-1},
                {"name":"高階空刃護符", "count":1, "cost":{"中階空刃護符":2, "金幣":50, "樹枝":10}, "total_limit":-1, "limit":-1}],
            "烘焙商人":
                [{"name":"蜂蜜麵包", "count":3, "cost":{"金幣":20}, "total_limit":-1, "limit":-1},
                {"name":"微風薄餅", "count":1, "cost":{"金幣":10}, "total_limit":-1, "limit":-1},
                {"name":"秋日餽贈", "count":1, "cost":{"金幣":500}, "total_limit":1, "limit":1}]
            }
Lootchest_info.exist = False
Lootchest_info.claimed = 0
menu = True
running = True
time = 0
second = 0
hovering_menu = False
hovering_stats = False
hovering_backpack = False
hovering_info = False
hovering_w_skill = False
hovering_e_skill = False
hovering_r_skill = False
hovering_s_skill = False
hovering_q_skill = False
background_location_x = 0
first_time_load_scrolling_background = True
hotbar_index_temp = True
#進入遊戲位置
teleport(0)
#遊戲迴圈
while running:
    if menu:
        close = show_menu()
        if close:
            break
        menu = False
    #更新玩家屬性
    update_stats()
    clock.tick(FPS)
    #取得游標位置
    Mouse.x, Mouse.y = pygame.mouse.get_pos()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    Mouse.x = (mouse_x - x_offset) / scale
    Mouse.y = (mouse_y - y_offset) / scale
    # 縮放並繪製到全螢幕視窗
    if FULLSCREEN:
        scaled_surface = pygame.transform.smoothscale(screen, (new_width, new_height))
        display.fill((0, 0, 0))  # 填充黑邊
        display.blit(scaled_surface, (x_offset, y_offset))
    #控制音樂
    try:
        if Music.music == True: pygame.mixer.music.unpause()
        if Music.music == False: pygame.mixer.music.pause()
    except:
        None
    #滾動式背景
    scrolling_background(first_time_load_scrolling_background)
    first_time_load_scrolling_background = False
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if player.holding["food"] == 0:
                if event.key == pygame.K_1: player.weapon = 1 #刺客
                if event.key == pygame.K_2: player.weapon = 2 #弓箭手
                if event.key == pygame.K_3: player.weapon = 3 #法師
                if event.key == pygame.K_w: player.skill(A_tree.keybind[player.weapon - 1]["W" + str(A_tree.row)])
                if event.key == pygame.K_e: player.skill(A_tree.keybind[player.weapon - 1]["E" + str(A_tree.row)])
                if event.key == pygame.K_r: player.skill(A_tree.keybind[player.weapon - 1]["R" + str(A_tree.row)])
                if event.key == pygame.K_s and Inv.selected_item != "": player.use_item(Inv.selected_item) #使用物品
                if event.key == pygame.K_q: player.ultimate() #終結技
            if event.key == pygame.K_f: Areas.use = True #使用
            if event.key == pygame.K_z: Damage_to_player.damage += 10000 #自殺
            if event.key == pygame.K_k:#檢查傷害/查看滑鼠位置
                print(Mouse.x, Mouse.y)
                # for attack in player.attacks:
#                     print(f"""
# 位置: ({attack[0]}, {attack[1]})
# 半徑: {attack[2]}
# 傷害: {attack[3]}
# 屬性: {attack[4]}
# 編號: {attack[5]}
# 來源: {attack[6]}
# 持續時間: {attack[7]}
# 擊退距離: {attack[8]}
# 效果: {attack[9]}
# 效果持續時間: {attack[10]}
# --------------------
# """)
            if event.key == pygame.K_ESCAPE:#選單
                menu = True
            if event.key == pygame.K_i:#物品欄
                Inv.open = True
                Inv.type = "normal"
                menu = True
            if event.key == pygame.K_c:#角色屬性
                Stats.open = True
                menu = True
            if event.key == pygame.K_F3:#角色屬性
                if Info.open == False:
                    Info.open = True
                else:
                    Info.open = False
            if event.key == pygame.K_b and Areas.area == -7:
                Depth.blessing_menu = True
                menu = True
            if event.key == pygame.K_t and Player.cooldowns["message"] == 0:
                Player.cooldowns["message"] = 100
            elif event.key == pygame.K_t and Player.cooldowns["message"] != 0:
                Player.cooldowns["message"] = 0
            if event.key == pygame.K_v:
                Hint.open = not Hint.open
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player.jump_height = 0
                player.jump_time -= 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2: A_tree.row = 3 - A_tree.row
            if event.button in (4, 5) and any(Inv.equip["hotbar"]):  # 滾輪事件發生時
                original_index = Inv.hotbar_index  # 記錄當前 hotbar_index，避免無限循環
                direction = -1 if event.button == 4 else 1  # 4=向上滾，5=向下滾
                while True:
                    # 變更 hotbar_index，確保循環
                    Inv.hotbar_index = (Inv.hotbar_index + direction) % len(Inv.equip["hotbar"])
                    # 確保當前選擇的是有效物品
                    if Inv.equip["hotbar"][Inv.hotbar_index] != "": break  # 找到有效物品則停止
                    # 如果繞了一圈仍然找不到有效物品，則保持原位
                    if Inv.hotbar_index == original_index: break
                # 設定選擇標誌，開始計時
                Inv.hotbar_selecting = True
                Inv.hotbar_selection_timer = 0
        press_button = pygame.mouse.get_pressed()
        if (press_button[0]):
            if player.holding["food"] == 0:
                if hovering_w_skill: player.skill(A_tree.keybind[player.weapon - 1]["W" + str(A_tree.row)])
                elif hovering_e_skill: player.skill(A_tree.keybind[player.weapon - 1]["E" + str(A_tree.row)])
                elif hovering_r_skill: player.skill(A_tree.keybind[player.weapon - 1]["R" + str(A_tree.row)])
                elif hovering_s_skill and Inv.selected_item != "": player.use_item(Inv.selected_item) #使用物品
                elif hovering_q_skill: player.ultimate()
                else:
                    if Mouse.x > player.rect.x: player.facing = 1
                    if Mouse.x < player.rect.x: player.facing = -1
                    player.main_attack()
            if hovering_menu: menu = True
            if hovering_stats:
                menu = True
                Stats.open = True
            if hovering_backpack:
                menu = True
                Inv.open = True
            if hovering_info:
                if Info.open == False:
                    Info.open = True
                else:
                    Info.open = False
        if (press_button[2]) and Player.cooldowns["dash"] == 0 and Player_location.disable_move == False and Player_location.midair_dash and player.holding["food"] == 0:
            Player_location.midair_dash -= 1
            Player.cooldowns["dash"] += 20
            Player_location.dash_distance += player.facing * 300
    #等級
    Assassin.xp_req = Assassin.level * 10 + 10
    Archer.xp_req = Archer.level * 10 + 10
    Mage.xp_req = Mage.level * 10 + 10
    if Assassin.xp >= Assassin.xp_req:
        Assassin.xp -= Assassin.xp_req
        Assassin.level += 1
        Assassin.a_point += 1
    if Archer.xp >= Archer.xp_req:
        Archer.xp -= Archer.xp_req
        Archer.level += 1
        Archer.a_point += 1 
    if Mage.xp >= Mage.xp_req:
        Mage.xp -= Mage.xp_req
        Mage.level += 1
        Mage.a_point += 1
    if Player.cooldowns["rogue_skill_time"] == 0 and Assassin.ultimate_time == 0: Assassin.smite = False
    if A_tree.archer["專注力強化"] > 0: Archer.focus_limit = 7
    else: Archer.focus_limit = 5
    #技能計時器
    for cd in Player.cooldowns:
        Player.cooldowns[cd] = max(0, Player.cooldowns[cd] - 1)
    for cd in Player.skill_cooldowns:
        Player.skill_cooldowns[cd] = max(0, Player.skill_cooldowns[cd] - 1)
    if player.holding["rise_sword"]: Player.cooldowns["破空突擊"] += 1
    if Player.cooldowns["幻影分身持續時間"]: Player.cooldowns["幻影分身"] += 1
    if Assassin.ultimate_time > 0: Player.cooldowns["暗影襲擊"] += 1
    if Archer.kunai_amount > 0: Player.cooldowns["苦無"] += 1
    if Mage.ultimate: Player.cooldowns["瞬水爆"] += 1
    #傷害
    for attack in player.attacks:
        attack[7] -= 1
        if attack[7] <= 0: player.attacks.remove(attack)
    #回血
    for effect in player.effects:
        if effect.get("name", False) == "生命回復":
            player.health = min(player.health + ((Stats.total["生命回復"] / 60)), player.health_limit)
    player.health = min(player.health, player.health_limit)
    #夜幕潛行
    if A_tree.rogue["流放者"] and Player.cooldowns["rogue_riptide"]: Player.cooldowns["rogue_riptide"] = min(Player.cooldowns["rogue_riptide"] + 1, 300)
    #專注力降低
    if Player.cooldowns["archer_focus"] == 0: Archer.focus = max(Archer.focus - 1 / 120, 0)
    #回魔
    if Player.cooldowns["mage_mana"] == 0:
        if Assassin.magic_enchant == 1:
            Mage.mana = min(Mage.mana + (Stats.total["魔力回復"] / 60), Mage.mana_limit)
        elif Assassin.magic_enchant > 1 and player.weapon == 1 and Mage.mana > 0:
            Mage.mana = max(Mage.mana - ((10 - A_tree.mage["水爆節省魔力"] * 2) / 60), 0)
        else:
            Assassin.magic_enchant = 1
        Player.cooldowns["mage_mana"] += 1
    #衝刺
    if Player_location.dash_distance != 0:
        if player.facing == 1: draw_img(screen, player_dash_right_img, player.rect.centerx - 80, player.rect.y + 120)
        if player.facing == -1: draw_img(screen, player_dash_left_img, player.rect.centerx, player.rect.y + 120)
        Damage_to_player.damage = 0
        if player.facing == 1 and not (Areas.lock_right and current_coord_x + 30 > 1000): teleport(Player_location.coord_x + 30 * player.facing)
        elif player.facing == -1 and not (Areas.lock_left and current_coord_x - 30 < 0): teleport(Player_location.coord_x + 30 * player.facing)
        Player_location.dash_distance -= 30 * player.facing
        if Player_location.dash_distance > 300 or Player_location.dash_distance < -300: Player_location.dash_distance = 0
    if time < 60:
        time += 1
    else:
        time = 0
        second += 1
    if second >= 1:
        second = 0
        if Area7.w_clock > 0: Area7.w_clock -= 1
    #玩家戰敗
    if player.health <= 0 or player.health_limit <= 0:
        if Depth.score < 1:
            teleport(Areas.spawnpoint)
        elif Areas.area == -7 and Depth.score > 0:
            Depth.location = 16
        if Area16.ascension_distant < 1500:
            Quest_03.stage = 6
            Area16.ascension_distant = 0
        All_mobs.kill = True
        All_mobs.remove_lootchest = True
        Areas.spawn = True
        Areas.changed = True
        All_mobs.boss_fight_active = False
        title("戰敗!", "小心怪物!")
        default()
    #是否進入安全區
    safe_zone = [2, 3, 11, 17]
    if Areas.area in safe_zone:
        Areas.safe = True
    else: Areas.safe = False
    #安全區
    if Areas.safe:
        if Areas.regen_lock == False:
            player.health = player.health_limit
            Mage.mana = Stats.total["魔力上限"]
        for areas in Areas.mob_killed:
            Areas.mob_killed[areas] = False
    #區域攻略檢測
    skip_areas = [-5, 0, 7, 8, 9, 10, 16]
    if Areas.lootchest[Areas.area] == 0 and Areas.area not in skip_areas: Areas.cleared[Areas.area] = True
    if 0 < Areas.area < 11:
        if Areas.first["破曉平原"]:
            title("發現區域 - 破曉平原")
            Areas.first["破曉平原"] = False
    elif 11 < Areas.area:
        if Areas.first["天空群島"]:
            title("發現區域 - 天空群島")
            Areas.first["天空群島"] = False
    #區域
    if Areas.area == -1:#城鎮中心
        #常駐事件
        Areas.lock_left = True
        Areas.lock_right = True
        pygame.display.set_caption("Finding The Light - 城鎮中心")
        if current_coord_x >= 730:
            teleport(-1270)
        option = summon_npc(-1300, 350, {"對話":"開啟任務"}, "市長", dmg_indicator_img)
        if option != None and option[0] == "對話":
            Quest.tracking = 2
            Quest.open = True
            menu = True
        if 0 <= current_coord_x <= 100:
            draw_img(screen, button_use_img, Player_location.x, 300)
            if Areas.use:
                teleport(1050)
                Areas.use = False
    if Areas.area == -2:#法師塔頂樓
        #常駐事件
        Areas.lock_left = True
        Areas.lock_right = True
        pygame.display.set_caption("Finding The Light - 法師塔頂樓")
        if 775 <= current_coord_x <= 825:
            draw_img(screen, button_use_img, 800, 300)
            if Areas.use:
                A_tree.gui_location_x = 0
                A_tree.gui_location_y = 0
                A_tree.open = True
                menu = True
                Areas.use = False
        if 400 <= current_coord_x <= 600:
            draw_img(screen, button_use_img, Player_location.x, 300)
            if Areas.use:
                teleport(1500)
                Areas.use = False
        if 50 <= current_coord_x <= 100:
            draw_img(screen, button_use_img, 75, 300)
            if Areas.use:
                Portal.open = True
                menu = True
                Areas.use = False
        #每次觸發事件
        if Areas.spawn:
            Areas.spawn = False
    if Areas.area == -5:#曙光之城廢墟地下室
        #常駐事件
        Areas.lock_left = True
        Areas.lock_right = True
        pygame.display.set_caption("Finding The Light - 曙光之城廢墟地下室")
        if current_coord_x <= 30:
            draw_img(screen, button_use_img, 30, 300)
            if Areas.use:
                teleport(-6150)
                Areas.lock_left = True
                Areas.lock_right = True
                All_mobs.kill = True
                All_mobs.remove_lootchest = True
                Areas.use = False
        #攻略判定
        if Areas.spawn == False and All_mobs.crack_wall_broken and Areas.cleared[-5] == False and Areas.lootchest[-5] == 1 and Lootchest_info.exist != True:
            spawn_lootchest(900, GROUND - 30, 3, -5, [{"index":"靈魂碎片", "count":1}, {"index":"中階空刃護符", "count":1}])
            Lootchest_info.exist = True
        #每次觸發事件
        if Areas.spawn:
            if All_mobs.crack_wall_broken == False and Areas.cleared[-5] == False:
                summon_mob(740, GROUND - 235, 0, -5, "crack_wall")
            if  All_mobs.count == 0:
                summon_mob(750, GROUND + 30, 3, -5, "slime")
            Areas.spawn = False
    if Areas.area == -6:#曙光之城廢墟房屋
        #常駐事件
        Areas.lock_left = True
        Areas.lock_right = True
        pygame.display.set_caption("Finding The Light - 曙光之城廢墟房屋")
        All_mobs.kill = True
        option = summon_npc(-6750, 350, {"交易":"刺客護符商人", "對話":"2"}, "無鋒", rogue_charm_shop_img)
        if option != None and option[0] == "交易":
            Trade.items = option[1]
            Trade.sidebar = Trade.shops[Trade.items][0]
            Trade.open = True
            menu = True
            Areas.use = False
        if 825 <= current_coord_x <= 875:
            draw_img(screen, button_use_img, 850, 300)
            if Areas.use:
                teleport(-5950)
                Areas.spawn = True
                Areas.use = False
        if 450 <= current_coord_x <= 500:
            draw_img(screen, button_use_img, current_coord_x, 300)
            if Areas.use:
                teleport(4500)
                Areas.use = False
        Areas.spawn = False
    if Areas.area == -7:#至黑深淵
        Areas.lock_right = True
        Areas.lock_left = True
        #深淵讀取
        def load_depth():
            Depth.room = 1
            for blessing in Depth.blessings:
                blessing["rarity"] = 0
            Depth.stats = {"民心值%":0, "警戒值%":0, "情報值%":0, "寶藏分":0, "黑市%":0, "祝福":0}
            Depth.blessings_order = [i["name"] for i in Depth.blessings]
            random.shuffle(Depth.blessings_order)
            Depth.score = 0
            Depth.floor = 1
            Depth.current_room_name = "起始房間1"
            #臨時測試:魔王戰
            Depth.current_room_name = "魔王1"
            Depth.room = 10
            summon_mob(500, 400, 20, -7, "Samwell Calder")
            #測試結束
        
        if Depth.start:
            load_depth()
            Depth.start = False
        #常駐事件
        pygame.display.set_caption("Finding The Light - Darkest Depth " + str(Depth.floor) + " - " + str(Depth.room))
        #警戒值加成敵人數值
        Depth.multiplier["攻擊力%"] = 1 + round((Depth.stats["警戒值%"] / 100 ** 1.5), 2)
        Depth.multiplier["生命值%"] = 1 + Depth.stats["警戒值%"] // 10 * 0.05
        draw_img(screen, depth_room_background_img.get(Depth.current_room_name, area_background_imgs["0"]), 0, 0)
        #開場房間
        if Depth.room == 1 and Depth.floor == 1:
            option = summon_npc(-7800, 400, {"對話":"接續任務"}, "凱恩", kevin_1_img)
            if option != None and option[0] == "對話":
                Depth.get_room_reward = False
                Quest.tracking = 4
                Quest.open = True
                menu = True
                Areas.use = False
        else:
            room_info = Depth.room_info[Depth.current_room_name]
            selected_option = ""
            #生成敵人
            if Depth.spawn:
                if room_info.get("enemy"):
                    for enemy_info in room_info["enemy"]:
                        enemy_skill = {"毒霧"}
                        summon_mob(enemy_info["pos"][0], enemy_info["pos"][1], 12 + Depth.stats["警戒值%"] // 10, -7, enemy_info["name"], enemy_info["name"] not in enemy_skill)
                Depth.spawn = False
            #完成房間
            if All_mobs.count == 0 and Depth.get_room_reward == False:
                All_mobs.kill = True
                if room_info.get("effect"):
                    for effect, value in room_info["effect"].items():
                        Depth.stats[effect] += value
                elif room_info.get("choice") and selected_option != "":
                    for effect, value in room_info["choice"].get(selected_option).items():
                        Depth.stats[effect] += value
                Depth.get_room_reward = True
        for i in range(Depth.stats["祝福"]):
            Depth.stats["祝福"] -= 1
            Depth.menu_type = 1
            Depth.blessing_quality_roll = 2
            Depth.blessing_menu = True
            menu = True
        #開啟選關卡介面
        if 850 <= Player_location.x <= 950 and All_mobs.count == 0 and Areas.spawn and Quest_04.stage > 27:
            draw_img(screen, button_use_img, 900, 300)
        if Areas.use and All_mobs.count == 0 and Quest_04.stage > 27:
            if Depth.room != 16 and (Depth.room != 10 if Depth.floor == 3 else True) and 850 <= Player_location.x <= 950:
                Depth.roll_room_type = True
                Depth.menu_open = True
                menu = True
            elif Depth.room == 16:
                Areas.lock_right = False
                Areas.lock_left = False
                Depth.room = 1
                teleport(10500)
            if Depth.room == 10:
                title("挑戰成功!", "至黑深淵第" + str(Depth.floor) + "層")
                if Depth.floor < 3:
                    Depth.floor += 1
                    Depth.room = 1
                else: Depth.room = 16
            Areas.use = False
            upgradable_blessing_count = len([b for b in Depth.blessings if 0 < b["rarity"] < 5])
    if Areas.area == 1:#破曉平原
        #常駐事件
        pygame.display.set_caption("Finding The Light - 破曉平原")
        Areas.lock_left = True
        #攻略判定
        if Areas.spawn == False and Lootchest_info.exist != True and Areas.cleared[Areas.area] == False:
            spawn_lootchest(player.rect.x - (Player_location.coord_x - 600), GROUND + 100, 2, 1, [{"index":"初階影脈護符", "count":1}])
            Lootchest_info.exist = True
        #每次觸發事件
        if Areas.spawn and All_mobs.count == 0 and Areas.mob_killed[Areas.area] == False:
            switch_music(9)
            summon_mob(player.rect.x - (Player_location.coord_x - 600), GROUND, 1, 1, "slime")
            summon_mob(player.rect.x - (Player_location.coord_x - 700), GROUND, 1, 1, "slime")
            Areas.spawn = False
    if Areas.area == 2:#曙光之城
        #常駐事件
        pygame.display.set_caption("Finding The Light - 曙光之城")
        if 0 <= current_coord_x <= 100 and Areas.lock_right == False and Areas.lock_left == False:
            draw_img(screen, button_use_img, Player_location.x, 300)
            if Areas.use:
                teleport(-1500)
                All_mobs.kill = True
                All_mobs.remove_lootchest = True
                Areas.lock_left = True
                Areas.lock_right = True
                Areas.use = False
        if 450 <= current_coord_x <= 550 and Areas.lock_right == False and Areas.lock_left == False:
            draw_img(screen, button_use_img, Player_location.x, 300)
            if Areas.use:
                teleport(-2500)
                All_mobs.kill = True
                All_mobs.remove_lootchest = True
                Areas.lock_left = True
                Areas.lock_right = True
                Areas.use = False
        if 800 <= current_coord_x <= 850:
            draw_img(screen, button_use_img, 500, 300)
            if Areas.use:
                Quest.tracking = 1
                Quest.open = True
                menu = True
                Areas.use = False
        #攻略判定
        if Areas.spawn == False and Lootchest_info.exist != True and Areas.cleared[2] == False:
            spawn_lootchest(player.rect.x - (Player_location.coord_x - 1700), GROUND + 10, 1, 2)
            Lootchest_info.exist = True
        #每次觸發事件
        if Areas.spawn:
            Areas.spawnpoint = 1500
        Areas.spawn = False
    if Areas.area == 3:#曙光之城
        #常駐事件
        pygame.display.set_caption("Finding The Light - 曙光之城")
        if abs(Player_location.coord_x - 2700) < 100:
            draw_img(screen, button_use_img, player.rect.x, 300)
            if Areas.use:
                Trade.items = "烘焙商人"
                Trade.sidebar = Trade.shops[Trade.items][0]
                Trade.open = True
                menu = True
                Areas.use = False
        if 200 <= current_coord_x <= 250:
            draw_img(screen, button_use_img, Player_location.x, 300)
            if Areas.use:
                Forge.open = True
                menu = True
                Areas.use = False
        #每次觸發事件:無
        Areas.spawn = False
    if Areas.area == 4:#靜謐森林
        #常駐事件
        pygame.display.set_caption("Finding The Light - 靜謐森林")
        #每次觸發事件
        if Areas.spawn and All_mobs.count == 0 and Areas.mob_killed[Areas.area] == False:
            summon_mob(player.rect.x - (Player_location.coord_x - 3700), GROUND - 50, 3, 4, "skeleton")
            summon_mob(player.rect.x - (Player_location.coord_x - 3500), GROUND - 50, 3, 4, "tree_monster")
            Areas.spawn = False
        #攻略判定
        if Areas.spawn == False and Lootchest_info.exist != True and Areas.cleared[Areas.area] == False:
            spawn_lootchest(player.rect.x - (Player_location.coord_x - 3600), GROUND, 2, 4)
            Lootchest_info.exist = True
    if Areas.area == 5:#曙光之城廢墟
        #常駐事件
        pygame.display.set_caption("Finding The Light - 曙光之城廢墟")
        if 450 <= current_coord_x <= 500:
            draw_img(screen, button_use_img, Player_location.x, 300)
            if Areas.use:
                teleport(-6500)
                Areas.spawn = True
                All_mobs.kill = True
                All_mobs.remove_lootchest = True
                Areas.use = False
        #每次觸發事件
        if Areas.spawn and All_mobs.count == 0 and Areas.mob_killed[Areas.area] == False:
            summon_mob(player.rect.x - (Player_location.coord_x - 4650), GROUND, 4, 5, "skeleton")
            summon_mob(player.rect.x - (Player_location.coord_x - 4750), GROUND, 4, 5, "skeleton")
            Areas.spawn = False
    if Areas.area == 6:#墓園
        #常駐事件
        pygame.display.set_caption("Finding The Light - 墓園")
        if Area6.cata_open == False:
            Areas.lock_right = True
        else:
            Areas.lock_right = False
        if 850 <= current_coord_x <= 950 and Areas.cleared[6]:
            if Area6.cata_open != True:
                draw_img(screen, button_use_img, player.rect.x, 300)
            if Areas.use and Area6.cata_open == False and Quest_02.progressing == False and Quest_02.complete == False:
                new_message("請先接取任務:黑暗勢力的威脅")
            if Areas.use and Area6.cata_open == False and Quest_02.progressing:
                Quest.tracking = 2
                Quest.open = True
                menu = True
                Areas.use = False
        #攻略判定
        if Areas.spawn == False and Lootchest_info.exist != True and Areas.cleared[Areas.area] == False:
            spawn_lootchest(player.rect.x - (Player_location.coord_x - 5780), GROUND, 2, 6)
            Lootchest_info.exist = True
        #每次觸發事件
        if Areas.spawn and All_mobs.count == 0 and Areas.mob_killed[Areas.area] == False:
            summon_mob(player.rect.x - (Player_location.coord_x - 5650), GROUND - 30, 5, 6, "zombie")
            summon_mob(player.rect.x - (Player_location.coord_x - 5750), GROUND - 30, 5, 6, "zombie")
            Areas.spawn = False
    if Areas.area == 7:#地下墓穴大廳
        #常駐事件
        pygame.display.set_caption("Finding The Light - 地下墓穴大廳")
        if Areas.cleared[7] == False:
            Areas.lock_right = True
            Areas.lock_left = True
        if Area7.wave == 2 and Areas.cleared[7] == False:
            if Area7.w_clock > 0:
                title("Wave 2", "In " + str(Area7.w_clock) + "s")
            if Area7.w_clock == 0:
                title("Wave 2", " ")
        if Area7.wave == 3 and Areas.cleared[7] == False:
            if Area7.w_clock > 0:
                title("Wave 3", "In " + str(Area7.w_clock) + "s")
            if Area7.w_clock == 0 and Areas.cleared[7] == False:
                title("Wave 3", " ")
        #每次觸發事件
        if Area7.wave == 2 and Areas.cleared[7] == False:
            if Area7.w_clock > 0:
                title("Wave 2", "In " + str(Area7.w_clock) + "s")
            if Area7.w_clock == 0:
                title("Wave 2", " ")
        if Area7.wave == 3 and Areas.cleared[7] == False:
            if Area7.w_clock > 0:
                title("Wave 3", "In " + str(Area7.w_clock) + "s")
            if Area7.w_clock == 0 and Areas.cleared[7] == False:
                title("Wave 3", " ")
        if Areas.spawn:
            Area7.wave = 1
            if Area7.wave == 1 and Areas.cleared[7] == False:
                title("Wave 1", " ")
                summon_mob(player.rect.x - (Player_location.coord_x - 6150), GROUND - 30, 3, 7, "slime")
                summon_mob(player.rect.x - (Player_location.coord_x - 6250), GROUND - 30, 3, 7, "skeleton")
                Areas.spawn = False
        if Area7.w_clock == 0 and Area7.wave_clear:
            if Area7.wave == 2 and Areas.cleared[7] == False:
                summon_mob(player.rect.x - (Player_location.coord_x - 6150), GROUND - 30, 4, 7, "slime")
                summon_mob(player.rect.x - (Player_location.coord_x - 6350), GROUND - 30, 4, 7, "zombie")
                Area7.wave_clear = False
            if Area7.wave == 3 and Areas.cleared[7] == False:
                summon_mob(player.rect.x - (Player_location.coord_x - 6250), GROUND - 30, 4, 7, "skeleton")
                summon_mob(player.rect.x - (Player_location.coord_x - 6450), GROUND - 50, 4, 7, "tree_monster")
                Area7.wave_clear = False
        #攻略判定
        if All_mobs.count == 0 and Area7.wave == 1 and Area7.w_clock == 0:#第一波怪物判定
            Area7.wave_clear = True
            Area7.wave = 2
            Area7.w_clock = 3
        if  All_mobs.count == 0 and Area7.wave == 2 and Area7.w_clock == 0:#第二波怪物判定
            Area7.wave_clear = True
            Area7.wave = 3
            Area7.w_clock = 3
        if  All_mobs.count == 0 and Area7.wave == 3 and Area7.w_clock == 0:#第三波怪物判定
            Areas.cleared[7] = True
            Area7.wave_clear = True
            Areas.lock_right = False
            Areas.lock_left = False
    if Areas.area == 8:#地下墓穴符文鎖
        #常駐事件
        if Areas.cleared[8]:
            Areas.lock_right = False
        else:
            Areas.lock_right = True
        if 320 <= current_coord_x <= 430 and Area8.puzzle_complete == False:
            draw_img(screen, button_use_img, player.rect.x, 300)
            if Areas.use:
                Puzzle.open = True
                menu = True
                Areas.use = False
        #攻略判定
        if Area8.puzzle_complete:
            Areas.cleared[8] = True
        #每次觸發事件:無
        Areas.spawn = False
    if Areas.area == 9:#地下墓穴魔王房
        #常駐事件
        pygame.display.set_caption("Finding The Light - 地下墓穴魔王房")
        if Area9.boss_summoned == False and 450 <= current_coord_x <= 500:
            draw_img(screen, button_use_img, 500, 300)
            if Areas.use:
                Areas.lock_left = True
                Areas.lock_right = True
                summon_mob(WIDTH / 2 + 10, GROUND - 100, 10, 9, "xerath")
                switch_music(8)
                Area9.boss_summoned = True
                new_dialogue("你膽敢踏入我的領域，凡人?", "你的存在只會增加我的力量。", "Xerath", "暗影統治者")
                Areas.use = False
        if Area9.first_beat_boss:
            Areas.lock_right = True
        #攻略判定
        if Areas.spawn == False and Area9.boss_summoned and All_mobs.count == 0:
            Areas.lock_right = False
            Areas.lock_left = False
            Areas.cleared[9] = True
            Area9.boss_summoned = False
            All_mobs.boss_fight_active = False
        #每次觸發事件
        if Areas.spawn:
            Area9.boss_summoned = False
        Areas.spawn = False
    if Areas.area == 10:#地下墓穴獎勵房
        #常駐事件
        pygame.display.set_caption("Finding The Light - 地下墓穴獎勵房")
        #攻略判定
        if Areas.spawn == False and Areas.lootchest[10] == 0 and Areas.cleared[10] == False: Areas.cleared[10] = True
        #每次觸發事件
        if Areas.spawn and Lootchest_info.exist != True and Areas.cleared[10] == False:
            spawn_lootchest(player.rect.x - (Player_location.coord_x - 9520), GROUND - 20, 4, 10, [{"index":"生命水晶", "count":1}])
            Lootchest_info.exist = True
            Areas.spawn = False
    if Areas.area == 11:#一號路口
        #常駐事件
        pygame.display.set_caption("Finding The Light - 一號路口")
        Areas.lock_right = True
        if 0 <= current_coord_x <= 100:
            draw_img(screen, button_use_img, Player_location.x, 300)
            if Areas.use:
                Portal.open = True
                menu = True
                Areas.use = False
        #進入空島
        if 200 <= current_coord_x <= 400:
            draw_img(screen, button_use_img, Player_location.x, 300)
            if Areas.use:
                Player_location.disable_move = True
                Area11.x_velocity = 450
                Area11.y_velocity = 820
                Areas.use = False
        if Quest_04.stage <= 14:
            option = summon_npc(10600, 350, {"對話":"開啟任務"}, "夜刃", nightblade_1_img)
            if option != None and option[0] == "對話":
                Quest.tracking = 4
                Quest.open = True
                menu = True
        #進入深淵
        if 850 <= current_coord_x <= 950:
            draw_img(screen, button_use_img, Player_location.x, 300)
            if Areas.use:
                teleport(-7500)
                Depth.start = True
                All_mobs.kill = True
                Areas.spawn = False
                Areas.use = False
        #每次觸發事件:無
        Areas.spawn = False
    if Areas.area == 12:#天空群島1
        #常駐事件
        pygame.display.set_caption("Finding The Light - 天空群島")
        Areas.lock_left = True
        if current_coord_x < 240 and player.rect.y >= GROUND - 50 and Area12.falling == False:
            Areas.changed = True
            Area12.falling = True
            player.rect.y = 0
            player.velocity = 0
        if Area12.falling:
            Areas.lock_right = True
            Areas.lock_left = True
            All_mobs.kill = True
            All_mobs.remove_lootchest = True
            Player_location.disable_ground = True
        if player.rect.y > 700 and Area12.falling:
            Area12.falling = False
            Player_location.disable_ground = False
            teleport(10300)
            player.rect.y = 0
        #攻略判定
        if Areas.spawn == False and Lootchest_info.exist != True and Areas.cleared[12] == False:
            spawn_lootchest(player.rect.x - (Player_location.coord_x - 11650), GROUND + 100, 2, 12)
            Lootchest_info.exist = True
        #每次觸發事件
        if Areas.spawn and All_mobs.count == 0 and Areas.mob_killed[Areas.area] == False:
            summon_mob(player.rect.x - (Player_location.coord_x - 11800), 150, 10, 12, "skywing_beast")
            summon_mob(player.rect.x - (Player_location.coord_x - 11700), GROUND, 6, 12, "slime")
            Areas.spawn = False
    if Areas.area == 13:#天空群島2
        #常駐事件
        pygame.display.set_caption("Finding The Light - 天空群島")
        Player_location.disable_ground = (690 < current_coord_x < 800)
        if player.rect.y >= GROUND:
            teleport(11000)
            player.rect.y = GROUND
        #每次觸發事件
        if Areas.spawn and All_mobs.count == 0 and Areas.mob_killed[Areas.area] == False:
            summon_mob(player.rect.x - (Player_location.coord_x - 12500), 400, 11, 13, "cursed_silver_knight")
            Areas.spawn = False
    if Areas.area == 14:#天空群島3
        #常駐事件
        pygame.display.set_caption("Finding The Light - 天空群島")
        Player_location.disable_ground = (current_coord_x < 240 or current_coord_x > 920)
        if player.rect.y > GROUND:
            teleport(11000)
            player.rect.y = GROUND
        #每次觸發事件
        if Areas.spawn and All_mobs.count == 0 and Areas.mob_killed[Areas.area] == False:
            summon_mob(player.rect.x - (Player_location.coord_x - 13300), 200, 12, 14, "skywing_beast")
            summon_mob(player.rect.x - (Player_location.coord_x - 13700), 200, 12, 14, "thunder_cloud")
            Areas.spawn = False
    if Areas.area == 15:#天空群島4
        #常駐事件
        pygame.display.set_caption("Finding The Light - 天空群島")
        Player_location.disable_ground = False
        #每次觸發事件
        if Areas.spawn and All_mobs.count == 0 and Areas.mob_killed[Areas.area] == False:
            summon_mob(player.rect.x - (Player_location.coord_x - 14500), 150, 15, 15, "thunder_dragon")
            summon_mob(player.rect.x - (Player_location.coord_x - 14300), 400, 13, 15, "cursed_silver_knight")
            Areas.spawn = False
    if Areas.area == 16:#天空群島5
        #常駐事件
        pygame.display.set_caption("Finding The Light - 天空群島")
        if Player_location.player_move and Area16.ascension_distant == 0 and Quest_03.stage < 12: draw_img(screen, aurora_1_img, 850, 400)
        elif Area16.ascension_distant == 0 and Quest_03.stage < 12: draw_img(screen, aurora_1_img, player.rect.x - (Player_location.coord_x - 15850), 400)
        if Area16.ascension_distant < 1480 or Area16.ascension_distant == 0:
            Areas.lock_right = True
        if Player_location.coord_x > 15830 and Area16.ascension_distant == 0 and Quest_03.stage < 12: teleport(15830)
        if 770 < player.rect.centerx and Area16.ascension_distant == 0 and Quest_03.stage < 12:
            option = summon_npc(15830, 350, {"對話":"開啟任務"}, "Aurora", dmg_indicator_img)
            if option != None and option[0] == "對話":
                Quest.tracking = 3
                Quest.open = True
                menu = True
        #任務動畫
        if Quest_03.stage == 10 and player.rect.y >= 0 and Area16.ascension_distant == 0:
            player.flying = True
            player.rect.y -= 10
            Player_location.anti_gravity = True
            Player_location.disable_move = True
        if Quest_03.stage == 10 and player.rect.y < 0:
            Player_location.disable_move = False
            Area16.ascension_distant = 1
            Areas.changed = True
            Quest_03.stage += 1
            player.rect.y = 600
            All_mobs.boss_fight_active = True
            Areas.lock_left = True
            switch_music(10, 1)
            summon_mob(random.randint(0, 500), random.randint(0, 300), 1, 16, "cloud", False)
            summon_mob(random.randint(500, 1000), random.randint(300, 400), 1, 16, "cloud", False)
        if Quest_03.stage == 11:
            if player.rect.y > 425: player.rect.y = max(425, player.rect.y - 10)
            #開始上升
            if player.rect.y != 425 and Area16.ascension_distant < 1490: player.rect.y = 425
            Area16.ascension_distant = min(1500, Area16.ascension_distant + 1 / 6)
            progress_bar(Area16.ascension_distant, Area16.max_ascension_distant, "上升距離", "階段: " + Area16.ascension_phase, "m", BLUE, PURPLE, LBLUE)
            Area16.ascension_time += 1 
            #產生掉落物件
            #雲
            if Area16.ascension_time % 30 == 0:
                summon_mob(random.randint(0, 500), random.randint(-500, -100), 1, 16, "cloud")
            #掉落物
            if Area16.ascension_time % 60 == 0 and Area16.ascension_distant < 1480:
                summon_mob(random.randint(0, 500), random.randint(-500, -100), 1, 16, "falling_" + choose(falling_items), False)
                summon_mob(random.randint(500, 1000), random.randint(-500, -100), 1, 16, "falling_" + choose(falling_items), False)
                summon_mob(random.randint(300, 700), random.randint(-500, -100), 1, 16, "falling_" + choose(falling_items), False)
            #階段1: Ascension
            if round(Area16.ascension_distant) == 1: title("PART I", "Ascension")
            if 0 < Area16.ascension_distant < 600:
                Area16.ascension_phase = "Ascension"
                falling_items = {"rock":34, "stick":33, "brick":33}
            #階段2: Encounter
            if round(Area16.ascension_distant) == 600: title("PART II", "Encounter")
            if 600 < Area16.ascension_distant < 1000:
                Area16.ascension_phase = "Encounter"
                falling_items = {"rock":20, "stick":20, "brick":20, "star_raindrop":20, "log":20}
            #階段3: Trials
            if round(Area16.ascension_distant) == 1000: title("PART III", "Trials")
            if 1000 < Area16.ascension_distant < 1200:
                Area16.ascension_phase = "Trials"
                falling_items = {"rock":10, "stick":10, "brick":10, "star_raindrop":20, "meteor":20, "log":30}
            #階段4: Ultimate Ascension
            if round(Area16.ascension_distant) == 1200: title("PART IV", "Ultimate Ascension")
            if 1200 < Area16.ascension_distant < 1400:
                Area16.ascension_phase = "Ultimate Ascension"
                falling_items = {"rock":5, "stick":5, "brick":5, "star_raindrop":10, "meteor":25, "log":30, "pillar":20}
            #階段5: Paradise
            if round(Area16.ascension_distant) == 1400: title("PART V", "Paradise")
            if 1400 < Area16.ascension_distant < 1480:
                Area16.ascension_phase = "Paradise"
                falling_items = {"rock":5, "stick":5, "brick":5, "star_frag":25, "meteor":20, "log":20, "pillar":20}
            if Player_location.coord_x < 16000 and round(Area16.ascension_distant) == 1490:
                Areas.lock_right = False
                Player_location.disable_move = True
                teleport(15500)
                area16_2_img = pygame.image.load(os.path.join("resource", "area16_2.png")).convert()
            if Player_location.coord_x < 16000 and round(Area16.ascension_distant) > 1490:
                teleport(Player_location.coord_x + 5)
                player.rect.y -= 5
                background_location_y = max(background_location_y - 5, -300)
                draw_img(screen, area16_2_img, background_location_x + 1000, 600 + background_location_y)
    if Areas.area == 17:#天堂
        #常駐事件
        pygame.display.set_caption("Finding The Light - 天堂")
        Areas.lock_left = True
        if 0 <= current_coord_x <= 100:
            draw_img(screen, button_use_img, Player_location.x, 300)
            if Areas.use:
                Portal.open = True
                menu = True
                Areas.use = False
        #進入天堂
        if Area16.ascension_distant >= 1500 and Quest_03.stage == 11:
            background_location_y = 0
            Quest_03.stage += 1
            player.flying = False
            All_mobs.boss_fight_active = False
            Player_location.anti_gravity = False
            Player_location.disable_move = False
            Player_location.disable_jump = False
        Areas.spawn = False
    if Areas.area == 18 or Areas.area == 19:#星界聖域1
        #常駐事件
        #顯示NPC
        draw_img(screen, aurora_2_img, player.rect.x - (Player_location.coord_x - 17010), GROUND - 120)
        draw_img(screen, tuleen_img, player.rect.x - (Player_location.coord_x - 17200), GROUND - 120)
        draw_color_text(screen, "[Aurora]", 20, player.rect.x - (Player_location.coord_x - 17080), GROUND - 150, LBLUE)
        draw_color_text(screen, "[Tuleen]", 20, player.rect.x - (Player_location.coord_x - 17250), GROUND - 150, RED)
        if Player_location.coord_x < 17100 and Quest_03.stage != 31:
            draw_img(screen, button_use_img, player.rect.x - (Player_location.coord_x - 17040), 250)
            if Areas.use:
                if All_mobs.boss_fight_active:
                    new_dialogue("現在可不是閒聊的時候! 我們還得對付令使!", "", "Aurora", "魔法師")
                if All_mobs.boss_fight_active == False and Quest_03.stage != 31:
                    Quest.tracking = 3
                    Quest.open = True
                    menu = True
                Areas.use = False
        pygame.display.set_caption("Finding The Light - 星界聖域")
        #召喚 星辰令使 - Stellaris
        def summon_stellaris():
            All_mobs.boss_fight_active = True
            Area18.boss_summoned = True
            summon_mob(player.rect.x - (Player_location.coord_x - 17600), -100, 20, 18, "Stellaris")
            switch_music(11)
        if Area18.first_beat_boss and Player_location.coord_x > 17400 and Area18.boss_summoned == False and Quest_03.stage == 31: summon_stellaris()
        if All_mobs.boss_fight_active and Areas.area == 18: Areas.lock_left = True
        elif Area18.boss_summoned == False and 17400 < Player_location.coord_x < 17500 and Area18.first_beat_boss == False:
            draw_img(screen, button_use_img, player.rect.x, 300)
            if Areas.use:
                summon_stellaris()
                Areas.use = False 
        #佔領進度
        if All_mobs.boss_fight_active and Area18.stellaris_phase != 2:
            progress_bar(Area18.blight_area // 10, 1000 // 10, "Stellaris", "星辰令使", "%", TEAL, PURPLE, BLUE)
            draw_img(screen, aurora_2_img, player.rect.x - (Player_location.coord_x - 17010), GROUND - 120)
            draw_img(screen, tuleen_img, player.rect.x - (Player_location.coord_x - 17200), GROUND - 120)
        #每次觸發事件
        if Areas.spawn:
            Area18.boss_summoned = False
            Areas.spawn = False
    if Areas.area == 19:#星界聖域2
        #常駐事件
        Areas.lock_right = True
        if Player_location.coord_x > 18200: teleport(18200)
    Lootchest_info.exist = False
    all_sprites.update()
    all_sprites.draw(screen)
    if All_mobs.count == 0 and Areas.spawn == False: Areas.mob_killed[Areas.area] = True
    All_mobs.kill = False
    All_mobs.coord_x = 0
    All_mobs.remove_lootchest = False
    Areas.use = False
    #右上快捷圖標
    if All_mobs.boss_fight_active == False:
        draw_img(screen, icon_menu_img, 900, 10)
        draw_img(screen, icon_backpack_img, 820, 10)
        draw_img(screen, icon_stats_img, 740, 15)
        draw_img(screen, icon_info_img, 660, 10)
        draw_color_text(screen, "[F3]", 20, 690, 70, BLACK)
        hovering_menu = is_hovering(920, 970, 20, 70, Mouse.x, Mouse.y)
        hovering_backpack = is_hovering(820, 900, 10, 70, Mouse.x, Mouse.y)
        hovering_stats = is_hovering(740, 800, 10, 60, Mouse.x, Mouse.y)
        hovering_info = is_hovering(660, 720, 10, 70, Mouse.x, Mouse.y)
    #快捷欄
    if player.health > 0 and player.health_limit > 0:
        draw_img(screen, hotbar_img, 0, 600)
        draw_color_text(screen, Player.name, 20, 370, 610, LBLUE)
        draw_passive_bar(screen, player.health * 60, player.health_limit * 60, 170, 665, RED, "生命值")
    hovering_w_skill = is_hovering(450, 540, 630, 720, Mouse.x, Mouse.y)
    hovering_e_skill = is_hovering(560, 650, 630, 720, Mouse.x, Mouse.y)
    hovering_r_skill = is_hovering(670, 760, 630, 720, Mouse.x, Mouse.y)
    hovering_s_skill = is_hovering(780, 870, 630, 720, Mouse.x, Mouse.y)
    hovering_q_skill = is_hovering(890, 980, 630, 720, Mouse.x, Mouse.y)
    #畫出W技能
    if A_tree.keybind[player.weapon - 1]["W" + str(A_tree.row)] != "":
        draw_color_text(screen, str("W"), 20, 490, 725, WHITE)
        draw_img(screen, A_tree.skill_img[player.weapon - 1][A_tree.keybind[player.weapon - 1]["W" + str(A_tree.row)]], 447, 630)
        draw_color_text(screen, str(round(Player.cooldowns[str(A_tree.keybind[player.weapon - 1]["W" + str(A_tree.row)])] / 60, 1)) if Player.cooldowns[str(A_tree.keybind[player.weapon - 1]["W" + str(A_tree.row)])] / 60 else "", 30, 490, 660, WHITE)
    #畫出E技能
    if A_tree.keybind[player.weapon - 1]["E" + str(A_tree.row)] != "":
        draw_color_text(screen, str("E"), 20, 600, 725, WHITE)
        draw_img(screen, A_tree.skill_img[player.weapon - 1][A_tree.keybind[player.weapon - 1]["E" + str(A_tree.row)]], 557, 630)
        draw_color_text(screen, str(round(Player.cooldowns[str(A_tree.keybind[player.weapon - 1]["E" + str(A_tree.row)])] / 60, 1)) if Player.cooldowns[str(A_tree.keybind[player.weapon - 1]["E" + str(A_tree.row)])] / 60 else "", 30, 600, 660, WHITE)
    #畫出R技能
    if A_tree.keybind[player.weapon - 1]["R" + str(A_tree.row)] != "":
        draw_color_text(screen, str("R"), 20, 710, 725, WHITE)
        draw_img(screen, A_tree.skill_img[player.weapon - 1][A_tree.keybind[player.weapon - 1]["R" + str(A_tree.row)]], 667, 630)
        draw_color_text(screen, str(round(Player.cooldowns[str(A_tree.keybind[player.weapon - 1]["R" + str(A_tree.row)])] / 60, 1)) if Player.cooldowns[str(A_tree.keybind[player.weapon - 1]["R" + str(A_tree.row)])] / 60 else "", 30, 710, 660, WHITE)
    #畫出S技能(裝備欄)
    if any(Inv.equip["hotbar"]):
        # 更新武器：若有裝備武器則更新 hotbar[0]，否則設為 ""
        if Inv.equip["sword"] and player.weapon == 1: Inv.equip["hotbar"][0] = Inv.equip["sword"]
        elif Inv.equip["bow"] and player.weapon == 2: Inv.equip["hotbar"][0] = Inv.equip["bow"]
        elif Inv.equip["wand"] and player.weapon == 3: Inv.equip["hotbar"][0] = Inv.equip["wand"]
        else: Inv.equip["hotbar"][0] = ""
    
        filtered_hotbar = [item for item in Inv.equip["hotbar"] if item != "" and search_item(item)["count"] > 0]
        # 如果 hotbar[0] 是空的，則確保 [""] 仍然在前面
        if Inv.equip["hotbar"][0] == "": Inv.equip["hotbar"] = [""] + filtered_hotbar
        else: Inv.equip["hotbar"] = filtered_hotbar
        # 如果 hotbar 變空，則強制設為 [""] 以避免錯誤
        if not Inv.equip["hotbar"]: Inv.equip["hotbar"] = [""]
        # 如果選中的物品被移除，則 hotbar_index 需要調整
        if Inv.hotbar_index >= len(Inv.equip["hotbar"]): Inv.hotbar_index = max(0, len(Inv.equip["hotbar"]) - 1)  # 防止 hotbar_index 超出範圍

         # 計算有效物品數量（不包括 hotbar[0] 的空佔位符）
        hotbar_item_count = len([item for item in Inv.equip["hotbar"] if item != ""])
        # 取得目前選中的物品，並處理找不到物品的情況
        Inv.selected_item = search_item(Inv.equip["hotbar"][Inv.hotbar_index])

        # 若當前選擇的物品無效，則嘗試選擇下一個
        if not Inv.selected_item or Inv.selected_item == "":
            original_index = Inv.hotbar_index  # 記錄原始 hotbar_index，避免死循環
            while True:
                if hotbar_item_count:
                    Inv.hotbar_index = (Inv.hotbar_index + 1) % hotbar_item_count  # 選擇下一個物品（環繞）
                # 若找到有效物品，則跳出迴圈
                if Inv.selected_item and Inv.selected_item != "": break
                # 如果回到了原始選擇的 index，表示整個 hotbar 都是空的，則停止
                if Inv.hotbar_index == original_index:
                    Inv.selected_item = ""  # 設定為空，表示 hotbar 內無可用物品
                    break
            hotbar_update = True  # 確保後續更新 hotbar 狀態
            Inv.selected_item = search_item(Inv.equip["hotbar"][Inv.hotbar_index] if Inv.equip["hotbar"][0] else Inv.equip["hotbar"][Inv.hotbar_index + 1])
        # 僅在 hotbar_index、player.weapon、hotbar內容變更或 hotbar_update 為 True 時更新 s_skill_img
        if Inv.selected_item and (hotbar_index_temp != Inv.hotbar_index or class_temp != player.weapon or hotbar_temp != Inv.equip["hotbar"] or hotbar_update):
            s_skill_img = Inv.selected_item["img"].convert().copy()
            s_skill_img.set_colorkey(Inv.selected_item["rarity"])
            hotbar_update = False
            hotbar_temp = Inv.equip["hotbar"].copy()

        # 更新暫存變數
        hotbar_index_temp = Inv.hotbar_index
        class_temp = player.weapon

        # 繪製大框及主要道具顯示
        if Inv.selected_item and Inv.selected_item["img"]:
            draw_img(screen, s_skill_img, 780, 630)
            draw_color_text(screen, "S", 20, 820, 725, WHITE)
            if Inv.selected_item["itemType"] == "consumable": outline_text("  " + str(Inv.selected_item["count"]) if "無限使用t" not in Inv.selected_item.get("attribute", []) else "∞", 40, 820 - (25 if Inv.selected_item["count"] >= 10 else 5), 620, WHITE)
            # 顯示冷卻時間
            s_skill_cd = Player.skill_cooldowns.get(Inv.selected_item["name"], 0)
            if s_skill_cd > 0: draw_color_text(screen, str(round(s_skill_cd / 60, 1)), 30, 820, 660, WHITE)

        # 顯示小框（如果在選擇模式中）
        if Inv.hotbar_selecting:
            Inv.hotbar_selection_timer = min(Inv.hotbar_selection_timer + 1, 120)
            if Inv.hotbar_selection_timer == 120:
                Inv.hotbar_selecting = False
                hotbar_selection_timer = 0
            # 計算小框總寬度與起始 X 坐標（居中）
            total_width = hotbar_item_count * 40 + (hotbar_item_count - 1) * 1
            start_x = 820 - total_width // 2
            for i, item in enumerate(Inv.equip["hotbar"]):
                if item != "":
                    x = i if Inv.equip["hotbar"][0] else (i - 1)
                    pygame.draw.rect(screen, WHITE if i == Inv.hotbar_index else BLACK, (start_x + x * 50, 580, 40, 40), 4)
                    draw_img(screen, pygame.transform.scale(search_item(item)["img"], (36, 36)), start_x + 2 + x * 50, 582)
            # 如果條件變化，更新 s_skill_img
            if Inv.selected_item and (hotbar_index_temp != Inv.hotbar_index or class_temp != player.weapon or hotbar_update):
                s_skill_img = Inv.selected_item["img"].convert().copy()
                s_skill_img.set_colorkey(Inv.selected_item["rarity"])
                hotbar_update = False

        # 最後，確保在每次更新後 hotbar 正確保存使用完的物品不在列表中
        new_hotbar = [item for item in Inv.equip["hotbar"] if item == "" or search_item(item)["count"] > 0]
        Inv.equip["hotbar"] = new_hotbar
    #畫出Q技能
    if A_tree.rogue["暗影襲擊"] and player.weapon == 1:
        draw_color_text(screen, str("Q"), 20, 930, 722, WHITE)
        draw_img(screen, rogue_ultimate_img, 887, 640)
        draw_color_text(screen, str(round(Player.cooldowns["暗影襲擊"] / 60, 1)) if Player.cooldowns["暗影襲擊"] / 60 else "", 30, 930, 660, WHITE)
    if A_tree.archer["苦無"] and player.weapon == 2:
        draw_color_text(screen, str("Q"), 20, 930, 722, WHITE)
        draw_img(screen, archer_ultimate_img, 887, 640)
        draw_color_text(screen, str(round(Player.cooldowns["苦無"] / 60, 1)) if Player.cooldowns["苦無"] / 60 else "", 30, 930, 660, WHITE)
    if A_tree.mage["瞬水爆"] and player.weapon == 3:
        draw_color_text(screen, str("Q"), 20, 930, 722, WHITE)
        draw_img(screen, mage_ultimate_img, 887, 640)
        draw_color_text(screen, str(round(Player.cooldowns["瞬水爆"] / 60, 1)) if Player.cooldowns["瞬水爆"] / 60 else "", 30, 930, 660, WHITE)
    def circle_indicator_location(key):
        if key.startswith("W"): return 452
        if key.startswith("E"): return 562
        if key.startswith("R"): return 672
        if key.startswith("S"): return 782
        if key.startswith("Q"): return 892
    def ability_stack_indicator(key, stack):
        if key.startswith("W"): x = 490 + 20
        if key.startswith("E"): x = 600 + 20
        if key.startswith("R"): x = 710 + 20
        if key.startswith("S"): x = 820 + 20
        if key.startswith("Q"): x = 930 + 20
        outline_text(stack, 40, x, 620, WHITE)
    #狀態效果顯示欄
    effect_imgs = {"生命回復":icon_health_regen_img, "移動速度":icon_speed_img, "腥紅收割":icon_crimson_harvest_img}
    if player.effects:
        for idx, effect in enumerate(player.effects):
            if effect_imgs.get(effect["name"]):
                pygame.draw.rect(screen, AGRAY, (0 + idx * 50, 530, 60, 70))
                pygame.draw.rect(screen, DGRAY, (10 + idx * 50, 535, 40, 40))
                draw_img(screen, effect_imgs[effect["name"]], 10 + idx * 50, 535)
                outline_text(effect["level"], 15, 40 + idx * 50 - 10 * len(str(effect["level"])), 553, WHITE)
                pygame.draw.rect(screen, BLACK, (10 + idx * 50, 535, 40, 40), 3)
                effect_min = str(effect["tick"] // 3600)
                effect_sec = str(effect["tick"] // 60).zfill(2)
                draw_color_text(screen, effect_min + ":" + effect_sec, 20, 30 + idx * 50, 570, WHITE)
        for idx, effect in enumerate(player.effects):
            if effect_imgs.get(effect["name"]):
                if is_hovering(10 + idx * 50, 10 + idx * 50 + 40, 535, 575, Mouse.x, Mouse.y, "?"):
                    pygame.draw.rect(screen, AGRAY, (Mouse.x, Mouse.y - 100, 150, 100))
                    pygame.draw.rect(screen, BLACK, (Mouse.x, Mouse.y - 100, 150, 100), 3)
                    outline_text(effect["name"], 25, Mouse.x + 25, Mouse.y - 100, WHITE)
                    draw_color_text(screen, "等級: " + str(effect["level"]), 25, Mouse.x + 75, Mouse.y - 70, WHITE)
                    draw_color_text(screen, "剩餘: " + str(effect["tick"] // 60) + "秒", 25, Mouse.x + 75, Mouse.y - 45, WHITE)
    #圓形&技能疊層顯示器
    if player.weapon == 1:
        for keys, skills in A_tree.keybind[player.weapon - 1].items():
            if skills == "暗影脈衝" and Player.cooldowns["rogue_skill_time"] and keys.endswith(str(A_tree.row)):
                circle_cd_indicator(circle_indicator_location(keys), 637, 40, Player.cooldowns["rogue_skill_time"], 300, 5, LBLUE)
            elif skills == "幻影分身" and Player.cooldowns["幻影分身持續時間"] and keys.endswith(str(A_tree.row)):
                circle_cd_indicator(circle_indicator_location(keys), 637, 40, Player.cooldowns["幻影分身持續時間"], 180, 5, RED)
                draw_img(screen, icon_recast_img, circle_indicator_location(keys), 630)
        if Player.cooldowns["暗影襲擊剩餘時間"]: circle_cd_indicator(892, 637, 40, Player.cooldowns["暗影襲擊剩餘時間"], 600, 5, RED)
        if Assassin.ultimate_time: ability_stack_indicator("Q", Assassin.ultimate_time)
    if player.weapon == 2:
        if Player.cooldowns["苦無剩餘時間"]: circle_cd_indicator(892, 637, 40, Player.cooldowns["苦無剩餘時間"], 600, 5, RED)
        if Archer.kunai_amount: ability_stack_indicator("Q", Archer.kunai_amount)
    if player.weapon == 3:
        if Player.cooldowns["mage_water_burst"]: circle_cd_indicator(892, 637, 40, Player.cooldowns["mage_water_burst"], 120 + A_tree.mage["水爆延長"] * 120, 5, RED)
    if Player.cooldowns["暗影襲擊剩餘時間"] == 0: Assassin.ultimate_time = 0
    if Player.cooldowns["苦無剩餘時間"] == 0: Archer.kunai_amount = 0
    #職業被動
    if player.weapon == 1:
        draw_img(screen, Mage2_icon_img, 42, 662)
        draw_img(screen, Archer2_icon_img, 92, 662)
        draw_img(screen, hotbar_class_slot_img, 55, 650)
        draw_img(screen, Rogue1_icon_img, 60, 654)
        rogue_specialization = list(A_tree.specialization_unlock["rogue"].keys())
        rogue_class_name = next((spec for spec in rogue_specialization if A_tree.rogue.get(spec) == 1), "刺客")
        draw_color_text(screen, "[Lv." + str(Assassin.level) + "] " + rogue_class_name, 20, 220, 610, LBLUE)
        draw_passive_bar(screen, Assassin.xp * 60, Assassin.xp_req * 60, 170, 715, GREEN, "Rogue EXP")
        if Assassin.magic_enchant > 1:
            draw_passive_bar(screen, Mage.mana * 60, Mage.mana_limit * 60, 170, 690, LBLUE, "Mana")
        if A_tree.rogue["流放者"]: riptide_bar = {"name":"夜幕潛行", "color":PURPLE}
        elif A_tree.rogue["聖騎士"]: riptide_bar = {"name":"聖光注能", "color":GOLD}
        else: riptide_bar = {"name":"激流", "color":BLUE}
        if Assassin.magic_enchant == 1: draw_passive_bar(screen, Player.cooldowns["rogue_riptide"], 300, 170, 690, riptide_bar["color"], riptide_bar["name"])
    if player.weapon == 2:
        draw_img(screen, Rogue2_icon_img, 42, 662)
        draw_img(screen, Mage2_icon_img, 92, 662)
        draw_img(screen, hotbar_class_slot_img, 55, 650)
        draw_img(screen, Archer1_icon_img, 60, 654)
        archer_specialization = list(A_tree.specialization_unlock["archer"].keys())
        archer_class_name = next((spec for spec in archer_specialization if A_tree.archer.get(spec) == 1), "射手")
        draw_color_text(screen, "[Lv." + str(Archer.level) + "] " + archer_class_name, 20, 220, 610, LBLUE)
        draw_passive_bar(screen, Archer.focus * 60, Archer.focus_limit * 60, 170, 690, YELLOW, "專注力")
        draw_passive_bar(screen, Archer.xp * 60, Archer.xp_req * 60, 170, 715, GREEN, "Archer EXP")
    if player.weapon == 3:
        draw_img(screen, Archer2_icon_img, 42, 662)
        draw_img(screen, Rogue2_icon_img, 92, 662)
        draw_img(screen, hotbar_class_slot_img, 55, 650)
        draw_img(screen, Mage1_icon_img, 60, 654)
        mage_specialization = list(A_tree.specialization_unlock["mage"].keys())
        mage_class_name = next((spec for spec in mage_specialization if A_tree.mage.get(spec) == 1), "法師")
        for specialization in mage_specialization:
            if specialization == 1: mage_class_name = specialization
        if mage_class_name == "": mage_class_name = "法師"
        draw_color_text(screen, "[Lv." + str(Mage.level) + "] 法師", 20, 220, 610, LBLUE)
        draw_passive_bar(screen, Mage.mana * 60, Mage.mana_limit * 60, 170, 690, LBLUE, "魔力")
        draw_passive_bar(screen, Mage.xp * 60, Mage.xp_req * 60, 170, 715, GREEN, "Mage EXP")
    if Info.open:
        #顯示座標資訊
        draw_color_text(screen, "座標: " + str(Player_location.coord_x // 10), 20, 50, 300, BLACK)
        draw_color_text(screen, "背景: " + str(background_location_x // 10), 20, 50, 330, BLACK)
        draw_color_text(screen, "區域: " + str(Areas.area), 20, 50, 360, BLACK)
        draw_color_text(screen, "區域座標: " + str(current_coord_x), 20, 50, 390, BLACK)
        for atks in player.attacks:
            pygame.draw.circle(screen, RED, (atks[0], atks[1]), atks[2])
        if Areas.lock_left:draw_color_text(screen, "邊界:左邊", 20, 50, 420, BLACK)
        if Areas.lock_right:draw_color_text(screen, "邊界:右邊", 20, 50, 450, BLACK)
    #顯示訊息
    if Player.cooldowns["message"] > 1:
        draw_img(screen, message_background_img, 0, 0)
        draw_color_text(screen, Messages.text[4], 20, 150, 50, BLACK)
        draw_color_text(screen, Messages.text[3], 20, 150, 100, BLACK)
        draw_color_text(screen, Messages.text[2], 20, 150, 150, BLACK)
        draw_color_text(screen, Messages.text[1], 20, 150, 200, BLACK)
        draw_color_text(screen, Messages.text[0], 20, 150, 250, BLACK)
    #顯示標題
    if Player.cooldowns["title"] > 0:
        draw_color_text(screen, str(Title.text[0]), 50, WIDTH / 2, 200, WHITE)
        draw_color_text(screen, str(Title.text[1]), 30, WIDTH / 2, 250, WHITE)
    #顯示無任務框對話
    if Player.cooldowns["dialogue"] > 0:
        draw_color_text(screen, str(Dialogue.name[0]), 30, 500, 450, GOLD)
        draw_color_text(screen, str(Dialogue.name[1]), 20, 500, 480, GOLD)
        draw_color_text(screen, str(Dialogue.text[1]), 30, 500, 500, WHITE)
        draw_color_text(screen, str(Dialogue.text[0]), 30, 500, 530, WHITE)
    for i in range(len(Boss_skill_bar.bars)):
        boss_skill_bar(Boss_skill_bar.bars[i][0], Boss_skill_bar.bars[i][1], Boss_skill_bar.bars[i][2], i, Boss_skill_bar.bars[i][3])
    Boss_skill_bar.bars = []
    #顯示提示
    if Hint.open:
        if Quest.tracking == 1 and Quest_01.complete == False:
            draw_color_text(screen, "[藥水實驗]", 30, 900, 200, GOLD)
            if Quest_01.stage == 4:
                draw_color_text(screen, "帶給煉金術士8個史萊姆黏液", 20, 850, 230, GOLD)
                draw_color_text(screen, "返回舊的區域將會重生怪物", 20, 850, 260, GOLD)
            if Quest_01.stage == 10:
                draw_color_text(screen, "擊敗跑出來的史萊姆", 20, 850, 230, GOLD)
        if Quest.tracking == 2 and Quest_02.complete == False:
            draw_color_text(screen, "[黑暗勢力的威脅]", 30, 880, 200, GOLD)
            if search_item("生命水晶")["count"] == 0 and Area6.cata_open == False:
                if Quest_02.stage == 15 and -2 < Areas.area < 4:
                    draw_color_text(screen, "前往森林", 20, 900, 230, GOLD)
                if Quest_02.stage == 15 and Areas.area == 4:
                    draw_color_text(screen, "前往曙光之城廢墟", 20, 900, 230, GOLD)
                if Quest_02.stage == 15 and Areas.area == 5:
                    draw_color_text(screen, "尋找靈魂碎片", 20, 900, 230, GOLD)
                if Quest_02.stage == 15 and Areas.area == 6:
                    draw_color_text(screen, "前往曙光之城廢墟", 20, 900, 230, GOLD)
                if Quest_02.stage == 15 and Areas.area == -6:
                    draw_color_text(screen, "尋找靈魂碎片", 20, 900, 230, GOLD)
                if Quest_02.stage == 15 and Areas.area == -5:
                    draw_color_text(screen, "尋找靈魂碎片", 20, 900, 230, GOLD)
            if search_item("生命水晶")["count"] == 1 and Area6.cata_open == False:
                if Quest_02.stage == 15:
                    draw_color_text(screen, "進入地下墓穴", 20, 900, 230, GOLD)
            if Area6.cata_open:
                if Quest_02.stage == 15 and Area9.first_beat_boss == True:
                    draw_color_text(screen, "攻略地下墓穴", 20, 900, 230, GOLD)
                if Quest_02.stage == 15 and search_item("生命水晶")["count"] > 0:
                    draw_color_text(screen, "前往下一區，用傳送門返回城鎮中心", 20, 840, 230, GOLD)
            #快捷欄
    pygame.display.flip()

pygame.quit()