import librosa
import soundfile
from scipy.io import wavfile
import numpy as np
from math import ceil, log2, pi
from cmath import phase, exp


def str_to_arr(s):
    """
    :param str s: some string
    :return [] bits: array of bits representing string
    """
    bits = []
    for symb in s:
        for bit in (bin(ord(symb))[2:]).zfill(8):
            if ord(symb) > 255:
                return [None]
            bits.append(int(bit))
    return bits


def arr_to_str(bits):
    """
    :param [] bits: array of bits representing string
    :return str s: some string
    """
    s = ""
    for i in range(len(bits) // 8):
        byte = bits[i * 8:i * 8 + 8]
        n = int(''.join(list(map(str, byte))), 2)
        s += chr(n)
    return s


def recover(source, segment_width):
    """
    :param source:
    :param segment_width:
    :return:
    """
    samples, sample_rate = librosa.load(source, mono=False)
    left = samples
    if samples.ndim >= 2:
        left = samples[0]
    segment0 = left[:segment_width]
    wave0 = np.fft.rfft(segment0)
    vphase = np.vectorize(phase)
    phase0 = vphase(wave0)
    waves_count = segment_width // 2 + 1
    bits = []
    for i in range(segment_width // 4):
        # delta = abs(abs(phase0[waves_count - i - 2]) - pi / 2)
        # if delta < 0.3:
        #     if phase0[waves_count - i - 2] > 0:
        #         bits.append(1)
        #     else:
        #         bits.append(0)
        # else:
        #     break
        ind = waves_count - i - 2
        # ind = i + 1
        delta = phase0[ind]
        if delta < -pi / 3:
            bits.append(0)
        elif delta > pi / 3:
            bits.append(1)
        else:
            break
    return arr_to_str(bits)


def hide(source, message):
    """
    :param source:
    :param message:
    :return:
    """
    print("getting samples")
    samples, sample_rate = librosa.load(source, mono=False)

    print("segments and add silence if needed")
    left = samples
    if samples.ndim >= 2:
        left = samples[0]
    message_len = len(message) * 8
    v = ceil(log2(message_len) + 1)
    segment_width = 2 ** (v + 1)
    segment_count = ceil(len(left) / segment_width)
    left = np.resize(left, segment_count * segment_width)
    segments = left.reshape(segment_count, -1)
    if samples.ndim >= 2:
        right_mod = np.resize(samples[1], segment_count * segment_width)

    print("phases and amplitubes using fft")

    waves_count = segment_width // 2 + 1  # number of waves in each segment not len(waves)
    waves = [np.fft.rfft(segments[i]) for i in range(segment_count)]
    vphase = np.vectorize(phase)
    phases = [vphase(waves[i]) for i in range(segment_count)]
    vabs = np.vectorize(abs)
    amps = [vabs(waves[i]) for i in range(segment_count)]

    print("delta of phases between segments")

    delta_phases = [None] * segment_count
    delta_phases[0] = [0] * waves_count
    for i in range(1, segment_count):
        delta_phases[i] = phases[i] - phases[i - 1]

    print("phase of first segment with embedded data")

    phase0_mod = phases[0].copy()
    msg_bits = str_to_arr(message)
    if msg_bits == [None]:
        print("Unknown symbol")
        return
    for i in range(message_len):
        ind = waves_count - i - 2
        # ind = i + 1
        if msg_bits[i] == 1:
            phase0_mod[ind] = pi / 2
        else:
            phase0_mod[ind] = -pi / 2

    print("restoring phases using phase of first segment and delta of  phases")

    phases_mod = [None] * segment_count
    phases_mod[0] = phase0_mod.copy()
    for i in range(1, segment_count):
        phases_mod[i] = delta_phases[i] + phases_mod[i - 1]

    print("segments using ifft")

    def get_complex(amp, ph):
        """
        :param amp:
        :param ph:
        :return:
        """
        return amp * exp(ph * 1j)

    vwave = np.vectorize(get_complex)
    waves_mod = [vwave(amps[i], phases_mod[i]) for i in range(segment_count)]
    segments_mod = [np.fft.irfft(waves_mod[i]) for i in range(segment_count)]
    left_mod = np.reshape(segments_mod, -1)

    print("saving file")

    new_source = '.'.join(source.split('.')[:-1]) + "_changed.wav"
    if samples.ndim >= 2:
        new_samples = np.array([[left_mod[i], right_mod[i]] for i in range(len(left_mod))])
    else:
        new_samples = left_mod

    # soundfile.write(new_source, new_samples, sample_rate)
    wavfile.write(new_source, sample_rate, new_samples.astype(np.float32))
    # wavfile.write(new_source, sample_rate, new_samples)
    return new_source, segment_width
