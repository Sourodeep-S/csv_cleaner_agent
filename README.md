# 🛠️ Mini Agent-Based Data Fixing System

This project is a lightweight, modular, agent-based pipeline for automatically **detecting**, **correcting**, and **enriching** messy customer data from a CSV file — with an optional interactive UI built using **Streamlit**.

---

## 📦 Features

✅ Agent-based design (detection, correction, enrichment)  
✅ Handles missing/malformed data, duplicates, and invalid values  
✅ Auto-correction using fuzzy matching  
✅ Enrichment logic based on inference (e.g. names from emails)  
✅ Clean, scrollable agent logs per session  
✅ Upload → Clean → Download flow via Web UI  
✅ Modular code structure for reusability and testing


---

## 🧪 How It Works

The system processes messy CSV files using a modular pipeline:

### 🔍 Detection Agent
- Flags missing values in `name`, `email`, `phone`, `country`
- Identifies malformed emails and phone numbers
- Detects invalid country names (against `valid_countries.txt`)
- Logs everything in `logs/detection_log.txt`

### 🛠 Correction Agent
- Removes duplicate rows
- Standardizes emails and names
- Corrects invalid countries using fuzzy matching
- Fixes invalid phones (replaces with `0000000000`)
- Logs corrections in `logs/correction_log.txt`

### ✨ Enrichment Agent
- Infers names from email addresses if missing
- Fills in placeholder values for missing emails/phones
- Logs enrichment steps in `logs/enrichment_log.txt`

---

## 🌐 Streamlit Web UI

Easily use the system via the included UI:

```bash
streamlit run ui_app.py
```

---

## UI Features:
📤 Upload a messy CSV

🚀 One-click agent pipeline

🧼 View cleaned data in browser

⬇ Download enriched output

📄 Scrollable logs per agent

⚠️ Logs are cleared automatically before each run to keep things clean.


