def bubble_sort(items):
    while items:
        mini = items[0]
        for i in range(len(items) - 1):
            if items[i] < mini:
                mini = items[i]
                items[0] = mini
        return bubble_sort(items[1::])



items = [2, 3, 4, 3, 1, 2, 4, 5, 1, 2]
bubble_sort(items)
print(items)  # => [1, 1, 2, 2, 2, 3, 3, 4, 4, 5]
