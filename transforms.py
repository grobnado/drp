import librosa
import numpy as np

def augment_spectrogram(spectrogram):
    # Сдвиг по времени
    if np.random.rand() < 0.5:
        spectrogram = np.roll(spectrogram, shift=int(spectrogram.shape[1] * 0.1), axis=1)

    # Добавление шума
    if np.random.rand() < 0.5:
        noise = np.random.randn(*spectrogram.shape) * 0.1
        spectrogram += noise

    # Изменение громкости
    if np.random.rand() < 0.5:
        spectrogram = spectrogram * np.random.uniform(0.8, 1.2)

    return spectrogram

class ToMelSpectrogram:
    def __init__(self, n_mels=64, n_fft=1024, hop_length=512, augment=False):
        self.n_mels = n_mels
        self.n_fft = n_fft
        self.hop_length = hop_length
        self.augment = augment

    def __call__(self, signal):
        mel_spectrogram = librosa.feature.melspectrogram(
            y=signal, 
            sr=22050, 
            n_mels=self.n_mels, 
            n_fft=self.n_fft, 
            hop_length=self.hop_length
        )
        mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)
        
        if self.augment:
            mel_spectrogram = augment_spectrogram(mel_spectrogram)

        # Нормализация мини-батчей
        mel_spectrogram = (mel_spectrogram - mel_spectrogram.mean()) / mel_spectrogram.std()

        # Нормализация минимакс
        mel_spectrogram = (mel_spectrogram - mel_spectrogram.min()) / (mel_spectrogram.max() - mel_spectrogram.min())

        return mel_spectrogram

# Пример использования:
# transform = ToMelSpectrogram(augment=True)
# mel_spectrogram = transform(audio_signal)
