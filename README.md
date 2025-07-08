# 🌍 DateCompass

**DateCompass** is a smart web app that uses Reddit community wisdom and OpenAI's language models to recommend unique date spots in any city. Whether you're in Berlin, New York, or Tokyo — discover curated ideas for your next romantic outing.

---

## ✨ Features

- 🔍 **Search by city** to find top-rated date spots from real Reddit posts  
- 🤖 **AI-curated suggestions** using OpenAI's GPT-4  
- 💬 Clear, charming descriptions and reasons why the spot is perfect for a date  
- 🌐 Stylish and responsive **frontend interface**  
- 🚀 FastAPI backend with OpenAI + Reddit API integration  

---

## 🛠️ Tech Stack

| Layer     | Technology            |
|-----------|------------------------|
| Frontend  | HTML, CSS, JavaScript  |
| Backend   | Python, FastAPI        |
| APIs      | Reddit API, OpenAI GPT-4 |
| Env Mgmt  | python-dotenv          |
| CORS      | FastAPI CORS middleware |
| Hosting   | Localhost (for now)    |

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/datecompass.git
cd datecompass
```

### 2. Set up environment variables

Create a `.env` file in the project root and add your API keys:

```env
OPENAI_API_KEY=your_openai_api_key
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
```

---

### 3. Install dependencies

We recommend using a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `requirements.txt` file containing:

```txt
fastapi
uvicorn
httpx
openai
python-dotenv
```

---

### 4. Run the backend

Start the FastAPI server with:

```bash
uvicorn main:app --reload
```

By default, the server runs on `http://localhost:8000`.

---

### 5. Open the frontend

Simply open the `index.html` file in your browser to access the app.  
You can also serve it using:

```bash
python -m http.server
```

---

## 🧪 API Endpoints

### `GET /api/search?query=CityName`

Searches for city-specific date spot recommendations.

**Example Response:**

```json
{
  "recommendations": [
    {
      "name": "Skylight",
      "description": "Rooftop bar with city views (££)",
      "reason": "Perfect for sunset drinks"
    }
  ],
  "postCount": 10
}
```

---

### `GET /api/health`

Health check endpoint.

**Example Response:**

```json
{
  "status": "ok",
  "timestamp": "2025-04-09T18:30:00"
}
```

---

## 💡 Example Usage

Try queries like:

- `Berlin`
- `London`
- `New York`
- `Tokyo`

And receive curated suggestions like:

> 🍷 **The Winery**: Intimate cellar with tasting menu (£££) | Great for quiet, cozy conversations

---

## 🙌 Credits

- 💬 **Reddit** – Community-based recommendations  
- 🤖 **OpenAI GPT-4** – AI-powered insights  
- ✨ **You** – For bringing this project to life

---

## 📄 License

This project is licensed under the **MIT License**.  
Feel free to build, modify, and share it 🚀
