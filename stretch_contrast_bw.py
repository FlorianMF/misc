def stretch_contrast(image, min=None, max=None):
    # only for grayscale images
    # if min or max are not defined, the image is stretched over the whole grayscale spectrum

    # check if min and max were passed and are positive and smaller than the max. possible value 2^16
    if min is None or max is None or any(x not in range(0, 2 ** 16) for x in [min, max]):
            stretched_image = (image - image.min()) / (image.max() - image.min()) * 255
    else:  # stretch the image to its min and max
            stretched_image = (image - min) / (max - min) * 255
            stretched_image[image < min] = 0
            stretched_image[image > max] = 255

    return stretched_image
