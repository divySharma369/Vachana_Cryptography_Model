import os
import json
import base64
import logging
import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- SDK CONFIGURATION ---
try:
    from sarvamai import SarvamAI
    logger.info("SarvamAI SDK loaded successfully.")
except ImportError:
    logger.warning("sarvamai SDK not found. Using professional fallback wrapper.")
    class SarvamAI:
        """
        Fallback wrapper to ensure compatibility with Sarvam AI API
        when the official SDK is not available.
        """
        def __init__(self, api_subscription_key):
            self.api_key = api_subscription_key
            self.url = "https://api.sarvam.ai/v1/chat/completions"

        class Chat:
            def __init__(self, parent):
                self.parent = parent

            def completions(self, messages, model="sarvam-30b", temperature=0.7):
                if not self.parent.api_key:
                    raise ValueError("SARVAM_API_KEY is missing. Please provide it in .env or main.py.")
                
                headers = {
                    "api-subscription-key": self.parent.api_key, # Correct header for Sarvam
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": model,
                    "messages": messages,
                    "temperature": temperature
                }
                logger.info(f"Dispatching request to Sarvam 30B...")
                response = requests.post(self.parent.url, json=payload, headers=headers)
                
                if response.status_code != 200:
                    error_data = response.json() if response.content else {"message": response.text}
                    logger.error(f"Sarvam API Error: {error_data}")
                    raise Exception(f"Sarvam API Error: {error_data.get('error', {}).get('message', response.text)}")
                
                return response.json()

        @property
        def chat(self):
            return self.Chat(self)

app = FastAPI(title="Vachana-Crypt AI Backend")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Client
# Priority: 1. Environment Variable, 2. Hardcoded (if user pastes it)
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY", "") 

if not SARVAM_API_KEY:
    logger.warning("SARVAM_API_KEY not detected in environment. System will require manual key injection.")

client = SarvamAI(api_subscription_key=SARVAM_API_KEY)

# --- MODELS ---
class EncryptRequest(BaseModel):
    message: str
    password: str

class DecryptRequest(BaseModel):
    camouflage_text: str
    password: str

# --- CRYPTO UTILS ---
def derive_key(password: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return kdf.derive(password.encode())

# --- ENDPOINTS ---

@app.post("/api/encrypt")
async def encrypt_and_camouflage(req: EncryptRequest):
    logger.info("Encryption request received.")
    try:
        # 1. Local AES-GCM Encryption
        salt = os.urandom(16)
        nonce = os.urandom(12)
        key = derive_key(req.password, salt)
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, req.message.encode(), None)
        
        # Combine salt + nonce + ciphertext for portability
        combined_payload = base64.b64encode(salt + nonce + ciphertext).decode('utf-8')
        logger.info("Local AES-256-GCM encryption complete.")

        # 2. Sarvam-30B Semantic Camouflage
        system_prompt = (
            "You are a 'Semantic Camouflage' agent for Vachana-Crypt. Your task is to hide a cryptographic payload "
            "within a natural-sounding, high-end technical or philosophical message. "
            "Use Hinglish (Hindi + English) to create a sense of Indian tech sovereignty. "
            "The message must sound sophisticated, perhaps like a verse or a security manifesto. "
            "CRITICAL: The payload string must be included exactly once, naturally woven into the text. "
            "Start your response with 'VACHANA:' and end it with ':SHASTRY'."
        )
        
        user_content = f"Payload: {combined_payload}\nTheme: Digital Dharma and Cybersecurity Sovereignty."
        
        response = client.chat.completions(messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ], model="sarvam-30b")

        # 3. Extract the content from the response
        # The official SDK returns an object, while our fallback returns a dictionary
        if hasattr(response, 'choices'):
            camouflage_text = response.choices[0].message.content
        else:
            camouflage_text = response['choices'][0]['message']['content']
            
        logger.info("Sarvam-30B camouflage generation successful.")

        return {
            "status": "success",
            "camouflage_text": camouflage_text,
            "raw_payload": combined_payload
        }
    except Exception as e:
        logger.error(f"Encryption Process Failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/decrypt")
async def extract_and_decrypt(req: DecryptRequest):
    logger.info("Decryption request received.")
    try:
        # 1. Extract the payload using more robust regex
        # We look for a base64 sequence that is likely our payload
        # Standard base64 with potential padding
        match = re.search(r'[A-Za-z0-9+/]{32,}=*', req.camouflage_text)
        if not match:
            logger.warning("Payload extraction failed: No valid pattern found.")
            raise HTTPException(status_code=400, detail="No cryptographic payload found in the text.")
        
        combined_payload = match.group(0)
        logger.info("Payload signature extracted.")
        
        try:
            data = base64.b64decode(combined_payload)
        except Exception:
            raise HTTPException(status_code=400, detail="Extracted payload is not a valid Base64 string.")

        if len(data) < 28: # Min size: salt(16) + nonce(12)
            raise HTTPException(status_code=400, detail="Extracted payload is too short or corrupted.")

        salt = data[:16]
        nonce = data[16:28]
        ciphertext = data[28:]
        
        # 2. Local Decryption
        key = derive_key(req.password, salt)
        aesgcm = AESGCM(key)
        decrypted_message = aesgcm.decrypt(nonce, ciphertext, None).decode('utf-8')
        
        logger.info("Decryption successful.")
        return {
            "status": "success",
            "message": decrypted_message
        }
    except Exception as e:
        logger.error(f"Decryption failed: {str(e)}")
        raise HTTPException(status_code=400, detail="Authentication failed: Incorrect password or corrupted payload.")

@app.get("/health")
async def health_check():
    return {"status": "operational", "engine": "Sarvam-30B"}

if __name__ == "__main__":
    import uvicorn
    # Use environment port if available (for cloud deployments)
    port = int(os.getenv("PORT", 8000))
    logger.info(f"Vachana-Crypt Backend starting on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
