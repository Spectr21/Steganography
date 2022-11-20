
def open_mp3(source):
    """
    :param str source: path to mp3 file
    :return tuple data: (array of arrays(audio channels) of samples, frame rate, sample width)
    """
    audio = AudioSegment.from_mp3(source)
    samples = []
    raw = audio.split_to_mono()
    if audio.channels >= 2:
        samples.append(np.array(raw[0].get_array_of_samples()))
        samples.append(np.array(raw[1].get_array_of_samples()))
    else:
        samples = [raw[0].get_array_of_samples()]
    return samples, audio.frame_rate, audio.sample_width

def create_mp3(place, samples, fr, sw):
    """
    :param str place: path to new mp3 file
    :param [[]] samples: array of array of samples
    :param int fr: frame rate
    :param int sw: sample width
    :return: void
    """
    if len(samples) == 2:
        ch_1 = AudioSegment(samples[0].tobytes(), frame_rate=fr, sample_width=sw, channels=1)
        ch_2 = AudioSegment(samples[1].tobytes(), frame_rate=fr, sample_width=sw, channels=1)
        audio = AudioSegment.from_mono_audiosegments(ch_1, ch_2)
    else:
        audio = AudioSegment(samples[0].tobytes(), frame_rate=fr, sample_width=sw, channels=1)
    audio.export(place, format="mp3")

def split_to_segments(channel, message):
    """
    :param [] channel: array of samples
    :param str message:
    :return [[]] segments: array of arrays of segments
    """
    message_len = len(message) * 8
    v = ceil(log2(message_len) + 1)
    segment_width = 2 ** (v + 1)
    segment_count = ceil(len(channel) / segment_width)
    channel = np.resize(channel, segment_count * segment_width)
    segments = channel.reshape(segment_count, -1)
    return segments

def fourier_and_so_on(segments, segment_count, segment_width, msg):
    """
    :param segments:
    :param segment_count:
    :param segment_width:
    :param msg:
    :return:
    """
    waves_count = segment_width // 2 + 1  # number of waves in each segment not len(waves)
    waves = [np.fft.rfft(segments[i]) for i in range(segment_count)]
    vphase = np.vectorize(phase)
    phases = [vphase(waves[i]) for i in range(segment_count)]
    vabs = np.vectorize(abs)
    amps = [vabs(waves[i]) for i in range(segment_count)]
    delta_phases = [None] * segment_count
    delta_phases[0] = [0] * waves_count
    for i in range(1, segment_count):
        delta_phases[i] = phases[i] - phases[i - 1]
    phase0_mod = phases[0].copy()
    msg_bits = str_to_arr(msg)
    # for i in range(1, len(msg_bits) + 1):
    #     if msg_bits[i - 1] == 1:
    #         phase0_mod[waves_count - i] = pi / 2
    #     else:
    #         phase0_mod[waves_count - i] = -pi / 2
    phases_mod = [None] * segment_count
    phases_mod[0] = phase0_mod.copy()
    for i in range(1, segment_count):
        phases_mod[i] = delta_phases[i] + phases_mod[i - 1]

    def get_complex(amp, ph):
        return amp * exp(ph * 1j)

    vwave = np.vectorize(get_complex)
    tmp_mod = [vwave(phases_mod[i], amps[i]) for i in range(segment_count)]
    segments_mod = [np.fft.irfft(tmp_mod[i]) for i in range(segment_count)]
    return segments_mod
