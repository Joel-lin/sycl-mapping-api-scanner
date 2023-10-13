#!/root/miniconda3/envs/idp/bin/python

import os
import csv
import sys
import re
#import regex as re
import myarrays_20230926
#from joblib import Parallel, delayed
#from multiprocessing import Manager


def traverse_and_count_ASM_occurrences(folder_path, element_strings):
    #manager = Manager()
    #occur_dict = manager.dict()
    occur_dict = {}
    for element in element_strings:
        occur_dict[element] = 0
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith((".cu", ".cuh", ".cpp", ".c", ".hpp", ".h", ".py")):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r',errors='ignore') as file:
                        contents = file.read()
                            #for line in file:
                            #    contents = line.strip()
                        #occur_dict[element] += contents.count(''.join([" ",element,"("]))
                        #occur_dict[element] += contents.count(''.join([" ",element, " ("]))
                        occur_dict[element] += contents.count(''.join(["\"", element, "."]))
                        occur_dict[element] += contents.count(''.join(["\" ", element,"."]))
    return occur_dict
    
#20230801 trim the spaces of the project folder used in -p
def traverse_and_count_occurrences(folder_path, element_strings):
    #manager = Manager()
    #occur_dict = manager.dict()
    occur_dict = {}
    for element in element_strings:
        occur_dict[element] = 0
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith((".cu", ".cuh", ".cpp", ".c", ".hpp", ".h", ".py")):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r',errors='ignore') as file:
                        contents = file.read()
                            #for line in file:
                            #    contents = line.strip()
                        #occur_dict[element] += contents.count(''.join([" ",element,"("]))
                        #occur_dict[element] += contents.count(''.join([" ",element, " ("]))
                        occur_dict[element] += contents.count(''.join([element,"("]))
                        occur_dict[element] += contents.count(''.join([element, " ("]))
    return occur_dict

def generate_ASM_csv_report(folder_paths, element_strings, brkflag):
    with open("report_ASM.csv", "w", newline="") as file:
        writer = csv.writer(file)
        nested_dict = {}
        header_row = ["folder name"]
        my2ndrow_sum = ["occurence of total unsupported ASMs"]
        for eachfolder_path in folder_paths:
            folder_name = os.path.basename(os.path.dirname(os.path.abspath(eachfolder_path))) + "_" + os.path.basename(os.path.abspath(eachfolder_path))
            header_row += [folder_name]
            nested_dict[folder_name] = traverse_and_count_ASM_occurrences(eachfolder_path,element_strings)
            
            sum_occurrences = sum(nested_dict[folder_name].values())
            my2ndrow_sum += [sum_occurrences]
 
        writer.writerow(header_row)
        writer.writerow(my2ndrow_sum)
        
        max_folders = len(folder_paths)
        
        if brkflag == 1:
            for i, element in enumerate(element_strings):
                # Initialize the row with None values
                row = [None] * (max_folders + 1)
                #if element[-1] == '(':
                    #element = element[:-1]
                #    row[0] = element[:-1]
                #else:
                row[0] = element
                
                #
                #pattern = re.compile(re.escape(element) + r"\s*\(")
                ## Iterate over folder paths
                for j, folder_path in enumerate(folder_paths):
                    folder_name = os.path.basename(os.path.dirname(os.path.abspath(folder_path))) + "_" + os.path.basename(os.path.abspath(folder_path))
                #    # Set the count in the corresponding column
                    row[j + 1] = nested_dict[folder_name][element]
                
                # Write the row to the CSV file
                writer.writerow(row)
                
def generate_csv_report(folder_paths, element_strings, brkflag):
    with open("report.csv", "w", newline="") as file:
        writer = csv.writer(file)
        nested_dict = {}
        # Transpose the header row
        #header_row = ["folder name", "sum of total elements strings"] + element_strings
        # Iterate over folder paths
        header_row = ["folder name"]
        my2ndrow_sum = ["occurence of total unsupported APIs"]
        for eachfolder_path in folder_paths:
            #folder_name = os.path.basename(os.path.abspath(eachfolder_path))
            folder_name = os.path.basename(os.path.dirname(os.path.abspath(eachfolder_path))) + "_" + os.path.basename(os.path.abspath(eachfolder_path))
            #print(folder_name) # "dirname_lastitem" as folder_name
            header_row += [folder_name]
            #occurrences = traverse_and_count_occurrences(eachfolder_path,element_strings)
            #nested_dict[os.path.basename(os.path.abspath(eachfolder_path))] = traverse_and_count_occurrences(eachfolder_path,element_strings)
            nested_dict[folder_name] = traverse_and_count_occurrences(eachfolder_path,element_strings)
            
            sum_occurrences = sum(nested_dict[folder_name].values())
            #for each_occur in nested_dict[folder_name].values():
            #    sum_occurrences = sum_occurrences + 1
            
            #print(nested_dict[folder_name].values())#debug
            my2ndrow_sum += [sum_occurrences]
 
        writer.writerow(header_row)
        writer.writerow(my2ndrow_sum)
        #transposed_header = [[cell] for cell in header_row]
        
        # Write the transposed header row
        #writer.writerows(transposed_header) 

        # Determine the maximum number of folders
        max_folders = len(folder_paths)
        
        #debug
        #for eachfolder_path in folder_paths:
        #    for key, value in nested_dict[os.path.basename(os.path.abspath(eachfolder_path))].items():
        #        print(f"{key,value}")
        
        if brkflag == 1:
            
            # Iterate over element strings
            for i, element in enumerate(element_strings):
                # Initialize the row with None values
                row = [None] * (max_folders + 1)
                
                # Set the element string in the first column
                #if element[-1] == '(':
                    #element = element[:-1]
                #    row[0] = element[:-1]
                #else:
                row[0] = element
                
                #
                #pattern = re.compile(re.escape(element) + r"\s*\(")
                ## Iterate over folder paths
                for j, folder_path in enumerate(folder_paths):
                    #folder_name = os.path.basename(os.path.abspath(folder_path))
                    folder_name = os.path.basename(os.path.dirname(os.path.abspath(folder_path))) + "_" + os.path.basename(os.path.abspath(folder_path))
                #    count = traverse_and_count_single_str(folder_path, element, pattern)
                #    
                #    # Set the count in the corresponding column
                    row[j + 1] = nested_dict[folder_name][element]
                
                # Write the row to the CSV file
                writer.writerow(row)


def print_table(headers, rows):
    # Calculate column widths
    column_widths = [max(len(str(row[i])) for row in rows + [headers]) for i in range(len(headers))]

    # Print headers
    for i, header in enumerate(headers):
        print(f"{header:{column_widths[i]}}", end="  ")
    print()

    # Print separator line
    #print("-" * (sum(column_widths) + (3 * len(headers) - 1)))

    # Print rows
    sumofnonzerorow = 0
    for rowindex, row in enumerate(rows):
        if rowindex == 1:
            print("-" * (sum(column_widths) + (3 * len(headers) - 1)))
        row_values = row[1:]  # Exclude the first column
        if sum(map(float, row_values)) != 0:  # Check if sum of non-zero values is non-zero
            sumofnonzerorow += 1
            for i, value in enumerate(row):
                print(f"{value:{column_widths[i]}}", end="  ")
            print()
            
    print("-" * (sum(column_widths) + (3 * len(headers) - 1)))
    if sumofnonzerorow >= 1:
        print(f"{sumofnonzerorow-1}" + " unique unsupported APIs(or ASMs) are likely being used in the project")


        
def print_howtofindstr():
    print("")
    print("--------------------------------------------------------------------------------------")
    print("You can use the following commands to find where are these unsupported APIs in codes lines numbers")
    print("")
    print("    windows: findstr /S /N <APIs name> <projectfolderpath>\*.cu")
    print("    Linux: grep -rn <APIs name> <projectfolderpath>/*.cu")
    print("")

def print_report(reportfilename):
    with open(reportfilename, "r") as file:
        reader = csv.reader(file)
        rows = list(reader)
        headers = rows.pop(0)  # Assume the first row contains headers
    
        # Display table
        print_table(headers, rows)
        print_howtofindstr()
        
if __name__ == '__main__':
    folder_paths = []  # List of folder paths specified with -p parameter
    
    brkflag = 1
    if '--breakdown' in sys.argv:
        brkflag = 1 
        
    if '-p' in sys.argv:
        folder_paths = sys.argv[sys.argv.index('-p') + 1]
        folder_paths="".join(folder_paths).split(',')
        for i, folder_path in enumerate(folder_paths):
            folder_path = folder_path.lstrip()
            folder_path = folder_path.rstrip()
            folder_paths[i] = folder_path
            dirname = os.path.basename(os.path.dirname(os.path.abspath(folder_path))) + "_" + os.path.basename(os.path.abspath(folder_path))
            print(dirname)
    
        element_strings = []  # List of element strings from myarrays2 module
        #ASM_element_strings = [] # list of ASM_API_migration_status arrary
        module_vars = vars(myarrays_20230926)
    
        for var_name, var_value in module_vars.items():
            if isinstance(var_value, list) and var_name != "ASM_API_migration_status":
                element_strings.extend(var_value)
                #print(var_name)
        #for mystr in myarrays_20230926.ASM_API_migration_status:
        #    print(mystr)
        
        generate_csv_report(folder_paths, element_strings, brkflag)
        print("report.csv should be generated.")
        print_report("report.csv")
        
        generate_ASM_csv_report(folder_paths, myarrays_20230926.ASM_API_migration_status, brkflag)
        print("report_ASM.csv should be generated. use \"--printcsv report_ASM.csv\" to list unsupported PTXs if there is")
        
        
    elif '--printcsv' in sys.argv:
        index = sys.argv.index('--printcsv')
        if index < len(sys.argv) - 1:  # Check if there is an extra parameter
            reportfile = sys.argv[index + 1]
        else:
            reportfile = "./report.csv"
        print_report(reportfile)
        
    else: #usage
        print("")
        print("Brief:")
        print("  This utility mainly scans the preset filetypes(.cu, .cuh, .c, .h, .cpp, .hpp, .py and etc..) to find unsupported APIs listed by SYCLomatic project.\
 Reference link(2023-10-12):https://oneapi-src.github.io/SYCLomatic/dev_guide/api-mapping-status.html")
        print("")
        print("  Please specify the folder path using the -p parameter.")
        print("")
        print("  -p <projectfolderpath>     specify the CUDA migration projects folder path.")
        #print("       --breakdown           provide the breakdown details of unsupported APIs.")
        print("  --printcsv                 print report(experimental)")
        print("  ")
        print("Example usages:")
        print("  ")
        print("    1. sycl_mapping_APIs_scanner -p <cudaproject_folderpath>")
        print("  ")
        print("    2. sycl_mapping_APIs_scanner --printcsv <examplereport.csv>")
        print("  ")


