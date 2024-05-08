import os
import re
from pathlib import Path

import pandas as pd


def compute_reading_times():
    data = pd.read_csv(
        '/Users/debor/repos/wg1-experiment-implementation/experiment_implementation/multipleye_ET_data_en_Andreas/eye_tracking_data_en_gb_1/core_dataset/666/logfiles/EXPERIMENT_LOGFILE_1_666_2024-03-25_1711373019.txt',
        sep='\t')

    page_name = []
    page_duration = []
    page_duration_ms = []

    overall_duration_ms = 0
    num_breaks = 0

    last_end_ts = 974838.5699999053

    for i, row in data.iterrows():

        message = row['message']

        if message.startswith('optional break duration'):

            onset_ts = row['screen_onset_timestamp']
            time_inbetween = onset_ts - last_end_ts
            page_name.append(f'time inbetween')
            page_duration_ms.append(float(time_inbetween))
            page_duration.append(convert_to_time_str(time_inbetween))
            last_end_ts = row['keypress_timestamp']
            overall_duration_ms += time_inbetween

            num_breaks += 1
            duration_ms = float(message.split(' ')[-1])
            page_duration_ms.append(duration_ms)
            page_name.append(f'Break_{num_breaks}')
            duration = convert_to_time_str(duration_ms)
            overall_duration_ms += duration_ms
            page_duration.append(duration)

        elif message.startswith('stop showing'):
            try:
                onset_ts = row['screen_onset_timestamp']
                time_inbetween = onset_ts - last_end_ts
                page_duration.append(convert_to_time_str(time_inbetween))
                page_name.append(f'time inbetween')
                page_duration_ms.append(time_inbetween)
                overall_duration_ms += time_inbetween
                last_end_ts = onset_ts
            except ValueError:
                print('cannot convert for message:', message)
                page_name.append(f'time inbetween')
                page_duration.append(pd.NA)
                page_duration_ms.append(pd.NA)

            text = message.split(' ')[-1]
            page_name.append(text)

            try:
                duration_ms = int(row['keypress_timestamp'] - row['screen_onset_timestamp'])
            except ValueError:
                print('cannot convert for message:', message)
                page_duration.append(pd.NA)
                page_duration_ms.append(pd.NA)
                continue

            duration = convert_to_time_str(duration_ms)
            overall_duration_ms += duration_ms
            page_duration.append(duration)
            page_duration_ms.append(duration_ms)

    reading_time_df = pd.DataFrame({
        'text': page_name,
        'duration-hh:mm:ss': page_duration,
        'duration-ms': page_duration_ms

    })

    sum_df = reading_time_df[['text', 'duration-ms']].dropna()
    sum_df['duration-ms'] = sum_df['duration-ms'].astype(float)
    sum_df = sum_df.groupby(by=['text']).sum().reset_index()
    sum_df = sum_df['duration-ms'].apply(lambda x: convert_to_time_str(x)).reset_index()
    sum_df.to_csv('reading_times_sum.tsv', index=False, sep='\t')

    reading_time_df.to_csv('reading_times.tsv', index=False, sep='\t')

    print('Overall duration:', convert_to_time_str(overall_duration_ms))


def analyse_asc(asc_file: str,
                num: int,
                initial_ts: int,
                lab: str,
                stimuli_trial_mapping: dict):
    start_ts = []
    stop_ts = []
    start_msg = []
    stop_msg = []
    duration_ms = []
    duration_str = []
    trials = []
    pages = []
    status = []
    stimulus_name = []

    parent_folder = Path(__file__).parent.parent
    asc_file = parent_folder / asc_file

    with open(asc_file, 'r', encoding='utf8') as f:

        start_regex = re.compile(
            r'MSG\s+(?P<timestamp>\d+)\s+(?P<type>start_recording)_(?P<trial>(PRACTICE_)?trial_\d\d?)_(?P<page>.*)')
        stop_regex = re.compile(
            r'MSG\s+(?P<timestamp>\d+)\s+(?P<type>stop_recording)_(?P<trial>(PRACTICE_)?trial_\d\d?)_(?P<page>.*)')

        for l in f.readlines():
            if match := start_regex.match(l):
                start_ts.append(match.groupdict()['timestamp'])
                start_msg.append(match.groupdict()['type'])
                trials.append(match.groupdict()['trial'])

                if match.groupdict()['trial'] in stimuli_trial_mapping:
                    stimulus_name.append(stimuli_trial_mapping[match.groupdict()['trial']])

                pages.append(match.groupdict()['page'])
                status.append('reading time')
            elif match := stop_regex.match(l):
                stop_ts.append(match.groupdict()['timestamp'])
                stop_msg.append(match.groupdict()['type'])

    total_reading_duration_ms = 0
    for start, stop in zip(start_ts, stop_ts):
        time_ms = int(stop) - int(start)
        time_str = convert_to_time_str(time_ms)
        duration_ms.append(time_ms)
        duration_str.append(time_str)
        total_reading_duration_ms += time_ms

    print('Total reading duration:', convert_to_time_str(total_reading_duration_ms))

    # calcualte duration between pages
    temp_stop_ts = stop_ts.copy()
    temp_stop_ts.insert(0, initial_ts)
    temp_stop_ts = temp_stop_ts[:-1]

    total_set_up_time_ms = 0
    for stop, start, page, trial in zip(temp_stop_ts, start_ts, pages, trials):
        time_ms = int(start) - int(stop)
        time_str = convert_to_time_str(time_ms)
        duration_ms.append(time_ms)
        duration_str.append(time_str)
        start_msg.append('time inbetween')
        stop_msg.append('time inbetween')
        start_ts.append(stop)
        stop_ts.append(start)
        trials.append(trial)
        total_set_up_time_ms += time_ms

        if trial in stimuli_trial_mapping:
            stimulus_name.append(stimuli_trial_mapping[trial])

        pages.append(page)
        status.append('time before pages and breaks')

    print('Total set up and break time:', convert_to_time_str(total_set_up_time_ms))

    df = pd.DataFrame({
        'start_ts': start_ts,
        'stop_ts': stop_ts,
        'trial': trials,
        'stimulus': stimulus_name,
        'page': pages,
        'type': status,
        'duration_ms': duration_ms,
        'duration-hh:mm:ss': duration_str
    })

    df.to_csv(f'reading_times/times_per_page_pilot_{num}.tsv', sep='\t', index=False)

    sum_df = df[['stimulus', 'trial', 'type', 'duration_ms']].dropna()
    sum_df['duration_ms'] = sum_df['duration_ms'].astype(float)
    sum_df = sum_df.groupby(by=['stimulus', 'trial', 'type']).sum().reset_index()
    duration = sum_df['duration_ms'].apply(lambda x: convert_to_time_str(x))
    sum_df['duration-hh:mm:ss'] = duration
    sum_df.to_csv(f'reading_times/times_per_trial_pilot_{num}.tsv', index=False, sep='\t')

    print('Total exp time: ', convert_to_time_str(total_reading_duration_ms + total_set_up_time_ms))
    print('\n')

    # write total times to csv
    total_times = pd.DataFrame({
        'pilot': num,
        'lab': lab,
        'language': 'en',
        'total_trials': [len(sum_df) / 2],
        'total_pages': [len(df) / 2],
        'total_reading_time': [convert_to_time_str(total_reading_duration_ms)],
        'total_non-reading_time': [convert_to_time_str(total_set_up_time_ms)],
        'total_exp_time': [convert_to_time_str(total_reading_duration_ms + total_set_up_time_ms)]
    })
    if os.path.exists('reading_times/total_times.tsv'):
        temp_total_times = pd.read_csv('reading_times/total_times.tsv', sep='\t')
        total_times = pd.concat([temp_total_times, total_times], ignore_index=True)

    total_times.to_csv('reading_times/total_times.tsv', sep='\t', index=False)

    total_times.to_excel('reading_times/total_times.xlsx', index=False)
    sum_df.to_excel(f'reading_times/times_per_trial_pilot_{num}.xlsx', index=False)
    df.to_excel(f'reading_times/times_per_page_pilot_{num}.xlsx', index=False)


def convert_to_time_str(duration_ms: float) -> str:
    seconds = int(duration_ms / 1000) % 60
    minutes = int(duration_ms / (1000 * 60)) % 60
    hours = int(duration_ms / (1000 * 60 * 60)) % 24

    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'


if __name__ == '__main__':
    # compute_reading_times()
    # pilot 1
    analyse_asc(
         '/Users/debor/repos/wg1-experiment-implementation/experiment_implementation/multipleye_pilot_1/'
         'eye_tracking_data_en_gb_1/core_dataset/666/gb1en666.asc',
        #"data/eye_tracking_data_en_gb_1/core_dataset/666/gb1en666.asc",
        num=1,
        lab='dili-zh',
        initial_ts=1262133,
        stimuli_trial_mapping={
            'PRACTICE_trial_0': 'Enc_WikiMoon',
            'PRACTICE_trial_1': 'Lit_HarryPotter',
            'trial_0': 'Lit_NorthWind',
            'trial_1': 'Lit_Solaris',
            'trial_2': 'Lit_EmperorClothes',
            'trial_3': 'Lit_MagicMountain',
            'trial_4': 'Arg_PISARapaNui',
            'trial_5': 'PopSci_Caveman',
            'trial_6': 'Lit_BrokenApril',
            'trial_7': 'Arg_PISACowsMilk',
        }
    )

    # # pilot 2
    analyse_asc(
         '/Users/debor/repos/wg1-experiment-implementation/experiment_implementation/multipleye_pilot_2/'
        'eye_tracking_data_en_gb_1/core_dataset/002/gb1en002.asc',
        #"data/eye_tracking_data_en_gb_1/core_dataset/002/gb1en002.asc",
        num=2,
        lab='dili-zh',
        initial_ts=1642408,
        stimuli_trial_mapping={
            'PRACTICE_trial_0': 'Enc_WikiMoon',
            'PRACTICE_trial_1': 'Lit_HarryPotter',
            'trial_0': 'Lit_MagicMountain',
            'trial_1': 'Lit_EmperorClothes',
            'trial_2': 'Lit_Solaris',
            'trial_3': 'Lit_NorthWindSun',
            'trial_4': 'Arg_PISACowsMilk',
            'trial_5': 'Lit_BrokenApril',
            'trial_6': 'PopSci_Caveman',
            'trial_7': 'Arg_PISARapaNui',
            'trial_8': 'Ins_HumanRights',
            'trial_9': 'PopSci_Multipleye',
            'trial_10': 'Lit_Alchemist',
            'trial_11': 'Ins_Mobility',
        }
    )
    #
    # analyse_asc(
    #     "C:\\Users\debor\\repos\wg1-experiment-implementation\experiment_implementation\data\\"
    #     "eye_tracking_data_en_gb_1\core_dataset\\00"
    #     "9\gb1en009.asc",
    #     num=3,
    #     lab='dili-zh',
    #     stimuli_trial_mapping={
    #         'PRACTICE_trial_0': 'Enc_WikiMoon',
    #         'PRACTICE_trial_1': 'Lit_NorthWind',
    #         'trial_0': 'Lit_MagicMountain',
    #         'trial_1': 'Lit_Solaris',
    #         'trial_2': 'Lit_BrokenApril',
    #         'trial_3': 'Arg_PISACowsMilk',
    #         'trial_4': 'Arg_PISARapaNui',
    #         'trial_5': 'PopSci_Caveman',
    #         'trial_6': 'PopSci_Multipleye',
    #         'trial_7': 'Ins_HumanRights',
    #         'trial_8': 'Ins_Mobility',
    #         'trial_9': 'Lit_Alchemist',
    #     }
    # )

    analyse_asc(
        "/Users/debor/repos/wg1-experiment-implementation/experiment_implementation/multipleye_pilot_4/il1en001.asc",
        num=4,
        lab='haifa',
        initial_ts=116157,
        stimuli_trial_mapping={
            'PRACTICE_trial_0': 'Enc_WikiMoon',
            'PRACTICE_trial_1': 'Lit_NorthWind',
            'trial_0': 'Ins_LearningMobility',
            'trial_1': 'Lit_Alchemist',
            'trial_2': 'PopSci_MultiplEYE',
            'trial_3': 'Ins_HumanRights',
            'trial_4': 'Lit_BrokenApril',
            'trial_5': 'Arg_PISACowsMilk',
            'trial_6': 'Lit_MagicMountain',
            'trial_7': 'Lit_Solaris',
            'trial_8': 'Arg_PISARapaNui',
            'trial_9': 'PopSci_Caveman',
        }
    )
