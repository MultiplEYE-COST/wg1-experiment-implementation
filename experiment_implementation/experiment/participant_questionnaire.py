import json
from pprint import pprint

import pandas as pd
from PyQt5 import QtGui, QtWidgets
from psychopy import gui
from experiment_implementation import constants


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
            ['gender', 'years_education', 'age', 'socio_economic_status'],
            button=self.instructions['pq_next_button'],
        )

        self._show_questions(
            '',
            ['childhood_languages'],
            button=self.instructions['pq_next_button'],
        )

        if self.pq_data['childhood_languages'] == 'one language':
            self._show_questions(
                '',
                ['native_language_1'],
                button=self.instructions['pq_next_button'],
            )

        elif self.pq_data['childhood_languages'] == 'two languages':
            self._show_questions(
                '',
                ['native_language_1', 'native_language'],
                button=self.instructions['pq_next_button'],
                keys=['native_language_1', 'native_language_2']
            )

        elif self.pq_data['childhood_languages'] == 'three languages':
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
            option_labels=dialect_languages,
            keys=dialect_keys,
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
                keys=lang_keys_with_dialects,
                option_labels=lang_with_dialects,
                option_type='text'
            )

        # TODO: Fix save other_reading_time

        for lang in unique_language_keys:
            reading_questions = ['read_language','academic_reading_time', 'magazine_reading_time',
                                 'newspaper_reading_time',
                                 'email_reading_time', 'fiction_reading_time', 'nonfiction_reading_time',
                                 'internet_reading_time',
                                 'other_reading_time']

            self._show_questions(
                f'Please answer the following questions for the language {self.pq_data[lang]}',
                reading_questions,
                button=self.instructions['pq_next_button'],
                keys=[f'{lang}_{question}' for question in reading_questions],
            )

        # we allow for 4 additional languages to be mentioned
        self._show_questions(
            '',
            ['additional_read_language'],
            button=self.instructions['pq_next_button'],
            keys=[f'additional_read_language_{i}' for i in range(1, 5)],
            option_labels=[f'Additional language {i}' for i in range(1, 5)],
            option_type='dropdown_file',
            optional=True
        )

        # TODO: add the above questions again for all the additional reading languages
        # Finished

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

        # TODO: Fix save other_reading_time

        for lang in unique_reading_language_keys:
            reading_questions = ['read_language', 'academic_reading_time', 'magazine_reading_time',
                                 'newspaper_reading_time',
                                 'email_reading_time', 'fiction_reading_time', 'nonfiction_reading_time',
                                 'internet_reading_time',
                                 'other_reading_time']

            self._show_questions(
                f'Please answer the following questions for the language {self.pq_data[lang]}',
                reading_questions,
                button=self.instructions['pq_next_button'],
                keys=[f'{lang}_{question}' for question in reading_questions],
            )

        self._show_questions(
            '',
            ['tiredness', 'eyewear', 'alcohol_yesterday', 'alcohol_today'],
            button=self.instructions['pq_submit_button'],
        )

        # TODO: add confirmation dialog, i.e. list all questions and answers and they can tick a box if any of
        #  those is wrong, if yes, we show them again

        for screen_number in range(1, 8):
            self._make_changes(screen_number, unique_language_keys,
                               lang_keys_with_dialects, unique_reading_language_keys, reading_languages_mentioned)

        pprint(self.pq_data)
        # TODO: save the data! it would be best to save the dictionary, possibly just as a json file to the folder
        #  for the participant. I think it would make sense to write it to the same participant folder where the
        #  et data is. We can just pass this folder to the PQ via the exp, it should be the "abs_results_path"
        #  or something like that. The name fo the file should
        #  {Participant ID}_{LANGUAGE}_{COUNTRY_CODE}_{LAB_NUMBER}_pq_data.json or sth like that...

        self._save_data()

    def _save_data(self):
        result_file_name = (f'/{self.participant_id}_{constants.LANGUAGE}_'
                            f'{constants.COUNTRY_CODE}_{constants.LAB_NUMBER}_pq_data.json')

        result_file_path = self.results_folder + result_file_name

        with open(result_file_path, 'w') as f:
            json.dump(self.pq_data, f)

    def _show_questions(self, instructions: str, questions: list, button: str,
                        existing_data: dict = None,
                        keys: list = None,
                        option_labels: list = None,
                        option_type: str = None,
                        optional: bool = False) -> None:
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
        option_labels: list
            labels for additional free text options

        """

        if (option_type is None and option_labels is not None) or (option_type is not None and option_labels is None):
            raise ValueError('If option labels are passed, the option type must be specified.')

        if existing_data is None:
            existing_data = {}

        # TODO: the size somehow does not work, but I think it could be a bug and that we cannot change it..
        pq_gui = gui.Dlg(
            title='Participant Questionnaire',
            # Positioning the dialog boxes in the top left corner of the screen
            pos=(0, 0),
            size=(800, 900),
        )

        pq_gui.cancelBtn.setHidden(True)
        pq_gui.okBtn.setText(button)

        initial_text = pq_gui.addText(instructions)
        initial_text.setFont(QtGui.QFont(*constants.PQ_FONT_BOLD))

        # id_text = f'{self.instructions["pq_participant_id"]} {self.participant_id}'
        # part_id = pq_gui.addText(id_text)

        if keys is None:
            # use the original question identifiers as keys
            keys = questions
        else:
            # use the passed keys
            keys = keys
        if not existing_data:
            pq_data = {}
        else:
            pq_data = existing_data

        # first 4 questions on one page
        for question_id in questions:

            answer_type = self.questions[question_id]["pq_answer_type"]

            if (question_id in existing_data.keys() and
                    existing_data[question_id] != ''):

                initial_value = existing_data[question_id]
                pq_gui.addFixedField(question_id, str(initial_value))

            else:
                if answer_type == 'interval':
                    interval = self.questions[question_id]["pq_answer_option_1"].split(';')
                    options = list(range(int(interval[0]), int(interval[1]) + 1))

                elif answer_type == 'dropdown_file':
                    option_xlsx = pd.read_excel(constants.PQ_DATA_FOLDER_PATH /
                                                self.questions[question_id]["pq_answer_option_1"])
                    options = sorted(option_xlsx['language_name'].tolist())

                else:
                    options = []
                    for i in range(1, 9):
                        option = self.questions[question_id][f'pq_answer_option_{i}'].strip()
                        if option:
                            options.append(option)

                # if it is a dropdown (i.e. multiple options), the initial value is an empty string
                # which is prepended to the options
                if len(options) > 1:
                    options.insert(0, '')

                if len(options) > 0:

                    pq_gui.addField(self.questions[question_id]["pq_question_text"],
                                    choices=options,
                                    required=True,
                                    tip=self.questions[question_id]["pq_question_help"])

                else:
                    pq_gui.addText(self.questions[question_id]["pq_question_text"])

                # add help text if there is one
                if self.questions[question_id]["pq_question_help"]:
                    help_text = pq_gui.addText(self.questions[question_id]["pq_question_help"])
                    help_text.setFont(QtGui.QFont(*constants.PQ_FONT_ITALIC, italic=True))

            # if there are additional options that are no in the question file but have been passed
            if option_labels:
                for option_label in option_labels:
                    if option_type == 'checkbox':
                        pq_gui.addField(option_label, initial=False)
                    elif option_type == 'dropdown_file':
                        option_xlsx = pd.read_excel(constants.PQ_DATA_FOLDER_PATH / constants.PQ_LANGUAGES_XLSX)
                        options = sorted(option_xlsx['language_name'].tolist())
                        options.insert(0, '')
                        pq_gui.addField(option_label, choices=options, required=True)
                    else:
                        pq_gui.addField(option_label, required=True)

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

        answer_dict = {}
        for key, value in zip(keys, ok_data):
            answer_dict[key] = value

        pq_data.update(answer_dict)

        if pq_gui.OK:
            # check whether one value is empty, if yes, prompt the user to fill in all questions
            if not optional:
                for key, value in pq_data.items():
                    pprint(pq_data)
                    if value == '':
                        gui.infoDlg(prompt='Please fill in all questions.')
                        self._show_questions('Please fill in all questions! ' + instructions, questions, button=button,
                                             existing_data=pq_data, keys=keys, option_labels=option_labels,
                                             option_type=option_type)

            self.pq_data.update(pq_data)

    def _show_confirmation(self, instructions: str, questions: list, button: str,
                           existing_data: dict = None,
                           keys: list = None,
                           option_labels: list = None,
                           option_type: str = None,
                           optional: bool = False) -> None:

        if (option_type is None and option_labels is not None) or (option_type is not None and option_labels is None):
            raise ValueError('If option labels are passed, the option type must be specified.')

        if existing_data is None:
            existing_data = {}

        # TODO: the size somehow does not work, but I think it could be a bug and that we cannot change it..
        pq_gui = gui.Dlg(
            title='Participant Questionnaire',
            # Positioning the dialog boxes in the top left corner of the screen
            pos=(0, 0),
            size=(800, 900),
        )

        pq_gui.cancelBtn.setHidden(True)
        pq_gui.okBtn.setText(button)

        initial_text = pq_gui.addText(instructions)
        initial_text.setFont(QtGui.QFont(*constants.PQ_FONT_BOLD))

        # id_text = f'{self.instructions["pq_participant_id"]} {self.participant_id}'
        # part_id = pq_gui.addText(id_text)

        if keys is None:
            # use the original question identifiers as keys
            keys = questions
        else:
            # use the passed keys
            keys = keys
        if not existing_data:
            pq_data = {}
        else:
            pq_data = existing_data

        # first 4 questions on one page
        for question_id in questions:

            # answer_type = self.questions[question_id]["pq_answer_type"]

            if (question_id in existing_data.keys() and
                    existing_data[question_id] != ''):

                initial_value = existing_data[question_id]
                pq_gui.addFixedField(question_id, str(initial_value))

                pq_gui.addText(self.questions[question_id]["pq_question_text"])

                # add help text if there is one
                if self.questions[question_id]["pq_question_help"]:
                    help_text = pq_gui.addText(self.questions[question_id]["pq_question_help"])
                    help_text.setFont(QtGui.QFont(*constants.PQ_FONT_ITALIC, italic=True))

            # if there are additional options that are no in the question file but have been passed
            if option_labels:
                for option_label in option_labels:
                    if option_type == 'checkbox':
                        pq_gui.addField(option_label, initial=False)
                    elif option_type == 'dropdown_file':
                        option_xlsx = pd.read_excel(constants.PQ_DATA_FOLDER_PATH / constants.PQ_LANGUAGES_XLSX)
                        options = sorted(option_xlsx['language_name'].tolist())
                        options.insert(0, '')
                        pq_gui.addField(option_label, choices=options, required=True)
                    else:
                        pq_gui.addField(option_label, required=True)

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

        answer_dict = {}
        for key, value in zip(keys, ok_data):
            answer_dict[key] = value

        pq_data.update(answer_dict)

        if pq_gui.OK:
            # check whether one value is empty, if yes, prompt the user to fill in all questions
            if not optional:
                for key, value in pq_data.items():
                    pprint(pq_data)
                    if value == '':
                        gui.infoDlg(prompt='Please fill in all questions.')
                        self._show_questions('Please fill in all questions! ' + instructions, questions, button=button,
                                             existing_data=pq_data, keys=keys, option_labels=option_labels,
                                             option_type=option_type)

            self.confirmation_data.update(pq_data)

    def _make_changes(self, screen_number: int, unique_language_keys: list, lang_keys_with_dialects: list,
                      unique_reading_language_keys: list, reading_languages_mentioned: list):

        # The confirmation data dictionary contains all the previously filled data in the following format:
        # key=gender value= key+value (gender:female)
        confirmation_data = {}
        for key, value in self.pq_data.items():
            if value != '':
                confirmation_data[key] = ''.join(': '.join((key, str(value))))

        print(confirmation_data)

        if screen_number == 1:
            # appearance of confirmation screen. Clicking any checkboxes, would result in the appearance of the
            # fields to be changed
            first_confirmation_screen = [confirmation_data['gender'], confirmation_data['years_education'],
                                         confirmation_data['age'],
                                         confirmation_data['socio_economic_status']]
            first_confirmation_screen_keys = []
            for key, value in confirmation_data.items():
                for v in first_confirmation_screen:
                    if value == v:
                        first_confirmation_screen_keys.append(key)

            self._show_confirmation(
                '1. Click on the answers you want to change.',
                [''],
                button=self.instructions['pq_next_button'],
                keys=first_confirmation_screen_keys,
                option_labels=first_confirmation_screen,
                option_type='checkbox'
            )

            # showing the questions that have been checked in the first screen
            first_questions_checked = []
            first_questions_keys_checked = []

            # get those questions which has been checked
            for q in first_confirmation_screen_keys:
                if self.confirmation_data[q]:
                    first_questions_checked.append(q)
                    first_questions_keys_checked.append(q)

            if len(first_questions_checked) > 0:
                self._show_questions(
                    '',
                    first_questions_checked,
                    button=self.instructions['pq_next_button'],
                )

        elif screen_number == 2:
            # appearance of second confirmation screen.
            second_confirmation_screen = []
            second_confirmation_screen_key = []

            for key, value in confirmation_data.items():
                if key in unique_language_keys:
                    second_confirmation_screen.append(confirmation_data[key])
                    second_confirmation_screen_key.append(key)

            self._show_confirmation(
                '2. Click on the answers you want to change.',
                [''],
                button=self.instructions['pq_next_button'],
                keys=second_confirmation_screen_key,
                option_labels=second_confirmation_screen,
                option_type='checkbox'
            )

            # showing the questions that have been checked in the second screen
            second_questions_checked = []
            second_questions_keys_checked = []

            # get those questions which has been checked
            for q in second_confirmation_screen_key:
                if self.confirmation_data[q] and (
                        q == 'native_language_1' or q == 'dominant_language' or q == 'use_language'):
                    second_questions_checked.append(q)
                    second_questions_keys_checked.append(q)
                elif self.confirmation_data[q] and (
                        q != 'native_language_1' or q != 'dominant_language' or q != 'use_language'):
                    second_questions_checked.append(q[0:15])
                    second_questions_keys_checked.append(q)

            if len(second_questions_checked) > 0:
                self._show_questions(
                    '',
                    second_questions_checked,
                    button=self.instructions['pq_next_button'],
                    keys=second_questions_keys_checked,
                )

        elif screen_number == 3:
            # appearance of third confirmation screen.

            if lang_keys_with_dialects:
                third_confirmation_screen = []
                third_confirmation_screen_key = []
                for key, value in confirmation_data.items():
                    if key in lang_keys_with_dialects:
                        third_confirmation_screen.append(confirmation_data[key])
                        third_confirmation_screen_key.append(key)

                self._show_confirmation(
                    '3. Click on the answers you want to change.',
                    [''],
                    button=self.instructions['pq_next_button'],
                    keys=third_confirmation_screen_key,
                    option_labels=third_confirmation_screen,
                    option_type='checkbox'
                )

                third_questions_checked = []
                third_questions_keys_checked = []

                # get those questions which has been checked
                for q in third_confirmation_screen_key:
                    if self.confirmation_data[q]:
                        pprint(q[-12:])
                        third_questions_checked.append(q[-12:])
                        third_questions_keys_checked.append(q)

                # TODO Find a way to remove the option_label so that the question is not duplicated

                if len(third_questions_checked) > 0:
                    self._show_questions(
                        '',
                        third_questions_checked,
                        button=self.instructions['pq_next_button'],
                        keys=third_questions_keys_checked,
                        option_labels=third_questions_checked,
                        option_type='text'
                    )

        elif screen_number == 4:
            # appearance of fourth confirmation screen.

            # TODO: Fix to show other_reading_time

            for lang in unique_language_keys:
                fourth_confirmation_screen = []
                fourth_confirmation_screen_key = []
                reading_questions = ['read_language', 'academic_reading_time', 'magazine_reading_time',
                                     'newspaper_reading_time',
                                     'email_reading_time', 'fiction_reading_time', 'nonfiction_reading_time',
                                     'internet_reading_time',
                                     'other_reading_time']

                for key, value in confirmation_data.items():
                    if key in [f'{lang}_{question}' for question in reading_questions]:
                        fourth_confirmation_screen.append(confirmation_data[key])
                        fourth_confirmation_screen_key.append(key)

                self._show_confirmation(
                    f'4. Click on the answers you want to change for the language {self.pq_data[lang]}.',
                    [''],
                    button=self.instructions['pq_next_button'],
                    keys=fourth_confirmation_screen_key,
                    option_labels=fourth_confirmation_screen,
                    option_type='checkbox',
                )

                fourth_questions_checked = []
                fourth_questions_keys_checked = []

                # get those questions which has been checked
                for q in fourth_confirmation_screen_key:
                    if self.confirmation_data[q]:
                        # email_reading_time
                        if q[-18:] == 'email_reading_time':
                            fourth_questions_checked.append(q[-18:])
                            fourth_questions_keys_checked.append(q)
                        # academic_reading_time
                        elif q[-21:] == 'academic_reading_time':
                            fourth_questions_checked.append(q[-21:])
                            fourth_questions_keys_checked.append(q)
                        # nonfiction_reading_time
                        elif q[-23:] == 'nonfiction_reading_time':
                            fourth_questions_checked.append(q[-23:])
                            fourth_questions_keys_checked.append(q)
                        # fiction_reading_time
                        elif q[-20:] == 'fiction_reading_time':
                            fourth_questions_checked.append(q[-20:])
                            fourth_questions_keys_checked.append(q)
                        # internet_reading_time
                        elif q[-21:] == 'internet_reading_time':
                            fourth_questions_checked.append(q[-21:])
                            fourth_questions_keys_checked.append(q)
                        # magazine_reading_time
                        elif q[-21:] == 'magazine_reading_time':
                            fourth_questions_checked.append(q[-21:])
                            fourth_questions_keys_checked.append(q)
                        # newspaper_reading_time
                        elif q[-22:] == 'newspaper_reading_time':
                            fourth_questions_checked.append(q[-22:])
                            fourth_questions_keys_checked.append(q)

                        # TODO: Fix for other_reading_time
                        # elif q[-18:] == 'other_reading_time':
                        #    fourth_questions_checked.append(q[-18:])
                        #    fourth_questions_keys_checked.append(q)

                if len(fourth_questions_checked) > 0:
                    self._show_questions(
                        '',
                        fourth_questions_checked,
                        button=self.instructions['pq_next_button'],
                        keys=fourth_questions_keys_checked,
                    )

        elif screen_number == 5:

            if reading_languages_mentioned:
                fifth_confirmation_screen = []
                fifth_confirmation_screen_key = []
                for key, value in confirmation_data.items():
                    if key in reading_languages_mentioned:
                        fifth_confirmation_screen.append(confirmation_data[key])
                        fifth_confirmation_screen_key.append(key)

                self._show_confirmation(
                    '5. Click on the answers you want to change.',
                    [''],
                    button=self.instructions['pq_next_button'],
                    keys=fifth_confirmation_screen_key,
                    option_labels=fifth_confirmation_screen,
                    option_type='checkbox'
                )

                fifth_questions_checked = []
                fifth_questions_keys_checked = []

                # get those questions which has been checked
                for q in fifth_confirmation_screen_key:
                    if self.confirmation_data[q]:
                        fifth_questions_checked.append(q[0:24])
                        fifth_questions_keys_checked.append(q)

                # TODO Find a way to remove the option_label so that the question is not duplicated

                if len(fifth_questions_checked) > 0:
                    self._show_questions(
                        '',
                        fifth_questions_checked,
                        button=self.instructions['pq_next_button'],
                        keys=fifth_questions_keys_checked,
                        option_labels=fifth_questions_checked,
                        option_type='dropdown_file'
                    )

        elif screen_number == 6:
            # TODO: Fix to show other_reading_time

            for lang in unique_reading_language_keys:
                sixth_confirmation_screen = []
                sixth_confirmation_screen_key = []
                reading_questions = ['read_language', 'academic_reading_time', 'magazine_reading_time',
                                     'newspaper_reading_time',
                                     'email_reading_time', 'fiction_reading_time', 'nonfiction_reading_time',
                                     'internet_reading_time',
                                     'other_reading_time']

                for key, value in confirmation_data.items():
                    if key in [f'{lang}_{question}' for question in reading_questions]:
                        sixth_confirmation_screen.append(confirmation_data[key])
                        sixth_confirmation_screen_key.append(key)

                self._show_confirmation(
                    f'6. Click on the answers you want to change for the language {self.pq_data[lang]}.',
                    [''],
                    button=self.instructions['pq_next_button'],
                    keys=sixth_confirmation_screen_key,
                    option_labels=sixth_confirmation_screen,
                    option_type='checkbox',
                )
                sixth_questions_checked = []
                sixth_questions_keys_checked = []

                # get those questions which has been checked
                for q in sixth_confirmation_screen_key:
                    if self.confirmation_data[q]:
                        # email_reading_time
                        if q[-18:] == 'email_reading_time':
                            sixth_questions_checked.append(q[-18:])
                            sixth_questions_keys_checked.append(q)
                        # academic_reading_time
                        elif q[-21:] == 'academic_reading_time':
                            sixth_questions_checked.append(q[-21:])
                            sixth_questions_keys_checked.append(q)
                        # nonfiction_reading_time
                        elif q[-23:] == 'nonfiction_reading_time':
                            sixth_questions_checked.append(q[-23:])
                            sixth_questions_keys_checked.append(q)
                        # fiction_reading_time
                        elif q[-20:] == 'fiction_reading_time':
                            sixth_questions_checked.append(q[-20:])
                            sixth_questions_keys_checked.append(q)
                        # internet_reading_time
                        elif q[-21:] == 'internet_reading_time':
                            sixth_questions_checked.append(q[-21:])
                            sixth_questions_keys_checked.append(q)
                        # magazine_reading_time
                        elif q[-21:] == 'magazine_reading_time':
                            sixth_questions_checked.append(q[-21:])
                            sixth_questions_keys_checked.append(q)
                        # newspaper_reading_time
                        elif q[-22:] == 'newspaper_reading_time':
                            sixth_questions_checked.append(q[-22:])
                            sixth_questions_keys_checked.append(q)

                        # TODO: Fix for other_reading_time
                        # elif q[-18:] == 'other_reading_time':
                        #    fourth_questions_checked.append(q[-18:])
                        #    fourth_questions_keys_checked.append(q)

                # if there are any dialects
                if len(sixth_questions_checked) > 0:
                    self._show_questions(
                        '',
                        sixth_questions_checked,
                        button=self.instructions['pq_next_button'],
                        keys=sixth_questions_keys_checked,
                    )

        elif screen_number == 7:
            seventh_confirmation_screen_key = []

            seventh_confirmation_screen = [confirmation_data['tiredness'],
                                           confirmation_data['eyewear'],
                                           confirmation_data['alcohol_yesterday'],
                                           confirmation_data['alcohol_today']]

            for key, value in confirmation_data.items():
                for v in seventh_confirmation_screen:
                    if value == v:
                        seventh_confirmation_screen_key.append(key)

            self._show_confirmation(
                '7. Click on the answers you want to change.',
                [''],
                button=self.instructions['pq_next_button'],
                keys=seventh_confirmation_screen_key,
                option_labels=seventh_confirmation_screen,
                option_type='checkbox'
            )

            seventh_questions_checked = []
            seventh_questions_keys_checked = []

            # get those questions which has been checked
            for q in seventh_confirmation_screen_key:
                if self.confirmation_data[q]:
                    seventh_questions_checked.append(q)
                    seventh_questions_keys_checked.append(q)

            # if there are any dialects
            if len(seventh_questions_checked) > 0:
                self._show_questions(
                    '',
                    seventh_questions_checked,
                    button=self.instructions['pq_next_button'],
                    keys=seventh_questions_keys_checked
                )

if __name__ == '__main__':
    participant_id = 1
    pq = MultiplEYEParticipantQuestionnaire(participant_id, 'res')
    pq.run_questionnaire()
