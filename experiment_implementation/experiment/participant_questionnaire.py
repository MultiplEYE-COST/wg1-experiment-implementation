import json
import os.path
from pprint import pprint

import pandas as pd
from PyQt6 import QtGui, QtWidgets
from psychopy import gui
import constants


class MultiplEYEParticipantQuestionnaire:

    def __init__(self, participant_identifier: int, results_folder: str):
        self.instructions, self.questions = self.load_data()
        self.participant_id = participant_identifier
        self.pq_data = {}
        self.confirmation_data = {}
        self.results_folder = results_folder

    def load_data(self):

        # read the instructions to a dictionary
        pq_instructions_dict = pd.read_excel(constants.PQ_PARTICIPANT_INSTRUCTIONS_XLSX,
                                             index_col='pq_instructions').to_dict(
            orient='dict')
        pq_instructions_dict = pq_instructions_dict['pq_text']

        pq_questions = pd.read_excel(constants.PQ_QUESTIONS_XLSX, index_col='pq_question_identifier').fillna('')
        pq_questions = pq_questions.to_dict(orient='index')

        return pq_instructions_dict, pq_questions

    def run_questionnaire(self):
        self._show_questions(
            self.instructions['pq_initial_message'],
            ['gender', 'years_education', 'level_education', 'age', 'socio_economic_status'],
            button=self.instructions['pq_next_button'],
        )

        self._show_questions(
            '',
            ['childhood_languages'],
            button=self.instructions['pq_next_button'],
        )

        # check whether there are multiple languages that the person grew up with
        if self.pq_data['childhood_languages'] == self.questions['childhood_languages']['pq_answer_option_1']:
            self._show_questions(
                '',
                ['native_language_1'],
                button=self.instructions['pq_next_button'],
            )
        elif self.pq_data['childhood_languages'] == self.questions['childhood_languages']['pq_answer_option_2']:
            self._show_questions(
                '',
                ['native_language_1', 'native_language'],
                button=self.instructions['pq_next_button'],
                keys=['native_language_1', 'native_language_2']
            )
        elif self.pq_data['childhood_languages'] == self.questions['childhood_languages']['pq_answer_option_3']:
            self._show_questions(
                '',
                ['native_language_1', 'native_language', 'native_language'],
                button=self.instructions['pq_next_button'],
                keys=['native_language_1', 'native_language_2', 'native_language_3']
            )

        self._show_questions(
            '',
            ['use_language', 'dominant_language'],
            button=self.instructions['pq_next_button'],
        )

        languages_mentioned = ['native_language_1', 'native_language_2',
                               'native_language_3', 'use_language', 'dominant_language'
                               ]
        # get those languages that have been mentioned in the previous questions and whose keys are in the pq_data
        languages_mentioned = [language for language in languages_mentioned if
                               language in self.pq_data.keys() and self.pq_data[language] != '']

        unique_languages = []
        unique_language_keys = []
        for lang_key in languages_mentioned:
            if self.pq_data[lang_key] not in unique_languages:
                unique_language_keys.append(lang_key)
                unique_languages.append(self.pq_data[lang_key])

        # only ask for unique languages, no need to ask for the same language twice
        dialect_keys = []
        dialect_languages = []
        for lang in languages_mentioned:
            if self.pq_data[lang] not in dialect_languages:
                dialect_languages.append(self.pq_data[lang])
                dialect_keys.append(f'{lang}_dialect')

        self._show_questions(
            '',
            ['dialect'],
            button=self.instructions['pq_next_button'],
            option_labels=[(k, v) for (k, v) in zip(dialect_languages, dialect_keys)],
            option_type='checkbox',
        )

        lang_with_dialects = []
        lang_keys_with_dialects = []
        # get those languages for which dialects have been mentioned
        for dialect_k in dialect_keys:
            if self.pq_data[dialect_k]:
                lang_key = '_'.join(dialect_k.split('_')[:-1])
                language_name = self.pq_data[lang_key]

                # if the language is already in the list
                if language_name not in lang_with_dialects:
                    lang_with_dialects.append(self.pq_data[lang_key])

                    lang_keys_with_dialects.append(f'{lang_key}_dialect_name')

        # if there are any dialects
        if len(lang_with_dialects) > 0:
            self._show_questions(
                '',
                ['dialect_name'],
                button=self.instructions['pq_next_button'],
                option_labels=[(k, v) for (k, v) in zip(lang_with_dialects, lang_keys_with_dialects)],
                option_type='text'
            )

        for lang in unique_language_keys:
            reading_questions = ['read_language', 'academic_reading_time', 'magazine_reading_time',
                                 'newspaper_reading_time',
                                 'email_reading_time', 'fiction_reading_time', 'nonfiction_reading_time',
                                 'internet_reading_time',
                                 'other_reading_time']

            self._show_questions(
                f'{self.instructions["pq_answer_for_lang"]} {self.pq_data[lang]}',
                reading_questions,
                button=self.instructions['pq_next_button'],
                keys=[f'{lang}_{question}' for question in reading_questions[1:]],
            )

        # we allow for 4 additional languages to be mentioned
        options = zip([f'{self.instructions["pq_additional_language"]} {i}' for i in range(1, 5)],
                      [f'additional_read_language_{i}' for i in range(1, 5)])

        self._show_questions(
            '',
            ['additional_read_language'],
            button=self.instructions['pq_next_button'],
            existing_data=self.pq_data,
            option_labels=[(k, v) for (k, v) in options],
            option_type='dropdown_file',
            optional=True
        )

        reading_languages_mentioned = ['additional_read_language_1', 'additional_read_language_2',
                                       'additional_read_language_3', 'additional_read_language_4']

        # get those languages that have been mentioned in the previous questions and whose keys are in the pq_data
        reading_languages_mentioned = [language for language in reading_languages_mentioned if
                                       language in self.pq_data.keys() and self.pq_data[language] != '']

        unique_reading_languages = []
        unique_reading_language_keys = []
        for lang_key in reading_languages_mentioned:
            if self.pq_data[lang_key] not in unique_reading_languages:
                unique_reading_language_keys.append(lang_key)
                unique_reading_languages.append(self.pq_data[lang_key])

        for lang in unique_reading_language_keys:
            reading_questions = ['read_language', 'academic_reading_time', 'magazine_reading_time',
                                 'newspaper_reading_time',
                                 'email_reading_time', 'fiction_reading_time', 'nonfiction_reading_time',
                                 'internet_reading_time',
                                 'other_reading_time']

            self._show_questions(
                f'{self.instructions["pq_answer_for_lang"]}: {self.pq_data[lang]}',
                reading_questions,
                button=self.instructions['pq_next_button'],
                keys=[f'{lang}_{question}' for question in reading_questions[1:]],
            )

        self._show_questions(
            '',
            ['tiredness', 'eyewear', 'alcohol_yesterday', 'alcohol_today'],
            button=self.instructions['pq_submit_button'],
        )

        pprint(self.pq_data)
        self._save_data()

        # show goodbye message
        gui.infoDlg(prompt=self.instructions['pq_final_message'])

    def _save_data(self):
        result_file_name = (f'/{self.participant_id}_{constants.LANGUAGE}_'
                            f'{constants.COUNTRY_CODE}_{constants.LAB_NUMBER}_pq_data.json')

        result_file_path = self.results_folder + result_file_name

        with open(result_file_path, 'w', encoding='utf8') as f:
            json.dump(self.pq_data, f, indent=4)

    def _show_questions(self, instructions: str, questions: list, button: str,
                        existing_data: dict = None,
                        keys: list = None,
                        option_labels: list[tuple[str, str]] = None,
                        option_type: str = None,
                        optional: bool = False,
                        confirmed: bool = False,
                        recalled: bool = False) -> None:
        """
        Show the questions in a dialog box and save the answers to the pq_data dictionary.

        instructions: str
            the instructions for the questionnaire
        questions: list
            the identifiers of the questions to be shown, cna be retrieved from the question dictionary
        existing_data: dict
            the answers to the questions that have already been answered
        keys: list
            in case that the keys that should be used for the final data are not the same as the question identifiers,
            they can be passed as a list
        option_labels: list[tuple(str, str)]
            labels for additional free text options together with their identifiers (label, identifier)
        option_type: str
            the type of the additional options, either 'text' or 'checkbox'
        optional: bool
            whether the questions are optional or not
        confirmed: bool
            whether the answers have been confirmed or not
        recalled: bool
            whether the questions are being recalled or not, e.g. if something was wrong with the answers

        """

        if (option_type is None and option_labels is not None) or (option_type is not None and option_labels is None):
            raise ValueError('If option labels are passed, the option type must be specified.')

        if existing_data is None:
            existing_data = {}

        pq_gui = gui.Dlg(
            title=self.instructions['pq_title'],
            # Positioning the dialog boxes in the top left corner of the screen
            pos=(constants.IMAGE_WIDTH_PX // 12, constants.IMAGE_HEIGHT_PX // 10),
            size=(800, 900),
        )

        try:
            pq_gui.cancelBtn.setHidden(True)
            pq_gui.okBtn.setText(button)
        except AttributeError:
            pass

        font = QtGui.QFont(*constants.PQ_FONT_BOLD)
        font.setBold(True)
        initial_text = pq_gui.addText(instructions)
        initial_text.setFont(font)

        if not recalled:
            # we only need to do this if it is the first time that the questions are presented on the screen
            if keys is None:
                # use the original question identifiers as keys
                keys = questions
            else:
                # use the passed keys
                keys = keys

            # update questions to be a list of tuples containing the question id and the key
            questions = list(zip(questions, keys))

        if not existing_data:
            pq_data = {}
        else:
            pq_data = existing_data

         # first 4 questions on one page
        for question_id, question_key in questions:
            # Adding the current language in the additional_read_language question
            if question_id == "additional_read_language":
                self.questions["additional_read_language"][
                    "pq_question_text"] = f'{self.questions["additional_read_language"]["pq_question_text"]}'

            answer_type = self.questions[question_id]["pq_answer_type"]

            # collect all the options for the questions if there are any
            if answer_type == 'interval':
                interval = self.questions[question_id]["pq_answer_option_1"].split(';')
                options = list(range(int(interval[0]), int(interval[1]) + 1))
                if question_id == "years_education":
                    options.append(self.questions[question_id]["pq_answer_option_2"])

            elif answer_type == 'dropdown_file':
                option_xlsx = pd.read_excel(constants.PQ_DATA_FOLDER_PATH /
                                            self.questions[question_id]["pq_answer_option_1"])
                options = sorted(option_xlsx['language_name'].tolist())

            else:
                options = []
                for i in range(1, 10):
                    option = self.questions[question_id][f'pq_answer_option_{i}'].strip()
                    if option:
                        options.append(option)

            # if it is a dropdown (i.e. multiple options), the initial value is an empty string
            # which is prepended to the options
            if len(options) > 1:
                options.insert(0, '')

            if len(options) > 0:

                question_text = pq_gui.addField(question_key,
                                                label=self.questions[question_id]["pq_question_text"],
                                                choices=options,
                                                initial=existing_data.get(question_id, ''),
                                                tip=self.questions[question_id]["pq_question_help"]
                                                )

                question_text.setFont(QtGui.QFont(*constants.PQ_FONT_BOLD))

            else:
                question_text = pq_gui.addText(self.questions[question_id]["pq_question_text"])
                question_text.setFont(QtGui.QFont(*constants.PQ_FONT_BOLD))

            # add help text if there is one
            if self.questions[question_id]["pq_question_help"]:
                help_text = pq_gui.addText(self.questions[question_id]["pq_question_help"])
                help_text.setFont(QtGui.QFont(*constants.PQ_FONT_ITALIC, italic=True))

            # if there are additional options that are no in the question file but have been passed
            if option_labels:
                for option_label, option_key in option_labels:
                    if option_type == 'checkbox':
                        pq_gui.addField(option_key, label=option_label, initial=False)
                    elif option_type == 'dropdown_file':
                        option_xlsx = pd.read_excel(constants.PQ_DATA_FOLDER_PATH / constants.PQ_LANGUAGES_XLSX)
                        options = sorted(option_xlsx['language_name'].tolist())
                        options.insert(0, '')
                        pq_gui.addField(option_key, label=option_label, choices=options)
                    else:
                        pq_gui.addField(option_key, label=option_label)

        pq_gui.addText('')
        pq_gui.addText('')
        pq_gui.addField('confirm_answer', self.instructions['pq_confirm_answers'], initial=False)

        # the item in the top left position is some default text that I don't know how to remove otherwise
        pq_gui.layout.itemAtPosition(0, 0).widget().hide()

        # via psychopy it is not possible to access the label information, which is why we do it like below.
        # This is simply to change the font size via the layout grid
        num_rows = pq_gui.layout.rowCount()
        num_cols = pq_gui.layout.columnCount()

        # exclude the first two rows, these are the instructions and the ID
        for row in range(2, num_rows):
            for col in range(num_cols):
                item = pq_gui.layout.itemAtPosition(row, col)
                # if we have already changed the font to italic, we don't want to change it again
                if not item.widget().font().family() == constants.PQ_FONT_ITALIC[0]:
                    item.widget().setFont(QtGui.QFont(*constants.PQ_FONT))

        ok_data = pq_gui.show()
        # the last entry is always the confirmation checkbox
        answers_confirmed = pq_gui.data['confirm_answer']

        pq_data.update(ok_data)

        if pq_gui.OK:
            # check whether one value is empty, if yes, prompt the user to fill in all questions
            if not optional:
                for key, value in pq_data.items():
                    if value == '':
                        gui.warnDlg(prompt=self.instructions['pq_answer_all'],
                                    title=self.instructions['pq_error_title'])
                        self._show_questions(self.instructions['pq_answer_all'] + ' ' + instructions, questions,
                                             button=button,
                                             existing_data=pq_data, keys=keys, option_labels=option_labels,
                                             option_type=option_type, confirmed=answers_confirmed,
                                             recalled=True, optional=optional)
            if not answers_confirmed:
                gui.warnDlg(prompt=self.instructions['pq_confirmation'],
                            title=self.instructions['pq_error_title'])
                self._show_questions(self.instructions['pq_answer_all'] + ' ' + instructions, questions,
                                     button=button,
                                     existing_data=pq_data, keys=keys, option_labels=option_labels,
                                     option_type=option_type, confirmed=answers_confirmed,
                                     recalled=True, optional=optional)

            # update the dictionary with the new data and save it to file
            self.pq_data.update(pq_data)
            self._save_data()


if __name__ == '__main__':
    participant_id = 1

    # create res folder
    os.makedirs('res', exist_ok=True)

    pq = MultiplEYEParticipantQuestionnaire(participant_id, 'res')
    pq.run_questionnaire()