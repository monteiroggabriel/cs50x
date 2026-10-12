def count_letters(text):
    count = 0
    for letter in text:
        if letter.isalpha():
            count += 1
    return count

def count_words(text):
    count = 0
    for word in text.split():
        count += 1
    return count

def count_sentences(text):
    count = 0
    for letter in text:
        if letter in ".?!":
            count += 1
    return count

text = input("Text: ")
letters = count_letters(text)
words = count_words(text)
sentences = count_sentences(text)

L = letters / words * 100
S = sentences / words * 100
index = 0.0588 * L - 0.296 * S - 15.8

if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {round(index)}")
