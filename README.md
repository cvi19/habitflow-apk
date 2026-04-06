# HabitFlow APK — Build Guide 🤖

This folder contains everything needed to build a **real Android APK** using Python + Buildozer.

---

## 📁 Project Structure

```
habitflow-apk/
├── main.py          ← Python entry point (Kivy + Android WebView)
├── buildozer.spec   ← Build configuration
├── assets/
│   └── index.html   ← Complete HabitFlow app (HTML/CSS/JS)
└── README.md        ← This file
```

---

## 🛠️ Requirements

You need a **Linux machine** (or WSL2 on Windows) with:

| Tool | Install |
|------|---------|
| Python 3.10+ | `sudo apt install python3` |
| pip | `sudo apt install python3-pip` |
| Git | `sudo apt install git` |
| Java JDK 17 | `sudo apt install openjdk-17-jdk` |
| Buildozer | `pip install buildozer` |
| Cython | `pip install cython` |
| Build tools | `sudo apt install build-essential zip unzip` |

> **Windows users:** Use WSL2 (Ubuntu) — works perfectly.
> **macOS:** Buildozer does not fully support macOS for Android builds. Use a Linux VM or GitHub Actions (see below).

---

## 🚀 Build Steps

### Step 1 — Install dependencies

```bash
# System packages
sudo apt update
sudo apt install -y python3 python3-pip git zip unzip openjdk-17-jdk \
  build-essential libssl-dev libffi-dev libsqlite3-dev \
  autoconf libtool pkg-config zlib1g-dev

# Python tools
pip install buildozer cython
```

### Step 2 — Navigate to the project folder

```bash
cd habitflow-apk
```

### Step 3 — Build the debug APK

```bash
buildozer android debug
```

⏳ First build takes **15–30 minutes** — it downloads the Android SDK, NDK, and compiles everything.
Subsequent builds are much faster (2–3 min).

### Step 4 — Find your APK

```bash
ls bin/
# → habitflow-1.0.0-arm64-v8a-debug.apk
```

### Step 5 — Install on your phone

**Option A — ADB (cable):**
```bash
buildozer android debug deploy run
```

**Option B — Copy manually:**
Copy `bin/habitflow-*.apk` to your phone → open it → tap Install.
(Enable "Install from unknown sources" in Android Settings first.)

---

## 🌐 Build on GitHub Actions (free, no Linux needed)

Create `.github/workflows/build.yml` in your repo:

```yaml
name: Build APK
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y openjdk-17-jdk build-essential zip unzip
          pip install buildozer cython
      - name: Build APK
        run: |
          cd habitflow-apk
          buildozer android debug
      - name: Upload APK
        uses: actions/upload-artifact@v3
        with:
          name: HabitFlow-APK
          path: habitflow-apk/bin/*.apk
```

Push to GitHub → Actions tab → download APK from Artifacts. **Completely free.**

---

## 📱 Install APK on Android

1. Transfer the `.apk` file to your phone (WhatsApp, Google Drive, USB, etc.)
2. Open your phone's **Settings → Security** (or Privacy)
3. Enable **"Install Unknown Apps"** or **"Unknown Sources"**
4. Open the APK file → tap **Install**
5. Launch **HabitFlow** from your home screen 🎉

---

## 💾 Data Storage

The APK uses Android's **localStorage** via the WebView's DOM storage — data persists across app restarts automatically, stored securely on the device. No internet required.

---

## 🐛 Troubleshooting

**Build fails with "SDK license not accepted":**
```bash
yes | ~/.buildozer/android/platform/android-sdk/tools/bin/sdkmanager --licenses
```

**Out of memory during build:**
```bash
export GRADLE_OPTS="-Xmx2048m"
buildozer android debug
```

**"minSdkVersion" error:**
Edit `buildozer.spec` → set `android.minapi = 24`

**App crashes on launch:**
Run `buildozer android debug deploy run logcat` to see the logs.
