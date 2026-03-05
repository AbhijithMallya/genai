
# While loop example 

secret_number = 7
guess = None

while guess != secret_number:
    try:
        guess = int(input("Guess the secret number between 1 and 10: "))
        if guess < secret_number:
            print("Too low! Try again.")
        elif guess > secret_number:
            print("Too high! Try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")
print("Congratulations! You've guessed the secret number.")

