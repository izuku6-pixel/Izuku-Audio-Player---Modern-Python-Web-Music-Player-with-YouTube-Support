# 🎵 Izuku Audio Player - 2025 Edition

A beautifully designed and feature-rich music player built with Python and Tkinter, bundled with a sleek HTML UI for modern presentation. It supports local audio files, folders, and YouTube URLs for streaming and playback.

---

## ✨ Features

- 🎧 Play audio files in MP3, WAV, FLAC, OGG, and M4A formats
- 📂 Load entire music folders at once
- 📺 Stream and play audio from YouTube URLs *(requires yt-dlp or youtube-dl)*
- 🎨 Multiple UI themes and dark mode toggle
- ⌨️ Keyboard shortcuts for play/pause and navigation
- 📊 Visualizer and real-time progress
- ⚙️ Settings panel with customization options
- 🖥️ Accompanying HTML UI with futuristic glassmorphism design

---

## 🖼️ Preview

> ![Screenshot](https://via.placeholder.com/800x500.png?text=Izuku+Audio+Player+Preview)

---

## 📦 Requirements

### Python Dependencies
Make sure to install the following Python packages:

```bash
pip install pygame mutagen
```

### Optional (for YouTube support)

```bash
pip install yt-dlp
# or
pip install youtube-dl
```

---

## 🚀 How to Use

### 🔧 Python App

1. Clone the repo:
    ```bash
    git clone https://github.com/your-username/izuku-audio-player.git
    cd izuku-audio-player
    ```

2. Run the player:
    ```bash
    python izuku_audio_player.py
    ```

3. Features inside the player:
    - Load files or folders
    - Paste YouTube links and play audio
    - Switch themes and enable dark mode
    - Use shortcuts: `Space`, `←`, `→`

### 🌐 HTML UI

To open the HTML frontend:

1. Open `modern_audio_player.html` in any modern browser.
2. The web UI simulates music control and visualization with a beautiful interface.
3. *(Audio streaming in HTML version is demo-simulated; future implementation can integrate real audio APIs.)*

---

## 🛠️ Tech Stack

- **Python**: Tkinter, Pygame, Mutagen
- **JavaScript & HTML/CSS**: Modern UI with glassmorphism, CSS animations
- **YouTube Audio Support**: yt-dlp or youtube-dl
- **Design**: Responsive, accessible, and customizable

---

## 📁 Project Structure

```
├── izuku_audio_player.py       # Main Python desktop player
├── modern_audio_player.html    # Frontend HTML UI
└── README.md                   # Project documentation
```

---

## 🙌 Credits

- `yt-dlp` and `youtube-dl` for YouTube audio extraction
- `pygame` and `mutagen` for audio playback and metadata
- UI inspired by modern music apps and web UI trends

---

## 📜 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute.

---

## 💡 Future Improvements

- Integrated playlist management
- Cross-platform packaging (Windows/Mac/Linux)
- Web-based audio backend
- Real-time audio visualizer using audio FFT

---

## ❤️ Support

If you enjoy this project, consider giving it a ⭐️ on GitHub and sharing it with your friends!
