import json
from app import classify_message
from tqdm import tqdm
import matplotlib.pyplot as plt
from collections import Counter

def run_tests(jsonl_path):
    correct = 0
    total = 0
    errors = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in tqdm(lines, desc="Classifying", unit="msg"):
        data = json.loads(line)
        text = data['text']
        expected = data['label']
        predicted = classify_message(text)
        print(f"Text: {text}\nExpected: {expected}\nPredicted: {predicted}\n")
        if predicted == expected:
            correct += 1
        else:
            errors.append((text,expected, predicted))
        total += 1
    print(f"Accuracy: {correct}/{total} ({correct/total:.2%})")  
    # Save misclassifications as JSONL
    if errors:
        with open("misclassifications.jsonl", "w", encoding="utf-8") as out:
            for text, expected, predicted in errors:
                out.write(json.dumps({"text": text, "expected": expected, "predicted": predicted}, ensure_ascii=False) + "\n")
    # Visualize misclassifications
    if errors:
        error_types = [f"{exp}→{pred}" for txt,exp, pred in errors]
        error_counts = Counter(error_types)
        plt.figure(figsize=(10, 5))
        plt.bar(error_counts.keys(), error_counts.values(), color='red')
        plt.xlabel('Misclassification (expected→predicted)')
        plt.ylabel('Count')
        plt.title('Most Frequent Misclassifications')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    run_tests('test.jsonl')
