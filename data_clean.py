# data_clean.py - Tu Nguyen 2022
#
# ----------------------------------
#
# Cleans the heart rate data and stores the results in cleaned_'read'.csv
#
# Cleaning parameters:
#   re-label columns to specific names
#   convert to heartrate data to float type, if it is a range of values, take the mean
#       this is possible because ranges are recorded with small intervals, and there
#       isn't much variation in HR for these intervals, so it is reasonably accurate
#   convert duration data to float type, sum if it is a range of values
#   convert varying datetime formats into uniform pacific time
#   remove stray, obviously invalid data
#
# Transforms & populating data:
#   groups & aggregates data points into singular intervals
#   adds null columns for time intervals with no data
#
# Resulting columns:
#   datetime (YYYY-MM-DD HH:M0:00) - string
#   heartrate (bpm) - float
#   duration (s) - float
#

# Imports
import pandas as pd
import numpy as np

# The read csv file
read = 'raw_hr_hr.csv'
# The write csv file
write = 'cleaned_' + read
# The csv file with as a data frame
dataframe = pd.read_csv(read)
# Suppress numpy float sci form
np.set_printoptions(suppress=True)

# The date of the most recent data 
# Date format - 'YYYY-MM-DD HH:MM:SS'
recent_data_date = '2022-05-01 00:00:00'

def main():
    # resulting cleaned data frame
    dest_map = {}
    
    # convert the datetime data to pacific time
    dest_map.update(conv_to_pacific(dataframe, 'start', 'datetime'))
    # convert the heart rate data to single integers
    dest_map.update(conv_hr_to_int(dataframe, 'value', 'heartrate'))
    # convert the duration data to integers
    dest_map.update(conv_dur_to_int(dataframe, 'duration', 'duration'))

    # drop all rows with invalid data
    dest_df = rows_drop_invalid(pd.DataFrame.from_dict(dest_map), [int, str])

    # keep data from selected months
    dest_df = rows_keep_months(dest_df, ['2022-04-', '2022-03-', '2021-10-', '2021-11-'])

    # sort data by datetimes
    dest_df = dest_df.sort_values(by=['datetime'], axis=0)

    # generate equal interval time keys
    tk_map = {}
    tk_map.update(generate_tk_map_range(pd.to_datetime('2021-10-01 00:00:00'), pd.to_datetime('2021-12-01 00:00:00'), 10, 'm'))
    tk_map.update(generate_tk_map_range(pd.to_datetime('2022-03-01 00:00:00'), pd.to_datetime(recent_data_date), 10, 'm'))

    # group recorded data into time intervals and aggregate
    dest_df = rows_standardize_intervals(dest_df, tk_map)

    # output results to write csv
    dest_df.to_csv(write, index=False)

# Takes a data frame and a time key map and 
# returns a data frame grouped on equal intervals
#
# df - the data frame being accessed
# tk_map - the time key map being accessed
def rows_standardize_intervals(df, tk_map):
    ret_rows = []
    times = df['datetime'].to_numpy()
    cols = df.to_numpy()
    for i, dt in enumerate(times):
        conv_time = dt[0:14] + str(int(dt[14:16]) // 10 * 10) + ':00'
        if (len(conv_time) < len(dt)):
            conv_time = conv_time[:len(conv_time) - 3] + '0' + conv_time[len(conv_time) - 3:]
        tk_map[conv_time] += [cols[i]]
    for i, tk in enumerate(tk_map):
        rows = tk_map[tk]
        if (len(rows) == 0):
            ret_rows.append({'datetime': tk, 'heartrate': None, 'duration': None})
        else:
            heartrates = [rows[j][1] for j in range(len(rows))]
            durations = [rows[j][2] for j in range(len(rows))]
            heartrate = np.average(heartrates, weights=durations)
            duration = sum(durations)
            ret_rows.append({'datetime': tk, 'heartrate': int(heartrate), 'duration': int(duration)})
    return pd.DataFrame.from_dict(ret_rows)

# Populates a map with time keys from start to end
# on an interval, returns the map
#
# start - the date to start at
# end - the date to end at
# interval - the value of the interval
# unit - the unit of the interval
def generate_tk_map_range(start, end, interval, unit):
    tk_map = {str(start): []}
    time = start
    inc = pd.Timedelta(interval, unit)
    nt = time + inc
    while (str(end) not in str(nt)):
        tk_map[str(nt)] = []
        nt += inc
    return tk_map

# Drops all rows that are not in the specified month
# returns the resulting data frame
#
# df - the data frame modified
# months - the months where data will be kept
def rows_keep_months(df, months):
    rows = df.to_numpy()
    ev = ""
    for month in months:
        ev += "\'" + month + "\'"+ " not in row and "
    for i in range(len(rows)):
        row = rows[i][0]
        if (eval(ev[:len(ev)-5])):
            df = df.drop(i)
    return df

# Drops all rows that do not have the specified types
# returns the resulting data frame
#
# df - the data frame modified
# types - the types to be checked in each row
def rows_drop_invalid(df, types):
    rows = df.to_numpy()
    for i in range(len(rows)):
        for item in rows[i]:
            if (type(item) not in types):
                df = df.drop(i)
                break
    return df

# Converts duration data to integers, sums if there are
# multiple integers, returns the resulting column
#
# df - the data frame being accessed
# colname - the column name being accessed
# newcolname - the returned column name
def conv_dur_to_int(df, colname, newcolname):
    c = df[colname].to_numpy()
    col = [np.fromstring(c[i].replace('[', '').replace(']', '').replace(',', ' '), dtype=int, sep= ' ') for i in range(len(c))]
    return {newcolname: {i:np.sum(col[i], dtype=int) for i in range(len(col))}}

# Converts heart rate data to integers, averages if there are
# multiple integers, returns the resulting column
#
# df - the data frame being accessed
# colname - the column name being accessed
# newcolname - the returned column name
def conv_hr_to_int(df, colname, newcolname):
    c = df[colname].to_numpy()
    col = [np.fromstring(c[i].replace('[', '').replace(']', '').replace(',', ' '), dtype=int, sep= ' ') for i in range(len(c))]
    return {newcolname: {i:np.mean(col[i], dtype=int) for i in range(len(col))}}

# Converts timedate data to pacific time, trims 
# timezone identifier, returns the resulting column
#
# df - the data frame being accessed
# colname - the column name being accessed
# newcolname - the returned column name
def conv_to_pacific(df, colname, newcolname):
    col = df[colname].to_numpy()
    dati = pd.to_datetime(col, utc=True).astype('datetime64[ns, US/Pacific]').astype('str')
    return {newcolname: {i:dati[i][:len(dati[i])-6] for i in range(len(dati))}}

# Splits a column on spliton and returns the resulting
# columns with new column names
#
# df - the data frame being accessed
# colname - the column name being accessed
# newcolnames - the returned column names
# spliton - the character to split on 
def cols_split(df, colname, newcolnames, spliton):
    col = df[colname]
    cols = []
    for i in range(len(col)):
        cols += [col[i].split(spliton)]
    cols = np.array(cols).transpose()
    return {newcolnames[i]: {j:cols[i][j] for j in range(len(cols[i]))} for i in range(len(newcolnames))}

# Prints n rows of data in the format:
# col1: data, col2: data, ...
#
# df - the data frame being accessed
# n - the number of rows to print
def print_n_rows_info(df, n):
    rows = df.to_numpy()
    cols = df.columns.to_numpy()
    if (n > len(rows)):
        n = len(rows)
    row = ""
    for i in range(n):
        r = rows[i]
        for j in range(len(r)):
            row += str(cols[j]) + ":  " + str(r[j]) + ", "
        print(row[:len(row)-2])
        row = ""

# Prints all the column names in the data frame
#
# df - the data frame being accessed
def print_col_names(df):
    colnames = df.columns.to_numpy()
    for i in range(len(colnames)):
        print(colnames[i])

if __name__ == "__main__":
    main()

#######################################################################################################################
#                                                     Data Format                                                     #
#######################################################################################################################

# ***** Provided by Withings *****
# Below are the details of the data you've exported from Health Mate:

# activities.csv: Activities history

# aggregates_calories_earned.csv: Active calories burned regrouped by days

# aggregates_calories_passive.csv: Passive calories burned regrouped by days

# aggregates_distance.csv: Travelled distance regrouped by days

# aggregates_elevation.csv: Floor climbed regrouped by days
# · Value : (steps number)

# aggregates_steps.csv: Steps data regrouped by days
# · Value : (steps number)

# bp.csv: Blood Pressure Data
# · Heart Rate : (bpm)
# · Systolic : (mmHg)
# · Diastolic : (mmHg)

# height.csv: Height Measurements
# · Height : (meters)

# raw_hr_hr.csv: Heart rate data
# · Heart Rate : (bpm)

# raw_tracker_calories-earned.csv: Calories earned data
# · Duration : (seconds)
# · Value : (number of calories)

# raw_tracker_distance.csv: Distance data
# · Duration : (seconds)
# · Value : (meters)

# raw_tracker_elevation.csv: Elevation data
# · Duration : (seconds)
# · Value : (meters)

# raw_tracker_lap-pool.csv: Lap pool data
# · Duration : (seconds)
# · Value : (number of laps)

# raw_tracker_sleep-state.csv: Sleep trackers data
# · Duration : (seconds)
# · Value : (0 -> awake; 1 -> light sleep; 2 -> deep sleep)

# raw_tracker_steps.csv: Steps data
# · Duration : (seconds)
# · Value : (steps number)

# signal.csv: Your ECG signals
# · Frequency: Sampling frequency in Hz
# · Duration: Duration in seconds
# · Wear Position: Position of the device when tracking measurement :
#  - 0 -> right wrist;  1 -> left wrist
#  - 2 -> right arm;  3 -> left arm
# · Signal: Full data set of the ECG recordings
#  - Value in microvolts (μV) for ECG recorded with a watch.
#  - Value in millivolts (mV) for ECG recorded with a blood pressure monitor.

# sleep.csv: Sleep data

# weight.csv: Weights Measurements
# · Weight : Weight (kg)
# · Fat mass : Fat mass (kg)
# · Bone mass : Bone mass (kg)
# · Muscle mass : Muscle mass (kg)
# · Hydration : Hydration (kg)