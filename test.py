a = [{}]
a[0]["a"] = 42

l = ["a"]

for i in a:
    if("a" in i):
        l = [w.replace("a",str(i["a"])) for w in l]

print(l)
