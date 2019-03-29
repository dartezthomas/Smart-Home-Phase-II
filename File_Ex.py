data = open("test.txt", "a")
data.write("Beginning of file!\n")
data.close()

data = open("test.txt", "r")
print(data.read())

