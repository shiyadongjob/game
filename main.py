import pygame
import random
import os

# ====================== 初始化 ======================
pygame.init()

# 适配窗口，安卓与Windows兼容
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame飞机大战")

# 字体配置（思源黑体）
font_path = os.path.join(os.path.dirname(__file__), "fonts/SourceHanSansSC-Regular.otf")
font = pygame.font.Font(font_path, 36)

clock = pygame.time.Clock()
FPS = 60

# 颜色定义
BG_COLOR = (20, 20, 30)
WHITE = (255, 255, 255)
RED = (220, 60, 60)
BLUE = (60, 160, 240)

# ====================== 游戏对象 ======================
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 60
        self.height = 70
        self.rect = pygame.Rect(SCREEN_WIDTH//2 - self.width//2,
                                SCREEN_HEIGHT - 120,
                                self.width, self.height)

    def update(self):
        # 鼠标/触屏跟随
        mx, my = pygame.mouse.get_pos()
        self.rect.centerx = mx
        self.rect.centery = my
        # 边界限制
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 50
        self.height = 50
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH-self.width),
                                random.randint(-100, -40),
                                self.width, self.height)
        self.speed = random.randint(3,6)

    def update(self):
        self.rect.y += self.speed
        # 飞出屏幕重置位置
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = random.randint(-100,-40)
            self.rect.x = random.randint(0, SCREEN_WIDTH-self.width)
            self.speed = random.randint(3,6)

# ====================== 游戏主循环 ======================
def main():
    player = Player()
    enemy_group = pygame.sprite.Group()
    # 生成敌机
    for _ in range(6):
        enemy_group.add(Enemy())

    score = 0
    game_over = False

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(BG_COLOR)

        # 事件监听
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            player.update()
            enemy_group.update()

            # 碰撞检测
            hit = pygame.sprite.spritecollideany(player, enemy_group)
            if hit:
                game_over = True

            # 绘制玩家
            pygame.draw.rect(screen, BLUE, player.rect, border_radius=8)
            # 绘制敌机
            for enemy in enemy_group.sprites():
                pygame.draw.rect(screen, RED, enemy.rect, border_radius=6)
                score += 0.01

            # 绘制分数
            score_text = font.render(f"得分：{int(score)}", True, WHITE)
            screen.blit(score_text, (10, 10))
        else:
            # 游戏结束界面
            over_text = font.render(f"游戏结束！得分：{int(score)}", True, WHITE)
            screen.blit(over_text, (SCREEN_WIDTH//2 - over_text.get_width()//2, SCREEN_HEIGHT//2))

        pygame.display.flip()

if __name__ == "__main__":
    main()