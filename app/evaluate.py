from rouge import Rouge

rouge = Rouge()  

def evaluate_response(predicted: str, reference: str) -> dict:
    try:
        scores = rouge.get_scores(predicted, reference, avg=True)
        return {
            "rouge-1": round(scores["rouge-1"]["f"], 3),
            "rouge-2": round(scores["rouge-2"]["f"], 3),
            "rouge-l": round(scores["rouge-l"]["f"], 3)
        }
    except Exception as e:
        print("⚠️ ROUGE evaluation failed:", e)
        return {"rouge-1": 0.0, "rouge-2": 0.0, "rouge-l": 0.0}
