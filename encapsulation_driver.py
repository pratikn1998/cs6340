import os 
import shutil

class Driver:
    def __init__(self, files):
        self._modified_classes = {}
        self._files = files 

    def convert_py_file_to_txt(self, filePath):
        thisFile = filePath
        base = os.path.splitext(thisFile)[0] + "_as_txt_file"
        shutil.copyfile(thisFile, base + ".txt")
        txt_file_name = base + ".txt"
        return txt_file_name

    def read_txt_file(self, filePath):
        base = os.path.splitext(filePath)[0]
        lines = []
        with open(filePath) as f:
            lines = f.readlines()
        
        return base, lines

    def find_classes(self, lines):
        curr_start, curr_end = None, None
        class_lines, other_lines = [], []
        i = 0
        while i < len(lines):
            if 'class' in lines[i]:
                curr_start = i
                i += 1
                while lines[i][0] == ' ':
                    i += 1
                curr_end = i 
                class_lines.append(lines[curr_start:curr_end])
                curr_start, curr_end = None, None
            else:
                # Not code for a class 
                curr_start = i 
                i += 1
                while i < len(lines) and 'class' not in lines[i]:
                    i += 1
                curr_end = i
                other_lines.append(lines[curr_start:curr_end])
                curr_start, curr_end = None, None

        return class_lines, other_lines

    def add_getters_and_setters(self, class_lines):
        for _class in class_lines:
            #get the variables that should be instance variables 
            class_name, instance_vars_sets = self.get_instance_variables(_class)
            #replace instance variables with _ if it doesn't have it 
            for i in range(0, len(_class)):
                curr_line = _class[i]
                for iv in instance_vars_sets:
                    if iv in curr_line and 'def' not in curr_line and 'self._' not in curr_line:
                        curr_line = curr_line.replace('self.', 'self._')
                        _class[i] = curr_line

            iv_dict_setters_getters = self.check_if_iv_setter_getters(instance_vars_sets, _class)
            #print(iv_dict_setters_getters)
            for i in iv_dict_setters_getters:
                if iv_dict_setters_getters[i]['setter'] == False:
                    first_line = '    def set_' + i + '(self, new_' + i + '):\n'
                    second_line = '        self._'+i + ' = ' + 'new_' + i
                    _class.append(first_line)
                    _class.append(second_line)
                if iv_dict_setters_getters[i]['getter'] == False:
                    first_line = '    def get_' + i + '(self):\n'
                    second_line = '        return self._'+i
                    _class.append(first_line)
                    _class.append(second_line)
                    
            self._modified_classes[class_name] = instance_vars_sets
        return class_lines

    def use_setters_and_getters(self, other_lines):
        modified_classes = []
        variables_reffering_to_modified_classes = {}
        
        # key modified class names
        for key in self._modified_classes.keys():
            modified_classes.append(key)

        # find all variables initializing modified classses 
        for _other in other_lines:
            for line in _other:
                if any(modified_class in line for modified_class in modified_classes) and '=' in line:
                    mod_class = line.split('=')[1].split('(')[0][1:]
                    var = line.split(' ')[0]
                    variables_reffering_to_modified_classes[var] = mod_class
        
        for _other in other_lines:
            for i in range(0, len(_other)):
                line = _other[i]
                if any(var in line for var in variables_reffering_to_modified_classes.keys()) and not any(modified_class in line for modified_class in modified_classes):
                    # Replace with setter 
                    if '.' in line and '=' in line:
                        # 1. find variable, attribute, and value
                        var = line.split('.')[0]
                        attr = line.split('.')[1].split('=')[0][:-1]
                        value = line.split('.')[1].split('=')[1][1:].replace("\n", "")
                        # 2. find modded class 
                        modded_class = variables_reffering_to_modified_classes[var]
                        # 3. find modded class' iv
                        iv = self._modified_classes[modded_class]
                        # 4. sanity check if attr is iv 
                        if attr not in iv:
                            continue
                        # replace with setter 
                        _other[i] = var+'.set_'+attr+'('+value+')'
                
                    # Replace with getter 
                    else:
                        # 1. find variable
                        var = None
                        for v in variables_reffering_to_modified_classes.keys():
                            if v in line:
                                var = v
                                break
                        # 2. find modded class 
                        modded_class = variables_reffering_to_modified_classes[var]
                        # 3. find modded class' iv
                        iv = self._modified_classes[modded_class]
                        # 4. find atttribute
                        attr = None
                        for v in iv:
                            if v in line:
                                attr = v
                                break
                        # 5. sanity check
                        if attr is None:
                            break
                        # 6. get indices to mod
                        start_index = line.find(var)
                        end_index = line.find(attr) + len(attr)
                        begin_of_line = line[0:start_index]
                        end_of_line = line[end_index:]
                        # replace with getter
                        _other[i] = begin_of_line+var+'.get_'+attr+'()'+end_of_line
                    
        return other_lines

    def get_instance_variables(self, lines):
        working_on_class = None
        instance_vars_sets = set()
        for i in range(0, len(lines)):
            if 'class' in lines[i]:
                working_on_class = lines[i].split(" ")[1][:-2]
            if 'self.' in lines[i]:
                instance_var_split = lines[i].split(' ')
                for iv in range(0, len(instance_var_split)):
                    if 'self.' in instance_var_split[iv] and '(' not in instance_var_split[iv] and ')' not in instance_var_split[iv]:
                        curr_iv = instance_var_split[iv].replace('self.', '')
                        instance_vars_sets.add(curr_iv)
        return working_on_class, instance_vars_sets

    def check_if_iv_setter_getters(self, instance_vars_set, lines):
        iv_dict_setters_getters = {}
        for i in instance_vars_set:
            iv_dict_setters_getters[i] = {
                'setter': False,
                'getter': False
            }
        in_init_func = False
        for i in instance_vars_set:
            for lin in lines:
                if 'def __init__' in lin:
                    in_init_func = True
                if 'def' in lin and 'def __init__' not in lin:
                    in_init_func = False 
                if 'self._' + i in lin and '=' in lin and not in_init_func:
                    iv_dict_setters_getters[i]['setter'] = True
                if 'return' in lin and i in lin:
                    iv_dict_setters_getters[i]['getter'] = True
        return iv_dict_setters_getters

    def convert_new_lines_to_txt(self, base, class_lines, other_lines):
        new_file_name = base + "_protected.txt"
        with open(new_file_name, 'w') as filehandle:
            for _class in class_lines:
                for listitem in _class:
                    filehandle.write('%s\n' % listitem)
            for _other in other_lines:
                for listitem in _other:
                    filehandle.write('%s\n' % listitem)
        return new_file_name

    def convert_txt_to_python(self, filePath):
        thisFile = filePath
        base = os.path.splitext(thisFile)[0] 
        shutil.copyfile(thisFile, base + ".py")
        txt_file_name = base + ".py"
        return txt_file_name

    def analyze(self):
        for file in self._files:
            curr_txt_file = self.convert_py_file_to_txt(file)
            base, lines = self.read_txt_file(curr_txt_file)
            class_lines, other_lines = self.find_classes(lines)
            class_lines = self.add_getters_and_setters(class_lines)
            other_lines = self.use_setters_and_getters(other_lines)
            protected_txt_file = self.convert_new_lines_to_txt(base, class_lines, other_lines)
            result_py_file = self.convert_txt_to_python(protected_txt_file)
            print("your new file is: " + result_py_file)
