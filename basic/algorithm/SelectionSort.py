def select_sort(arr):
    length  = len(arr)
    for i in range(length):
        min_index = i
        for j in range(i+1,length):
            if arr[j] < arr[min_index]:
                min_index = j
        if min_index != i:
            temp = arr[min_index]
            arr[min_index] = arr[i]
            arr[i] = temp
    return arr

if __name__ == "__main__":
    arr = [1,4,2,6,99,22,60]
    for elem in select_sort(arr):
        print elem