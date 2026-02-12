# 🎨 Virtual Paint Pro

> Paint in the air like a wizard. No brushes required. Just your hand and some serious finger-pointing skills.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Try%20It%20Now!-brightgreen?style=for-the-badge&logo=streamlit)](https://mp-visual-drawing-board.streamlit.app/)

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.0+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🤔 What's This?

Ever wanted to paint without getting your hands dirty? Well, now you can! Virtual Paint Pro turns your webcam into a magical canvas where you draw using just your fingers. It's like Microsoft Paint met Harry Potter and had a baby.

<div align="center">
  <img src="https://media.giphy.com/media/3o7TKSjRrfIPjeiVyM/giphy.gif" width="400" alt="Magic GIF"/>
</div>

## ✨ Features

- 🖐️ **Hand Tracking**: Uses MediaPipe to track your hand movements (yes, it's watching you)
- 🎨 **Multiple Colors**: Pink, Orange, Green, and the classic "oops I messed up" eraser
- 🔄 **Real-time Drawing**: Draw as smooth as butter (internet connection permitting)
- 📹 **WebRTC Streaming**: Works right in your browser via Streamlit
- 🧼 **Clean Canvas**: Reset button for when your art looks more like a crime scene

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- A webcam (obviously)
- Two functioning hands (one works too, but you'll look cooler with two)

### Try It Live!

🚀 **[Launch Visual-Drawing-Board](https://mp-visual-drawing-board.streamlit.app/)** - No installation needed!

### Run Locally

Want to tinker with the code? Run it on your machine:

```bash
# Clone this masterpiece
git clone https://github.com/Wizard-Mayank/Visual-Drawing-Board.git
cd Visual-Drawing-Board

# Install dependencies
pip install -r requirements.txt

# Run the magic
streamlit run app.py
```

## 🎮 How to Use

1. **Start the app** - Allow camera access (I promise I'm not recording your reactions)
2. **Selection Mode** - Show ✌️ two fingers (index + middle) and hover over the top bar to pick colors
3. **Drawing Mode** - Point with ☝️ one finger (index only) and start drawing
4. **Eraser Mode** - Select the black icon for a thicc eraser
5. **Reset** - Click the sidebar button when your art needs a fresh start

<div align="center">
  <img src="https://media.giphy.com/media/l0HlNaQ6gWfllcjDO/giphy.gif" width="300" alt="Drawing GIF"/>
</div>

## 📁 Project Structure

```
virtual-paint-pro/
├── app.py                    # Main Streamlit application
├── HandTrackingModule.py     # Hand tracking logic (the brain)
├── Bar/                      # Color selection header images
│   ├── 1.png
│   ├── 2.png
│   └── ...
├── requirements.txt          # Python dependencies
├── packages.txt             # System dependencies
└── README.md                # You are here 👋
```

## 🐛 Known Issues

- Sometimes the hand tracking thinks your nose is a finger. I'm working on it. (JK)
- Drawing too fast might make the lines look like modern art (feature, not bug?)
- If it doesn't work, try turning it off and on again. Works 60% of the time, every time.

## 🤝 Contributing

Found a bug? Want to add rainbow colors? PRs are welcome! Just:

1. Fork it
2. Create your feature branch (`git checkout -b feature/rainbow-mode`)
3. Commit your changes (`git commit -am 'Add rainbow mode'`)
4. Push to the branch (`git push origin feature/rainbow-mode`)
5. Create a Pull Request

## 📜 License

MIT License - Feel free to use this for your next art exhibition or to impress your friends.

## 🙏 Acknowledgments

- **MediaPipe** - For making hand tracking actually work
- **Streamlit** - For making deployment stupidly simple
- **Coffee** - For making this project possible at 3 AM

---

<div align="center">
  Made with questionable life choices
  
  <img src="https://media.giphy.com/media/LmNwrBhejkK9EFP504/giphy.gif" width="200" alt="Bob Ross"/>
  
  *"There are no mistakes, just happy accidents" - Bob Ross probably*
</div>

## 🌟 Star This Repo!

If this saved you from buying an actual whiteboard, give it a ⭐!
