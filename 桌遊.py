import os
import sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
import math
import datetime
import time
import copy

#基本定義
FPS = 60
WIDTH = 320
HEIGHT = 800
#顏色
GREEN = 0, 255, 0
BLACK = 0, 0, 0 

pygame.init()

#標題
pygame.display.set_caption("桌遊")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#引入圖片
if getattr(sys, 'frozen', False):
    # 打包後的執行：桌遊資源資料夾跟 .exe 同目錄
    current_folder = os.path.dirname(sys.executable)
else:
    # 開發階段：使用原所在位置
    current_folder = os.path.dirname(os.path.abspath(__file__))
font = os.path.join(current_folder, "桌遊資源", "font2.ttf")
card_A_img = pygame.image.load(os.path.join(current_folder, "桌遊資源", "card_A.png")).convert()
card_Q_img = pygame.image.load(os.path.join(current_folder, "桌遊資源", "card_Q.png")).convert()
button_flip_img = pygame.image.load(os.path.join(current_folder, "桌遊資源", "button_flip.png")).convert()
card_A_img = pygame.transform.scale(card_A_img, (300, 500))
card_Q_img = pygame.transform.scale(card_Q_img, (300, 500))
card_A_img.set_colorkey(GREEN)
card_Q_img.set_colorkey(GREEN)
button_flip_img.set_colorkey(GREEN)

#函式
def draw_img(img, x, y):
    if type(img) != int:
        img_rect = img.get_rect()
        img_rect.x = x
        img_rect.y = y
        screen.blit(img, img_rect)

#中文字+顏色
def draw_color_text(text, size, x, y, color):
    f = pygame.font.Font(font, size)
    text_surface = f.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    screen.blit(text_surface, text_rect)

#問題顯示
def question_text(text, size, x, y, color):
    for i in range(len(text) // 10 + 1):
        draw_color_text(text[i * 10 : (i + 1) * 10], size, x, y + i * size * 1.3, color)
    return (len(text) // 10 + 1) * size * 1.3

#答案顯示
def answer_text(text, size, x, y, color, mouse_x, mouse_y):
    hovering_option = None
    for i in range(len(text)):
        draw_color_text("(" + chr(65 + i) + ")" + text[i], size, x, y + i * size * 1.3, color)
        if is_hovering(0, 320, y + i * size * 1.3, y + i * size * 1.3 + 20, mouse_x, mouse_y):
            hovering_option = i
    return hovering_option

#選項轉索引
def result_to_index(option):
    return ord(option) - 65
#滑鼠璇停
def is_hovering(x1, x2, y1, y2, mouse_x = 0, mouse_y = 0):
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)
    if x1 < mouse_x < x2 and y1 < mouse_y < y2:
        return x1 < mouse_x < x2 and y1 < mouse_y < y2

showing_card = card_Q_img
#卡片資料
card_data = {
  "1": {
    "Q": ["下列有關保護色的說明何者錯誤?", "北極狐改變毛髮屬於適應色", "毛毛蟲使用警戒色嚇阻天敵", "鬥魚使用隱蔽色避免被獵捕", "老虎使用隱蔽色靠近獵物"],
    "A": ["C"],
    "D": 0
  },
  "2": {
    "Q": ["下列色彩在生活中的應用何者正確?", "讓醫院有平靜感用冷色", "為避免髒污天花板用深色", "幼兒園應以平靜單調冷色為主", "古建築以鮮豔原色表信仰"],
    "A": ["A"],
    "D": 0
  },
  "3": {
    "Q": ["曼賽爾表色體系中表色法H/V/C分別是代表甚麼", "彩度 明度 色相", "色相 明度 彩度", "明度 色相 彩度", "亮度 色相 濃度"],
    "A": ["B"],
    "D": 0
  },
  "4": {
    "Q": ["下列選項何者錯誤?", "暖色系為積極的「外向型」色彩", "冷色系波長較短，具後退感", "用淺色系的包裝可製造輕盈感", "紅，黃色屬於寒色系"],
    "A": ["D"],
    "D": 0
  },
  "5": {
    "Q": ["下列配對何者注目性較高?", "黑底黃字", "黑底橙字", "黑底藍字", "白底綠字"],
    "A": ["A"],
    "D": 0
  },
  "6": {
    "Q": ["日本川添登教授將設計世界簡單分成三個領域，下列何者不識其中之一?", "時間設計", "產品設計", "空間設計", "視覺傳達設計"],
    "A": ["A"],
    "D": 0
  },
  "7": {
    "Q": ["下列何者不是造型領域的分類要素?", "空間要素", "地域要素", "經濟要素", "型式原理要素"],
    "A": ["C"],
    "D": 0
  },
  "8": {
    "Q": ["中國歷史上的夏，商，周等朝代是以什麼為工藝與造型文化為代表?", "石器", "鐵器", "陶器", "青銅器"],
    "A": ["D"],
    "D": 0
  },
  "9": {
    "Q": ["下列何者不是希臘文化中有採用的石柱樣式?", "依莉菲歐斯", "愛奧尼亞", "柯林斯", "多利克"],
    "A": ["A"],
    "D": 0
  },
  "10": {
    "Q": ["下列型態的分類何者正確?", "主觀型", "抽象型", "流線型", "無機型"],
    "A": ["B"],
    "D": 0
  },
  "11": {
    "Q": ["PET是一種熱塑型塑膠，常用於製造寶特瓶，請問PET的中文是什麼?", "聚氯乙烯", "壓克力樹酯", "飽和聚酯", "聚丙烯塑膠"],
    "A": ["C"],
    "D": 0
  },
  "12": {
    "Q": ["下列哪一個不是法國哲學家亨利﹒列斐伏爾在﹤空間的再現﹥這本書中所提出的辯證?", "空間再現", "想像空間", "空間再現", "空間實踐"],
    "A": ["B"],
    "D": 0
  },
  "13": {
    "Q": ["依據地方環境與設計的四個面向，台南白河蓮花節應屬於哪種?", "自然資源維護發展", "生活形態營造", "文化資源展現創意", "產業經營營造"],
    "A": ["D"],
    "D": 0
  },
  "14": {
    "Q": ["有關日本環境共生住宅三要素，下列選項何者正確?", "親和的周圍環境", "地球環境的安全", "居住環境的環境健康", "以上皆是"],
    "A": ["D"],
    "D": 0
  },
  "15": {
    "Q": ["後先代主義之父是誰?", "文丘里", "羅威", "塔特林", "阿爾豐斯﹒慕夏"],
    "A": ["A"],
    "D": 0
  },
  "16": {
    "Q": ["吉爾在爺爺家找到一罐瓶身印有「反共抗俄」等字樣的酒瓶，請問這是台灣什麼時期的設計特色?", "啟蒙時期", "起飛與轉型時期", "奠基時期", "發展時期"],
    "A": ["C"],
    "D": 0
  },
  "17": {
    "Q": ["日文中「Design」可譯為圖案、設計或意匠，請問意匠的解釋是什麼?", "有特殊技能的工匠", "設計意義與技術", "匠師們的住所", "設計師們"],
    "A": ["B"],
    "D": 0
  }
}

#隨機抽選題目
card_names = []
for card_name in card_data:
    card_names.append(card_name)
result = random.choices(card_names)[0]

#迴圈
running = True
while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))
    #取得游標位置
    mouse_x, mouse_y = pygame.mouse.get_pos()
    card_pos_x = WIDTH / 2 - showing_card.get_width() / 2
    card_pos_y = HEIGHT / 2 - showing_card.get_height() / 2
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if is_hovering(160 - 75, 160 + 75, 50, 50 + 50, mouse_x, mouse_y):
                    #隨機抽選
                    result = random.choices(card_names)[0]
                    showing_card = card_Q_img
                elif isinstance(selecting_option, int):
                    if showing_card == card_A_img:
                        showing_card = card_Q_img
                    else:
                        showing_card = card_A_img

    draw_img(showing_card, card_pos_x, card_pos_y)
    draw_img(button_flip_img, 160 - 75, 50)
    if is_hovering(160 - 75, 160 + 75, 50, 50 + 50, mouse_x, mouse_y):
        pygame.draw.rect(screen, (255, 255, 255), (160 - 75, 50, 150, 50), 5)
    if showing_card == card_Q_img:
        y_move = question_text(card_data[result]["Q"][0], 20, WIDTH / 2, 250, BLACK)
        selecting_option = answer_text(card_data[result]["Q"][1:], 20, WIDTH / 2, y_move + 280, BLACK, mouse_x, mouse_y)
    else:
        for i in range(len(card_data[result]["A"])):
            question_text("(" + card_data[result]["A"][i] + ")" + card_data[result]["Q"][result_to_index(card_data[result]["A"][i]) + 1], 20, WIDTH / 2, 260 + i * 20 * 1.3, BLACK)
            draw_color_text("正確" if selecting_option == result_to_index(card_data[result]["A"][0]) else "錯誤", 20, WIDTH / 2, 230, GREEN if selecting_option == result_to_index(card_data[result]["A"][0]) else (255, 0, 0))
    if isinstance(selecting_option, int) and showing_card == card_Q_img:
        pygame.draw.rect(screen, (100, 100, 100), (20, 280 + y_move + selecting_option * 26, 280, 26), 3)
    pygame.display.flip()

pygame.quit()