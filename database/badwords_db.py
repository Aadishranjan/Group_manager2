from .db import bad_words_collection

def add_bad_word(chat_id, word):
    word = word.lower()
    bad_words_collection.update_one(
        {"chat_id": chat_id},
        {"$addToSet": {"words": word}},
        upsert=True
    )

def get_bad_words(chat_id):
    doc = bad_words_collection.find_one({"chat_id": chat_id})
    return doc.get("words", []) if doc else []
