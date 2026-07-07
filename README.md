# 📖 Churn Detection — Classification Project

A bank customer churn prediction system: a trained ML model served through a **FastAPI** backend, with a **Streamlit** dashboard ("Churn Ledger") for interactive scoring, batch predictions, and portfolio analytics.

---

## 🔗 Live Demo

| Component | URL |
|---|---|
| **API (FastAPI, on Hugging Face Spaces)** | https://eyadzz-churn-live.hf.space/ |
| **Dashboard (Streamlit)** | https://churnlive-6mnfachkcjvec7gfaqhfjb.streamlit.app/ |

> ⚠️ **Security note:** the `X-API-Key` below is a **demo key** shared for evaluation purposes only. If this repository is public, rotate the key (set a new `SECRET_KEY_TOKEN` in your Hugging Face Space secrets) so this value stops working. Never rely on a key that has appeared in a public README for anything beyond a quick demo.

```
Demo X-API-Key: c0c2d9d05029aed5d5174ff5ff8e6d88
```

---

## 🧭 Project Overview

The project predicts whether a bank customer is likely to **churn** (leave the bank), based on the classic `Churn_Modelling.csv` dataset (~10,000 customers). It covers the full pipeline:

1. **EDA & preprocessing** (notebook) — cleaning, feature selection, encoding, scaling
2. **Imbalance handling** — class weighting and SMOTE oversampling (churn is ~20% of customers)
3. **Modeling** — Logistic Regression baseline → tuned **Random Forest** and **XGBoost**
4. **Serving** — a FastAPI service exposing both tuned models behind an API key
5. **Interface** — a Streamlit dashboard that calls the API for single-customer scoring, batch scoring, and portfolio/model analytics

---

## 🏗️ Architecture

``` bash
┌─────────────────────┐        HTTPS + X-API-Key           ┌───────────────────────┐
│   Streamlit Cloud   │ ───────────────────────────────▶ │  Hugging Face Spaces  │
│   streamlit_app.py  │◀───────────────────────────────  │  FastAPI (main.py)    │
│   "Churn Ledger"    │        JSON prediction            │  + Docker             │
└─────────────────────┘                                    └──────────┬────────────┘
                                                                      │
                                                          ┌───────────▼────────────┐
                                                          │  models/*.pkl          │
                                                          │  preprocessor,         │
                                                          │  forest_tuned,         │
                                                          │  xgb-tuned             │
                                                          └────────────────────────┘
```

--- 

## 📁 Repository Structure

``` bash
churn_live/
├── main.py                    # FastAPI app & routes
├── requirements.txt           # Backend dependencies
├── Dockerfile                 # Container spec for Hugging Face Spaces
├── streamlit_app.py           # Streamlit dashboard
├── requirements_streamlit.txt # Dashboard dependencies
├── .streamlit/
│   └── config.toml            # Dashboard theme
├── utils/
│   ├── __init__.py
│   ├── config.py              # Env vars + model loading
│   ├── CustomerData.py        # Pydantic request schema
│   └── inference.py           # Prediction logic
├── models/
│   ├── preprocessor.pkl
│   ├── forest_tuned.pkl
│   └── xgb-tuned.pkl
├── notebooks/
│   └── notebook.ipynb          # Full training/EDA workflow
└── README.md
```

---

## ⚙️ API Reference

Base URL: `https://eyadzz-churn-live.hf.space`

All prediction endpoints require an `X-API-Key` header.

### `GET /`
Health check.
```json
{ "Message": "Welcome To My Churn-Detection API v1.0" }
```

### `POST /predict/forest`
### `POST /predict/xgboost`

**Headers**
```
X-API-Key: <your-key>
Content-Type: application/json
```

**Body**
```json
{
  "CreditScore": 650,
  "Geography": "France",
  "Gender": "Male",
  "Age": 38,
  "Tenure": 5,
  "Balance": 75000.0,
  "NumOfProducts": 1,
  "HasCrCard": 1,
  "IsActiveMember": 1,
  "EstimatedSalary": 100000.0
}
```

| Field | Type | Constraints |
|---|---|---|
| `CreditScore` | int | — |
| `Geography` | string | `France`, `Spain`, `Germany` |
| `Gender` | string | `Male`, `Female` |
| `Age` | int | 18–100 |
| `Tenure` | int | 0–10 |
| `Balance` | float | ≥ 0 |
| `NumOfProducts` | int | 1–4 |
| `HasCrCard` | int | 0 or 1 |
| `IsActiveMember` | int | 0 or 1 |
| `EstimatedSalary` | float | ≥ 0 |

**Response**
```json
{
  "Churn_Prediction": false,
  "Churn_Probability": 0.258
}
```

**Example (curl)**
```bash
curl -X POST "https://eyadzz-churn-live.hf.space/predict/forest" \
  -H "X-API-Key: c0c2d9d05029aed5d5174ff5ff8e6d88" \
  -H "Content-Type: application/json" \
  -d '{
        "CreditScore": 650, "Geography": "France", "Gender": "Male",
        "Age": 38, "Tenure": 5, "Balance": 75000.0,
        "NumOfProducts": 1, "HasCrCard": 1, "IsActiveMember": 1,
        "EstimatedSalary": 100000.0
      }'
```

Interactive docs (Swagger UI) are available at `/docs` on the API base URL.

---

## 📊 Dashboard Features ("Churn Ledger")

- **Portfolio Overview** — dataset-level KPIs, geography/gender breakdowns, churn rate
- **Score a Customer** — single-customer form with a live risk gauge and top model drivers
- **Batch Scoring** — upload a CSV of customers, score them all, download results
- **Model Insights** — the full model development journey, a leaderboard of every configuration tried, and feature importance

---

## 🔐 Environment Variables

The API reads its configuration from a `.env` file via `utils/config.py`. Copy the template and fill in your own values:

```bash
cp .env.example .env
```

**`.env.example`**
```
APP_NAME="Churn-Detection"
VERSION="1.0"
SECRET_KEY_TOKEN="your-secret-key-here"
```

| Variable | Used for |
|---|---|
| `APP_NAME` | App title shown in FastAPI docs and the `/` welcome message |
| `VERSION` | API version shown in FastAPI docs and the `/` welcome message |
| `SECRET_KEY_TOKEN` | The value every request must send in the `X-API-Key` header to hit `/predict/*` |

`.env` is already listed in `.gitignore`, so it's never committed. When deploying to **Hugging Face Spaces**, don't upload a `.env` file at all — set these same three variables under **Settings → Variables and secrets** on the Space instead; the app reads them as normal environment variables either way.

> Tip: double-check `.env.example` in your repo — as currently written it has a stray `==` on the `VERSION` line and no value after `SECRET_KEY_TOKEN =`. Fix it to match the block above so teammates can copy it directly.

--- 

## 🐳 Docker

The `Dockerfile` builds the exact environment used in production on Hugging Face Spaces, so you can test it locally before pushing:

```bash
docker build -t churn-api .
docker run --rm --env-file .env -p 8000:7860 churn-api
```

- The container listens on **port 7860** (required by Hugging Face Spaces) — the command above maps it to `8000` on your machine so it matches the "Running Locally" instructions below.
- `--env-file .env` passes `APP_NAME`, `VERSION`, and `SECRET_KEY_TOKEN` into the container; make sure `.env` exists first (see above).
- Once running, the API behaves identically to the hosted version: `http://localhost:8000/docs` for Swagger UI, `http://localhost:8000/predict/forest` etc.

On Hugging Face Spaces, this same `Dockerfile` is picked up automatically on every push — no extra configuration needed beyond the repository secrets.

---

## 🖥️ Running Locally

### 1. Backend (FastAPI)
```bash
git clone <your-repo-url>
cd churn_live
pip install -r requirements.txt
cp .env.example .env   # fill in APP_NAME, VERSION, SECRET_KEY_TOKEN
uvicorn main:app --reload
```
API available at `http://localhost:8000` (docs at `/docs`).

> Prefer containers? See the **🐳 Docker** section above for the exact same setup running in Docker.

### 2. Dashboard (Streamlit)
```bash
pip install -r requirements_streamlit.txt
streamlit run streamlit_app.py
```
Open the sidebar and set:
- **API base URL** → `http://localhost:8000` (or the deployed URL above)
- **X-API-Key** → the same value as `SECRET_KEY_TOKEN`

---

## ☁️ Deployment

| Component | Platform | Notes |
|---|---|---|
| API | Hugging Face Spaces (Docker SDK) | Free tier, sleeps after inactivity (~30–60s cold start) |
| Dashboard | Streamlit Community Cloud | Free tier |

Environment variables (`APP_NAME`, `VERSION`, `SECRET_KEY_TOKEN`) are set as **repository secrets** on the Space — never committed to the repo.

--- =

## 🧠 Model Performance

| Model | Configuration | Test F1 |
|---|---|---|
| Logistic Regression | baseline | 0.375 |
| Logistic Regression | class-weighted / SMOTE | ~0.50 |
| Random Forest | class-weighted / SMOTE | 0.57 – 0.59 |
| **Random Forest** | **tuned (GridSearchCV)** | **0.623** ⭐ |
| XGBoost | base | 0.595 |
| XGBoost | tuned (RandomizedSearchCV) | 0.609 |

Both tuned models are deployed in production. Random Forest currently has the best test-set F1; XGBoost is offered as an alternative for comparison.

**Top predictive features (Random Forest):** `Age`, `NumOfProducts`, `Balance`, `IsActiveMember`, `Geography`.

---

## 🛠️ Tech Stack

- **ML:** scikit-learn, XGBoost, imbalanced-learn (SMOTE)
- **API:** FastAPI, Uvicorn, Pydantic
- **Dashboard:** Streamlit, Plotly, Pandas
- **Deployment:** Docker, Hugging Face Spaces, Streamlit Community Cloud