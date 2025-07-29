# 🩺 HealthPilot Backend

**HealthPilot** is a mobile-first health application backend built with **Django** and **Docker Compose**. It powers intelligent features such as health article crawling, personalized symptom tracking, medication reminders, and AI-driven recommendations. Designed for scalability and user-centric care, HealthPilot aims to integrate decentralized data storage using **Smart contracts** in the near future.

---

## 📌 Table of Contents

- [📖 Overview](#overview)
- [⚙️ Tech Stack](#tech-stack)
- [✨ Key Features](#key-features)
- [📦 Setup Instructions](#setup-instructions)
- [🧠 AI & Recommendation Systems](#ai--recommendation-systems)
- [🔗 Blockchain Integration (Planned)](#blockchain-integration-planned)
- [📁 Project Structure](#project-structure)
- [🛡 Security & Privacy](#security--privacy)
- [🤝 Contributing](#contributing)
- [📄 License](#license)
- [🌐 Contact](#contact)

---

## 📖 Overview

The HealthPilot backend acts as the foundation for all health-related services provided by the mobile app. It crawls health content from reputable sources like the **World Health Organization (WHO)** and **Healthline**, while managing user data, health logs, medication routines, and recommendations.

This backend also supports:

- AI-powered article and remedi recommendations
- AI-Powered Assistant for any health related Issue and helps
- Real-Time Chat and call support with socket
- Real-time notifications and reminders
- Planned support for on-chain data storage (Smart Contract blockchain)
- Peer-to-peer health support via chat and community features

---

## ⚙️ Tech Stack

- **Backend Framework:** Django 4.x
- **Language:** Python 3.10+
- **Database:** PostgreSQL
- **Async Tasks:** Celery + Redis
- **Containerization:** Docker & Docker Compose
- **API Layer:** Django REST Framework (DRF)
- **Smart Contracts:** Cardano (Testnet – *Planned*)

---

## ✨ Key Features

### 📰 Article Recommendation System (AI-Powered)

- Crawls and recommends credible health information from sources like WHO, Healthline, and Wellness Mama.
- Uses AI to personalize recommendations based on user interaction and interest.
- Users can comment, reply, and interact with articles for community learning.

### 💊 Disease & Medication Recommendation AI

- Delivers personalized medication suggestions based on symptoms, history, and user feedback.
- Continuously learns and adapts using machine learning techniques.

### ⏰ Medication Reminders

- Sends real-time alerts to ensure users never miss a dose.
- Helps improve adherence to medication schedules and routines.

### 🧾 Symptom Tracking & Health Insights

- Logs and analyzes symptoms to detect patterns and trends over time.
- Enables users to make informed health decisions with visualized data.

### 📄 Health Reports for Doctors

- Auto-generates health summaries and trends for sharing with approved healthcare professionals.
- Ensures secure and customizable access controls.

### 🧬 Personalized Health Recommendations

- Provides lifestyle, medication, and exercise suggestions tailored to each user.
- Combines multiple data points and feedback loops to optimize accuracy.

### 👥 Similar Person Recommendation

- Recommends other users with similar health conditions for support and interaction.
- Fosters community-driven healing and learning.

### 💬 Community Chat & Peer Support

- Supports personal and group chat, voice and video calls.
- Enables file sharing, discussion groups, and real-time assistance.

### 🚨 Emergency Support Features

- Quick-access emergency contacts and service integrations for urgent health issues.

### 🤖 AI Assistant Bot

- In-app conversational bot trained on health data to answer user questions instantly.
- Available 24/7 for support and navigation.

---

# 📦 Setup Instructions
To run the backend of HealthPilot locally using Docker:

1. **Clone the Repository**

```bash
git clone https://github.com/your-org/healthpilot-backend.git
cd healthpilot-backend


2. **Configure Environment Variables**

Copy the sample environment file:

```bash
cp .env.example .env
```

Then open the `.env` file and configure the necessary values:

* `SECRET_KEY` – Django secret key
* `DATABASE_URL` – PostgreSQL connection string
* `REDIS_URL` – Redis server for Celery
* `DEBUG` – Set to `True` for development
* Other fields like email, API keys, etc., as required

3. **Build and Run with Docker**

```bash
docker-compose up --build
```

This will start:

* Django server (port 8000)
* PostgreSQL (port 5432)
* Redis (port 6379)

ℹ️ Run `docker ps` to verify all containers are active.

4. **Apply Migrations & Create Superuser**

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

Then access the Django admin at [http://localhost:8000/admin](http://localhost:8000/admin)

# 🧠 AI & Recommendation Systems

* **Article Crawler & Classifier:** Fetches content from WHO, Healthline, etc.
* **Disease Detection Module:** Uses symptom keywords to recommend possible conditions
* **User Health Profiling:** Stores user logs to personalize insights and alerts
* **Daily Reminders & Medication Scheduling:** Powered by Celery beat tasks

# 🔗 Blockchain Integration (Planned)

⚠️ This feature is currently in planning and not yet integrated.

* Users will be able to log immutable health records on the Cardano Testnet
* Smart contract interactions for health data verifiability and transparency
* Integration via Blockfrost API and Plutus smart contracts (future milestone)

# 📁 Project Structure

```
healthpilot-backend/
├── core/                   # Core Django app: user, health logs, etc.
├── recommender/            # AI recommendation logic
├── crawler/                # Article crawling and parsing
├── blockchain/             # Smart contract interaction (placeholder)
├── notifications/          # Email, reminders, scheduling logic
├── media/                  # Uploaded files
├── static/                 # Static files
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

# 🛡 Security & Privacy

* **Data Encryption:** User health data is encrypted at rest
* **OAuth2 Ready:** Optional integration for secure user authentication
* **Permissions:** Granular access control using DRF permission classes
* **GDPR-Compliant:** User consent and data removal APIs available

# 🤝 Contributing

We welcome contributions! To get started:

* Fork the repository
* Create a feature branch

```bash
git checkout -b feature/your-feature
```

* Commit and push your changes
* Open a pull request

Please follow the contribution guidelines before submitting.

# 📄 License

This project is licensed under the MIT License.
See the `LICENSE` file for details.

# 🌐 Contact

* 🌍 Website:
* 🐦 Twitter: [@healthpilot\_app](https://twitter.com/healthpilot_app)
* 📧 Email: [dev@healthpilot.app](mailto:dev@healthpilot.app)

```

Let me know if you want me to remove or add anything else!
```


And other variables relevant to external services (e.g., Twilio, Firebase)

3. Build and Run D
REDIS_URL=redis://redis:6379
...
