#   ECG Signal Processing - R Peak Detection


##  Objective
The basic task of electrocardiogram - ECG - processing is R-peaks detection. There are some difficulties one can encounter in processing ECG such as irregular distance between peaks, irregular peak form, presence of low frequency component in ECG due to patient breathing etc. To solve the task the processing pipeline should contain particular stages to reduce influence of those factors. Present sample demonstrates such a pipeline. The aim is to show results of processing in main pipeline stages.
-   This electrical activity can be measured by placing electrodes at specific points on the skin
-   An Ideal ECG looks like this and it keeps repeating itself
-   We will try to detect R - peaks in this project


##  Theory

### Fast Fourier Transform - FFT:
A fast Fourier transform (FFT) is an algorithm that computes the discrete Fourier transform (DFT) of a sequence, or its inverse (IDFT). Fourier analysis converts a signal from its original domain to a representation in the frequency domain and vice versa.

The idea is to apply direct fast Fourier transform - FFT, remove low frequencies and restore ECG with the help of inverse FFT.

### Window Filter:
The window method for digital filter design is fast, convenient, and robust, but generally suboptimal. It is easily understood in terms of the convolution theorem for Fourier transforms, making it instructive to study after the Fourier theorems and windows for spectrum analysis. It can be effectively combined with the frequency sampling method.

The window method consists of simply “windowing” a theoretically ideal filter impulse response h(n) by some suitably chosen window function w(n), yielding.

$$h_w\left (n \right) = w\left(n \right). h\left(n \right), \quad n \in Z.$$


##  Algorithm
1.  Start
1.  Remove low frequency components
    1.  Change to frequency domain using FFT
    1.  Remove low frequency components
    1.  Back to time domain using IFFT
1.  Find local maxima using windowed filter
1.  Remove small value, store significant ones
1.  Adjust filter size and repeat step 3 and step 4
1.  Finish


##  Conclusion
Using the Principles of Fast Fourier Transform (FFT) and window filter method, the code can detect the R Peaks of the given ECG Waveform, having significant values and removing the low frequencies (i.e. P, Q, S and T waves). Any distorted or irregular ECG waveform can easily be detected by calculating the irregularity in the heart rate.

Heart Beat Rate in (beats/second) can be calculated by the formula,

$$\text{Rate} = \frac{60\times\left(\text{Sampling Rate} \right)}{\left(\text{R-R interval} \right)}$$

I learnt,
1.  The Fast Fourier Transform (FFT) algorithm and the digital frequency principle
1.  How to build a digital FIR filter to solve the problem and construct implementation algorithms
