def batches(items, n):
    if n < 1:
        raise ValueError("n must be at least 1")
    items = list(items)
    for i in range(0, len(items), n):
        yield items[i:i + n]
