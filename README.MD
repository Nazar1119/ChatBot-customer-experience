# 📧 GymBeam – Email Intent Classification System

## Overview

This project implements an automated system for processing customer emails for GymBeam.
The goal is to classify incoming emails by intent, detect spam or phishing messages, and
decide whether an email can be handled automatically by a chatbot or should be routed to
a human customer support agent.

The solution is designed for scenarios where **no labeled training data is initially
available**, therefore it relies on **semantic embeddings, prototype-based classification,
and rule-based logic**.

---

## Objectives

- Automatically classify customer emails into 5–8 meaningful intent categories
- Detect spam and phishing emails reliably
- Route emails either to:
    - an automated chatbot (FAQ-type questions), or
    - a human customer support agent (complex or risky cases)
- Produce a structured output dataset suitable for further automation

---

## Dataset

The input dataset of customers emails, without ground truth labels, each with:
- Message ID
- Subject
- Email body
- Language

---

## System Architecture

The system follows a multi-stage pipeline:

1. Text preprocessing
2. Feature extraction
3. Spam & phishing detection
4. Intent classification
5. Confidence estimation
6. Human vs. bot routing
7. Export of structured results

---

## 1. Text Preprocessing

Each email is normalized to ensure consistent input:
- Whitespace normalization
- Lowercasing (where applicable)
- Subject and email body are merged into a single text field

This unified text is used for all downstream NLP tasks.

---

## 2. Feature Extraction

Additional structured information is extracted from emails:

### Order ID Extraction
- Regular expressions are used to detect order numbers (4+ digits)

### URL Detection
- URLs are extracted to help identify suspicious or phishing messages

These features are included in the final output dataset.

---

## 3. Spam & Phishing Detection

Spam detection is implemented as a **layered approach** combining multiple signals.

### 3.1 Rule-Based Detection
The following heuristics are used:
- Presence of known spam / phishing keywords (SK + EN)
- Excessive use of capital letters
- Multiple exclamation marks
- Suspicious URLs

A `spam_score` is computed based on these rules.

---

### 3.2 Semantic Spam Detection

To improve robustness, **semantic similarity** is used:

- A set of predefined spam/phishing prototype texts is created
- Emails are compared against these prototypes using embeddings
- Cosine similarity is calculated

Spam is detected **relatively**, not using an absolute threshold:
- An email is marked as spam if it is **more similar to spam prototypes than to any business intent**
- Rule-based spam signals act as a fallback

This significantly reduces false positives.

---

## 4. Intent Classification

### Model
- **intfloat/multilingual-e5-base**
- Supports Slovak and English
- Produces dense semantic embeddings

### Method
- Prototype-based semantic classification
- Each intent category is represented by multiple prototype texts
- Email embeddings are compared to prototype embeddings using cosine similarity

### Intent Categories
- Order Status
- Order Cancel
- Order Modify
- Return / Complaint
- Product Question
- Store / Delivery / Availability
- Cooperation / Partnership
- Spam / Phishing

The category with the highest similarity score is assigned.

---

## 5. Confidence Estimation (Margin)

Instead of using raw similarity scores, **confidence is measured using a margin**: margin = best_similarity − second_best_similarity


- A small margin indicates uncertainty
- A large margin indicates confident classification

This approach is more reliable than absolute similarity thresholds.

---

## 6. Human vs. Bot Routing

Emails are routed based on **confidence and business rules**:

### Automated Chatbot
Only safe FAQ-type intents are handled automatically:
- Order Status
- Order Cancel
- Product Question
- Store / Delivery / Availability

### Human Agent
Emails are routed to human support if:
- The model confidence is low (small margin)
- The intent involves money, orders, complaints, or cooperation

### Spam and Phishing are  blocked by system
This ensures safety and minimizes automation risks.

---

## 7. Final Output

The final dataset includes:
- Message ID
- Original subject and email text
- Extracted order ID(s)
- Detected URLs
- Final intent category
- Spam flag
- Confidence indicators
- Routing decision (bot / human)

The results are exported to:
- `emails_categorized.csv`
- `emails_categorized.xlsx`

---

## Conclusion

This solution demonstrates how customer email classification can be implemented **without labeled training data** using:
- Multilingual embeddings
- Prototype-based intent matching
- Semantic confidence estimation
- Layered spam detection
- Business-aware routing logic

The system is modular, explainable, and suitable as a foundation for real-world customer support automation.

