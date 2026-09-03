from merge import deep_merge
a = {"x": 1, "n": {"y": 2, "z": [1]}}
b = {"n": {"y": 9, "w": 3}, "k": 4}
out = deep_merge(a, b)
assert out == {"x": 1, "n": {"y": 9, "z": [1], "w": 3}, "k": 4}
assert a == {"x": 1, "n": {"y": 2, "z": [1]}}
print("py2 OK")
