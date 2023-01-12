
def draw_homg_line(img, l):
    out = img.copy()
    x1 = 0
    y1 = int(-l[2] / l[1])
    x2 = img.shape[1]
    y2 = int(-(l[2] + l[0] * x2) / l[1])
    cv2.line(out, (x1, y1), (x2, y2), (255, 0, 0), 1)
    return out
