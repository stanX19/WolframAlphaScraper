import os
import sys
import base64
import logging
import time


def add_to_path():
    sys.path.append(os.path.dirname(__file__))

def write_img(path, data):
    add_to_path()
    image_data = base64.b64decode(data)
    with open(path, "wb+") as f:
        f.write(image_data)
    logging.info(f"Data written to {path}")

if __name__ == '__main__':
    import os
    import requests
    data = "data:image/gif;base64,R0lGODlhRgAnAOYAAAAAAAICAgMDAwYGBggICAoKCgsLCw4ODg8PDxAQEBISEhMTExkZGRoaGhwcHCcnJyoqKjIyMjMzMzU1NTg4OD4+PkFBQUJCQkNDQ0dHR0hISElJSUpKSk9PT1VVVVZWVldXV1hYWFlZWVpaWl5eXmBgYGFhYWNjY2RkZGZmZmdnZ2hoaGtra21tbW5ubnBwcHZ2dnd3d3t7e35+fn9/f4KCgoaGhoiIiIqKiouLi4+Pj5CQkJGRkZKSkpqampycnJ+fn6KioqOjo6SkpKWlpaampqenp6ioqKmpqaqqqq6urq+vr7Ozs7a2tri4uLm5ubu7u7y8vL29vcDAwMPDw8XFxcbGxsfHx8nJyc3Nzc7Ozs/Pz9DQ0NHR0dXV1dfX19jY2Nra2tvb29zc3N7e3uDg4OHh4ePj4+jo6Orq6uzs7O3t7e/v7/Dw8PHx8fPz8/X19ff39/j4+Pn5+fr6+vv7+/z8/P39/f7+/v///wAAAAAAAAAAAAAAAAAAAAAAACwAAAAARgAnAAAH/4B5goOEhYaHiImKi4yEcFlSjZKTlIhkFxNHlZucjSAySJ2io4N3C0JUpKqUeEZFQQZEdKu0i3IdT3kfHEW1vogmNIIVOpq/x4JXBWt5bQVDX8jIKR2COw1J0sgbJXliFSRATczatUAHK0osGhZj5b9sc4Ju7/X294Z2OmeJWkKqa4iISKCmlokui4zgILXkRw8ABVcVOTGICQQKdvLUYGBFEIUtqqZApDWhCSEwA7A4cSGjjCAbKEKOJPSgps2bOGv6EJRm5qAQM1QUitKgEB0MSJMmbYFIZERSWQTgKWRkwJRCXALUIYRHjNevX/kdcroKCwFDNwZ4KfQFgLxRZM5VkXFL6M2LDAsJYUFgtIPfv39hNPU5yo4CMIKgXBlxBoeEqYOQVCiEZ4vly5fDDH5KysQPQTEU9DLjwMNVQS54jELjIQKADC9WlblwZ9GaCnHuPYrEqEoORXNiuLR3KZOkMmYSdaGH71MofLRMocpjEaNGjtAltXoVa1YelCpZDs+u6FauXb1+BiUvKdiwYoSqnmavSBkzZ9AIpV1LXxE1a9jUdVde/SHCjTfgiLOGYow5BlmBhpyTzjrt5BHaaKXNByEh8cyz4YcghkhIIAA7"
    data = data.split(',')[1]
    base_dir = "test"
    name = time.strftime('%Y-%m-%d %H_%M_%S', time.localtime(1347517370))
    path = f"{base_dir}\\{name}.png"
    write_img(path, data)
    os.startfile(path)
