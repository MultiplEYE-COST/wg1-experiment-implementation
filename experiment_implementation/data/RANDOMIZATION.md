# Randomization for the MultiplEYE experiment
This directory contains the randomization files for the MultiplEYE experiment. 
There are multiple parts of the experiment that are randomized:

1. The order of the stimulus texts
2. The order of the questions (within each question type)
3. The order of the question answer options for each question

## Stimulus Texts
The file `stimulus_order_versions.tsv` contains ca. 250 versions of the order of the stimulus texts. The first two
texts in each version are always the two practice texts with identifiers 11 and 12. The remaining texts are randomized
such that each text appears an equal number of times in each position across all versions. If a core session is run 
with a participant, a version will be determined and marked as used by that participant in the designated column ``participant_id``.
A test session will use a random version but not mark the version as used by a participant.

## Questions
The questions are shuffled within each type but not across types. There are three types of questions each of which has 
two questions:
1. Local
2. Bridging
3. Global

The question types are presented in the order above but the 2 questions are shuffled within each type. The question order
for each participant will be randomly selected from the possible combinations for each trial. The file 
`question_order_versions.tsv` contains the 8 possible combinations.

The number in each column denotes the question number for the respective question type. The first number is the question type number
and the second number is the question number within that type. For example, if in column `local_questions_1` the
number is 12, it refers to the second question of the local question type which has condition number 1. As each type has two questions,
the available numbers are 11, 12, 21, 22, 31, 32 (first number determines the type).

## Question Answer Options
The answer options are randomly shuffled for each question for each text. As the experiment shows images that are created before
running the experiment, ca. 250 versions (same number as for the stimulus versions) of answer option orders are determined and
the images for each version are created. Those images are stored in the stimulus folder for the respective language
that is used for the experiment, e.g., `stimuli_toy_x_1/question_images_toy_x_1/question_images_version_1/...` contains
the images for the questions that will be shown if the participant is assigned simulus order version 1.

The explicit shuffling of the answer options is written to a file found in the same stimulus folder in a folder called
`config/question_answer_option_shuffling_toy_x_1/`. It contains a file for each version and where is each option for each 
question is located (i.e. left, right, up, or down which corresponds to the position of the answer option in the image and the 
arrows keys that need to be pressed in order to select the respective answer).