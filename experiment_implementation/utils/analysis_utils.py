import re

import pandas as pd

STIMULUS_NAMES = {
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
        'duration-HH:MM:SS': page_duration,
        'duration-ms': page_duration_ms

    })

    sum_df = reading_time_df[['text', 'duration-ms']].dropna()
    sum_df['duration-ms'] = sum_df['duration-ms'].astype(float)
    sum_df = sum_df.groupby(by=['text']).sum().reset_index()
    sum_df = sum_df['duration-ms'].apply(lambda x: convert_to_time_str(x)).reset_index()
    sum_df.to_csv('reading_times_sum.tsv', index=False, sep='\t')

    reading_time_df.to_csv('reading_times.tsv', index=False, sep='\t')

    print('Overall duration:', convert_to_time_str(overall_duration_ms))


def analyse_asc(asc_file: str):
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

                if match.groupdict()['trial'] in STIMULUS_NAMES:
                    stimulus_name.append(STIMULUS_NAMES[match.groupdict()['trial']])

                pages.append(match.groupdict()['page'])
                status.append('reading time')
            elif match := stop_regex.match(l):
                stop_ts.append(match.groupdict()['timestamp'])
                stop_msg.append(match.groupdict()['type'])

    total_duration_ms = 0
    for start, stop in zip(start_ts, stop_ts):
        time_ms = int(stop) - int(start)
        time_str = convert_to_time_str(time_ms)
        duration_ms.append(time_ms)
        duration_str.append(time_str)
        total_duration_ms += time_ms

    print('Total duration:', convert_to_time_str(total_duration_ms))

    # calcualte duration between pages
    temp_stop_ts = stop_ts.copy()
    temp_stop_ts.insert(0, 1262133)
    temp_stop_ts = temp_stop_ts[:-1]

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

        if trial in STIMULUS_NAMES:
            stimulus_name.append(STIMULUS_NAMES[trial])

        pages.append(page)
        status.append('time between pages or breaks')

    df = pd.DataFrame({
        'start_ts': start_ts,
        'stop_ts': stop_ts,
        'trial': trials,
        'stimulus': stimulus_name,
        'page': pages,
        'status': status,
        'duration_ms': duration_ms,
        'duration-HH:MM:SS': duration_str
    })

    df.to_csv('asc_analysis.tsv', sep='\t', index=False)


def convert_to_time_str(duration_ms: float) -> str:
    seconds = int(duration_ms / 1000) % 60
    minutes = int(duration_ms / (1000 * 60)) % 60
    hours = int(duration_ms / (1000 * 60 * 60)) % 24

    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'


if __name__ == '__main__':
    # compute_reading_times()
    analyse_asc(
        '/Users/debor/repos/wg1-experiment-implementation/experiment_implementation/multipleye_ET_data_en_Andreas/eye_tracking_data_en_gb_1/core_dataset/666/gb1en666.asc')
