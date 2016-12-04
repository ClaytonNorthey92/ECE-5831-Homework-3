import datetime
import random
import speech_recognition

from config import dictionary, training_data_dir

if __name__=='__main__':
	r = speech_recognition.Recognizer()
	audio = None
	for i in range(3):
		for random_word in dictionary:
			with speech_recognition.Microphone() as source:
				print 'say {}'.format(random_word)
				audio = r.listen(source)

			print 'writing'
			now = str(datetime.datetime.now()).replace(' ', '_')
			with open('{}/{}_test_data_{}.wav'.format(training_data_dir, random_word, now), 'wb') as output_file:
				output_file.write(audio.get_wav_data())