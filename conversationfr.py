import csv
import re

def preprocess_sentence(sentence):
    # Convertir en minuscules et enlever les espaces inutiles
    sentence = sentence.lower().strip()
    # Ajouter un espace avant et après les signes de ponctuation
    sentence = re.sub(r"([?.!,])", r" \1 ", sentence)
    # Remplacer les multiples espaces par un seul espace
    sentence = re.sub(r' +', ' ', sentence)
    # Nettoyer les contractions en français
    sentence = re.sub(r"je suis", "je suis", sentence)
    sentence = re.sub(r"il est", "il est", sentence)
    sentence = re.sub(r"elle est", "elle est", sentence)
    sentence = re.sub(r"c'est", "c'est", sentence)
    sentence = re.sub(r"ce que", "ce que", sentence)
    sentence = re.sub(r"où est", "où est", sentence)
    sentence = re.sub(r"comment est", "comment est", sentence)
    sentence = re.sub(r"j'ai", "j ai", sentence)
    sentence = re.sub(r"tu as", "tu as", sentence)
    sentence = re.sub(r"il a", "il a", sentence)
    sentence = re.sub(r"elle a", "elle a", sentence)
    sentence = re.sub(r"nous avons", "nous avons", sentence)
    sentence = re.sub(r"vous avez", "vous avez", sentence)
    sentence = re.sub(r"ils ont", "ils ont", sentence)
    sentence = re.sub(r"elles ont", "elles ont", sentence)
    sentence = re.sub(r"ne sera pas", "ne sera pas", sentence)
    sentence = re.sub(r"ne peut pas", "ne peut pas", sentence)
    sentence = re.sub(r"n'est pas", "n'est pas", sentence)
    sentence = re.sub(r"n'", "n'", sentence)
    sentence = re.sub(r"'bout", "à propos de", sentence)
    # Supprimer les caractères non alphabétiques sauf ponctuation
    sentence = re.sub(r"[^a-zà-ÿÀ-ÿ?.!,]+", " ", sentence)
    sentence = sentence.strip()
    return sentence

def load_questions_answers_from_text(file_path):
    questions_answers = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Assumer : Les questions et réponses sont séparées par des lignes et marquées par "Q:" et "A:"
    question = None
    for line in lines:
        line = line.strip()
        if line.startswith("Q:"):
            if question is not None:
                questions_answers.append((preprocess_sentence(question), preprocess_sentence(answer)))
            question = line[2:].strip()
        elif line.startswith("A:"):
            answer = line[2:].strip()
    
    if question is not None and answer is not None:
        questions_answers.append((preprocess_sentence(question), preprocess_sentence(answer)))
    
    return questions_answers

# Définir le chemin vers votre fichier texte
path_to_text_file = r'C:\Users\User\Documents\CHATBOT\vscode\chatbot.py\datafr.txt'

# Charger et prétraiter les données
questions_answers = load_questions_answers_from_text(path_to_text_file)

if questions_answers:
    # Séparer les questions et les réponses
    questions, answers = zip(*questions_answers)

    # Enregistrer les données dans un fichier CSV
    csv_file_path = r'C:\Users\User\Documents\CHATBOT\vscode\chatbot.py\questions_answers.csv'

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Question", "Réponse"])  # En-têtes des colonnes
        for question, answer in zip(questions, answers):
            writer.writerow([question, answer])

    print(f"Les données ont été enregistrées dans {csv_file_path}")
else:
    print("Aucune paire question-réponse trouvée dans le fichier texte.")
