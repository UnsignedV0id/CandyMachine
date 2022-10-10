from cs50 import get_string

text = get_string("Text: ")

words = 1 + text.count(' ')
text = text.replace(" ", "")

sentences = text.count('!') + text.count('?') + text.count('.')
text = text.replace("!", "").replace("?", "").replace(".", "").replace("'", "").replace(",", "")

letters = len(text)

print(f"words {words}, letters {letters}, sentences {sentences}")
L = round(letters * 100 / words , 2)
S = round(sentences * 100 / words , 2)
print(L)
print(S)

index = round(0.0588 * L, 1) - round(0.296 * S, 1) - 15.8;
print(index)
index = round(index)

if index < 1:
    print("Before Grade 1")
elif index > 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")




