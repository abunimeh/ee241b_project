"""
This file contains helper functions for parsing a Verilog RTL file.

Note that this assumes the Verilog-2001 way of declaring inputs
module asdf (N1, N2, N3, ...);

    input N1, N2, N3;
    output N4, N5, N6;

endmodule
"""
import re
def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w)).search

class VerilogParser(object):
    def parseForString(self, string):
        return_string = ""
        parsing_section = False
        with open(self.verilog_file_path, 'r') as f:
            for line in f:
                if parsing_section:
                    return_string = return_string + line
                if findWholeWord(string)(line):
                    parsing_section = True
                    return_string = return_string + line
                if ';' in line and parsing_section == True:
                    break

        return_string = return_string.replace('\r', '')
        return_string = return_string.replace('\n', '')
        return_string = return_string.replace(' ', '')
        return_string = return_string.replace(string, '')
        return_string = return_string.replace(';', '')
        return_value = return_string.split(',')
        return return_value 

    def findModuleName(self):
        module_string = ""
        with open(self.verilog_file_path, 'r') as f:
            for line in f:
                if findWholeWord('module')(line):
                    module_string = line
                    break
        module_string = module_string.replace('module', '')
        module_string = module_string.split('(')
        return module_string[0].strip()
    
    def __init__(self, verilog_file_path):
        self.verilog_file_path = verilog_file_path
        print("Created VerilogParser to parse Verilog file at path: %s" % (self.verilog_file_path))
        self.inputs = self.parseForString('input')
        self.outputs = self.parseForString('output')
        self.module_name = self.findModuleName()

        print("Parsed Verilog module name: %s" % (self.module_name))

        print("Found these inputs to the Verilog module: %s" % (self.inputs))
        print("Num inputs: %d" % (len(self.inputs)))

        print("Found these outputs from the Verilog module: %s" % (self.outputs))
        print("Num outputs: %d" % (len(self.outputs)))

