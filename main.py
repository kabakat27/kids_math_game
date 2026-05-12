import random

fruits = [
    ("Apple", 2),
    ("Banana", 3),
    ("Orange", 4),
    ("Pear", 5),
    ("Grapes", 6)
]

fruit1, fruit2 = random.sample(fruits, 2)

name1, price1 = fruit1
name2, price2 = fruit2

count1 = random.randint(1, 5)
count2 = random.randint(1, 5)

correct_answer = (count1 * price1) + (count2 * price2)

wrong_answers = set()

while len(wrong_answers) < 3:

    wrong = correct_answer + random.randint(-5, 5)

    if wrong != correct_answer and wrong > 0:
        wrong_answers.add(wrong)

answers = list(wrong_answers)
answers.append(correct_answer)

random.shuffle(answers)

print("\n question")
print("-" * 30)

print(
    f"Adam bought {count1} {name1}(s) "
    f"and {count2} {name2}(s)."
)

print(
    f"Price of one {name1} = {price1} dollars."
)

print(
    f"Price of one {name2} = {price2} dollars."
)

print("\nHow much did Adam pay?")

for i, answer in enumerate(answers, start=1):
    print(f"{i}) {answer} dollars")

choice = int(
    input("\nChoose the correct answer number: ")
)

selected_answer = answers[choice - 1]

if selected_answer == correct_answer:

    print("\n Correct! Good Job!")

else:

    print("\n Wrong Answer!")

    print("\n Hint:")
    print(
        f"First calculate:\n"
        f"{count1} × {price1}\n"
        f"and\n"
        f"{count2} × {price2}\n"
        f"Then add the results together."
    )

    second_choice = int(
        input("\nTry again. Choose another number: ")
    )

    second_answer = answers[second_choice - 1]

    # Check second try
    if second_answer == correct_answer:

        print("\n Correct! Good Job!")

    else:
        print("\n Wrong Again!")

        print(
            f"\n The correct answer is: "
            f"{correct_answer}"
        )