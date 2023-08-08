import random

from display import *


def run_check(screen, height, arr):
    for a, b in zip(arr, arr[1:]):
        if a <= b:
            a.make_correct()
            update_display(screen, height, arr)
    if arr[0] < arr[-1]:
        arr[-1].make_correct()
    update_display(screen, height, arr)


def partition(screen, height, arr, delay, low, high):
    pivot = arr[high]
    pivot.turquoise()
    update_display(screen, height, arr, delay)
    i = low-1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            (arr[i], arr[j]) = (arr[j], arr[i])
            arr[i].red()
            arr[j].red()
            update_display(screen, height, arr, delay)

    (arr[i + 1], arr[high]) = (arr[high], arr[i + 1])
    update_display(screen, height, arr, delay)
    reset_colours(arr)

    return i+1


def quick(screen, height, arr, delay, low, high):
    if low < high:
        pi = partition(screen, height, arr, delay, low, high)
        quick(screen, height, arr, delay, low, pi - 1)
        quick(screen, height, arr, delay,  pi + 1, high)


def merge(screen, height, arr, delay, left, right):
    mid = (left + right) // 2
    if left < right:
        merge(screen, height, arr, delay,  left, mid)
        merge(screen, height, arr, delay,  mid + 1, right)
        mergesort(screen, height, arr, delay,  left, mid, mid + 1, right)


def mergesort(screen, height, arr, delay, left1, left2, right1, right2):
    i = left1
    j = right1
    temp = []
    temp_index = 0

    while i <= left2 and j <= right2:
        reset_colours(arr)
        arr[i].turquoise()
        arr[j].orange()
        update_display(screen, height, arr, delay)
        if arr[i] < arr[j]:
            temp.append(arr[i])
            i += 1
        else:
            temp.append(arr[j])
            j += 1

    while i <= left2:
        temp.append(arr[i])
        i += 1

    while j <= right2:
        temp.append(arr[j])
        j += 1

    for i in range(left1, right2 + 1):
        arr[i] = temp[temp_index]
        temp[temp_index].make_correct()
        temp_index += 1
        update_display(screen, height, arr, delay)


def heapify(screen, height, arr, delay, size, index):
    largest_root = index

    left = 2 * index + 1
    right = 2 * index + 2

    if left < size and arr[index] < arr[left]:
        largest_root = left

    if right < size and arr[largest_root] < arr[right]:
        largest_root = right

    if largest_root != index:
        (arr[index], arr[largest_root]) = (arr[largest_root], arr[index])
        arr[index].red()
        arr[largest_root].red()
        update_display(screen, height, arr, delay)
        reset_colours(arr, colour=(64, 224, 208))
        heapify(screen, height, arr, delay,  size, largest_root)


def build_max_heap(screen, height, arr, delay):
    for i in range(len(arr) // 2 - 1, -1, -1):
        heapify(screen, height, arr, delay, len(arr), i)


def heap(screen, height, arr, delay):
    build_max_heap(screen, height, arr, delay)
    for i in range(len(arr) - 1, 0, -1):
        (arr[i], arr[0]) = (arr[0], arr[i])
        arr[i].make_correct()
        update_display(screen, height, arr, delay)
        heapify(screen, height, arr, delay,  i, 0)


def merge_bits(screen, height, arr, delay, low, count, direction):
    if count > 1:
        mid = int(count / 2)
        for i in range(low, low + mid):
            if direction == 1 and arr[i] > arr[i + mid] or direction == 0 and arr[i] < arr[i + mid]:
                arr[i], arr[i + mid] = arr[i + mid], arr[i]
                arr[i].red()
                arr[i + mid].red()
                update_display(screen, height, arr, delay)
                reset_colours(arr)
        merge_bits(screen, height, arr, delay,  low, mid, direction)
        merge_bits(screen, height, arr, delay,  low + mid, mid, direction)


def bitonic(screen, height, arr, delay, low, count, direction):
    if count > 1:
        mid = int(count / 2)
        bitonic(screen, height, arr, delay,  low, mid, 1)
        bitonic(screen, height, arr, delay,  low + mid, mid, 0)
        merge_bits(screen, height, arr, delay,  low, count, direction)


def comb(screen, height, arr, delay):
    gap = len(arr)
    swap = True

    while gap != 1 or swap:
        gap = (gap * 10)//13
        if gap < 1:
            gap = 1

        swap = False

        for i in range(0, len(arr)-gap):
            arr[i].red()
            arr[i + gap].red()
            update_display(screen, height, arr, delay)
            reset_colours(arr)
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swap = True


def pigeonhole(screen, height, arr, delay):
    high = None
    low = None

    for val in arr:
        val.red()
        update_display(screen, height, arr, delay)
        val.reset()

        if high is None or high < val:
            high = val
            reset_colours(arr)

        if low is None or low > val:
            low = val
            reset_colours(arr)

        high.orange()
        low.turquoise()
        update_display(screen, height, arr, delay)

    high = high.value
    low = low.value

    size = high - low + 1

    pigeonholes = [0] * size

    for num in arr:
        num.red()
        update_display(screen, height, arr, delay)
        pigeonholes[num.value - low] += 1
        num.reset()

    i = 0
    for count in range(size):
        while pigeonholes[count] > 0:
            pigeonholes[count] -= 1
            arr[i].value = count + low
            arr[i].make_correct()
            update_display(screen, height, arr, delay)
            i += 1


def bubble(screen, height, arr, delay):
    for i in range(len(arr) - 1):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                arr[j].red()
                arr[j + 1].red()
                update_display(screen, height, arr, delay)
            reset_colours(arr)
            selected = arr[j+1]
        selected.make_correct()
        update_display(screen, height, arr, delay)

    arr[0].make_correct()
    update_display(screen, height, arr, delay)
    return arr


def bogo(screen, height, arr, delay):
    while not all(a <= b for a, b in zip(arr, arr[1:])):
        random.shuffle(arr)
        update_display(screen, height, arr, delay)
    return arr
