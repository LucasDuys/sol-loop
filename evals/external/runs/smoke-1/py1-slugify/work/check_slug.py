from slug import slugify
assert slugify("Hello,  World!") == "hello-world"
assert slugify("  A--B__c  ") == "a-b-c"
assert slugify("x") == "x"
print("py1 OK")
