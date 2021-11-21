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

    #get the variables that should be instance variables 
    instance_vars_sets = get_instance_variables(lines)
    #replace instance variables with _ if it doesn't have it 
    for i in range(0, len(lines)):
        curr_line = lines[i]
        for iv in instance_vars_sets:
            if iv in curr_line and 'def' not in curr_line and 'self._' not in curr_line:
                curr_line = curr_line.replace('self.', 'self._')
                lines[i] = curr_line

    
    iv_dict_setters_getters = check_if_iv_setter_getters(instance_vars_sets, lines)
    print(iv_dict_setters_getters)
    for i in iv_dict_setters_getters:
        if iv_dict_setters_getters[i]['setter'] == False:
            first_line = '    def set_' + i + '(self, new_' + i + '):\n'
            second_line = '        self._'+i + ' = ' + 'new_' + i
            lines.append(first_line)
            lines.append(second_line)
        if iv_dict_setters_getters[i]['getter'] == False:
            first_line = '    def get_' + i + '(self):\n'
            second_line = '        return self._'+i
            lines.append(first_line)
            lines.append(second_line)
        

    #def convert new lines to txt file 
    new_file_name = convert_new_lines_to_txt(base, lines)
    
    return new_file_name
def get_instance_variables(lines):
    instance_vars_sets = set()
    for i in range(0, len(lines)):
        if 'self.' in lines[i]:
            instance_var_split = lines[i].split(' ')
            for iv in range(0, len(instance_var_split)):
                if 'self.' in instance_var_split[iv] and '(' not in instance_var_split[iv] and ')' not in instance_var_split[iv]:
                    curr_iv = instance_var_split[iv].replace('self.', '')
                    instance_vars_sets.add(curr_iv)
    return instance_vars_sets
def check_if_iv_setter_getters(instance_vars_set, lines):
    iv_dict_setters_getters = {}
    for i in instance_vars_set:
        iv_dict_setters_getters[i] = {
            'setter': False,
            'getter': False
        }
    for i in instance_vars_set:
        for lin in lines:
            if 'self._' + i in lin and '=' in lin:
                iv_dict_setters_getters[i]['setter'] = True
            if 'return' in lin and i in lin:
                iv_dict_setters_getters[i]['getter'] = True
    return iv_dict_setters_getters
    


def convert_new_lines_to_txt(base, lines):
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