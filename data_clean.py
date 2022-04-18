import pandas as pd
import numpy as np

#
# Merges all relevant data, deletes the rest, stores the results in cleaned_'read'.csv
#

# The read csv file
read = 'raw_hr_hr.csv'
# The write csv file
write = 'cleaned_raw_hr_hr.csv'
# The csv file with as a data frame
df = pd.read_csv(read)
# Suppress numpy float sci form
np.set_printoptions(suppress=True)

def main():
    # # resulting merged & cleaned data frame
    # dest_map = {}
    
    # # Waste Treatment data
    # wt_keep = np.array(['WT reclaimed wastewater released by wastewater facilities','WT number of wastewater facilities','WT number of public wastewater facilities',
    #                     'WT returns by public wastewater facilities', 'WT reclaimed wastewater released by public wastewater facilities'])
    # wt_map = {}
    # dest_map.update(split(wt_keep, wt_map))

    # # Output merged & cleaned dataframe to csv file
    # dest_map.to_csv(write, float_format='%.3f', index=False)


    # 2022-04-11T00:00:40+02:00,[22],[86]
    # 2022-04-11T00:10:24+02:00,[42],[122]
    # 2022-04-11T00:29:54+02:00,[22],[104]
    # 2022-04-11T00:39:37+02:00,[41],[103]
    # 2022-04-11T00:49:25+02:00,[46],[102]
    print_col_reversed(df['start'])

# takes in an np arr of column names
# returns an np arr of float converted columns
def cols_to_conv_np(cols):
    return np.array([conv_col_to_float(df[cols[i]]) for i in range(len(cols))])

# Takes in a column, converts column values to float, zeroes out missing values
# col - the input column 
# returns an np array of the col
def conv_col_to_float(col):
    # print([ord(c) for c in c1[i]])
    c_arr = col.to_numpy()
    return np.array([0.00 if (str(c_arr[i])[0] == str(chr(45))) else float(c_arr[i]) for i in range(len(col))])

# keeps select columns, merges select columns
# keepCols - an np array of column names to keep
# mergeCols - a map of new col names to an array of column names to merge
# Returns a map of new columns to names
def split(keepCols, mergeCols):
    # sorry
    colMap = {{} if (len(keepCols) == 0) else keepCols[i]:conv_col_to_float(df[keepCols[i]]) for i in range(len(keepCols))}
    if (mergeCols):
        colMap.update({k:split_cols(cols_to_conv_np(mergeCols[k])) for k in mergeCols.keys()})
    return colMap

# Takes in columns as np arrays and merges 
# --column data values must be of type float--
# cols - np array of columns being merged
# returns a map of name to col
def split_cols(cols):
    return np.sum(cols, axis = 0)

# prints out the column headers in reversed order
# header - np array of the column headers
def print_col_reversed(header):
    for i in reversed(range(len(header))):
        print(header[i].split('T')[1])

# prints out the column headers in reversed order with a
# data value paired from select row
# header - np array of the column headers
def print_col_reversed_c(header, row):
    fRow = df.iloc[row].to_numpy()
    for i in reversed(range(len(header))):
        print(header[i] + ' ' + str(fRow[i]))

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