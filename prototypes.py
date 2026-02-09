LEGAL_WORDS = ["súd", "právnik", "SOI", "ochrana spotrebiteľa"]
DOSAGE_WORDS = ["dávkovanie", "koľko brať", "koľko užívať", "dosage"]
YES_WORDS = ["ano", "áno", "hej", "ok", "dobre", "prosím", "jasne"]
NO_WORDS = ["nie", "netreba", "dakujem", "ďakujem", "nie ďakujem"]

CATEGORIES = [
    "Order Status",
    "Order Cancel",
    "Order Modify",
    "Return / Complaint",
    "Product Question",
    "Store / Delivery / Availability",
    "Cooperation / Partnership"
]


PROTOTYPES = {
    "Order Status": [
        "Where is my order? delivery status, tracking number, order delayed, waiting for package, no update.",
        "I am still waiting for my order, it has not arrived yet, package not delivered, when will it arrive?",
        "Objednávka mešká, kde je moja objednávka, stav objednávky, doručenie, kuriér, tracking číslo.",
        "Čakám už týždeň, stále čakám, už týždeň nič, balík neprišiel, neprišlo mi nič.",
        "Objednal som a stále nič, objednávka stále nedorazila, kedy príde balík?",
        "Potrebujem urgentne informáciu o stave objednávky, balík stále neprišiel, čakám príliš dlho."
    ],
    "Order Cancel": [

        # Business definition
        "Customer wants to permanently cancel the order before delivery.",
        "The order should be stopped and not processed further.",
        "This is full cancellation, not modification of details.",
        "The customer does not want to receive the order anymore.",
        "Customer wants to completely stop the order process."

        # English
        "Cancel my order before shipping.",
        "I changed my mind, cancel the order.",
        "Duplicate order, please cancel one.",
        "Stop my order immediately.",

        # Slovak
        "Chcem zrušiť objednávku.",
        "Prosím o zrušenie objednávky.",
        "Objednávka bola omyl, zrušte ju.",
        "Nechcem objednávku, prosím zrušiť.",
        "ZRUŠIŤ",
    ],

    "Order Modify": [

        # Business definition
        "Customer wants to update information but keep the order active.",
        "The order remains valid but details should be changed.",
        "This is modification, not cancellation.",
        "Customer wants to edit order information before shipment.",
        "Customer wants to keep the order active but change details."

        # English
        "Change shipping address.",
        "Add another product to my order.",
        "Update recipient name.",
        "Change payment method.",

        # Slovak
        "Zmeniť adresu doručenia.",
        "Pridať produkt do objednávky.",
        "Zmena údajov v objednávke.",
        "Môžem upraviť objednávku?",
    ],
    "Return / Complaint": [

        # Business definition
        "Customer received the product and reports damage or defect.",
        "Post-delivery issue requiring refund or replacement.",
        "This is about damaged, missing, or wrong item.",
        "Product has already been delivered.",

        # English
        "Product arrived damaged.",
        "Wrong item delivered.",
        "One item missing from package.",
        "I want to return the product.",

        # Slovak
        "Produkt prišiel poškodený.",
        "V balíku chýba produkt.",
        "Zlá príchuť, chcem výmenu.",
        "Chcem vrátiť tovar.",
    ],
    "Product Question": [
        "Product question: ingredients, gluten-free, dosage, differences between supplements, recommendation.",
        "What is the difference between EAA and BCAA?",
        "Which protein is better for muscle gain?",
        "Is this product suitable for beginners?",
        "Does this supplement contain gluten?",
        "Is this product lactose-free?",
        "What is the recommended dosage?",
        "When should I take this supplement?",
        "Is this product safe for daily use?",
        "Which creatine is better?",
        "Does this contain artificial sweeteners?",
        "Is this product vegan?",
        "Can you recommend something for weight loss?",
        "Which product is best for joint pain?",


        "Otázka o produkte: bezgluténové, EAA vs BCAA, kreatín, kolagén, dávkovanie, zloženie.",
        "Aký je rozdiel medzi týmito produktmi?",
        "Ktorý proteín je najlepší na naberanie svalov?",
        "Je tento produkt vhodný pre začiatočníkov?",
        "Obsahuje tento produkt laktózu?",
        "Je tento proteín bez cukru?",
        "Ako sa tento produkt užíva?",
        "Kedy je najlepšie užívať kreatín?",
        "Je tento doplnok vhodný pre ženy?",
        "Máte niečo na chudnutie?",
        "Je tento produkt vhodný pri celiakii?",
        "Obsahuje produkt umelé sladidlá?",
        "Aké sú účinky kolagénu?",
        "Pomôže tento produkt pri bolestiach kĺbov?",
        "Môžete mi odporučiť vhodný doplnok výživy?"
    ],
    "Store / Delivery / Availability": [
        "Do you deliver to Czechia? shipping abroad, store location, pickup, opening hours.",
        "How long does delivery take?",
        "What are the shipping options?",
        "Do you offer express shipping?",
        "Where is your physical store located?",
        "Can I pick up my order in person?",
        "What are your opening hours?",
        "How much is shipping?",
        "Do you ship internationally?",
        "Is cash on delivery available?",
        "What payment methods do you accept?",
        "Can I pay by bank transfer?",
        "How can I track my order?",
        "Do you deliver on weekends?",


        "Doručujete do Česka, predajňa, pobočka, kamenná predajňa, osobný odber, dostupnosť.",
        "Koľko stojí doprava?",
        "Aké sú možnosti dopravy?",
        "Doručujete do zahraničia?",
        "Aké platobné metódy prijímate?",
        "Je možný osobný odber?",
        "Kedy bude objednávka odoslaná?",
        "Ako sledovať zásielku?",
        "Doručujete cez víkend?",
        "Odosielate aj v sobotu?",
        "Aká je otváracia doba predajne?",
        "Koľko dní trvá doručenie?",
        "Môžem nakúpiť telefonicky?",
        "Je tovar skladom?"
    ]
    ,
    "Cooperation / Partnership": [
        "Business cooperation inquiry, partnership proposal, influencer collaboration, wholesale or B2B offer.",
        "We would like to discuss a business partnership.",
        "Influencer collaboration proposal.",
        "We are interested in wholesale cooperation.",
        "Marketing partnership opportunity.",
        "Sponsorship request for sports event.",
        "Brand collaboration inquiry.",
        "Can we promote your products?",
        "Affiliate partnership proposal.",
        "B2B cooperation request.",
        "We would like to become a distributor.",
        "Proposal for event sponsorship.",

        "Spolupráca, kooperácia, partnerská ponuka, influencer spolupráca, veľkoobchod, B2B, marketingová spolupráca.",
        "Požiadavka o sponzoring.",
        "Potreboval by som sponzoring na podujatie.",
        "Záujem o obchodnú spoluprácu.",
        "Ponuka partnerskej spolupráce.",
        "Chceli by sme propagovať vaše produkty.",
        "Možnosť veľkoobchodnej spolupráce.",
        "Marketingová ponuka.",
        "Záujem o affiliate spoluprácu.",
        "Sponzorstvo športovca.",
        "Spolupráca s fitness influencerom."
    ]
}