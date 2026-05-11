# Vachana-Crypt: AI-Powered Semantic Steganography

**Vachana-Crypt** is a high-end, sovereign cybersecurity tool that pioneered the concept of "Semantic Camouflage." By combining the mathematical robustness of **AES-256-GCM** with the linguistic intelligence of the **Sarvam-30B** model, it hides sensitive data within naturally flowing Hinglish (Hindi + English) literature.

![Project Preview](https://via.placeholder.com/1200x600.png?text=Vachana-Crypt+Premium+Dashboard) <!-- Replace with your actual screenshot -->

## 🌟 Key Features
- **Neural Camouflage:** Encrypted payloads are transformed into sophisticated, human-readable Hinglish poems or technical manifestos.
- **Local-First Security:** All encryption and decryption happen locally using your Master Password. Only non-reversible encrypted hashes are processed by the AI.
- **Sarvam-30B Integration:** Utilizes the state-of-the-art Sarvam AI "Brain" for high-fidelity linguistic generation optimized for the Indian context.
- **Glassmorphic UI:** A premium, dark-mode dashboard with real-time "Neural Pulse" animations.

## 🛠️ Tech Stack
- **Backend:** FastAPI (Python), Uvicorn, Cryptography.py, SarvamAI SDK.
- **Frontend:** React, Vite, Axios, Lucide Icons, Vanilla CSS (Glassmorphism).

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js & npm
- A [Sarvam AI API Key](https://www.sarvam.ai/)

### Setup
1. **Clone the Repository:**
   ```bash
   git clone <your-repo-url>
   cd "A.I Powered High End Cyber Security project"
   ```

2. **Backend Setup:**
   ```bash
   cd server
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```
   - Create a `.env` file in the `server` folder and add:
     ```bash
     SARVAM_API_KEY=your_api_key_here
     ```

3. **Frontend Setup:**
   ```bash
   cd ../client
   npm install
   npm run dev
   ```

## 📜 Usage
1. Open the dashboard at `http://localhost:5173`.
2. **Encrypt:** Enter your secret, set a password, and watch the AI generate a "Camouflage" poem.
3. **Decrypt:** Paste the poem and the password to extract the hidden truth.

## 🛡️ License
MIT License. Created for educational and professional showcasing purposes.
