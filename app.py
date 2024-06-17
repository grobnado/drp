from flask import Flask, request, jsonify
import torch
import librosa
import os
import sys
from model import PretrainedResNet  # Импорт класса модели
from transforms import ToMelSpectrogram  # Импорт функции для преобразования в мел-спектрограмму
from flask_cors import CORS  # Импортируем CORS


app = Flask(__name__)
CORS(app)
model = PretrainedResNet(num_classes=7)  # Инициализация модели
model.load_state_dict(torch.load('models/trained_model.pth', map_location=torch.device('cpu')))  # Загрузка весов модели
model.eval()

label_to_index = {0: 'Healthy', 1: 'Pneumonia', 2: 'Asthma', 3: 'URTI', 4: 'Heart Failure', 5: 'Bronchitis', 6: 'COPD'}  # Маппинга меток

def predict(audio_data):
    signal, sr = librosa.load(audio_data, sr=None)
    mel_spectrogram = ToMelSpectrogram()(signal)
    
    input_tensor = torch.tensor(mel_spectrogram).unsqueeze(0).unsqueeze(0).float()
    with torch.no_grad():
        output = model(input_tensor)
        _, predicted = torch.max(output.data, 1)
    return predicted.item()

@app.route('/predict', methods=['POST'])
def predict_route():
    print("Received request")
    if 'audio' not in request.files:
        print("No audio file provided")
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    audio_path = os.path.join('uploads', audio_file.filename)
    audio_file.save(audio_path)
    print(f"Audio file saved at {audio_path}")
    
    try:
        prediction = predict(audio_path)
        predicted_label = label_to_index[prediction]
        print(f"Predicted label: {predicted_label}")
        response = jsonify({'prediction': predicted_label})
    except Exception as e:
        print(f"Error: {str(e)}")
        response = jsonify({'error': str(e)})
    finally:
        os.remove(audio_path)  # Удаляем временный файл после обработки
        print(f"Audio file {audio_path} removed")
    
    response.status_code = 200
    print(response)
    return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Используйте переменную окружения PORT
    app.run(debug=True, host='0.0.0.0', port=port)        # Установите host на '0.0.0.0'