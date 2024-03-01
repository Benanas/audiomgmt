import librosa
file = r'E:\Acapellas\Zed Bias + Slay - When The Rain Came Down - 03 When The Rain Came Down (Acapella).aiff'

y, sr = librosa.load(file)

print('waveform')
print(y)
print('\nsampling rate')
print(sr)

tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
print('Estimated tempo: {:.2f} beats per minute'.format(tempo))