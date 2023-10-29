"""docstring"""
import numpy as np


def apply_filter(image: np.array, kernel: np.array) -> np.array:
    """ Apply given filter on image """
    # A given image has to have either 2 (grayscale) or 3 (RGB) dimensions
    assert image.ndim in [2, 3]
    # A given filter has to be 2 dimensional and square
    assert kernel.ndim == 2
    assert kernel.shape[0] == kernel.shape[1]

    is_rgb = image.ndim == 3
    num_channels = 3 if is_rgb else 1
    kernel_size = kernel.shape[0]
    kernel_radius = kernel_size // 2

    if kernel_size % 2 == 0:
        kernel = np.pad(kernel, ((0, 1), (0, 1)), mode='constant')
        kernel_size = kernel.shape[0]
        kernel_radius = kernel_size // 2

    filtered_image = np.zeros_like(image, dtype=np.float32)

    if is_rgb:
        padded_image = np.zeros((image.shape[1] + (kernel_radius * 2), image.shape[0] + (kernel_radius * 2), num_channels), dtype=np.float32)
        for channel in range(3):
            padded_image[:, :, channel] = np.pad(image[:, :, channel], kernel_radius, mode="constant")
    else:
        padded_image = np.pad(image, kernel_radius, mode="constant")

    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            if is_rgb:
                for channel in range(3):
                    pixel_around = padded_image[x:x+kernel_size, y:y+kernel_size, channel]
                    new_pixel = np.sum(pixel_around * kernel)
                    filtered_image[x, y, channel] = new_pixel
            else:
                pixel_around = padded_image[x:x+kernel_size, y:y+kernel_size]
                new_pixel = np.sum(pixel_around * kernel)
                filtered_image[x, y] = new_pixel

    filtered_image = np.clip(filtered_image, 0, 255).astype(np.uint8)
    return filtered_image
