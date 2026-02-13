# 🚀 Quick Start - GPT Integration

## 30-Second Setup

### Step 1: Add OpenAI API Key
Edit `.env` and add your key:
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### Step 2: Restart Backend
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Step 3: Chat with Predictions
```bash
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What does glioma mean?",
    "prediction_label": "Glioma Tumor",
    "confidence_score": 0.92
  }'
```

**Response:**
```json
{
  "response": "Based on the MRI analysis showing a glioma tumor...",
  "source": "gpt",
  "disclaimer": "MEDICAL DISCLAIMER: This AI system is for educational purposes only..."
}
```

---

## ✅ Verify Installation

Run the test suite:
```bash
python test_gpt_complete.py
```

Expected: `🎉 All tests passed! GPT integration is working correctly.`

---

## 📊 Response Sources

| Source | Meaning | When It Happens |
|--------|---------|-----------------|
| **gpt** | Using OpenAI GPT | API key valid, GPT responding |
| **fallback** | Using rule-based chatbot | No API key, API quota exceeded, network error |
| **error** | Error occurred but recovered | System error (rare) |

---

## 🎯 Use Cases

### 1. Simple Question (No Prediction)
```json
{
  "message": "What is an MRI?"
}
```
→ `source: "fallback"` (rule-based response)

### 2. Question with Glioma Finding
```json
{
  "message": "Is this serious?",
  "prediction_label": "Glioma Tumor",
  "confidence_score": 0.85
}
```
→ `source: "gpt"` (GPT-powered response with context)

### 3. Positive Result (No Tumor)
```json
{
  "message": "Is this a good result?",
  "prediction_label": "No Tumor",
  "confidence_score": 0.99
}
```
→ `source: "gpt"` (Reassuring, educated response)

---

## 🔒 Security

- ✅ No API keys in code
- ✅ No API keys logged
- ✅ Uses environment variables only
- ✅ Graceful error handling
- ✅ Medical safety guardrails
- ✅ Works without API key (fallback mode)

---

## 📱 Frontend Integration

The frontend can now pass prediction context:

```javascript
// JavaScript example
const response = await fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: userQuestion,
    prediction_label: predictionResult?.label,  // "Glioma Tumor", etc.
    confidence_score: predictionResult?.confidence  // 0.0-1.0
  })
});

const data = await response.json();
console.log(data.response);  // AI response
console.log(data.source);    // "gpt" or "fallback"
```

---

## 🛠️ Troubleshooting

### "GPT service not available"
→ Set `OPENAI_API_KEY` in `.env`

### "Insufficient quota" error
→ Check OpenAI billing at https://platform.openai.com/account/billing/overview

### Getting generic responses (no GPT)
→ This is normal without an API key. System uses rule-based chatbot as fallback.

### Backend not starting
→ Run `pip install -r requirements.txt`

---

## 📖 Full Documentation

For detailed information, see:
- **GPT_INTEGRATION.md** - Complete guide with examples
- **GPT_IMPLEMENTATION_COMPLETE.md** - Implementation details

---

## ✨ Features

✅ AI-powered intelligent responses
✅ MRI prediction context awareness  
✅ Automatic fallback (no crashes)
✅ Medical safety guardrails
✅ No hardcoded secrets
✅ Works without API key
✅ Complete error handling
✅ Production-ready

---

**Status**: ✅ Ready to use!
