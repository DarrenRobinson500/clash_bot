

def only_colours(i, colours):
    new = i
    for row in new:
        for pixel in row:
            if (pixel[0],pixel[1],pixel[2]) not in colours:
                pixel[0], pixel[1], pixel[2] = 255, 255, 255
            else:
                pixel[0], pixel[1], pixel[2] = 0, 0, 0
    return new

def see_resources_background(i, background_colour, x, y):
    x_max, y_max = len(i[0]), len(i)
    found = False
    while not found:
        pixel = i[y][x]
        if (pixel[0], pixel[1], pixel[2]) in background_colour: return [x,y]
        x += 1
        if x > x_max - 500:
            x = 200
            y += 1
            if y > y_max - 300:
                return

def add_border(i):
    new = i.copy()
    h, w, channels = new.shape
    for x in range(w):
        for y in [0,1,h-2,h-1]:
            pixel = new[y][x]
            pixel[0], pixel[1], pixel[2] = 0, 0, 0
    for y in range(h):
        for x in [0,1,w-2,w-1]:
            pixel = new[y][x]
            pixel[0], pixel[1], pixel[2] = 0, 0, 0
    return new

