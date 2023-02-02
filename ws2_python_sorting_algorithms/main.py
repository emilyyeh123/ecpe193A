'''
Program to read file and sort random list in file
'''

def main():
    f = open("randomList.txt", "r")

    # place elements of file into an array
    arr = []
    for line in f:
        arr.append(int(line))
    print("Original Unsorted Array: ", arr)

    # perform insertion sort
    insertionSort = arr.copy()
    for i in range(len(insertionSort)-1):
        j = i+1
        while j > 0 and  insertionSort[j] < insertionSort [j-1]:
            temp = insertionSort[j]
            insertionSort[j] = insertionSort[j-1]
            insertionSort[j-1] = temp
            j -= 1

    # perform bubble sort
    bubbleSort = arr.copy()
    for i in range(len(bubbleSort)):
        for j in range(len(bubbleSort)-i-1):
            if bubbleSort[j] > bubbleSort[j+1]:
                temp = bubbleSort[j]
                bubbleSort[j] = bubbleSort[j+1]
                bubbleSort[j+1] = temp

    print("Insertion Sort: ", insertionSort, "\nBubble Sort: ", bubbleSort)

if __name__ == "__main__":
    main()
