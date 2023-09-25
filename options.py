import json
from dataclasses import dataclass


@dataclass
class Settings:
    def __init__(self):
        with open("settings.json", "r") as f:
            self.settings = json.load(f)

    def get_width(self):
        return self.settings["width"]

    def get_height(self):
        return self.settings["height"]

    def get_fps_cap(self):
        return self.settings["fps_cap"]

    def get_font(self):
        return self.settings["font"]

    def get_volume(self):
        return self.settings["volume"]

    def get_fullscreen(self):
        return self.settings["fullscreen"]

    def set_width(self, width):
        self.settings["width"] = width

    def set_height(self, height):
        self.settings["height"] = height

    def set_fps(self, fps):
        self.settings["fps"] = fps

    def set_font(self, font):
        self.settings["font"] = font

    def set_volume(self, volume):
        self.settings["volume"] = volume

    def set_fullscreen(self, fullscreen):
        self.settings["fullscreen"] = fullscreen

    def save(self):
        with open("settings.json", "w") as f:
            json.dump(self.settings, f, indent=4)

    def get_title(self):
        return self.settings["title"]

    def allow_screensaver(self):
        return self.settings["allow_screensaver"]

    def set_title(self, title):
        self.settings["title"] = title

    def set_allow_screensaver(self, allow_screensaver):
        self.settings["allow_screensaver"] = allow_screensaver

    def __repr__(self):
        return f"Settings(width={self.get_width()}, height={self.get_height()}, fps={self.get_fps_cap()}, font={self.get_font()}, volume={self.get_volume()}, fullscreen={self.get_fullscreen()})"
