# Edenshore - APK Production Build

Welcome to the official APK build repository for **Edenshore** (Part of The Edencore Project).

## 📱 Purpose
This repository is the dedicated production line for compiling the Kivy source code into a standalone Android APK. It is kept separate from the main R&D repositories to ensure a clean build environment.

## 🚀 How it Works
This repository uses **GitHub Actions** and **Buildozer** to automatically compile the APK in the cloud.
* Every time code is pushed to the `main` branch, a new build is triggered.
* The final `.apk` file can be downloaded from the **Actions** tab.

## 📂 Structure
* `main.py` - The entry point for the Android app.
* `terrarium.py` - The core application logic.
* `brain.py`, `audio.py`, etc. - The Edencore engine modules.
* `assets/` & `dialogue/` - Nested folders containing media and text.
* `buildozer.spec` - The instruction manual for the cloud builder.

## 🧠 The Edencore Vision
Edencore is a safety layer that wraps AI in a governed, stable boundary so it behaves predictably, transparently, and always in alignment with human intent.

*(Managed by the Director)*