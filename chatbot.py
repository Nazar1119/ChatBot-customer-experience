import re
import os
import requests
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
from spam_filter import is_spam
from prototypes import PROTOTYPES, LEGAL_WORDS, DOSAGE_WORDS, YES_WORDS, NO_WORDS
load_dotenv()


model = SentenceTransformer("intfloat/multilingual-e5-base")

proto_texts = []
proto_labels = []


for category, texts in PROTOTYPES.items():
    for t in texts:
        proto_texts.append(t)
        proto_labels.append(category)

proto_embeddings = model.encode(
    [f"passage: {t}" for t in proto_texts],
    normalize_embeddings=True
)

def classify_email(text):
    emb = model.encode(
        [f"query: {text}"],
        normalize_embeddings=True
    )

    sims = cosine_similarity(emb, proto_embeddings)[0]
    best_idx = sims.argmax()
    best_score = sims[best_idx]

    return proto_labels[best_idx], best_score


ORDER_ID_RE = re.compile(r"\b\d{4,}\b")


def should_escalate_legal(text):
    text_lower = text.lower()
    return any(word in text_lower for word in LEGAL_WORDS)

def is_dosage_question(text):
    text_lower = text.lower()
    return any(word in text_lower for word in DOSAGE_WORDS)

def is_angry(text):
    if len(text) > 10:
        upper_ratio = sum(1 for c in text if c.isupper()) / len(text)
        return upper_ratio > 0.3
    return False

def extract_order_number(text):
    match = ORDER_ID_RE.search(text)
    return match.group(0) if match else None


def cancel_order(order_number):

    API_URL = os.getenv("API_URL")
    API_KEY = os.getenv("API_KEY")

    if not API_URL or not API_KEY:
        raise ValueError("Missing API config")

    try:
        response = requests.post(
            f"{API_URL}?api_key={API_KEY}",
            json={"order_number": order_number},
            headers={"Content-Type": "application/json"},
            timeout=5
        )

        return response.status_code, response.json()


    except Exception as e:
        return None, {"error": str(e)}

def handle_cancel(text):

    order_number = extract_order_number(text)
    if not order_number:
        return {"message":"Prosím, pošli mi číslo objednávky.",
                    "needs_escalation_confirmation": False}

    status_code, data = cancel_order(order_number)

    if not isinstance(data, dict):
        return {
            "type": "system",
            "reason": "api_error",
            "original_text": text
        }

    api_status = data.get("status")

    if api_status == "error":
        error_code = data.get("error_code")

        if error_code == "ORDER_NOT_FOUND":
            return {"message": "Objednávku s týmto číslom som nenašiel. Skontroluj ho prosím ešte raz.",
                        "needs_escalation_confirmation": False}

        elif error_code == "ORDER_NOT_CANCELLABLE":
            current_status = data.get("current_status", "")
            return {
                "type": "customer",
                "message": f"Mrzí ma to, ale objednávku {order_number} už nie je možné zrušiť "
                           f"(aktuálny stav: {current_status})."
            }


        else:
            return {"message":f"Nastala chyba: {data.get('message', 'Neznáma chyba')}",
                        "needs_escalation_confirmation": False}

    elif api_status == "success":
        refund = data.get("refund_amount", "")
        return {"message": f"Tvoja objednávka {order_number} bola úspešne zrušená. "
                            f"Suma {refund} € ti bude vrátená.",
                    "needs_escalation_confirmation": False}

    else:
        return {"message":"Požiadavku odovzdávam kolegovi z podpory.",
                    "needs_escalation_confirmation": False}



def generate_response(text, category):

    if should_escalate_legal(text):
        return {
            "type": "system",
            "reason": "legal_issue",
            "original_text": text
        }

    if category == "Product Question" and is_dosage_question(text):
        return {"message":"Pri dávkovaní ti, žiaľ, nemôžem konkrétne poradiť. "
                          "Odporúčam obrátiť sa na výživového poradcu alebo lekára.",
                    "needs_escalation_confirmation": False}

    if category == "Return / Complaint":
        return {
            "message":
                "Mrzí ma, že nastal problém 😕\n\n"
                "Tovar môžeš zaslať na adresu:\n"
                "GymBeam, Rastislavova 93, 040 01 Košice\n\n"
                "Na balík napíš „Vratka“ alebo „Reklamácia“ + číslo objednávky.\n\n"
                "Chceš, aby som ťa prepojil na kolegu z podpory?",
            "needs_escalation_confirmation": True
        }


    if category == "Order Cancel":
        return handle_cancel(text)

    if category == "Order Status":
        return {"message":"Stav objednávky si môžeš skontrolovať cez tracking číslo,"
                          "ktoré ti prišlo v potvrdzovacom emaili.",
                    "needs_escalation_confirmation": False}

    if category == "Store / Delivery / Availability":
        return {"message":"Rád ti pomôžem 🙂 Napíš mi prosím konkrétnejšie, čo ťa zaujíma "
                          "(doprava, predajňa, dostupnosť tovaru...).",
                    "needs_escalation_confirmation": False}

    if category == "Cooperation / Partnership":
        return {"message":"Tvoju ponuku odovzdávam príslušnému oddeleniu.",
                    "needs_escalation_confirmation": False}

    return {
        "message": "Tvoju správu odovzdávam kolegovi z podpory.",
        "needs_escalation_confirmation": False
    }


def process_message(user_input, state):

    lower_input = user_input.lower()
    pending_action = state.get("pending_action")

    # =========================
    # CONFIRM ESCALATION
    # =========================
    if pending_action == "confirm_escalation":

        if any(word in lower_input for word in YES_WORDS):
            state["pending_action"] = None
            return "Prepojujem ťa na kolegu z podpory.", state

        elif any(word in lower_input for word in NO_WORDS):
            state["pending_action"] = None
            return "Rozumiem 🙂 Ak budeš niečo potrebovať, pokojne napíš.", state

        else:
            return "Prosím odpíš mi áno alebo nie 🙂", state


    # =========================
    # WAITING FOR ORDER NUMBER
    # =========================
    if pending_action == "cancel_order":

        order_number = extract_order_number(user_input)

        if order_number:
            result = handle_cancel(user_input)

            state["pending_action"] = None
            return result["message"], state

        else:
            return "Stále potrebujem číslo objednávky.", state


    # =========================
    # SPAM CHECK
    # =========================
    if is_spam(user_input):
        return "Správa bola vyhodnotená ako podozrivá.", state


    # =========================
    # CLASSIFICATION
    # =========================
    category, score = classify_email(user_input)

    if category == "Order Cancel":

        order_number = extract_order_number(user_input)

        if not order_number:
            state["pending_action"] = "cancel_order"
            return "Pošli mi prosím číslo objednávky.", state

        result = handle_cancel(user_input)
        return result["message"], state

    result = generate_response(user_input, category)

    reply = result["message"]

    if result.get("needs_escalation_confirmation"):
        state["pending_action"] = "confirm_escalation"

    if is_angry(user_input):
        reply = "Rozumiem, že situácia môže byť nepríjemná. " + reply

    return reply, state

state={
    "pending_action": None,
}

while True:

    user_input = input("Zákazník: ")

    if user_input.lower() == "exit":
        break

    reply, state = process_message(user_input, state)

    print("Chatbot:", reply)
