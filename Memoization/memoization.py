import time

cache = {}

def compute(num):
    if num in cache:
        return cache[num]

    print('Computing {}...'.format(num))
    time.sleep(1)
    result = num ** 2
    cache[num] = result
    return result

result = compute(4)
print(result)

result = compute(10)
print(result)

result = compute(4)
print(result)

result = compute(10)
print(result)