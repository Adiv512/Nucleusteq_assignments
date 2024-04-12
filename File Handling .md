```python
# Open a file in read mode
file = open("example.txt", "r")

# Open a file in write mode (creates a new file if it doesn't exist)
file = open("example.txt", "w")

# Open a file in append mode (creates a new file if it doesn't exist)
file = open("example.txt", "a")

# Open a file in binary mode
file = open("example.txt", "rb")

# Open a file in text mode (default mode)
file = open("example.txt", "rt")
```



```python
# Read the entire file
content = file.read()

# Read a specific number of bytes
content = file.read(10)

# Read a single line from the file
line = file.readline()

# Read all lines into a list
lines = file.readlines()
```



```python
# Write content to the file
file.write("Hello, world!")

# Write multiple lines to the file
lines = ["Line 1\n", "Line 2\n", "Line 3\n"]
file.writelines(lines)
```


   


```python
import os

# Check if a file exists
if os.path.exists("example.txt"):
    print("File exists")
else:
    print("File does not exist")
```

    File does not exist
    


```python
#to delete file
import os
os.remove("example.txt")
```


   


```python

```
