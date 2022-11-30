import numpy as np

def combine_image_horizontal(images):
    max_height = 0
    for image in images:
        if image is None: continue
        height, width, channels = image.shape
        max_height = max(max_height, height)

    line = np.zeros((max_height, 3, 3), np.uint8)
    line.fill(255)
    combined = np.zeros((max_height, 1, 3), np.uint8)

    for image in images:
        if image is None: continue
        height, width, channels = image.shape
        if height < max_height:
            buffer = np.zeros((max_height - height, width, 3), np.uint8)
            image = np.concatenate((image, buffer), axis=0)
        combined = np.concatenate((combined, line, image), axis=1)
    combined = np.concatenate((combined, line), axis=1)

    # show(combined)
    return combined[:, 1:]

def combine_image_vertical(images):
    max_width = 0
    for image in images:
        height, width, channels = image.shape
        max_width = max(max_width, width)

    line = np.zeros((3, max_width, 3), np.uint8)
    line.fill(255)
    combined = np.zeros((1, max_width, 3), np.uint8)

    for image in images:
        height, width, channels = image.shape
        if width < max_width:
            buffer = np.zeros((height, max_width - width, 3), np.uint8)
            image = np.concatenate((image, buffer), axis=1)
        combined = np.concatenate((combined, line, image), axis=0)
    combined = np.concatenate((combined, line), axis=0)

    # show(combined)
    return combined[1:, :]

