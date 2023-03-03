import os

import pandas as pd
from pygaze.screen import Screen


class DataLoader:

    def __init__(self, path_to_data_csv: str) -> None:
        self.data_csv = pd.read_csv(path_to_data_csv)

        self._root_path = os.getcwd()

        self.screens = []

        # TODO implements checks that all information is in the file

    def get_stimuli_screens(self) -> list[Screen]:
        image_paths = self.data_csv[['path_to_image']].tolist()

        for path in image_paths:
            full_path = self._root_path + path
            screen = Screen()
            screen.draw_image(full_path)

            self.screens.append(screen)

        return self.screens

    def _randomize(self):
        # TODO implement randomization of stimuli texts
        pass
