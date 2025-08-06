text = "int i = 0; int j = 1; bool k = true"
text = [x.strip() for x in text.split(";")]
stack = []
for line in text:
    if line.startswith("int"):
        pass
    elif line.startswith("bool"):
        pass
    elif 