import pickle
import random

MODEL_PATH = "app/ai/chatbot_index.pkl"

def load_index(model_path=MODEL_PATH):
    with open(model_path, "rb") as f:
        return pickle.load(f)


def get_response(user_input, index, similarity_threshold=0.3):
    vec = index["vectorizer"].transform([user_input.lower()])
    distances, indices = index["nn"].kneighbors(vec, n_neighbors=1)
    similarity = 1 - distances[0][0]  # cosine distance -> similarity
    match_idx = indices[0][0]

    if similarity < similarity_threshold:
        fallback_responses = index.get("fallback_responses")
        if fallback_responses:
            return random.choice(fallback_responses), "fallback", similarity
        # Last-resort default, only used if the dataset has no "fallback" intent at all
        return (
            "ខ្ញុំមិនជឿជាក់ថាខ្ញុំយល់រឿងនោះទេ។ តើអ្នកអាចនិយាយឡើងវិញ ឬបើកសំបុត្រជំនួយបានទេ?",
            None,
            similarity,
        )

    responses = index["pattern_to_responses"][match_idx]
    return random.choice(responses), index["pattern_to_tag"][match_idx], similarity