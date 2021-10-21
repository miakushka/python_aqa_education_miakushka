#print my.txt file content
file = open('../my.txt', 'r')
file_content = file.read()
print(file_content)


#create a new file, based on my.txt
new_file = open('test.txt', 'w')
new_file.write(file_content + " modified content")

file.close()
new_file.close()
