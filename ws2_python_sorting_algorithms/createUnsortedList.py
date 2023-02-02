import random

def main():
    f = open("randomList.txt", "w")
    s = ""
    for i in range(20):
        randNum = random.randrange(30)
        s += str(randNum) + "\n"
    f.write(s)
    f.close()


if __name__ == "__main__":
    main()
