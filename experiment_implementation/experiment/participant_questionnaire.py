import pandas as pd
from psychopy import gui
import constants

class MultiplEYEParticipantQuestionnaire:

    def __init__(self, participant_id: int):
        self.instructions, self.questions = self.load_data()
        self.gui = gui.Dlg(
            title='Participant Questionnaire',
        )

        self.gui.addText(self.instructions['pq_initial_message'])
        self.gui.addText(f'Participant ID {participant_id}')

        options = []
        for i in range(1, 9):
            option = self.questions["1"][f'pq_answer_option_{i}']
            if option:
                options.append(option)
        self.gui.addField(f'{self.questions["1"]["pq_question_text"]}', choices=options)


        ok_data = self.gui.show()

        if self.gui.OK:
            self.gui.validate()
            print(ok_data)
        else:
            print('cancelled')

    def load_data(self):
        # read the instructions to a dictionary
        pq_instructions_dict = pd.read_csv(constants.PQ_PARTICIPANT_INSTRUCTIONS_CSV, index_col='pq_instructions').to_dict(
            orient='dict')
        pq_instructions_dict = pq_instructions_dict['pq_text']

        pq_questions = pd.read_csv(constants.PQ_QUESTIONS_CSV, index_col='pq_question_no').fillna('')
        pq_questions = pq_questions.to_dict(orient='index')

        return pq_instructions_dict, pq_questions

    def run_questionnaire(self):
        pass
