
# PosePlay: T-Rex Game with Gesture Control

PosePlay is a modern adaptation of the classic T-Rex runner game, enhanced with real-time gesture control. Using a webcam and computer vision, players can control the character's actions through hand gestures without relying on traditional keyboard input.

---

## Features

- **Gesture-Based Input**: Jump using a fist gesture detected by the webcam.
- **Real-Time Hand Tracking**: Integrated with MediaPipe and OpenCV for responsive gesture detection.
- **Pygame Integration**: Smooth 2D gameplay with custom sprites, obstacles, and animation.
- **Score System**: Increments score based on obstacle avoidance.
- **Game States**:
  - Start Screen with instructions
  - In-game action
  - Game Over screen with restart option
- **Audio Feedback**: Background music during gameplay and sound effects on game over.

---

## Technologies Used

- **Python 3.10+**
- **Pygame** – Game interface and event loop
- **OpenCV** – Webcam feed processing
- **MediaPipe** – Hand gesture recognition
- **Custom Assets** – Character and obstacle images, audio files

---

## Project Structure



PosePlay-Trex/
├── assets/
│   ├── girl.png           # Character sprite
│   ├── RedFlag.png        # Obstacle sprite
│   ├── gameplay.mp3       # Background music
│   └── gameover.mp3       # Game over sound
├── hand\_detector.py       # Handles MediaPipe hand detection
├── trex\_game.py           # Game logic and rendering
├── main.py                # Game loop and gesture integration
└── README.md


---

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/PosePlay-Trex.git
cd PosePlay-Trex
````

2. **Install dependencies:**

```bash
pip install pygame opencv-python mediapipe
```

3. **Run the game:**

```bash
python main.py
```

> Ensure your webcam is connected and enabled.

---

## Usage

| Action     | Input Method               |
| ---------- | -------------------------- |
| Start Game | Press Space or Make a Fist |
| Jump       | Make a Fist                |
| Restart    | Press `R` after Game Over  |
| Quit       | Press `Q` in webcam window |

---

## Notes

* For optimal gesture detection, play in a well-lit environment.
* Distance from the camera should be approximately 1 meter.
* Assets can be customized by replacing images and audio files in the `assets/` directory.
