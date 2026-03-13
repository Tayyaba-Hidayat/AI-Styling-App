# ARIA — AI Chatbot (Streamlit Version)

A single-file AI chatbot powered by Claude, deployable for free on Streamlit Cloud.

## Files

```
streamlit-chatbot/
├── app.py                          # The entire app — one file!
├── requirements.txt                # Python dependencies
├── .gitignore                      # Keeps secrets out of GitHub
└── .streamlit/
    └── secrets.toml.example        # Copy to secrets.toml for local dev
```

---

## 🖥 Run Locally

### 1. Install dependencies
```bash
pip install streamlit anthropic
```

### 2. Add your API key
```bash
# Create the secrets file
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# Open secrets.toml and paste your Anthropic API key
# Get your key at: https://console.anthropic.com
```

### 3. Run the app
```bash
streamlit run app.py
```

Opens at **http://localhost:8501** ✅

---

## 🚀 Deploy FREE on Streamlit Cloud

### Step 1 — Push to GitHub
1. Create a new GitHub repository (can be public or private)
2. Upload these files:
   - `app.py`
   - `requirements.txt`
   - `.gitignore`
   - `.streamlit/` folder (WITHOUT secrets.toml — keep that local!)

### Step 2 — Deploy on Streamlit Cloud
1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repo, branch (`main`), and file (`app.py`)
5. Click **"Deploy"**

### Step 3 — Add your API key (IMPORTANT)
1. In Streamlit Cloud dashboard, open your app settings
2. Click **"Secrets"** in the left menu
3. Add this:
```toml
ANTHROPIC_API_KEY = "sk-ant-your-actual-key-here"
```
4. Save → your app restarts automatically ✅

Your app will be live at:
```
https://yourname-yourrepo-app-xxxx.streamlit.app
```

---

## Features
- 💬 Real-time streaming responses
- 🎭 4 AI modes: Assistant, Coder, Creative, Analyst
- 🗑 Clear conversation button
- ⚡ No backend server needed — just one Python file
- 🔒 API key stored securely in Streamlit Secrets

---

## Get your Anthropic API Key
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up / log in
3. Go to **API Keys** → **Create Key**
4. Copy and paste it into your secrets
