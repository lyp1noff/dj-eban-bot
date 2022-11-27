import os
import re


def slugify(value):
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def cleanup():
    directory = './songs'
    if not os.path.exists(directory):
        os.mkdir(directory)
    for f in os.listdir(directory):
        os.remove(os.path.join(directory, f))
