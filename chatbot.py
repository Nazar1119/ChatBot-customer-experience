import re
import os
import requests
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
from spam_filter import is_spam
from prototypes import PROTOTYPES, LEGAL_WORDS, DOSAGE_WORDS, YES_WORDS, NO_WORDS, CATEGORIES
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
            "message": "Nastala technická chyba. Skús to prosím neskôr.",
            "needs_escalation_confirmation": False
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
                "message": f"Mrzí ma to, ale objednávku {order_number} už nie je možné zrušiť "
                           f"(aktuálny stav: {current_status}). "
                           "Chceš, aby som ťa prepojil na kolegu z podpory?",
                    "needs_escalation_confirmation": True
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
        return {"message" :"Chceš, aby som ťa prepojil na kolegu z podpory?",
                    "needs_escalation_confirmation": True}

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


pending_action = None

while True:
    user_input = input("Zákazník: ")

    if user_input.lower() == "exit":
        break

    lower_input = user_input.lower()

    # ======================================
    # CONFIRM ESCALATION STATE (FIRST)
    # ======================================
    if pending_action == "confirm_escalation":

        if any(word in lower_input for word in YES_WORDS):
            print("Chatbot: Prepojujem ťa na kolegu z podpory.")
            pending_action = None
            continue

        elif any(word in lower_input for word in NO_WORDS):
            print("Chatbot: Rozumiem 🙂 Ak budeš niečo potrebovať, pokojne napíš.")
            pending_action = None
            continue

        else:
            print("Chatbot: Prosím odpíš mi áno alebo nie 🙂")
            continue


    # ======================================
    # WAITING FOR ORDER NUMBER
    # ======================================
    if pending_action == "cancel_order":
        order_number = extract_order_number(user_input)

        if order_number:
            result = handle_cancel(user_input)

            reply = result["message"]

            if result.get("needs_escalation_confirmation"):
                pending_action = "confirm_escalation"
            else:
                pending_action = None

        else:
            reply = "Stále potrebujem číslo objednávky, aby som ju vedel zrušiť."

        print("Chatbot:", reply)
        continue


    # ======================================
    # SPAM CHECK
    # ======================================
    if is_spam(user_input):
        print("Chatbot: Správa bola vyhodnotená ako podozrivá.")
        continue


    # ======================================
    # NORMAL CLASSIFICATION
    # ======================================
    category, score = classify_email(user_input)
    print(f"[DEBUG] Category: {category}, score: {score:.3f}")

    if category == "Order Cancel":
        order_number = extract_order_number(user_input)

        if not order_number:
            pending_action = "cancel_order"
            reply = "Aby som ti vedel pomôcť, pošli mi prosím číslo objednávky."
        else:
            result = handle_cancel(user_input)

            reply = result["message"]

            if result.get("needs_escalation_confirmation"):
                pending_action = "confirm_escalation"

    else:
        result = generate_response(user_input, category)
        reply = result["message"]

        if result["needs_escalation_confirmation"]:
            pending_action = "confirm_escalation"


    # ======================================
    # ANGER TONE
    # ======================================
    if is_angry(user_input):
        reply = "Rozumiem, že situácia môže byť nepríjemná. Pokúsim sa ti pomôcť. " + reply


    print("Chatbot:", reply)

