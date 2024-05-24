import pandas as pd
import constants

pq_questions = [row.tolist() for index, row in pd.read_csv(constants.PQ_QUESTIONS_CSV).iterrows()]

pq_language_list = sorted(pd.read_csv(constants.PQ_LANGUAGES_CSV).language_name.values.tolist())