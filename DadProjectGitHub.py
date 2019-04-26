
# coding: utf-8

# In[ ]:


def log_dec_function():
    #import necessary packages
    import numpy as np
    import pandas as pd
    from scipy.signal import find_peaks
    import matplotlib.pyplot as plt
    from math import log
    
    #set up the user input for receiving file path
    file_path = input("What is the file path? ")
    df =  pd.read_csv(file_path)
    data=df.iloc[:, 1].values
    
    #use find peaks to isolate the peaks and times from the data
    peaks, _ = find_peaks(data, height=[0.25, 1])
    peaks_list = peaks.tolist()
    peaks_only = df.iloc[peaks_list]
    
    #create a list of the peaks and trim the data to remove the first few recordings
    peak_amps = peaks_only.iloc[:,1].values
    peak_amps_trimmed = peak_amps[4:]
    
    #create a list of the times and trim the data to remove the first few recordings
    peak_times = peaks_only.iloc[:,0].values
    peak_times_trimmed = peak_times[4:]
    peak_times_seconds = [0]*(len(peak_times_trimmed))
    for i in range(len(peak_times_trimmed)):
        peak_times_seconds[i] = peak_times_trimmed[i][-5:]
        
    #take alternating peaks and times due to inaccuracies in the recording
    #instrument.  Start with the higher of the first two peaks and take 
    #every other one from there
    if peak_amps_trimmed[0] > peak_amps_trimmed[1]:
        peak_amps_alternating = peak_amps_trimmed[::2]
        peak_seconds = peak_times_seconds[::2]
    else:
        peak_amps_alternating = peak_amps_trimmed[1::2]
        peak_seconds = peak_times_seconds[1::2]
        
    #take the natural log of the peaks
    peak_logs = [0]*(len(peak_amps_alternating)) 
    for i in range(len(peak_amps_alternating)):
        peak_logs[i] = log(peak_amps_alternating[i])
    
    #calculate the periods and average period and log decrement and 
    #average log decrement
    periods = [0]*(len(peak_times_seconds)-1)
    for i in range(len(peak_times_seconds)-1):
        periods[i] = float(peak_times_seconds[i+1])-float(peak_times_seconds[i])
    period_avg = sum(periods[1:21])/10
    log_dec = [0]*(len(peak_amps)-1)
    for i in range(len(peak_amps)-1):
        log_dec[i] = np.log(peak_amps[i]/peak_amps[i+1])
    log_dec_avg= sum(log_dec)/float(len(log_dec))
    
    #print avg log decrement and avg period
    print("Your log decrement average is: ", log_dec_avg)
    print("Your average period is: ", period_avg)
    
    #create two plots, the first is time versus amplitude, the second is 
    #time versus the natural log of the amplitude
    plt.plot(peak_seconds,peak_amps_alternating, 'ro')
    plt.title('Plot of Peak Amplitude vs. Time')
    plt.show()
    plt.plot(peak_seconds,peak_logs, 'bo')
    plt.ylabel("Time of Peak (s)")
    plt.xlabel("Peak Amplitude")
    plt.ylabel("Time of Peak (s)")
    plt.xlabel("Natural Log of Peak Amplitude")
    plt.title('Plot of Natural Log of Peak Amplitude vs. Time')
    plt.show()
    
    #create versions of the time and peak log lists that are floats and not
    #strings
    peak_seconds_float = list(np.float_(peak_seconds))
    peak_logs_float = list(np.float_(peak_logs))
    
    #fit a line to the time versus peak log data and print the slope and 
    #intercept.
    slope,intercept = np.polyfit(peak_seconds_float, peak_logs_float, 1)
    print("Your slope is: ", slope)
    print("Your y-intercept is: ", intercept)

