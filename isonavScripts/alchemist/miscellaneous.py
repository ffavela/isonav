import sys
EPSILON = sys.float_info.epsilon  # smallest possible difference


def convert_to_rgb(minval, maxval, val):
    colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]  # [BLUE, GREEN, RED]
    fi = float(val-minval) / float(maxval-minval) * (len(colors)-1)
    i = int(fi)
    f = fi - i
    if f < EPSILON:
        return [c/255.0 for c in colors[i]]
    else:
        (r1, g1, b1), (r2, g2, b2) = colors[i], colors[i+1]
        # return (b1+f*(b2-b1))/255,(g1+f*(g2-g1))/255,r1+f*(r2-r1))/255
        return (b1+f*(b2-b1))/255, (g1+f*(g2-g1))/255, (r1+f*(r2-r1))/255


def getRgb(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    return r, g, b
