# GitHub Contribution Breakout 🎮

A beautiful, minimalist Breakout game that transforms your GitHub contribution graph into an interactive gaming experience.

<p align="center">
  <img src="assets/demo.gif" alt="GitHub Breakout Demo" width="600">
</p>

## ✨ Features

- **Seamless GitHub Integration**: Automatically fetches your contribution data from the past year
- **Beautiful Design**: Clean, minimalist interface inspired by Apple's design philosophy
- **Smooth Gameplay**: 60 FPS gameplay with responsive controls
- **Dynamic Difficulty**: Game speed increases as you progress
- **Dark/Light Mode**: Supports both themes with smooth transitions
- **Score Tracking**: Keep track of your high scores

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- GitHub account
- Personal Access Token (for API access)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/github-breakout.git
cd github-breakout
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory:
```bash
GITHUB_USERNAME=your_github_username
GITHUB_TOKEN=your_personal_access_token
```

4. Run the game:
```bash
python main.py
```

## 🎮 How to Play

- **Move Paddle**: Use ← → arrow keys or A/D keys
- **Launch Ball**: Press SPACE to start
- **Pause Game**: Press P
- **Toggle Theme**: Press T for dark/light mode
- **Quit**: Press ESC

## 📁 Project Structure

```
github-breakout/
│
├── main.py              # Entry point
├── game.py              # Main game logic
├── github_api.py        # GitHub API integration
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── README.md            # This file
│
├── assets/              # Game assets
│   ├── fonts/           # Custom fonts
│   └── sounds/          # Sound effects
│
└── utils/               # Utility modules
    ├── colors.py        # Color schemes
    └── effects.py       # Visual effects
```

## 🔧 Configuration

Edit `config.py` to customize:

- Window size and game speed
- Color schemes for different contribution levels
- Paddle and ball properties
- Sound effects volume

## 🎨 Design Philosophy

Following Steve Jobs' design principles:

- **Simplicity**: Clean interface with no unnecessary elements
- **Intuition**: Controls feel natural and responsive
- **Beauty**: Smooth animations and thoughtful color choices
- **Function**: Every element serves a purpose

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

Copyright © 2024 3S Holding OÜ, Tartu, Estonia  
All rights reserved.

Created by Prof. Shahab Anbarjafari

## 🙏 Acknowledgments

- Inspired by GitHub Breakout by Cyprien Guillemot
- GitHub API for contribution data
- The open-source community

---

<p align="center">Made with ❤️ in Estonia</p>