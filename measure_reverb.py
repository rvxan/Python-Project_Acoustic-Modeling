""" Measure Reverb Time 1 """
# code used as reference from L26 Lecture Slides
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

sample_rate, data = wavfile.read("PinkPanther30.wav")  # audio file uploaded by user
spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))


# prints var outputs
def debugg(fstring):
    print(fstring)  # comment out for prod
    # pass


def find_target_frequency(freqs):
    for x in freqs:
        if x > 1000:
            break
    return x


def frequency_check():
    # choose a frequency to check

    debugg(f'freqs {freqs[10]}')
    target_frequency = find_target_frequency(freqs)
    debugg(f'target_frequency {target_frequency}')
    # find index of target_frequency
    index_frequency = np.where(freqs == target_frequency)[0][0]
    # find a sound data for a particular frequency

    data_for_frequency = spectrum[index_frequency]
    debugg(f'data_for_frequency {data_for_frequency[10]}')

    # change a digital signal for a value in decibels
    data_db = np.log10(data_for_frequency, where=data_for_frequency > 0)  # uses natural log to convert output value to decibels
    data_db = 10 * data_db
    return data_db


# create plot and label
data_db = frequency_check()
plt.figure()
# plot reverb time on grid
plt.plot(t, data_db, linewidth=1, alpha=0.7, color='#004bc6')
plt.xlabel('Time (s)')
plt.ylabel('Power (dB)')

# find an index and max value for computation and marking plot
index_max = np.argmax(data_db)
value_max = data_db[index_max]
plt.plot(t[index_max], data_db[index_max], 'go')

# slice array from max value
slice_array = data_db[index_max]

# determine 5 dB less of max value
value_max_less_5 = value_max - 5


# find a nearest value
def find_nearest_value(array, value):
    # pass in sliced array list and value < 5 dB
    array = np.asarray(array)
    # convert input into array
    debugg(f'array {array[10]}')
    # determine absolute value and subtract the < 5 dB value
    idx = (np.abs(array - value)).argmin()
    debugg(f'idx {idx}')
    debugg(f'array[idx] {array[idx]}')

    return array[idx]


value_max_less_5 = find_nearest_value(slice_array, value_max_less_5)
index_max_less_5 = np.where(data_db == value_max_less_5)
# plot values
plt.plot(t[index_max_less_5], data_db[index_max_less_5], 'yo')

# determine 25 dB less of max value
# slice array from max < 5dB
value_max_less_25 = value_max - 25
value_max_less_25 = find_nearest_value(slice_array, value_max_less_25)
index_max_less_25 = np.where(data_db == value_max_less_25)

# plot point
plt.plot(t[index_max_less_25], data_db[index_max_less_25], 'ro')
rt20 = (t[index_max_less_5] - t[index_max_less_25])[0]  # computes RT20

# extrapolate rt20 to rt60
rt60 = 3 * rt20

# limits set on plot
plt.xlim(0, ((round(abs(rt60), 2)) * 1.5))
plt.grid()  # show grid
plt.show()  # show plots

print(f'The RT60 reverb time is {round(abs(rt60), 2)} seconds')
