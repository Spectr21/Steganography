from pydub import AudioSegment
import numpy as np
import math
import cmath


def str_to_arr(s):
    """
    :param str s: some string
    :return [] bits: array of bits representing string
    """
    bits = []
    for symb in s:
        for bit in (bin(ord(symb))[2:]).zfill(8):
            bits.append(int(bit))
    return bits


# samples
source = input("Введите путь до файла")
message = input("Введите сообщение")
audio = AudioSegment.from_mp3(source)
samples = []
raw = audio.split_to_mono()
if audio.channels >= 2:
    samples.append(np.array(raw[0].get_array_of_samples()))
    samples.append(np.array(raw[1].get_array_of_samples()))
else:
    samples = [raw[0].get_array_of_samples()]
# segments and add silence if needed
print('segments and add silence if needed')
left = samples[0]
message_len = len(message) * 8
v = math.ceil(math.log2(message_len) + 1)
segment_width = 2 ** (v + 1)
segment_count = math.ceil(len(left) / segment_width)
left = np.resize(left, segment_count * segment_width)
segments = left.reshape(segment_count, -1)
if audio.channels >= 2:
    right_mod = np.resize(samples[0], segment_count * segment_width)

# phases and amplitubes using fft
print('phases and amplitubes using fft')
waves_count = segment_width // 2 + 1  # number of waves in each segment not len(waves)
waves = [np.fft.rfft(segments[i]) for i in range(segment_count)]
vphase = np.vectorize(cmath.phase)
phases = [vphase(waves[i]) for i in range(segment_count)]
vabs = np.vectorize(abs)
amps = [vabs(waves[i]) for i in range(segment_count)]
# delta of phases between segments
print('delta of phases between segments')
delta_phases = [None] * segment_count
delta_phases[0] = [0] * waves_count
for i in range(1, segment_count):
    delta_phases[i] = phases[i] - phases[i - 1]
# phase of first segment with embedded data
print('phase of first segment with embedded data')
phase0_mod = phases[0].copy()
msg_bits = str_to_arr(message)
for i in range(1, len(msg_bits) + 1):
    if msg_bits[i - 1] == 1:
        phase0_mod[waves_count - i] = math.pi / 2
    else:
        phase0_mod[waves_count - i] = -math.pi / 2
# restore phases using phase of first segment and delta of  phases
print('restore phases using phase of first segment and delta of  phases')
phases_mod = [None] * segment_count
phases_mod[0] = phase0_mod.copy()
for i in range(1, segment_count):
    phases_mod[i] = delta_phases[i] + phases_mod[i - 1]

# segments using ifft
print('segments using ifft')


def get_complex(amp, phase):
    return amp * cmath.exp(phase * 1j)


vwave = np.vectorize(get_complex)
waves_mod = [vwave(amps[i],phases_mod[i]) for i in range(segment_count)]
segments_mod = [np.fft.irfft(waves_mod[i]) for i in range(segment_count)]
left_mod = np.reshape(segments_mod, -1)
left_mod = left_mod.astype(np.int16)
right_mod = right_mod.astype(np.int16)

fr = raw[0].frame_rate
sw = raw[0].sample_width
sadjfhbl = raw[0].frame_count()
if audio.channels >= 2:
    ch_1 = AudioSegment(left_mod.tobytes(), frame_rate=fr, sample_width=sw, channels=1)
    tuigj = ch_1.frame_count()
    ch_2 = AudioSegment(right_mod.tobytes(), frame_rate=fr, sample_width=sw, channels=1)
    tuigj2 = ch_2.frame_count()
    new_audio = AudioSegment.from_mono_audiosegments(ch_1, ch_2)
else:
    new_audio = AudioSegment(left_mod.tobytes(), frame_rate=fr, sample_width=sw, channels=1)
new_audio.export(source[0:-4] + "_changed.mp3", format="mp3")
