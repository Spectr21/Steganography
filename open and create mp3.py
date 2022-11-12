from pydub import AudioSegment
import numpy as np

def open_mp3(source):
	"""
	:param str source: path to mp3 file
	:return tuple data: (array of arrays(audio channels) of samples, frame rate, sample widhth)
	"""
	audio = AudioSegment.from_mp3(source)
	samples = []
	raw = audio.split_to_mono()
	if (audio.chennels == 2):
		sample = [[],[]]
		samples[0] = raw[0].get_array_of_samples()
		samples[1] = raw[1].get_array_of_samples()
	else:
		sample = [raw[0].get_array_of_samples()]
	return (samples, audio.frame_rate, audio.sample_widhth)

def create_mp3(place, samples, fr, sw):
	"""
	:param str place: path to new mp3 file
	:param [[]] samples: array of array of samples
	:param int fr: frame rate
	:param int sw: sample width
	:return: void
	"""
	if (len(samples) == 2):
		ch_1 = AudioSegment(sample[0].tobytes(), frame_rate = fr, sample_width = sw, channels = 1)
		ch_2 = AudioSegment(sample[1].tobytes(), frame_rate = fr, sample_width = sw, channels = 1)
		audio = AudioSegment.from_mono_audiosegments(ch_1,ch_2)
	else:
		audio = AudioSegment(sample[0].tobytes(), frame_rate = fr, sample_width = sw, channels = 1)
	audio.export(place, format="mp3")

	
