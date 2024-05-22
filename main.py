import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def best_matches_response(question: str, response: list[str]) -> str | None:
    matches: list = get_close_matches(question, response, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

def chat_bot():
    nama = input("Halo, Aku Bot. Siapa namamu? ")
    print(f"Selamat Datang {nama}, Mari belajar bersama!")

    knowledge_base: dict = load_knowledge_base('knowledge-base.json')

    while True:
        user_input: str = input(f"{nama}: ")

        if user_input.lower() == "quit":
            break

        best_match: str | None = best_matches_response(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_question(best_match, knowledge_base)
            print(f"Bot: {answer}")
        else:
            print(f"Bot: Maaf, saya tidak tahu harus menjawab apa. Bisakah anda ajari saya?")
            new_answer: str = input("Jawabannya atau 'skip' untuk lewati: ")

            if new_answer.lower() != "skip":
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge-base.json', knowledge_base)
                print("Bot: Terimakasih, saya belajar response baru!")

if __name__ == "__main__":
    chat_bot()
