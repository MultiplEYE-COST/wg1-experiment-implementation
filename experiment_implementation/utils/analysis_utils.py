import pandas as pd


def compute_reading_times():

    data = pd.read_csv('/Users/debor/repos/wg1-experiment-implementation/experiment_implementation/multipleye_ET_data_en_Andreas/eye_tracking_data_en_gb_1/core_dataset/666/logfiles/EXPERIMENT_LOGFILE_1_666_2024-03-25_1711373019.txt', sep='\t')

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


def convert_to_time_str(duration_ms: float) -> str:
    seconds = int(duration_ms / 1000) % 60
    minutes = int(duration_ms / (1000 * 60)) % 60
    hours = int(duration_ms / (1000 * 60 * 60)) % 24

    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'


if __name__ == '__main__':
    compute_reading_times()
