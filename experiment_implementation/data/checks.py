import csv


# the name of the output file, where the result will be written
result_file = 'check_file.txt'


"""This part is used to check if the images of stimuli and questions are complete"""

list_of_correct_stimuli_images = ['stimulus_id','stimulus_text_title','page_1','page_2','page_3','page_4','page_5','page_6','page_7','page_8',
                    'page_9','page_10','page_11','page_12','page_13','page_14','page_15','page_16','page_17',
                    'page_18','page_19','page_20','type_q1','type_q2','type_q3','type_q4',
                    'type_q5','question_1','question_2','question_3','question_4','question_5',
                    'answer_option_q1_1','answer_option_q1_2','answer_option_q1_3',
                    'answer_option_q2_1','answer_option_q2_2','answer_option_q2_3','answer_option_q3_1',
                    'answer_option_q3_2','answer_option_q3_3','answer_option_q4_1','answer_option_q4_2',
                    'answer_option_q4_3','answer_option_q5_1','answer_option_q5_2','answer_option_q5_3',
                    'answer_option_q1_1_key','answer_option_q1_2_key','answer_option_q1_3_key',
                    'answer_option_q2_1_key','answer_option_q2_2_key','answer_option_q2_3_key',
                    'answer_option_q3_1_key','answer_option_q3_2_key','answer_option_q3_3_key',
                    'answer_option_q4_1_key','answer_option_q4_2_key','answer_option_q4_3_key',
                    'answer_option_q5_1_key','answer_option_q5_2_key','answer_option_q5_3_key','correct_answer_col_name_q1',
                    'correct_answer_col_name_q2','correct_answer_col_name_q3',"correct_answer_col_name_q4",
                    "correct_answer_col_name_q5","correct_answer_q1","correct_answer_q2","correct_answer_q3",
                    "correct_answer_q4","correct_answer_q5","correct_answer_key_q1","correct_answer_key_q2",
                    "correct_answer_key_q3","correct_answer_key_q4","correct_answer_key_q5",
                    "page_1_img_path","page_1_img_file","page_2_img_path","page_2_img_file","page_3_img_path","page_3_img_file",
                    "page_4_img_path","page_4_img_file",'page_5_img_path',"page_5_img_file","page_6_img_path","page_6_img_file",
                    "page_7_img_path","page_7_img_file","page_8_img_path","page_8_img_file","page_9_img_path","page_9_img_file",
                    "page_10_img_path","page_10_img_file","page_11_img_path","page_11_img_file","page_12_img_path",
                    "page_12_img_file","page_13_img_path","page_13_img_file","page_14_img_path","page_14_img_file",
                    "page_15_img_path","page_15_img_file","page_16_img_path",'page_16_img_file',"page_17_img_path",
                    "page_17_img_file","page_18_img_path","page_18_img_file","page_19_img_path","page_19_img_file",
                    "page_20_img_path","page_20_img_file","question_1_img_path","question_1_img_file",
                    "question_2_img_path","question_2_img_file","question_3_img_path","question_3_img_file",
                    "question_4_img_path","question_4_img_file","question_5_img_path","question_5_img_file"]


stimuli_file = 'multipleye-stimuli-experiment-en_with_img_paths.csv'

def stimuli_check(stimuli_file, list_of_correct_stimuli_images):
    with open(stimuli_file, 'r') as f:
        data = csv.reader(f)
        list_of_stimuli_images = next(data)

    incomplete_stimuli = []

    for item in list_of_correct_stimuli_images:
        if item not in list_of_stimuli_images:
            incomplete_stimuli.append(item)

    if incomplete_stimuli:
        with open(result_file, 'a') as output_f:
            output_f.write(
                "Images of texts and questions are not complete. Please add the following items to the stimuli folder:\n")
            for item in incomplete_stimuli:
                output_f.write(f"- {item}\n")
    else:
        with open(result_file, 'a') as output_f:
            output_f.write("The images and texts are complete\n")


"""This part is used to check if the images of other screens are complete"""

list_of_correct_screens = ["other_screen_id","other_screen_title","other_screen_text","comment",
                           "other_screen_img_name","other_screen_img_path"]
screens_file = 'multipleye-other-screens-en_with_img_paths.csv'

def other_screens_checks (list_of_correct_screens,screens_file):
    with open(screens_file, 'r') as f:
        data = csv.reader(f)
        screen_images_list = next(data)

    incomplete_screens = []

    for item in list_of_correct_screens:
        if item not in screen_images_list:
            incomplete_screens.append(item)

    if incomplete_screens:
        with open(result_file, 'a') as output_f:
            output_f.write("Images of other screens are not complete. Please add the following items to the other screens folder:\n")
            for item in incomplete_screens:
                output_f.write(f"- {item}\n")
    else:
        with open(result_file, 'a') as output_f:
            output_f.write("The other screens are complete\n")


"""This part is used to check if the images of other screens are complete"""

list_of_stimuli_for_practice = ["stimulus_id_practice","stimulus_text_title_practice","page_1_practice",
                                "page_2_practice","page_3_practice", "type_q1_practice","type_q2_practice","type_q3_practice",
                                "question_1_practice","question_2_practice", "question_3_practice","answer_option_q1_1_practice",
                                "answer_option_q1_2_practice", "answer_option_q1_3_practice","answer_option_q2_1_practice",
                                "answer_option_q2_2_practice", "answer_option_q2_3_practice","answer_option_q3_1_practice",
                                "answer_option_q3_2_practice", "answer_option_q3_3_practice","answer_option_q1_1_key_practice",
                                "answer_option_q1_2_key_practice", "answer_option_q1_3_key_practice",
                                "answer_option_q2_1_key_practice","answer_option_q2_2_key_practice",
                                "answer_option_q2_3_key_practice","answer_option_q3_1_key_practice",
                                "answer_option_q3_2_key_practice","answer_option_q3_3_key_practice","correct_answer_col_name_q1_practice",
                                "correct_answer_col_name_q2_practice", "correct_answer_col_name_q3_practice",
                                "correct_answer_col_name_q4_practice","correct_answer_col_name_q5_practice",
                                "correct_answer_q1_practice","correct_answer_q2_practice","correct_answer_q3_practice",
                                "correct_answer_key_q1_practice",
                                "correct_answer_key_q2_practice","correct_answer_key_q3_practice","page_1_practice_img_path",
                                "page_1_practice_img_file","page_2_practice_img_path","page_2_practice_img_file",
                                "page_3_practice_img_path","page_3_practice_img_file","question_1_practice_img_path",
                                "question_1_practice_img_file","question_2_practice_img_path",
                                "question_2_practice_img_file","question_3_practice_img_path","question_3_practice_img_file" ]

practice_file = 'multipleye-stimuli-practice-en_with_img_paths.csv'

def practice_file_check(list_of_stimuli_for_practice, practice_file):
    with open(practice_file, 'r') as f:
        data = csv.reader(f)
        practice_images_list = next(data)

    incomplete_practice_list = []

    for item in list_of_stimuli_for_practice:
        if item not in practice_images_list:
            incomplete_practice_list.append(item)

    if incomplete_practice_list:
        with open(result_file, 'a') as output_f:
            output_f.write(
                "Images for the practical session are not complete. Please add the following items to the stimuli for practice folder:\n")
            for item in incomplete_practice_list:
                output_f.write(f"- {item}\n")
    else:
        with open(result_file, 'a') as output_f:
            output_f.write("The images for the practical session are complete\n")


def main():
    other_screens_checks(list_of_correct_screens, screens_file)
    stimuli_check(stimuli_file, list_of_correct_stimuli_images)
    practice_file_check(list_of_stimuli_for_practice, practice_file)

if __name__ == "__main__":
    main()








