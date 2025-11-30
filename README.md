# 🌍 Multi-Agent Travel Planner with Google ADK

A production-ready multi-agent travel planning system built with **Google Agent Development Kit (ADK)** and **Agent2Agent (A2A) Protocol**. Plan complete trips with parallel specialist agents for flights, accommodations, and activities.

## 📋 Project Overview

This project demonstrates advanced multi-agent system architecture using Google's latest ADK framework. The system orchestrates 4 specialized agents:

- **Flights Agent** (Port 8001) - Searches and recommends flight options
- **Stays Agent** (Port 8002) - Finds accommodation options  
- **Activities Agent** (Port 8003) - Suggests attractions and experiences
- **Coordinator Agent** (Port 8000) - Orchestrates all specialists and synthesizes results

### ✨ Key Features

- ✅ **Parallel Execution** - All agents query simultaneously for faster results
- ✅ **A2A Protocol** - Standard Google inter-agent communication via HTTP
- ✅ **Real Pricing** - Realistic Indian rupee costs for flights, hotels, activities
- ✅ **Multiple Options** - Budget and premium itinerary choices
- ✅ **Day-by-Day Schedule** - Detailed timing for each activity
- ✅ **Cost Breakdown** - Complete financial analysis
- ✅ **Smart Ranking** - Recommendations with pros/cons analysis
- ✅ **Web Interface** - Interactive HTML UI for easy testing
- ✅ **Production Ready** - Fully tested and documented

---

## 🏗️ Architecture

```
┌─────────────────────────────────┐
│   Web Browser (127.0.0.1:8000)  │
│   HTML Interface                │
└────────────────┬────────────────┘
                 │ HTTP POST
      ┌──────────▼──────────┐
      │  Coordinator Agent  │
      │  (Port 8000)        │
      └──────────┬──────────┘
           ┌─────┼─────┐
           │     │     │ (Parallel)
      ┌────▼──┐ ┌─────▼──┐ ┌────▼──┐
      │Flights│ │ Stays  │ │Activity│
      │Agent  │ │ Agent  │ │ Agent  │
      │(8001) │ │(8002)  │ │(8003) │
      └────┬──┘ └─────┬──┘ └────┬──┘
           │         │         │
           └─────────┼─────────┘
                     │ JSON
           ┌─────────▼──────────┐
           │ Synthesize Results │
           │ Create Itinerary   │
           └─────────┬──────────┘
                     │ JSON Response
           ┌─────────▼──────────┐
           │ Display in Browser │
           └────────────────────┘
```

---

## 📦 Project Structure

```
travel-planner/
│   ├── flights_agent/
│   │   ├── __init__.py
│   │   └── main.py                 # Flights specialist agent
│   ├── stays_agent/
│   │   ├── __init__.py
│   │   └── main.py                 # Stays specialist agent
│   └── activities_agent/
│       ├── __init__.py
│       └── main.py                 # Activities specialist agent
├── __init__.py
├── agent.py
├── .env
└── README.md

```

---

## 🚀 Quick Start (5 Minutes)

### **1. Clone Repository**

```bash
git clone https://github.com/ManashGiri/ADK-Capstone-Project.git
cd ADK-Capstone-Project
```

### **2. Create Virtual Environment**

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### **3. Create .env File**

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your Google API key
nano .env
# OR
code .env
```

**.env file content:**

```
GOOGLE_API_KEY=your-actual-api-key-from-aistudio.google.com
GOOGLE_GENAI_USE_VERTEXAI=0
```

**Get your free API key:**
1. Visit: https://aistudio.google.com
2. Click "Create API key"
3. Copy and paste into .env

### **4. Install Dependencies**

```bash
pip install google-adk
```

### **5. Run Travel Planner Agent**

```bash
python travel_planner/agent.py
```

### **6. Run Web Interface**

**In a new terminal:**

```bash
# Make sure .venv is activated
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# Run the web server
adk web
```

**Expected output:**
```
🌍 Travel Planner Web Interface
📍 Server running at: http://127.0.0.1:8000
✨ Open your browser and visit: http://127.0.0.1:8000
```

### **7. Test the Interface**

Open your browser and go to: **http://127.0.0.1:8000**

## 📝 Test Prompts

### **Test 1: Tokyo Adventure (Full Featured)**

```
Plan a 5-day trip from Mumbai to Tokyo in March 2026. 
Total budget: ₹1,50,000 (including flights, hotel, food, transport, activities)
Interests: anime, gaming, electronics shopping, Japanese street food
Hotel preference: 3-4 star near train stations
Give me 2 options (budget and premium) with day-by-day schedule and INR cost breakdown.
```

### **Test 2: Bangkok Budget Trip (Quick Test)**

```
Plan 3-day trip Delhi to Bangkok February 2026
Budget: ₹80,000 total
Focus: street food, temples, local markets
Give 2 itinerary options with costs
```

### **Test 3: Singapore Premium (Luxury Test)**

```
Plan 7-day luxury trip Bangalore to Singapore + Kuala Lumpur
Budget: ₹4,00,000
Interests: shopping, fine dining, adventure activities, cultural sites
Include high-end hotel recommendations and premium experiences
```

---

## 💡 Capstone Project Highlights

This project demonstrates:

- ✅ **Multi-Agent Architecture** - Specialist pattern with orchestration
- ✅ **Google ADK Framework** - Latest agent development tools
- ✅ **A2A Protocol** - Inter-agent HTTP communication
- ✅ **Parallel Processing** - Concurrent specialist queries
- ✅ **REST API Design** - FastAPI with OpenAPI docs
- ✅ **System Integration** - Complex workflow coordination
- ✅ **Error Handling** - Resilience and graceful degradation
- ✅ **Web Interface** - Interactive user experience
- ✅ **Production Ready** - Complete documentation and deployment

---

## 🤝 Contributors

**Manash Giri**
**Omkar Vaidya**
**Anchal Vaishya**


## ⭐ If you found this helpful, please star the repository!

**Happy trip planning!** 🌍✈️🎉
