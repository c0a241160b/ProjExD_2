import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {  # 移動量辞書
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, 5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：横方向・縦方向の真理値のタプル（True：画面内、False：画面外）
    """
    yoko, tate = True, True  # 初期値：画面の中
    if rct.left < 0 or rct.right > WIDTH:  # 横方向の画面外判定
        yoko = False
    if rct.top < 0 or rct.bottom > HEIGHT:  # 縦方向の画面外判定
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    go_img = pg.image.load("fig/pg_bg.jpg")  # 空のSurfaceを作る
    pg.draw.rect(go_img, (0, 0, 0), pg.Rect(0, 0, 1600, 900))  # 黒い四角を描く
    go_img.set_alpha(255/2)  # 透明度を半分にする
    go_rct = go_img.get_rect()  # 四角のRectを取得
    screen.blit(go_img, go_rct)  # 四角を画面に表示
    go_kk_img = pg.image.load("fig/8.png")  # 泣いているこうかとんの画像を取得
    go_kk_rct_left = go_kk_img.get_rect(center=(WIDTH/2-200, HEIGHT/2))  # 左側泣いているこうかとんのRectを取得
    go_kk_rct_right = go_kk_img.get_rect(center=(WIDTH/2+200, HEIGHT/2))  # 右側泣いているこうかとんのRectを取得
    screen.blit(go_kk_img, go_kk_rct_left)  # 左側こうかとんを画面に表示
    screen.blit(go_kk_img, go_kk_rct_right)  # 右側こうかとんを画面に表示
    fonto = pg.font.Font(None, 80)  # フォントサイズを80に設定
    txt_img = fonto.render("Game Over", True, (255, 255, 255))  # ・白字で"Game Over"と書かれたSurfaceインスタンスを生成
    txt_rct = txt_img.get_rect(center=(WIDTH/2,HEIGHT/2))  # 文字のRectを取得
    screen.blit(txt_img, txt_rct)  # 文字を画面に表示
    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_accs = [a for a in range(1,11)]
    img_list = []
    for r in range(1, 11):
        bb_img2 = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img2, (0, 0, 255), (10*r, 10*r), 10*r)
        bb_img2.set_colorkey((0, 0, 0))
        img_list.append(bb_img2)
    return [img_list, bb_accs]


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 空のSurfaceを作る
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤い円を描く
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()  # 爆弾Rectを取得
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT) 
    vx, vy = +5, +5  # 爆弾の移動速度

    bb_img2 = pg.Surface((20, 20))  # 空のSurfaceを作る
    pg.draw.circle(bb_img2, (0, 0, 255), (10, 10), 10)  # 赤い円を描く
    bb_img2.set_colorkey((0, 0, 0))
    bb_rct2 = bb_img2.get_rect()  # 爆弾Rectを取得
    bb_rct2.centerx = random.randint(0, WIDTH)
    bb_rct2.centery = random.randint(0, HEIGHT) 
    vx, vy = +5, +5  # 爆弾の移動速度

    clock = pg.time.Clock()
    tmr = 0


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):  # こうかとんRectと爆弾Rectの衝突判定
            print("ゲームオーバー")
            gameover(screen)
            return
        if kk_rct.colliderect(bb_rct2):  # こうかとんRectと爆弾Rectの衝突判定
            print("ゲームオーバー")
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[1] += mv[1]
                sum_mv[1] += mv[1]
                sum_mv[0] += mv[0]
                sum_mv[0] += mv[0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)

        bb_imgs, bb_accs = init_bb_imgs()
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img2 = bb_imgs[min(tmr//500, 9)]
        
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 移動を無かったことにする

        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        bb_rct2.move_ip(avx, avy)

        yoko, tate = check_bound(bb_rct)
        yoko2, tate2 = check_bound(bb_rct2)

        if not yoko:
            vx *= -1  # 横方向にはみ出ていたら反転

        if not tate:
            vy *= -1  # 縦方向にはみ出ていたら反転

        if not yoko2:
            avx *= -1  # 横方向にはみ出ていたら反転

        if not tate2:
            avy *= -1

        screen.blit(bb_img, bb_rct)
        screen.blit(bb_img2, bb_rct2)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
