from Configuration import Configuration

x = x = [[1,2,3], [4,5], [6]]

def transpose(array):
    array = array[:]  # make copy to avoid changing original
    n = len(array)
    for i, row in enumerate(array):
        array[i] = row + [None for _ in range(n - len(row))]

    array = list(zip(*array))
    #print(list(array))

    for i, row in enumerate(array):
        array[i] = [elem for elem in row if elem is not None]

    return array

def main():
    global x
    
    y = transpose(x)

    print(x)
    print(y)


    return

main()