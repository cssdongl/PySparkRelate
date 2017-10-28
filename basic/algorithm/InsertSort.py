def insert_sort(arr):
    length = len(arr)
    for i in range(length):
        key = arr[i]
        j = i -1
        while j >=0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key

    for elem in arr:
        print elem

if __name__ == '__main__':
    arr = [1,4,2,9,6,10,3]
    insert_sort(arr)
