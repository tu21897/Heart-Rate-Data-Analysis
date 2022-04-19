import pandas as pd
import numpy as np

#
# Cleans data and stores the results in cleaned_'read'.csv
#
# Cleaning parameters:
#   re-label columns to specific names
#   convert to heartrate data to int type, if it is a range of values, take the mean
#       this is possible because ranges are recorded with small intervals, and there
#       isn't much variation in HR for these intervals, so it is reasonably accurate
#   convert duration data to int type, sum if it is a range of values
#   convert varying datetime formats into uniform pacific time
#   remove stray, obviously invalid data

# The read csv file
read = 'raw_hr_hr_sm.csv'
# The write csv file
write = 'cleaned_' + read
# The csv file with as a data frame
df = pd.read_csv(read)
# Suppress numpy float sci form
np.set_printoptions(suppress=True)

def main():
    # resulting merged & cleaned data frame
    dest_map = {}
    
    dest_map.update(conv_to_pacific(df, 'start', 'datetime'))
    dest_map.update(conv_hr_to_int(df, 'value', 'heartrate'))
    dest_map.update(conv_dur_to_int(df, 'duration', 'duration'))

    dest_df = pd.DataFrame.from_dict(dest_map)
    dest_df.to_csv(write, float_format='%.3f', index=False)

def conv_dur_to_int(df, colname, newcolname):
    c = df[colname].to_numpy()
    col = [np.fromstring(c[i].replace('[', '').replace(']', '').replace(',', ' '), dtype=int, sep= ' ') for i in range(len(c))]
    return {newcolname: {i:np.sum(col[i], dtype=int) for i in range(len(col))}}

def conv_hr_to_int(df, colname, newcolname):
    c = df[colname].to_numpy()
    col = [np.fromstring(c[i].replace('[', '').replace(']', '').replace(',', ' '), dtype=int, sep= ' ') for i in range(len(c))]
    return {newcolname: {i:np.mean(col[i], dtype=int) for i in range(len(col))}}

def conv_to_pacific(df, colname, newcolname):
    col = df[colname].to_numpy()
    dati = pd.to_datetime(col, utc=True).astype('datetime64[ns, US/Pacific]').astype('str')
    return {newcolname: {i:dati[i][:len(dati[i])-6] for i in range(len(dati))}}

def cols_split(df, colname, newcolnames, spliton):
    col = df[colname]
    cols = []
    for i in range(len(col)):
        cols += [col[i].split(spliton)]
    cols = np.array(cols).transpose()
    return {newcolnames[i]: {j:cols[i][j] for j in range(len(cols[i]))} for i in range(len(newcolnames))}

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

def print_cols(df):
    colnames = df.columns.to_numpy()
    for i in range(len(colnames)):
        print(colnames[i])

if __name__ == "__main__":
    main()

#######################################################################################################################
#                                                     Data Format                                                     #
#######################################################################################################################

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