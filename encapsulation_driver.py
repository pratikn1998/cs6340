import os 
import shutil
import numpy as np 
def convert_py_file_to_txt(filePath):
    thisFile = filePath
    base = os.path.splitext(thisFile)[0] + "_as_txt_file"
    shutil.copyfile(thisFile, base + ".txt")
    txt_file_name = base + ".txt"
    return txt_file_name
    # os.rename(thisFile, base + ".txt")

def read_txt_file(filePath):
    base = os.path.splitext(filePath)[0]
    lines = []
    with open(filePath) as f:
        lines = f.readlines()
    instance_vars_sets = set()
    for i in range(0, len(lines)):
        if 'self.' in lines[i]:
            instance_var_split = lines[i].split(' ')
            for iv in range(0, len(instance_var_split)):
                if 'self.' in instance_var_split[iv] and '(' not in instance_var_split[iv] and ')' not in instance_var_split[iv]:
                    curr_iv = instance_var_split[iv].replace('self.', '')
                    instance_vars_sets.add(curr_iv)
    for i in range(0, len(lines)):
        curr_line = lines[i]
        for iv in instance_vars_sets:
            if iv in curr_line and 'def' not in curr_line:
                curr_line = curr_line.replace('self.', 'self._')
                lines[i] = curr_line
    print(lines)
    new_file_name = base + "_protected.txt"
    with open(new_file_name, 'w') as filehandle:
        for listitem in lines:
            filehandle.write('%s\n' % listitem)
    return new_file_name

def convert_txt_to_python(filePath):
    thisFile = filePath
    base = os.path.splitext(thisFile)[0] 
    shutil.copyfile(thisFile, base + ".py")
    txt_file_name = base + ".py"
    return txt_file_name

def main():
    curr_txt_file = convert_py_file_to_txt('test.py')
    protected_txt_file = read_txt_file(curr_txt_file)
    result_py_file = convert_txt_to_python(protected_txt_file)
    print("your new file is: " + result_py_file)

if __name__ == "__main__":
    main()