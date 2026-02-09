# 📦 Customer Support Automation Chatbot

## 📌 Overview

This project implements a **multilingual (Slovak + English) customer support chatbot** designed for automated email and message classification, response handling, and escalation.

The system is intended as a **production-ready foundation** for customer support automation, combining modern NLP techniques with strict business and safety rules.

### Core Capabilities

- Semantic embedding-based intent classification
- Business-rule enforcement
- External API integration
- Conversation state management
- Escalation logic
- Safety and risk constraints

---

## 🧠 Why This Approach?

The chatbot is built using **semantic embeddings** instead of traditional keyword matching.

### Advantages

- ✅ Supports both Slovak and English
- ✅ Captures semantic meaning instead of exact phrasing
- ✅ Easily extendable and scalable
- ✅ No labeled training dataset required
- ✅ Works well in low-data environments

Unlike keyword-based systems, embedding similarity enables intent recognition even when users phrase requests differently.

---

## 🗂 Intent Categories

Intent categories were designed based on:

- Dataset frequency
- Business impact
- Risk level
- Automation feasibility

### Implemented Categories

- **Order Status**
- **Order Cancel**
- **Order Modify**
- **Return / Complaint**
- **Product Question**
- **Store / Delivery / Availability**
- **Cooperation / Partnership**

### Design Principle

Categories reflect **business logic impact**, not only linguistic similarity.

> Example:  
> “Order Cancel” and “Order Modify” are semantically similar,  
> but their operational and financial consequences are completely different.

---

## ⚠️ Identified Edge Cases & Solutions

### 1. Cancellation Without Order Number

**Example:**

> Chcem zrušiť objednávku

**Problem:**  
Order number is missing.

**Solution:**

- The bot asks for the order number
- Conversation state is stored
- Cancellation continues once the number is provided

**Implementation Concept:**

```python
pending_action = "cancel_order"
```
## 🔁 2. Multi-Turn Context Handling

**Problem:**  
The second message contains only an order number and may be misclassified as a standalone request.

**Solution:**  
Conversation state management is applied to preserve context across multiple turns.

**Tracked states:**

- `cancel_order`
- `confirm_escalation`

---

## 🔌 3. API Error Handling

The system explicitly handles the following API scenarios:

- `ORDER_NOT_FOUND`
- `ORDER_NOT_CANCELLABLE`
- API technical failure
- Missing configuration

**On technical failure, the chatbot does not reply to the customer and instead generates a system escalation:**

```text
SYSTEM MESSAGE FOR CC AGENT
Reason: technical_failure
```

## ⚖️ 4. Legal Threat Detection

If a message contains any of the following keywords:

- súd  
- právnik  
- SOI  
- ochrana spotrebiteľa  

### Behavior

- ❌ The bot does **NOT** respond directly to the customer  
- ✅ The system generates an escalation for a human agent  

```text
SYSTEM MESSAGE FOR CC AGENT
Reason: legal_issue
```
This ensures legal risk mitigation and prevents automated responses in sensitive situations.

---

## 🩺 5. Dosage / Medical Advice Protection

The chatbot **never provides dosage or medical instructions**.

If dosage-related or medical advisory content is detected:

- The user is redirected to a nutrition specialist or a medical professional

This rule ensures **legal, ethical, and regulatory compliance**.

---

## 😠 6. Angry Message Handling

If excessive uppercase usage or an aggressive tone is detected:

- The bot adds a calming and empathetic prefix to its response

**Example:**

> Rozumiem, že situácia môže byť nepríjemná...

This approach helps de-escalate emotionally charged conversations.

---

## 🚫 7. Spam Filtering

An external spam detection module is applied **before intent classification**.

```python
from spam_filter import is_spam
```
Spam messages are filtered early in the processing pipeline to avoid unnecessary computation and false classifications.

## 🔄 Possible Improvements

With additional development time, the following enhancements could be implemented:

### 1. Confidence Threshold

Introduce a fallback mechanism for low-confidence intent predictions:

```python
if score < 0.60:
    escalate_to_agent()
```

This reduces the risk of incorrect automation and improves reliability.

---

## 2. Custom Classifier

Replace the prototype similarity approach with a more robust model:

- Fine-tuned transformer-based classifier
- Supervised learning on a labeled dataset

This would significantly improve classification accuracy and consistency.

---

## 3. Structured Logging

Replace `print()` statements with structured logging to:

- Store conversation history
- Log API calls
- Track escalation reasons

This enables effective monitoring, debugging, and performance evaluation.

---

## 4. CRM Integration

Instead of printing system messages:

- Automatically create CRM tickets
- Store escalation reason
- Attach the original customer message

This allows seamless handoff to human agents and improves operational efficiency.

---

## 5. Advanced Intent Detection

Implement a hybrid intent detection approach combining:

- Semantic embeddings
- Rule-based reinforcement
- Margin-based ambiguity detection

This improves intent robustness, especially in borderline or ambiguous cases.

---

## 6. User Interface

Possible UI implementations include:

- Tkinter desktop application
- Streamlit web interface
- Chat-style web UI

These options enable both internal tooling and customer-facing deployments.

---

## 🏗 Production Requirements

For real-world deployment, the system would require:

### 1. Secure Infrastructure

- Secure API key management
- Rate limiting
- Monitoring and alerting
- Error tracking

---

### 2. CRM / Order System Integration

- Real order database
- Live order status tracking
- Customer identity verification

---

### 3. Advanced NLP Layer

- Named Entity Recognition (NER)
- Sentiment analysis
- Cross-session context persistence

---

### 4. Monitoring & Metrics

- Classification accuracy tracking
- Escalation rate monitoring
- False positive detection
- Chaos index tracking

---

### 5. Risk Control Layer

- Automatic escalation of legal cases
- Financial action safeguards
- Human override mechanisms

---

## 🧩 System Architecture

```text
User Email / Message
        ↓
    Spam Filter
        ↓
Embedding Classification
        ↓
 Business Logic Layer
        ↓
 API Call (if required)
        ↓
Customer Response OR System Escalation


