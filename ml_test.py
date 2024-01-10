import librosa
import soundfile
import os, glob, pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import RFE
from sklearn.model_selection import GridSearchCV


def extract_feature(file_name, mfcc, chroma, mel):
    with soundfile.SoundFile(file_name) as sound_file:
        X = sound_file.read(dtype="float32")
        sample_rate=sound_file.samplerate
        if chroma:
            stft=np.abs(librosa.stft(X))
        result=np.array([])
        if mfcc:
            mfccs=np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
            result=np.hstack((result, mfccs))
        if chroma:
            chroma=np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
            result=np.hstack((result, chroma))
        if mel:
            mel=np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T,axis=0)
            result=np.hstack((result, mel))

    return result


#DataFlair - Emotions in the RAVDESS dataset
emotions={
  '01':'neutral',
  '02':'calm',
  '03':'happy',
  '04':'sad',
  '05':'angry',
  '06':'fearful',
  '07':'disgust',
  '08':'surprised'
}

observed_emotions=['calm', 'happy', 'fearful', 'disgust']


#DataFlair - Load the data and extract features for each sound file
def load_data(test_size=0.2):
    x,y=[],[]
    for file in glob.glob(".\\source\\Actor_*\\*.wav"):
        file_name = os.path.basename(file)
        emotion = emotions[file_name.split("-")[2]]
        if emotion not in observed_emotions:
            continue
        feature = extract_feature(file, mfcc=True, chroma=True, mel=True)
        x.append(feature)
        y.append(emotion)
    return train_test_split(np.array(x), y, test_size=test_size, random_state=9)


x_train, x_test, y_train, y_test = load_data(test_size=0.25)
print((x_train.shape[0], x_test.shape[0]))
print(f'Видобуто ознак: {x_train.shape[1]}')

# Масштабування ознак
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

# Оновлення моделі зі масштабованими ознаками
model = MLPClassifier(alpha=0.01, batch_size=256, epsilon=1e-08, hidden_layer_sizes=(300,), learning_rate='adaptive', max_iter=500)
model.fit(x_train_scaled, y_train)
y_pred_scaled = model.predict(x_test_scaled)
accuracy_scaled = accuracy_score(y_true=y_test, y_pred=y_pred_scaled)
print("Точність з масштабуванням: {:.2f}%".format(accuracy_scaled * 100))

# Відбір ознак
rfe = RFE(model, n_features_to_select=your_desired_number)
x_train_rfe = rfe.fit_transform(x_train, y_train)
x_test_rfe = rfe.transform(x_test)
model.fit(x_train_rfe, y_train)
y_pred_rfe = model.predict(x_test_rfe)
accuracy_rfe = accuracy_score(y_true=y_test, y_pred=y_pred_rfe)
print("Точність з відбором ознак: {:.2f}%".format(accuracy_rfe * 100))

# Тюнінг гіперпараметрів
param_grid = {
    'alpha': [0.001, 0.01, 0.1, 1],
    'hidden_layer_sizes': [(100,), (200,), (300,), (400,)],
    'max_iter': [200, 300, 400, 500],
}

grid_search = GridSearchCV(MLPClassifier(), param_grid, cv=3)
grid_search.fit(x_train, y_train)
best_params = grid_search.best_params_
model.set_params(**best_params)
model.fit(x_train, y_train)
y_pred_tuned = model.predict(x_test)
accuracy_tuned = accuracy_score(y_true=y_test, y_pred=y_pred_tuned)
print("Точність з тюнінгом гіперпараметрів: {:.2f}%".format(accuracy_tuned * 100))






