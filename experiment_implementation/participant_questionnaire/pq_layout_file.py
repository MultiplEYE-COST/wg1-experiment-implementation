import PySimpleGUI as sg
import pandas as pd

from participant_questionnaire import pq_read_files as read_questions
from participant_questionnaire import pq_constants as pq_constants
import constants


def pq_main_layout():
    # TODO: Change depending on the experiment config
    sg.theme('Native')
    sg.set_options(font=('Times New Roman', 20))

    # Creating the layout for the header element (program description + icon)
    c00 = [
        [sg.Text(pq_constants.pq_program_name, font=("Times New Roman", 16, "bold"), background_color='#ffffff')],
        [sg.Text(pq_constants.pq_program_description, font=("Times New Roman", 16), background_color='#ffffff')]
    ]
    c01 = [
        [sg.Image(constants.PQ_image_dir, size=(100, 120), background_color='#ffffff', )]
    ]
    c02 = [sg.Column(c00, background_color='#ffffff', expand_x=True, expand_y=True),
           sg.Column(c01, background_color='#ffffff', expand_x=True, expand_y=True, element_justification='r')]

    layout_h = [[sg.Frame("", [c02], size=(1000, 100), background_color='#ffffff', pad=0, expand_x=True)]]

    # Creating the layout for the first frame
    # ID_1 need to be replaced with the Participant ID from the experiment implementation
    c11 = [
        sg.Text('' + read_questions.pq_instructions[3][1] + '\n\n', font=("Times New Roman", 20, "bold", "italic")),
        sg.Text('' + constants.PQ_Participant_ID + '\n\n', font=("Times New Roman", 20, "bold", "italic"))]

    c12 = [sg.Text('1. ' + read_questions.pq_questions[0][1], size=(50, None)),
           sg.Combo([read_questions.pq_questions[0][2], read_questions.pq_questions[0][3],
                     read_questions.pq_questions[0][4], read_questions.pq_questions[0][5]], size=(25, 1),
                    pad=(50, 0),
                    key='gender')]

    c13 = [sg.Text('2. ' + read_questions.pq_questions[1][1], size=(50, None)),
           sg.Combo(list(range(1, 21)), size=(25, 1), pad=(50, 0), key='years_education')]

    c14 = [sg.Text(' ' + read_questions.pq_questions[1][11], size=(70, None), pad=(25, 0),
                   font=("Times New Roman", 14, "italic"))]

    c15 = [sg.Text('3. ' + read_questions.pq_questions[2][1], size=(50, None)),
           sg.In(pad=(50, 0), size=26, key='age')]

    c16 = [sg.Text(' ' + read_questions.pq_questions[2][11], size=(70, None), pad=(25, 0),
                   font=("Times New Roman", 14, "italic"))]

    c17 = [sg.Text('4. ' + read_questions.pq_questions[3][1], size=(50, None)),
           sg.Combo(
               [read_questions.pq_questions[3][2], read_questions.pq_questions[3][3],
                read_questions.pq_questions[3][4],
                read_questions.pq_questions[3][5]], size=(25, 1), pad=(50, 0), key='socio_economic_status')]

    layout1 = [c11, c12, c13, c14, c15, c16, c17]

    # Creating the layout for the second frame
    c21 = [sg.Text('5. ' + read_questions.pq_questions[4][1], size=(50, None)),
           sg.Combo([read_questions.pq_questions[4][2], read_questions.pq_questions[4][3],
                     read_questions.pq_questions[4][4]], size=25, pad=(50, 0), key='childhood_languages',
                    enable_events=True, readonly=False)]

    c22 = [sg.Text(' ' + read_questions.pq_questions[4][11], size=(70, None), pad=(20, 0),
                   font=("Times New Roman", 14, "italic"))]

    c23 = [sg.Text('6. ' + read_questions.pq_questions[5][1], size=(50, None)),
           sg.Combo(read_questions.pq_language_list, size=25, pad=(50, 0), key='first_native_language',
                    enable_events=True),
           ]
    col1 = [c21, c22, c23]

    # These elements are made visible depending on the answer to question 5
    c24 = [[sg.Text('7. ' + read_questions.pq_questions[6][1], size=(50, None))]]
    c25 = [
        [sg.Text('' + read_questions.pq_instructions[11][1], size=(25, None)),
         sg.Combo(read_questions.pq_language_list,
                  size=22,
                  key='second_native_language',
                  enable_events=True)]]
    c26 = [
        [sg.Text('' + read_questions.pq_instructions[12][1], size=(25, None)),
         sg.Combo(read_questions.pq_language_list,
                  size=22,
                  key='third_native_language',
                  enable_events=True)]]

    layout2 = [[sg.Column(col1, element_justification='l')],
               [sg.Column(c24, element_justification='l', key='question_7', visible=False)],
               [sg.Column(c25, element_justification='l', key='question_7_2', visible=False)],
               [sg.Column(c26, element_justification='l', key='question_7_3', visible=False)]]

    # Creating the layout for the third frame

    # TODO Fix the removal of selected languages from combobox
    # TODO Fix adding again dialects after removing all of them
    c31 = [sg.Text('8. ' + read_questions.pq_questions[7][1], size=(50, 2)),
           sg.Combo(read_questions.pq_language_list, size=25, pad=(50, 0), key='use_language', enable_events=True)]
    c32 = [sg.Text('9. ' + read_questions.pq_questions[8][1], size=(50, 2)),
           sg.Combo(read_questions.pq_language_list, size=25, pad=(50, 0), key='dominant_language',
                    enable_events=True)]
    c33 = [sg.Text('10. ' + read_questions.pq_questions[9][1], size=(50, 2)),
           sg.Combo([read_questions.pq_questions[9][2], read_questions.pq_questions[9][3]], size=25, pad=(50, 0),
                    key='dialect', enable_events=True, default_value=read_questions.pq_questions[9][3]),
           ]
    col3 = [c31, c32, c33]

    c34 = [[sg.Text('' + read_questions.pq_instructions[15][1]), sg.B('+', key='add_dialect', enable_events=True)]]

    c35 = [[sg.Frame('' + read_questions.pq_instructions[16][1], [[sg.T('')]], key='frame_dialect')]]

    layout3 = [[sg.Column(col3, element_justification='l')],
               [sg.Column(c34, element_justification='l', key='adding_dialect', visible=False)],
               [sg.Column(c35, element_justification='l', key='column_dialect', visible=False)]
               ]

    # The layouts from 4 to 8 are initially empty, made visible depending on languages chosen

    layout4 = [[sg.Text("", key='layout_4', pad=0, expand_x=True, expand_y=True)]]
    layout5 = [[sg.Text("", key='layout_5', pad=0, expand_x=True, expand_y=True)]]
    layout6 = [[sg.Text("", key='layout_6', pad=0, expand_x=True, expand_y=True)]]
    layout7 = [[sg.Text("", key='layout_7', pad=0, expand_x=True, expand_y=True)]]
    layout8 = [[sg.Text("", key='layout_8', pad=0, expand_x=True, expand_y=True)]]

    # Creating the layout for the fifth frame

    # TODO Fix adding again languages after having removed them
    c51 = [[sg.Text('12. ' + read_questions.pq_questions[19][1], size=(50, None)),
            sg.Combo([read_questions.pq_questions[19][2], read_questions.pq_questions[19][3]], size=(22, 1),
                     key='read_language', enable_events=True)]]
    c52 = [[sg.Text(' ' + read_questions.pq_questions[19][11], size=(50, None), pad=(20, 0),
                    font=("Times New Roman", 14, "italic"))]]
    c53 = [[sg.Text('' + read_questions.pq_instructions[8][1]), sg.B('+', key='add_language', enable_events=True)]]

    c54 = [[sg.Frame('' + read_questions.pq_instructions[10][1], [[sg.T('')]], key='frame_reading_language')]]

    layout9 = [[sg.Column(c51, element_justification='l')],
               [sg.Column(c52, element_justification='l')],
               [sg.Column(c53, element_justification='l', key='adding_language', visible=False)],
               [sg.pin(sg.Column(c54, element_justification='l', key='column_reading_language', visible=False))]
               ]

    # Creating the layout for the seventh frame

    c71 = [sg.Text('13. ' + read_questions.pq_questions[20][1], size=(45, None)),
           sg.Combo(
               [read_questions.pq_questions[20][2], read_questions.pq_questions[20][3],
                read_questions.pq_questions[20][4]],
               size=(47, 1), key='eyewear')]
    c72 = [sg.Text('14. ' + read_questions.pq_questions[21][1], size=(45, None)),
           sg.Combo([read_questions.pq_questions[21][2], read_questions.pq_questions[21][3],
                     read_questions.pq_questions[21][4], read_questions.pq_questions[21][5],
                     read_questions.pq_questions[21][6],
                     read_questions.pq_questions[21][7], read_questions.pq_questions[21][8],
                     read_questions.pq_questions[21][9], read_questions.pq_questions[21][10]], size=(47, 1),
                    key='tiredness')]
    c73 = [sg.Text('15. ' + read_questions.pq_questions[22][1], size=(45, None)),
           sg.Combo(
               [read_questions.pq_questions[22][2], read_questions.pq_questions[22][3],
                read_questions.pq_questions[22][4]],
               size=(47, 1), key='alcohol_yesterday')]
    c74 = [sg.Text(' ' + read_questions.pq_questions[22][11], size=(50, None), pad=(20, 0),
                   font=("Times New Roman", 14, "italic"))]
    c75 = [sg.Text('16. ' + read_questions.pq_questions[23][1], size=(45, None)),
           sg.Combo(
               [read_questions.pq_questions[23][2], read_questions.pq_questions[23][3],
                read_questions.pq_questions[23][4]],
               size=(47, 1), key='alcohol_today')]
    c76 = [sg.Text(' ' + read_questions.pq_questions[23][11], size=(50, None), pad=(20, 0),
                   font=("Times New Roman", 14, "italic"))]
    layout10 = [c71, c72, c73, c74, c75, c76]

   # Creating the layout for the eighth frame
    layout11 = [[sg.Text("" + read_questions.pq_instructions[19][1], size=(75, None),
                         justification='center')]]

    # Changing layout visibility to True/False depending on the selection of Prev/Next buttons
    q = [sg.VPush(),
         sg.Column(layout1, pad=20, key='-COL1-'),
         sg.Column(layout2, visible=False, pad=20, key='-COL2-'),
         sg.Column(layout3, visible=False, pad=20, key='-COL3-'),
         sg.Column(layout4, visible=False, key='-COL4-'),
         sg.Column(layout5, visible=False, key='-COL5-'),
         sg.Column(layout6, visible=False, key='-COL6-'),
         sg.Column(layout7, visible=False, key='-COL7-'),
         sg.Column(layout8, visible=False, key='-COL8-'),
         sg.Column(layout9, visible=False, pad=20, key='-COL9-'),
         sg.Column(layout10, visible=False, pad=20, key='-COL10-'),
         sg.Column(layout11, visible=False, pad=10, key='-COL11-', element_justification='c'),
         sg.VPush()]

    layout_questions = [
        [sg.Frame("", [q], size=(1000, 350), key='layout_questions', element_justification='c', pad=0, expand_x=True,
                  expand_y=True)]]

    # Create layout for the buttons (prev, next, submit)
    b = [sg.pin(sg.Button('' + read_questions.pq_instructions[5][1], key='prev', size=(10, 1), mouseover_colors='grey',
                          use_ttk_buttons=True, visible=False)),
         sg.Push(),
         sg.pin(sg.Button('' + read_questions.pq_instructions[4][1], key='next', size=(10, 1), mouseover_colors='grey',
                          use_ttk_buttons=True)),
         sg.pin(
             sg.Button('' + read_questions.pq_instructions[6][1], key='submit', size=(10, 1), mouseover_colors='grey',
                       use_ttk_buttons=True, visible=False))
         ]

    layout_b = [[sg.Frame("", [b], size=(1000, 55), pad=0, expand_x=True)]]

    # Create actual layout
    # Header + Layout of questions + Layout of buttons
    layout = [layout_h, layout_questions, layout_b]

    # Finalizing window
    window = sg.Window(pq_constants.pq_program_name, layout, resizable=True,
                       location=(0, 0), icon=constants.PQ_program_icon,
                       margins=(0, 0), return_keyboard_events=True, element_justification='c'
                       ).Finalize()

    # Maximize window for full screen
    # TODO To be fixed, get screen size
    window.Maximize()

    # Load the data if the file exists, if not, create a new DataFrame
    def load_data():
        FILE = constants.PQ_FILE
        if FILE.exists():
            df = pd.read_csv(FILE)
        else:
            df = pd.DataFrame()
        return df

    # validation of fields
    # TODO To be fixed depending on necessary validations
    def validate(fields):
        is_valid = True
        invalid_fields = []
        if len(values['gender']) == 0:
            invalid_fields.append('Gender')
            is_valid = False
        if int(values['age']) < 18 or int(values['age']) > 120:
            invalid_fields.append('Age')
            is_valid = False
        if values['years_education'] == 0:
            invalid_fields.append('Years of education')
            is_valid = False
            '''
        if len(values['first_native_language']) == 0:
            invalid_fields.append('First native language')
            is_valid = False
        if len(values['dominant_language']) == 0:
            invalid_fields.append('Dominant language')
            is_valid = False
        if len(values['academic_reading_time']) == 0:
            invalid_fields.append('Academic reading time')
            is_valid = False
        if len(values['magazine_reading_time']) == 0:
            invalid_fields.append('Magazine reading time')
            is_valid = False
        if len(values['newspaper_reading_time']) == 0:
            invalid_fields.append('Newspaper reading time')
            is_valid = False
        if len(values['email_reading_time']) == 0:
            invalid_fields.append('Email reading time')
            is_valid = False
        if len(values['fiction_reading_time']) == 0:
            invalid_fields.append('Fiction reading time')
            is_valid = False
        if len(values['nonfiction_reading_time']) == 0:
            invalid_fields.append('Nonfiction reading time')
            is_valid = False
        if len(values['other_reading_time']) == 0:
            invalid_fields.append('Other reading time')
            is_valid = False
        if len(values['socio_economic_status']) == 0:
            invalid_fields.append('Socio-economic status')
            is_valid = False
        if len(values['eyewear']) == 0:
            invalid_fields.append('Eyewear')
            is_valid = False
        if len(values['tiredness']) == 0:
            invalid_fields.append('Tiredness')
            is_valid = False
            '''
        result = [is_valid, invalid_fields]
        return result

    # The error message shown due to field validation
    def generate_error_message(values_invalid):
        pq_error_message = read_questions.pq_instructions[20][1]
        for value_invalid in values_invalid:
            pq_error_message += ('\n' + value_invalid)
        return pq_error_message

    # Elements shown when inserting dialects
    def item_dialect(item_d):
        row = [sg.pin(sg.Col([[sg.Text('' + read_questions.pq_instructions[17][1]),
                               sg.Combo(pq_languages, key=f'language_{item_d}'),
                               sg.Text('' + read_questions.pq_instructions[18][1]),
                               sg.In(size=22, key=f'dialect_language_{item_d}'),
                               sg.B(read_questions.pq_instructions[26][1], k=('delete_dialect', item_d),
                                    enable_events=True,
                                    tooltip='Delete this item')]], k=('row_dialect', item_d)))]
        return row

    # Elements shown when inserting new reading languages
    def item_read_language(item_read):
        row_language = [sg.pin(sg.Col([[sg.Text('' + read_questions.pq_instructions[13][1] + ' ' + f'{item_read}',
                                                key=f'language_number_{item_read}'),
                                        sg.Combo(read_questions.pq_language_list, size=22,
                                                 key=f'read_language_{item_read}'),
                                        sg.B(read_questions.pq_instructions[26][1],
                                             k=('delete_read_language', item_read), enable_events=True,
                                             tooltip='Delete this item')]],
                                      k=('row_read_language', item_read), visible=True))]
        return row_language

    # Repeat layout for each language
    def repeating_layout(language_name):
        c41 = [[sg.Text(' ' + read_questions.pq_questions[10][11] + '\n', size=(None, None), pad=(20, 0),
                        font=("Times New Roman", 14, "italic"))]]

        row4 = [sg.pin(sg.Col([
            [sg.Text(
                '11. ' + read_questions.pq_questions[10][1] + ' ' + language_name + ' ' +
                read_questions.pq_questions[10][
                    2],
                size=(None, None), key='language_question',
                enable_events=True)],
            [sg.Column(c41, element_justification='l')],
            [sg.Text(read_questions.pq_questions[11][1], size=(18, 1), justification='right'),
             sg.Combo(
                 [read_questions.pq_questions[11][2], read_questions.pq_questions[11][3],
                  read_questions.pq_questions[11][4],
                  read_questions.pq_questions[11][5], read_questions.pq_questions[11][6]],
                 key=f'academic_reading_time_{no_repeating_layout}'),
             sg.Text(read_questions.pq_questions[12][1], size=(18, 1), justification='right'),
             sg.Combo(
                 [read_questions.pq_questions[12][2], read_questions.pq_questions[12][3],
                  read_questions.pq_questions[12][4],
                  read_questions.pq_questions[12][5], read_questions.pq_questions[12][6]],
                 key=f'magazine_reading_time_{no_repeating_layout}')],
            [sg.Text(read_questions.pq_questions[13][1], size=(18, 1), justification='right'),
             sg.Combo(
                 [read_questions.pq_questions[13][2], read_questions.pq_questions[13][3],
                  read_questions.pq_questions[13][4],
                  read_questions.pq_questions[13][5], read_questions.pq_questions[13][6]],
                 key=f'newspaper_reading_time_{no_repeating_layout}'),
             sg.Text(read_questions.pq_questions[14][1], size=(18, 1), justification='right'),
             sg.Combo(
                 [read_questions.pq_questions[14][2], read_questions.pq_questions[14][3],
                  read_questions.pq_questions[14][4],
                  read_questions.pq_questions[14][5], read_questions.pq_questions[14][6]],
                 key=f'email_reading_time_{no_repeating_layout}')],
            [sg.Text(read_questions.pq_questions[15][1], size=(18, 1), justification='right'),
             sg.Combo(
                 [read_questions.pq_questions[15][2], read_questions.pq_questions[15][3],
                  read_questions.pq_questions[15][4],
                  read_questions.pq_questions[15][5], read_questions.pq_questions[15][6]],
                 key=f'fiction_reading_time_{no_repeating_layout}'),
             sg.Text(read_questions.pq_questions[16][1], size=(18, 2), justification='right'),
             sg.Combo(
                 [read_questions.pq_questions[16][2], read_questions.pq_questions[16][3],
                  read_questions.pq_questions[16][4],
                  read_questions.pq_questions[16][5], read_questions.pq_questions[16][6]],
                 key=f'nonfiction_reading_time_{no_repeating_layout}')],
            [sg.Text(read_questions.pq_questions[17][1], size=(18, None), justification='right'),
             sg.Combo(
                 [read_questions.pq_questions[17][2], read_questions.pq_questions[17][3],
                  read_questions.pq_questions[17][4],
                  read_questions.pq_questions[17][5], read_questions.pq_questions[17][6]],
                 key=f'internet_reading_time_{no_repeating_layout}'),
             sg.Text(read_questions.pq_questions[18][1], size=(18, 1), justification='right'),
             sg.Combo(
                 [read_questions.pq_questions[18][2], read_questions.pq_questions[18][3],
                  read_questions.pq_questions[18][4],
                  read_questions.pq_questions[18][5], read_questions.pq_questions[18][6]],
                 key=f'other_reading_time_{no_repeating_layout}')]
        ], key=f'row_time_{language_name}'))]
        return row4

    layout = 1  # The currently visible layout
    pq_no_reading_languages = 0  # to change frames
    pq_languages = []  # the languages selected so far
    copy_pq_languages = pq_languages  # copy of languages selected so far (to be used when removing from combobox)
    no_repeating_layout = 0  # to iterate between selected languages (to repeat layout)
    no_dialects = 0  # to iterate between selected languages (to determine dialects)
    i = 0  # for autocomplete text

    # Event to show autocomplete depending on key pressed
    combo = window['second_native_language']
    combo.bind('<Key>', ' Key')
    combo.bind('<Enter>', ' Enter')
    user_event = False

    while True:
        load_data()
        event, values = window.read()
        print(event, values)

        # Events happening depending on the number of childhood languages (1,2 or 3 native languages)
        if event == 'childhood_languages':
            if values['childhood_languages'] == read_questions.pq_questions[4][2]:
                window['question_7'].update(visible=False)
                window['question_7_2'].update(visible=False)
                window['question_7_3'].update(visible=False)
            elif values['childhood_languages'] == read_questions.pq_questions[4][3]:
                window['question_7'].update(visible=True)
                window['question_7_2'].update(visible=True)
                window['question_7_3'].update(visible=False)
            elif values['childhood_languages'] == read_questions.pq_questions[4][4]:
                window['question_7'].update(visible=True)
                window['question_7_2'].update(visible=True)
                window['question_7_3'].update(visible=True)

        # Save languages selected until now in pq_languages
        if event == 'use_language':
            if values['use_language'] not in pq_languages:
                pq_languages.append(values['use_language'])
        if event == 'dominant_language':
            if values['dominant_language'] not in pq_languages:
                pq_languages.append(values['dominant_language'])
        if event == 'first_native_language':
            if values['first_native_language'] not in pq_languages:
                pq_languages.append(values['first_native_language'])
        if event == 'second_native_language':
            if values['second_native_language'] not in pq_languages:
                pq_languages.append(values['second_native_language'])
        if event == 'third_native_language':
            if values['third_native_language'] not in pq_languages:
                pq_languages.append(values['third_native_language'])

        # Events happening when adding or removing dialects
        if event == 'dialect':
            if values['dialect'] == read_questions.pq_questions[9][2]:
                window['adding_dialect'].update(visible=True)
                window['column_dialect'].update(visible=True)
            elif values['dialect'] == read_questions.pq_questions[9][3]:
                window['adding_dialect'].update(visible=False)
                window['column_dialect'].update(visible=False)
            if len(pq_languages) == 0:
                sg.popup_ok(read_questions.pq_instructions[22][1], title=read_questions.pq_instructions[24][1])

        # TODO: the removal from combo box of the selected items
        if event == 'add_dialect':
            if no_dialects < len(pq_languages):
                no_dialects += 1
                window.extend_layout(window['frame_dialect'], [item_dialect(no_dialects)])
            else:
                sg.popup_ok(read_questions.pq_instructions[23][1], title=read_questions.pq_instructions[24][1])
        if event[0] == 'delete_dialect':
            window[('row_dialect', event[1])].update(visible=False)
            no_dialects -= 1

        # Does not work (supposed to remove from combo the selected languages)
        # if event == f'language_{no_dialects}':
        #    copy_pq_languages.remove(values[f'language_{no_dialects}'])
        #    window[f'language_{no_dialects}'].update()

        # Events happening when inserting/deleting new reading languages
        if event == 'read_language':
            if values['read_language'] == read_questions.pq_questions[19][2]:
                window['adding_language'].update(visible=True)
                window['column_reading_language'].update(visible=True)
            else:
                window['adding_language'].update(visible=False)
                window['column_reading_language'].update(visible=False)
        if event == 'add_language':
            if pq_no_reading_languages < 4:
                pq_no_reading_languages += 1
                window.extend_layout(window['frame_reading_language'],
                                     [item_read_language(pq_no_reading_languages)])
        if event[0] == 'delete_read_language':
            window[('row_read_language', event[1])].update(visible=False)

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        if event == 'next':
            print(pq_languages)
            window[f'-COL{layout}-'].update(visible=False)
            layout = layout + 1 if layout < 11 else 11

            if layout == 4 and no_repeating_layout < len(pq_languages):
                window[f'-COL{layout}-'].update(visible=True)
                window.extend_layout(window['layout_4'], [repeating_layout(pq_languages[no_repeating_layout])])
                no_repeating_layout += 1
            elif layout == 4 and no_repeating_layout == 0:
                window[f'-COL{layout}-'].update(visible=False)
                layout = layout + 1

            if layout == 5 and no_repeating_layout < len(pq_languages):
                window[f'-COL{layout}-'].update(visible=True)
                window.extend_layout(window['layout_5'], [repeating_layout(pq_languages[no_repeating_layout])])
                no_repeating_layout += 1
            elif layout == 5 and (no_repeating_layout == 0 or no_repeating_layout == 1):
                window[f'-COL{layout}-'].update(visible=False)
                layout = layout + 1

            if layout == 6 and no_repeating_layout < len(pq_languages):
                window[f'-COL{layout}-'].update(visible=True)
                window.extend_layout(window['layout_6'], [repeating_layout(pq_languages[no_repeating_layout])])
                no_repeating_layout += 1
            elif layout == 6 and (no_repeating_layout == 0 or no_repeating_layout == 1 or no_repeating_layout == 2):
                window[f'-COL{layout}-'].update(visible=False)
                layout = layout + 1

            if layout == 7 and no_repeating_layout < len(pq_languages):
                window[f'-COL{layout}-'].update(visible=True)
                window.extend_layout(window['layout_7'], [repeating_layout(pq_languages[no_repeating_layout])])
                no_repeating_layout += 1
            elif layout == 7 and (
                    no_repeating_layout == 0 or no_repeating_layout == 1 or no_repeating_layout == 2 or no_repeating_layout == 3):
                window[f'-COL{layout}-'].update(visible=False)
                layout = layout + 1

            if layout == 8 and no_repeating_layout < len(pq_languages):
                window[f'-COL{layout}-'].update(visible=True)
                window.extend_layout(window['layout_8'], [repeating_layout(pq_languages[no_repeating_layout])])
                no_repeating_layout += 1
            elif layout == 8 and (
                    no_repeating_layout == 0 or no_repeating_layout == 1 or no_repeating_layout == 2 or no_repeating_layout == 3 or no_repeating_layout == 4):
                window[f'-COL{layout}-'].update(visible=False)
                layout = layout + 1

            window[f'-COL{layout}-'].update(visible=True)

            if layout == 1:
                window['prev'].update(visible=False)
            else:
                window['prev'].update(visible=True)
            if layout == 11:
                window['next'].update(visible=False)
                window['submit'].update(visible=True)
            else:
                window['next'].update(visible=True)
                window['submit'].update(visible=False)

        elif event == 'prev':
            window[f'-COL{layout}-'].update(visible=False)
            layout = layout - 1 if layout > 1 else 1

            if layout == 8 and no_repeating_layout == 5:
                window[f'-COL{layout}-'].update(visible=True)
            elif layout == 8 and no_repeating_layout < 5:
                window[f'-COL{layout}-'].update(visible=False)
                layout -= 1

            if layout == 7 and no_repeating_layout >= 4:
                window[f'-COL{layout}-'].update(visible=True)
            elif layout == 7 and no_repeating_layout < 4:
                window[f'-COL{layout}-'].update(visible=False)
                layout -= 1

            if layout == 6 and no_repeating_layout >= 3:
                window[f'-COL{layout}-'].update(visible=True)
                layout -= 1
            elif layout == 6 and no_repeating_layout < 3:
                window[f'-COL{layout}-'].update(visible=False)
                layout -= 1

            if layout == 5 and no_repeating_layout >= 2:
                window[f'-COL{layout}-'].update(visible=True)
            elif layout == 5 and no_repeating_layout < 2:
                window[f'-COL{layout}-'].update(visible=False)
                layout -= 1

            if layout == 4 and no_repeating_layout >= 1:
                window[f'-COL{layout}-'].update(visible=True)
            elif layout == 4 and no_repeating_layout < 1:
                window[f'-COL{layout}-'].update(visible=False)
                layout -= 1

            if layout != 4 or layout != 5 or layout != 6 or layout != 7 or layout != 8:
                window[f'-COL{layout}-'].update(visible=True)

            if layout == 1:
                window['prev'].update(visible=False)
            else:
                window['prev'].update(visible=True)
            if layout == 11:
                window['next'].update(visible=False)
                window['submit'].update(visible=True)
            else:
                window['next'].update(visible=True)
                window['submit'].update(visible=False)

        # Events on button submit
        if event == 'submit':
            validation_result = validate(values)
            if validation_result[0]:
                new_record = pd.DataFrame(values, index=[0])
                df = pd.concat([load_data(), new_record], ignore_index=True)
                df.to_csv(constants.PQ_FILE,
                          index=False)  # This will create the file if it doesn't exist ->should be changed
                sg.popup(read_questions.pq_instructions[21][1], title=read_questions.pq_instructions[25][1])
                window.close()
            else:
                error_message = generate_error_message(validation_result[1])
                sg.popup(error_message, title=read_questions.pq_instructions[24][1])

        if event == 'second_native_language Enter':
            combo.Widget.select_range(0, 'end')
        if event == 'second_native_language Key':
            entry = values['second_native_language'].lower()
            if user_event:
                user_event = False
            else:
                if entry:
                    index = None
                    for i, item in enumerate(read_questions.pq_language_list):
                        if item.lower().startswith(entry):
                            index = i
                            break

                    if index is not None:
                        user_event = True
                        combo.Widget.set(read_questions.pq_language_list[index])
                        combo.Widget.event_generate('<Key-Down>')
                        combo.Widget.current(index)
    window.close()

    if __name__ == '__main__':
        pq_main_layout()
