'''
 * @Author: tyhye.wang 
 * @Date: 2018-07-05 16:06:16 
 * @Last Modified by:   tyhye.wang 
 * @Last Modified time: 2018-07-05 16:06:16 
'''

IMG_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif']
VIDEO_EXTENSIONS = ['.flv', '.avi', '.mp4', '.rm', '.rmvb']
def has_file_allowed_extension(filename, extensions):

    """Checks if a file is an allowed extension.
    Args:
        filename (string): path to a file
        extensions (iterable of strings): extensions to consider (lowercase)
    Returns:
        bool: True if the filename ends with one of given extensions
    """
    filename_lower = filename.lower()
    return any(filename_lower.endswith(ext) for ext in extensions)

def is_image_file(filename):
    """Checks if a file is an allowed image extension.
    Args:
        filename (string): path to a file
    Returns:
        bool: True if the filename ends with a known image extension
    """
    return has_file_allowed_extension(filename, IMG_EXTENSIONS)

def is_video_file(filename):
    """Checks if a file is an allowed image extension.
    Args:
        filename (string): path to a file
    Returns:
        bool: True if the filename ends with a known image extension
    """
    return has_file_allowed_extension(filename, VIDEO_EXTENSIONS)