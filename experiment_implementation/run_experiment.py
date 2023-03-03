#!/usr/bin/env python

from experiment.experiment import Experiment
from stimuli.stimuli_loader import DataLoader


def run_experiment():
    # TODO: implement functionality to load stimuli
    # stimuli_texts = [
    #     # "וּחַ־הַצָּפרׄן וְהַשֶּׁמֶשׁ הׅתְוֲכְּוּ בֵינֵהֶם, מִי מֵהֶם חָזָק יוֺתֵר.‏גָמְרוּ,",
    #     "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et"
    #     "dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet "
    #     "clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. t wisi enim ad minim veniam, "
    #     "quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem "
    # ]

    stimuli_loader = DataLoader()
    stimuli_loader.prepare_screens()

    experiment = Experiment(stimuli_loader=stimuli_loader)
    experiment.run_experiment()


if __name__ == '__main__':
    run_experiment()
