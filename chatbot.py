"""
chatbot.py
-----------------
A minimal chatbot that:
 - Uses Sentence-BERT embeddings
 - computes cosine similarity
 - gets the closest response from a knowledge base 

"""

import numpy as np
from sentence_transformers import SentenceTransformer

THRESHOLD = 0.3

# ----------------------------------------------------------------------
# knowledge base (user prompt: response)
# ----------------------------------------------------------------------
KB = [
    {"user": "hello", "bot": "Hi! How’s it going?"},
    {"user": "hi", "bot": "Hi there, what’s up?"},
    {"user": "what is cosine similarity", "bot": "It’s a way to check how similar two vectors are by looking at the angle between them."},
    {"user": "explain word embeddings", "bot": "Embeddings turn words into numbers so computers can understand meaning and compare them."},
    {"user": "how do I use embeddings", "bot": "You take some text, turn it into embeddings, and then compare them with cosine similarity to see what’s closest."},
    {"user": "thanks", "bot": "No worries! Glad I could help."},
]


# ----------------------------------------------------------------------
# chatbot
# ----------------------------------------------------------------------
class Chatbot:
    def __init__(self, kb, threshold=THRESHOLD):
        self.kb = kb
        self.threshold = threshold
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    # ------------------------
    # setup
    # ------------------------
    def fit(self):
        """pre computes embeddings for all knowledge base queries"""
        user_texts = [item["user"] for item in self.kb]
        embeddings = self.model.encode(user_texts, show_progress_bar=False, convert_to_numpy=True)

        # normalize embeddings 
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        self.kb_embeddings = embeddings / np.clip(norms, 1e-10, None)

    # ------------------------
    # query handling
    # ------------------------
    def embed_query(self, text):
        """Embed and normalize a single query."""
        vec = self.model.encode([text], convert_to_numpy=True)
        norm = np.linalg.norm(vec, axis=1, keepdims=True)
        return vec / np.clip(norm, 1e-10, None)

    def reply(self, query, top_k=3):
        """finds the best response for a query."""
        query_vector = self.embed_query(query)
        similarity_scores = np.dot(self.kb_embeddings, query_vector[0])

        # rank matches
        top_idx = np.argsort(similarity_scores)[::-1][:top_k]
        top_matches = [(self.kb[i]["user"], float(similarity_scores[i])) for i in top_idx]

        # choose best
        best_i, best_score = top_idx[0], similarity_scores[top_idx[0]]
        if best_score >= self.threshold:
            return self.kb[best_i]["bot"], top_matches
        else:
            return "Sorry - I don't know how to answer that. could you rephrase?", top_matches


# ----------------------------------------------------------------------
# main program
# ----------------------------------------------------------------------
if __name__ == "__main__":
    bot = Chatbot(kb=KB)
    bot.fit()

    print("\nChatbot ready! Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("Bot: Bye")
            break

        response, matches = bot.reply(user_input, top_k=3)
        print(f"Bot: {response}")

        # Show top matches 
        print("\n  Top matches:")
        for txt, score in matches:
            print(f"     - '{txt}'  -> {score:.3f}")
        print()
