from PIL import Image, ImageFont, ImageDraw

try:
    from cv2 import cv2
except ImportError:
    pass


def main(total_score, scoreM, scoreP, scoreGreat, scoreGood, scoreB, scoreMiss, accuracy, maxcombo, rank):
    DIR = "assets-panel/"
    color = (255, 255, 255, 255)

    ranking_panel = Image.open(DIR + "ranking-panel.png")
    marvelous = Image.open(DIR + "mania-hit300g.png")
    perfect = Image.open(DIR + "mania-hit300.png")
    great = Image.open(DIR + "mania-hit200.png")
    good = Image.open(DIR + "mania-hit100.png")
    bad = Image.open(DIR + "mania-hit50.png")
    miss = Image.open(DIR + "mania-hit0.png")

    ranking_perfect = Image.open(DIR + "ranking-perfect.png")
    ranking_accuracy = Image.open(DIR + "ranking-accuracy.png")
    ranking_maxcombo = Image.open(DIR + "ranking-maxcombo.png")

    Ranking_A = Image.open(DIR + "ranking-A.png")
    Ranking_B = Image.open(DIR + "ranking-B.png")
    Ranking_C = Image.open(DIR + "ranking-C.png")
    Ranking_D = Image.open(DIR + "ranking-D.png")
    Ranking_S = Image.open(DIR + "ranking-S.png")
    Ranking_SH = Image.open(DIR + "ranking-SH.png")
    Ranking_X = Image.open(DIR + "ranking-X.png")
    Ranking_XH = Image.open(DIR + "ranking-XH.png")

    background = cv2.imread("cover.jpg")

    background = cv2.resize(background, (1366, 760))
    cv2.imwrite('background_resized.jpg', background)

    background = Image.open("background_resized.jpg")

    backup = background.copy()

    # Ranking
    backup.paste(ranking_panel, (0, 0), ranking_panel)

    backup.paste(ranking_maxcombo, (9, 383), ranking_maxcombo)
    backup.paste(ranking_accuracy, (296, 383), ranking_accuracy)

    b_edit = ImageDraw.Draw(backup)

    # score
    score = total_score
    score = " ".join(score)
    score_pos = (250, 25)
    score_font = "Ubuntu.ttf"
    score_font = ImageFont.truetype(score_font, 45)
    b_edit.text(score_pos, score, fill=color, font=score_font)

    # Ranking
    if rank == "A":
        backup.paste(Ranking_A, (0, -230), Ranking_A)
    elif rank == "B":
        backup.paste(Ranking_B, (0, -230), Ranking_B)
    elif rank == "C":
        backup.paste(Ranking_C, (0, -230), Ranking_C)
    elif rank == "D":
        backup.paste(Ranking_D, (0, -230), Ranking_D)
    elif rank == "S":
        backup.paste(Ranking_S, (0, -230), Ranking_S)
    elif rank == "SH":
        backup.paste(Ranking_SH, (0, -230), Ranking_SH)
    elif rank == "X":
        backup.paste(Ranking_X, (0, -230), Ranking_X)
    elif rank == "XH":
        backup.paste(Ranking_XH, (0, -230), Ranking_XH)
    else:
        return "invalid parameter"

    # setup
    backup.paste(marvelous, (250, 125), marvelous)
    backup.paste(perfect, (-70, 125), perfect)
    backup.paste(good, (-80, 220), good)
    backup.paste(great, (260, 220), great)
    backup.paste(bad, (-70, 315), bad)
    backup.paste(miss, (250, 315), miss)

    # others
    backup.paste(ranking_perfect, (155, 480), ranking_perfect)

    b_edit = ImageDraw.Draw(backup)

    # 300
    score = scoreP + "x"
    score = " ".join(score)
    score_pos = (135, 133)
    score_font = "Ubuntu.ttf"
    score_font = ImageFont.truetype(score_font, 35)
    b_edit.text(score_pos, score, fill=color, font=score_font)

    # 300g
    score = scoreM + "x"
    score = " ".join(score)
    score_pos = (450, 133)
    score_font = "Ubuntu.ttf"
    score_font = ImageFont.truetype(score_font, 35)
    b_edit.text(score_pos, score, fill=color, font=score_font)

    # 200
    score = scoreGreat + "x"
    score = " ".join(score)
    score_pos = (122, 228)
    score_font = "Ubuntu.ttf"
    score_font = ImageFont.truetype(score_font, 35)
    b_edit.text(score_pos, score, fill=color, font=score_font)

    # 100
    score = scoreGood + "x"
    score = " ".join(score)
    score_pos = (448, 228)
    score_font = "Ubuntu.ttf"
    score_font = ImageFont.truetype(score_font, 35)
    b_edit.text(score_pos, score, fill=color, font=score_font)

    # 50
    score = scoreB + "x"
    score = " ".join(score)
    score_pos = (122, 325)
    score_font = "Ubuntu.ttf"
    score_font = ImageFont.truetype(score_font, 35)
    b_edit.text(score_pos, score, fill=color, font=score_font)

    # 0
    score = scoreMiss + "x"
    score = " ".join(score)
    score_pos = (448, 325)
    score_font = "Ubuntu.ttf"
    score_font = ImageFont.truetype(score_font, 35)
    b_edit.text(score_pos, score, fill=color, font=score_font)

    # maxcombo
    maxcombo = maxcombo + "x"
    maxcombo = " ".join(maxcombo)
    maxcombo_pos = (20, 440)
    maxcombo_font = "Ubuntu.ttf"
    maxcombo_font = ImageFont.truetype(maxcombo_font, 35)
    b_edit.text(maxcombo_pos, maxcombo, fill=color, font=maxcombo_font)

    # accuracy
    accuracy = accuracy + "%"
    accuracy = " ".join(accuracy)
    accuracy_pos = (310, 440)
    accuracy_font = "Ubuntu.ttf"
    accuracy_font = ImageFont.truetype(accuracy_font, 35)
    b_edit.text(accuracy_pos, accuracy, fill=color, font=accuracy_font)

    backup.save("panel.png", quality=95)
