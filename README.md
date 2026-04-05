# Display-Ultra-calibration

# 🖥️ Cachy Display Ultra

**Cachy Display Ultra** is a lightweight, Python-based GUI tool designed to provide Linux users (specifically on **CachyOS** and **Arch Linux**) with granular control over their display hardware. 

Developed through a collaborative process between a Linux enthusiast and **Artificial Intelligence**, this project bridges the gap between raw terminal commands and a seamless desktop experience. It allows for real-time adjustments of brightness, RGB gamma channels, and color saturation, ensuring your screen looks exactly how you want it from the moment you log in.

---

### ✨ Features

* **AI-Assisted Development:** Built using modern AI collaboration techniques to ensure clean and efficient code.
* **Granular Hardware Control:** Direct integration with `xrandr` for brightness and RGB gamma tuning.
* **Vibrant Colors:** Built-in saturation control via `vibrant-cli`.
* **Custom Profiles:** Quick-switch between presets like *AMOLED Deep*, *OLED Vivid*, and *Blue Light Filter*.
* **Zero-Effort Persistence:** Automatically applies your last saved configuration on system boot via a dedicated background script.
* **Modern GTK3 Interface:** A clean, semi-transparent UI with custom CSS styling and a dedicated "About" section.

---

### 🛠️ Technical Stack

* **Language:** Python 3
* **UI Toolkit:** GTK3 (PyGObject)
* **Backend Utilities:** `xrandr`, `vibrant-cli`, `JSON` for config management.
* **Packaging:** Arch Linux PKGBUILD system for easy installation and autostart integration.

---

### 🚀 How it Works

The project is split into two main components:

1.  **`main.py`**: The visual command center where you tweak and save your settings.
2.  **`apply_display.py`**: A lightweight "invisible" script that runs during the desktop environment (XFCE/GNOME/KDE) login process to restore your hardware settings instantly.

---

### 🔧 Installation (Arch-based)

1.  **Clone** this repository:
    ```bash
    git clone [https://github.com/zhartriad/Display-Ultra-calibration.git](https://github.com/zhartriad/Display-Ultra-calibration.git)
    cd Display-Ultra-calibration
    ```
2.  **Ensure** you have the dependencies installed: 
    `python-gobject`, `gtk3`, `libvibrant`, and `xorg-xrandr`.
3.  **Build and install** the package:
    ```bash
    makepkg -fsi
    ```
4.  **Launch** "Cachy Display Ultra" from your application menu, set your profile, and click **"Save as Default"**.

---

> *Created with a focus on performance, aesthetics, and the power of AI-assisted open-source development.*
