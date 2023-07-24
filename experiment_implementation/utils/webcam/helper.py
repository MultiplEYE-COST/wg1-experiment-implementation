import ast
from configparser import ConfigParser
import numpy as np


def get_config(path="utils/webcam/config.ini", comment_char=";"):
    config_file = ConfigParser(inline_comment_prefixes=comment_char)
    config_file.read(path)
    config_default = config_file["DEFAULT"]
    config_colours = config_file["COLOURS"]
    config_eyetracker = config_file["EYETRACKER"]
    config_tf = config_file["TF"]

    settings = {key: ast.literal_eval(config_default[key]) for key in config_default}
    colours = {key: ast.literal_eval(config_colours[key]) for key in config_colours}
    eyetracker = {
        key: ast.literal_eval(config_eyetracker[key]) for key in config_eyetracker
    }
    tf = {key: ast.literal_eval(config_tf[key]) for key in config_tf}

    return settings, colours, eyetracker, tf


def shape_to_np(shape, dtype="int"):
    coords = np.zeros((5, 2), dtype=dtype)
    for i in range(0, 5):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords
