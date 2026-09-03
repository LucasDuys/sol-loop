from batches import batches
assert list(batches([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]
assert list(batches([], 3)) == []
try:
    list(batches([1], 0))
    raise SystemExit("expected ValueError")
except ValueError:
    pass
print("py3 OK")
