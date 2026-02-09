import re

SPAM_PROTOTYPES = [
    "váš účet", "ucet", "zablokovan", "zablokovaný",
    "overiť identitu", "overit identitu",
    "prihlasovacie údaje", "prihlasovacie udaje",
    "zadať", "zadat",
    "kliknutím", "kliknutim",
    "kliknite tu", "upozornenie",
    "heslo", "potvrdiť účet", "overenie účtu",
    "24 hodín", "okamžitá akcia",
    "lacné", "exkluzívna ponuka" ,"investuj", "Bitcoin mining",
    "Účet bude zablokovaný, overenie identity, kliknite na link, zadajte prihlasovacie údaje.",
    "Vyhrali ste lotériu, kliknite tu a potvrďte účet.",
    "Exkluzívna ponuka, investuj do Bitcoinu teraz.",
    "Okamžitá akcia, potvrdiť účet do 24 hodín.",


    "your account", "account suspended", "account blocked",
    "verify your account", "verify identity",
    "click here", "confirm your details",
    "login immediately", "urgent action required",
    "security alert", "password reset",
    "update your payment", "payment failed",
    "limited time offer", "exclusive access",
    "invest now", "become millionaire",
    "earn money fast", "risk free investment",
    "guaranteed profit", "crypto investment",
    "wire transfer", "bank verification",
    "tax refund", "claim your prize",
    "free gift", "winner", "lottery",
    "act now", "immediate response required",
    "suspicious activity detected",
    "Your account will be blocked, verify your identity immediately.",
    "Click here to confirm your login details.",
    "Limited time offer, guaranteed profit investment.",
    "Earn money fast, risk free crypto investment.",
    "Security alert, update your payment information now."
]

URL_RE = re.compile(r"(https?://\S+|www\.\S+)", re.IGNORECASE)
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

def spam_score(text: str):
    score = 0
    text_lower = text.lower()

    for kw in SPAM_PROTOTYPES:
        if kw in text_lower:
            score += 1

    if URL_RE.search(text):
        score += 1

    if EMAIL_RE.search(text):
        score += 1

    if len(text) > 40:
        upper_ratio = sum(1 for c in text if c.isupper()) / len(text)
        if upper_ratio > 0.3:
            score += 1

    if "http" in text and "gymbeam" not in text:
        score += 1

    return score


def is_spam(text, threshold=3):
    return spam_score(text) >= threshold
