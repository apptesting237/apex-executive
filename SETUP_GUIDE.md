# Apex Executive — Complete End-to-End Free Account Setup Manual

This guide walks you through setting up every account on the 100% free-tier stack ($0/month).

---

### Step 1: GitHub (Code & Automated CI/CD Pipeline)
1. Go to https://github.com/ and create a free account if you don't have one.
2. Click **New Repository**, name it `apex-executive`, and set visibility to **Private**.
3. Push the unzipped codebase to your repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of Apex Executive Enterprise OS"
   git remote add origin https://github.com/YOUR_USERNAME/apex-executive.git
   git push -u origin main
   ```

---

### Step 2: Google AI Studio (Free LLM Intelligence — Zero Credit Card Required)
1. Go to https://aistudio.google.com/ and sign in with your Google account.
2. Click **Get API key** in the top left navigation.
3. Click **Create API key in new project**.
4. Copy your key (`AIzaSy...`).
   - Free Tier Quota: 15 requests per minute (RPM) and 1,500 requests per day on Gemini 1.5 Flash.

*(Optional Alternative: https://groq.com/ for free Llama 3.3 70B inference)*

---

### Step 3: Supabase (Free Database & Vector Memory "Brain")
1. Go to https://supabase.com/ and click **Start your project** (Sign in with GitHub).
2. Create an organization and click **New Project** (Choose a region close to you).
3. Set a database password and click **Create new project**.
4. Once created, go to **Project Settings -> API**:
   - Copy **Project URL** (`https://xyz.supabase.co`).
   - Copy **anon / public key** (`eyJ...`).
5. Enable `pgvector` in **Database -> Extensions**:
   - Search for `vector` and toggle it **ON**.

---

### Step 4: Railway or Render (Free 24/7 Python Backend Hosting)

#### Option A: Railway ($5 Monthly Free Credit)
1. Go to https://railway.app/ and sign in with GitHub.
2. Click **New Project -> Deploy from GitHub repo**.
3. Select your `apex-executive` repo and choose the `/backend` directory.
4. Click **Variables** and add:
   - `GEMINI_API_KEY`: Your key from Step 2
   - `SUPABASE_URL`: Your URL from Step 3
   - `SUPABASE_KEY`: Your key from Step 3
   - `CEO_SECRET_TOKEN`: Any secure password
5. Railway automatically detects the `Dockerfile` and deploys your server.

#### Option B: Render (750 Free Hours/Month)
1. Go to https://render.com/ and click **New + -> Web Service**.
2. Connect your GitHub repo, set the root directory to `backend`, runtime to `Python 3`, and start command to `uvicorn main:app --host 0.0.0.0 --port 10000`.
3. Add your environment variables under the **Environment** tab.

---

### Step 5: Mobile App on Your Phone (Expo Go — $0 App Store Fees)
1. Install **Node.js 20+** on your laptop.
2. Inside the `/mobile` folder, run:
   ```bash
   npm install
   npx expo start
   ```
3. A QR code will appear in your terminal.
4. Install **Expo Go** from the iOS App Store or Google Play Store on your physical phone.
5. Scan the QR code with your phone camera (iOS) or the Expo Go app (Android).
6. The Apex Executive mobile app loads immediately on your phone!
