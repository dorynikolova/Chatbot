from chatbot import ask_bildo

while True:
    msg = input("You: ")
    print("Bildo:", ask_bildo(msg))
