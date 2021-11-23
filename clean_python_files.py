from encapsulation_driver import Driver
import sys
 
# total arguments
n = len(sys.argv)

# file names 
filenames = []

for i in range(1, n):
    filenames.append(sys.argv[i])

driver = Driver(filenames)
driver.analyze()
