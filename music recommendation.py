import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QComboBox, QSpacerItem, QSizePolicy
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QDesktopServices, QFont
import pandas as pd
import numpy as np

# Sample music data with real song names and more user data
data = {
    "Song": ["Shape of You", "Bohemian Rhapsody", "Rolling in the Deep", "Imagine", "Yesterday", "Despacito", "Billie Jean", "Hey Jude", "Hotel California", "Purple Haze"],
    "User1": [4, 5, 4, 0, 3, 5, 0, 4, 3, 0],
    "User2": [0, 4, 3, 5, 0, 0, 0, 0, 5, 4],
    "User3": [3, 0, 4, 4, 3, 4, 0, 5, 0, 4],
    "User4": [0, 0, 5, 4, 4, 5, 0, 0, 0, 0],
    "User5": [5, 0, 0, 0, 4, 4, 5, 0, 0, 3],
    "User6": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}

music_df = pd.DataFrame(data)

# Function to recommend songs for a user
def recommend_songs(user_name):
    user_ratings = music_df[user_name]
    unrated_songs = user_ratings.index[user_ratings == 0].tolist()
    rated_songs = user_ratings.index[user_ratings > 0].tolist()
    
    # If there are no rated songs, return a random song
    if not rated_songs:
        return np.random.choice(unrated_songs, 1)

    recommended_song = np.random.choice(rated_songs, 1)
    
    return recommended_song

class MusicRecommendationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Music Recommendation App')
        self.setGeometry(100, 100, 500, 300)
        self.setStyleSheet("background-color: #2e2e2e; color: #ffffff;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.header_label = QLabel('Music Recommendation App', self)
        self.header_label.setFont(QFont('Arial', 18))
        self.header_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.header_label)

        self.label = QLabel('Get personalized music recommendations', self)
        self.label.setFont(QFont('Arial', 14))
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.user_select_label = QLabel('Select User:', self)
        self.user_select_label.setFont(QFont('Arial', 12))
        self.user_select_label.setAlignment(Qt.AlignLeft)
        self.layout.addWidget(self.user_select_label)

        self.user_combo_box = QComboBox(self)
        self.user_combo_box.setFont(QFont('Arial', 12))
        self.user_combo_box.addItems(music_df.columns[1:])
        self.layout.addWidget(self.user_combo_box)

        self.recommend_button = QPushButton('Get Recommendations', self)
        self.recommend_button.setFont(QFont('Arial', 12))
        self.recommend_button.setStyleSheet("background-color: #3b5998; color: #ffffff; padding: 10px;")
        self.recommend_button.clicked.connect(self.get_recommendations)
        self.layout.addWidget(self.recommend_button)

        self.recommendation_label = QLabel('', self)
        self.recommendation_label.setFont(QFont('Arial', 12))
        self.recommendation_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.recommendation_label)

        self.youtube_button = QPushButton('Listen on YouTube', self)
        self.youtube_button.setFont(QFont('Arial', 12))
        self.youtube_button.setStyleSheet("background-color: #ff0000; color: #ffffff; padding: 10px;")
        self.youtube_button.clicked.connect(self.open_youtube)
        self.youtube_button.setEnabled(False)  # Disabled until a recommendation is made
        self.layout.addWidget(self.youtube_button)

        # Add a spacer item to improve layout
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def get_recommendations(self):
        user_name = self.user_combo_box.currentText()
        recommended_song = recommend_songs(user_name)
        
        self.recommendation_label.setText(f"Recommended song for {user_name}: {music_df.at[recommended_song[0], 'Song']}")

        self.recommended_song = music_df.at[recommended_song[0], 'Song']
        self.youtube_button.setEnabled(True)

    def open_youtube(self):
        if hasattr(self, 'recommended_song'):
            youtube_url = f"https://www.youtube.com/results?search_query={self.recommended_song}"
            QDesktopServices.openUrl(QUrl(youtube_url))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MusicRecommendationApp()
    window.show()
    sys.exit(app.exec_())
