from os.path import dirname, join as pjoin
from scipy import io
import math
import numpy as np
import matplotlib.pyplot as plt

def ecgdemowinmax(original, winSize):
    winHalfSize = math.floor(winSize / 2)
    winHalfSizePlus = winHalfSize + 1
    winSizeSpec = winSize - 1
    frontIterator = 0
    winPos = winHalfSize
    winMaxPos = winHalfSize
    winMax = original[0]
    outputIterator = 0

    filtered = np.zeros(len(original))

    for lengthCounter in range(winHalfSize):
        if original[frontIterator + 1] > winMax:
            winMax = original[frontIterator + 1]
            winMaxPos = winHalfSizePlus + lengthCounter

        frontIterator += 1

    if winMaxPos == winHalfSize:
        filtered[outputIterator] = winMax
    else:
        filtered[outputIterator] = 0

    outputIterator += 1

    for lengthCounter in range(winHalfSize):
        if original[frontIterator + 1] > winMax:
            winMax = original[frontIterator + 1]
            winMaxPos = winSizeSpec
        else:
            winMaxPos -= 1

        if winMaxPos == winHalfSize:
            filtered[outputIterator] = winMax
        else:
            filtered[outputIterator] = 0

        frontIterator += 1
        outputIterator += 1

    for frontIterator in range(frontIterator, len(original) - 1):
        if original[frontIterator + 1] > winMax:
            winMax = original[frontIterator + 1]
            winMaxPos = winSizeSpec
        else:
            winMaxPos -= 1

            if winMaxPos < 0:
                winIterator = frontIterator - winSizeSpec
                winMax = original[winIterator + 1]
                winMaxPos = 0
                winPos = 0

                for winIterator in range(winIterator, frontIterator + 1):
                    if original[winIterator + 1] > winMax:
                        winMax = original[winIterator + 1]
                        winMaxPos = winPos

                    winPos += 1

        if winMaxPos == winHalfSize:
            filtered[outputIterator] = winMax
        else:
            filtered[outputIterator] = 0

        outputIterator += 1

    winIterator -= 1
    winMaxPos -= 1

    for lengthCounter in range(1, winHalfSizePlus):
        if winMaxPos < 0:
            winIterator = len(original) - winSize + lengthCounter
            winMax = original[winIterator + 1]
            winMaxPos = 0
            winPos = 1

            for winIterator in range(winIterator + 1, len(original) - 1):
                if original[winIterator + 1] > winMax:
                    winMax = original[winIterator + 1]
                    winMaxPos = winPos

                winPos += 1

        if winMaxPos == winHalfSize:
            filtered[outputIterator] = winMax
        else:
            filtered[outputIterator] = 0

        frontIterator -= 1
        winMaxPos -= 1
        outputIterator += 1

    return filtered


if __name__ == '__main__':
    #   We are processing two data samples to demonstrate two different situations
    for demo in range(2):
        #   Clear our variables
        ecg = samplingRate = corrected = filtered1 = peaks1 = filtered2 = peaks2 = fresult = None
        #   Load data sample
        if demo == 0:
            plotName = 'Sample 1'
            ecg = io.loadmat('data\\ecgdemodata1.mat')['ecg'][0]
            samplingRate = io.loadmat('data\\ecgdemodata1.mat')['samplingrate'][0, 0]
        elif demo == 1:
            plotName = 'Sample 2'
            ecg = io.loadmat('data\\ecgdemodata2.mat')['ecg'][0]
            samplingRate = io.loadmat('data\\ecgdemodata2.mat')['samplingrate'][0, 0]

        #   Remove lower frequencies
        fresult = np.fft.fft(ecg)
        fresult[0: round(len(fresult) * 5 / samplingRate)] = 0
        fresult[-round(len(fresult) * 5 / samplingRate):] = 0
        corrected = np.real(np.fft.ifft(fresult))
        
        #   Filter - first pass
        winSize = math.floor(samplingRate * 571 / 1000)

        if winSize % 2 == 0:
            winSize = winSize + 1

        filtered1 = ecgdemowinmax(corrected, winSize)

        #   Scale ecg
        peaks1 = filtered1 / (np.max(filtered1) / 7)

        #   Filter by threshold filter
        peaks1[peaks1 < 4] = 0
        peaks1[peaks1 >= 4] = 1

        positions = np.where(peaks1)[0]
        distance = positions[1] - positions[0]
        for data in range(1, len(positions)):
            if positions[data] - positions[data - 1] < distance:
                distance = positions[data] - positions[data - 1]
        
        #   Optimize filter window size
        QRdistance = int(0.04 * samplingRate)
        if QRdistance % 2 == 0:
            QRdistance += 1
        win_size = 2 * distance - QRdistance

        #   Filter - second pass
        filtered2 = ecgdemowinmax(corrected, win_size)
        peaks2 = filtered2
        peaks2[peaks2 < 4] = 0
        peaks2[peaks2 >= 4] = 1

        #   Create figure - stages of processing
        plt.figure(demo)

        #   Original input ECG data
        plt.subplot(3, 2, 1)
        plt.plot((ecg - np.min(ecg)) / (np.max(ecg) - np.min(ecg)))
        plt.title('1. Original ECG')
        plt.ylim([-0.2, 1.2])

        #   ECG with removed low-frequency component
        plt.subplot(3, 2, 2)
        plt.plot((corrected - np.min(corrected)) / (np.max(corrected) - np.min(corrected)))
        plt.title('2. FFT Filtered ECG')
        plt.ylim([-0.2, 1.2])
        
        #   Filtered ECG (1-st pass) - filter has default window size
        plt.subplot(3, 2, 3)
        plt.stem((filtered1 - np.min(filtered1)) / (np.max(filtered1) - np.min(filtered1)))
        plt.title('3. Filtered ECG - 1st Pass')
        plt.ylim([0, 1.4])
        
        #   Detected peaks in filtered ECG
        plt.subplot(3, 2, 4)
        plt.stem(peaks1)
        plt.title('4. Detected Peaks')
        plt.ylim([0, 1.4])

        #   Filtered ECG (2-d pass) - now filter has optimized window size
        plt.subplot(3, 2, 5)
        plt.stem((filtered2 - np.min(filtered2)) / (np.max(filtered2) - np.min(filtered2)))
        plt.title('5. Filtered ECG - 2nd Pass')
        plt.ylim([0, 1.4])
        
        #   Detected peaks - final result
        plt.subplot(3, 2, 6)
        plt.stem(peaks2)
        plt.title('6. Detected Peaks - Finally')
        plt.ylim([0, 1.4])
        
        #   Create figure - result
        plt.figure(demo + 1)
        
        #   Plotting ECG in green
        plt.plot((ecg - np.min(ecg)) / (np.max(ecg) - np.min(ecg)), '-g')
        plt.title('Comparative ECG R-Peak Detection Plot')

        #   Stemming peaks in dashed black
        plt.stem(peaks2 * ((ecg - np.min(ecg)) / (np.max(ecg) - np.min(ecg))), ':k')
        
        #   Show the plots
        plt.show()
