# Heart Rate Data Analysis Information
*Saved by data?*

## Visualization Link 
https://public.tableau.com/views/HeartRateAnalysisDashboard-TuNguyen/Dashboard?:language=en-US&:display_count=n&:origin=viz_share_link

## Overview
While correlation does **NOT** mean causation, it can provide valuable insight on possible variables for the cause. This repository documents the process used to find correlations between everyday activities and heart rate irregularities.

**Files**
- *data_clean.py* - The script used for data cleaning and data transforms
- *raw_hr_hr.csv* - The raw data exported from the Withings database
- *cleaned_hr_hr.csv* - The resulting data after cleaning and transforms
- *heartrate_visualized.twb* - The Tableau data visualization workbook

Below is the full breakdown of the data analysis process including: hardware/software used for data collection, methodology for data cleaning and data transforms, and design decisions for the data visualization.

## Withings Technology & Data Collection
**About Withings**
*"With more than 10 years experience in the field, Withings invents, designs, and manufactures a range of award-winning, clinically validated smart health devices and associated apps. Withings provides an easy way to take accurate measurements from the comfort of home, and can help anyone master long term health goals. - Withings"*

**Withings Watch - Hardware**
Both watches are clinically tested.

Date range of hardware used:
- *Data from 0ctober 1 2021 - April 19 2022 was recorded with the Withings Steel HR*
- *Data from April 20 2021 - May 4 2022 was recorded with the Withings ScanWatch*

**ScanWatch**
*"Developed with cardiologists and sleep experts, ScanWatch has been validated in two clinical studies for AFib detection. It has already touched countless lives in Europe where it has also been used in German hospitals, as part of a study to monitor patients remotely. ScanWatch is a hybrid smartwatch designed to monitor health parameters, detect AFib, and help improve overall fitness. ScanWatch boasts clinically validated ECG capabilities, an oximeter for SpO2 measures, and an exceptional battery life of up to 30 days. ScanWatch is the first Withings watch to be FDA-cleared for its oximetry and ECG features." - Withings*

**Withings Data - Software**
Data collected from the watch is archived and available for export on the Withings website. Data is only recorded while the watch is worn.

Data collection metrics:
- *Track heart rate trends day and night, plus continuous heart rate in workout mode*
- *Records heart rate every 10 minutes for round-the-clock tracking*

## Methodology
In order to design and implement an earnest visualization of the data, thorough data cleaning and data transformations were necessary. As a result, this created easily workable data that was utilized to create an interactive Tableau data visualization dashboard.

**Data Issues**
After an inital viewing of the data, these were the main concerns: dates and times were not in uniform timezones, times were in not in the Pacific timezone, data types were not defined, missing data was not shown, non-standardized time intervals, multiple recorded data points for some intervals, and extremely sparse data in months where the watch was not worn 24/7.

**The following solutions were implemented:**
*Data Cleaning*
- Uniform timezone conversion to Pacific time
- Uniform data type conversion
- Drop error values
- Isolated date range to 0ctober 1 2021 - November 30 2021, April 20 2021 - May 4 2022

*Data Transforms*
- Aggregate data points into single 10 minute intervals
- Heart rate is the weighted mean over the summed duration
- Duration is summed over the interval
- Null for missing interval values

*Resulting CSV Data Format (column name (data format) unit - data type)*
- datetime (YYYY-MM-DD HH:M0:00) date&time - string
- heartrate (###.0) bpm - float
- duration (###.0) s - float

**Rationale**
*Data Cleaning*
These specific date ranges were isolated for these reasons: highest data saturation relative to the data set, provides heart rate data before irregularities, during heart rate escalation, and after each isolated correlated factor was used.

*Data Transforms*
In order represent discrete chunks of continuous data, null data points needed to be added as opposed to 0. This is because 0 BPM is not possible (unless dead) and it skews statisical calculations. Data was then aggregated by 10 minute intervals and labelled by the time floored to 10 minutes (ex. 10:12:11, 10:17:23, 10:19:59 -> 10:10:00). This is because the watch records on non-uniform, roughly 10 minute intervals. It also records data more frequently during detected workouts/extremely high heart rates. The duration column was calculated by summing the grouped durations in an interval; and the heart rate column was calculated by a duration-weighted mean of BPMs (heart rates with higher durations were considered "more accurate" and subsequently weighted higher).

*Data Format*
The data was modified into the following format to provide simplified values for analysis and allow for Tableau's data detection algorithm to function more smoothly.

## Visualization - Design Decisions
This visualization was design to be interactive in order to easily interact with and isolate data during specific date ranges. The colors were chosen to imitate an ECG heart rate reading since doctors are most likely familiar with reading from ECG charts.

*Main Graph*
The main line graph provides a detailed, general view of the data.

*Stats Panel*
The statistics panel calculates statisical values from the selected date ranges. Min/Max was added to highlight possible problem areas. A mean weighted towards duration on the selected range was added (heart rates with higher durations were considered "more accurate" and subsequently weighted higher). This gives a general idea of heart rate values. There were difficulties calculating a weighted median through Tableau, so an unweighted median based on each 10 minute interval in the date range was added instead. This provides a general idea of heart rate values that are not skewed by outlier values. 

*Date Range Slider & Selector*
The date range slider allows for exact control of the selected date ranges. However, it is slow in further isolating values within that range. An interactive drag selection panel was added to combat this.

*Data Saturation & Warnings*
The data saturation value provides insight on how much data (recorded 10 minute intervals) is missing within the selected range. While the warnings provide information on the isolated data periods and potential sparse data. These were added to caution on drawing insights from possible inaccurate/incomplete data.