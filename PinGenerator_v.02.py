'''
Pin Generator v.02

This script can be used to general a custom length list of numbers for use with brute force tools.  
The list can contain all numbers in a range, or numbers that form a pattern.  The output file
can be broken up by file size.

https://github.com/Joeschmoe7/Pin-Generator

'''

import argparse
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description="Pin Generator v.02")
    parser.add_argument("-m", "--min_length", type=int, help="Minimum length of the PIN.")
    parser.add_argument("-x", "--max_length", type=int, help="Maximum length of the PIN.")
    parser.add_argument("-o", "--output_dir", help="Output directory to save the generated PINs.")
    parser.add_argument("-s", "--file_size" , type=int, help="File size limit in MB (Default 50MB).")
    
    group = parser.add_mutually_exclusive_group()
    
    group.add_argument("--quick", action='store_true', help='Quick patterns only.  Skips the lengthy search.')
    group.add_argument('--all', action='store_true', help='Print all numbers in the given range.')
    
    return parser.parse_args()

def get_min_length():      #Prompt for minium PIN length if not already added as an argument
    min_length = parse_arguments().min_length
    if min_length is None:
        while True:
            min_length_input = input('Enter the minimum PIN length: ')
            if min_length_input.isdigit():
                return int(min_length_input)
            else:
                print("That doesn't look like a number skippy")

    return min_length

def get_max_length():       #Prompt for maximum PIN length if not already added as an argument
    max_length = parse_arguments().max_length
    if max_length is None:
        while True:
            max_length_input = input('Enter the maximum PIN length: ')
            if max_length_input.isdigit():
                return int(max_length_input)
            else:
                print("That doesn't look like a number, skippy. Try again.") 

    return max_length

def generate_pins(min_length, max_length):    #Generate a list of all numbers within the provided range
    number_list = []
    for length in range(min_length, max_length + 1):
        for num in range(10 ** length):
            zero_num = str(num).zfill(length)   #Add leading zeros
            number_list.append(zero_num)
            if num >= 10 ** length:
                number_list.append(num)      
    return number_list

def find_same_number(number_list):   #Finds PINS with all the same digits
    same_set = set()
    for number in number_list:
        if len(set(number)) == 1:
            same_set.add(number) 
    return sorted(same_set)

def find_sequential(number_list, min_length):  #Finds sequential pins
    seq_set = set()
    for number in number_list:
        if number.startswith("00"):
            continue
        current_length = len(number)
        digits = list(map(int, number))
        consecutive = True
        for i in range(1, len(digits)):
            if digits[i] != digits[i - 1] + 1:
                consecutive = False
                break
        if consecutive:
            seq_set.add(number.zfill(min_length))  #add leading zeros
    return sorted(seq_set) #Sorts the results to make it easier to review the PIN list

def find_reverse(number_list, min_length):  #Finds reverse sequential pins
    rev_set = set()    
    for number in number_list:
        if number.startswith("00"):
            continue
        current_length = len(number)
        digits = list(number)
        consecutive = True
        for i in range(1, len(digits)):
            if int(digits[i]) != int(digits[i - 1]) - 1:
                consecutive = False
                break
        if consecutive:
            rev_set.add(str(number).zfill(min_length))  
    return sorted(rev_set)

def find_pattern(number_list):   #Looks for repeating patterns
    pattern_set = set()
    for number in number_list:
        if len(number) >= 2:
            pattern = number[0:2]
            if pattern * (len(number) // 2) + pattern[:len(number) % 2] == number:
                pattern_set.add(number) 
        if len(number) >= 6:
            pattern = number[:3]  
            if pattern * (len(number) // 3) + pattern[:len(number) % 3] == number:
                pattern_set.add(number)  
        if len(number) >= 7:  
            pattern = number[:4] 
            if pattern * (len(number) // 4) + pattern[:len(number) % 4] == number:
                pattern_set.add(number)   
        if len(number) >= 9:  
            pattern = number[:5]  
            if pattern * (len(number) // 5) + pattern[:len(number) % 5] == number:
                pattern_set.add(number)          
        if len(number) >= 11:  
            pattern = number[:6]  
            if pattern * (len(number) // 6) + pattern[:len(number) % 6] == number:
                pattern_set.add(number)
            if len(number) >= 13:  
                pattern = number[:7]  
                if pattern * (len(number) // 7) + pattern[:len(number) % 7] == number:
                    pattern_set.add(number)
    return sorted(pattern_set)

def write_list_to_files(number_list, min_length, filename_base="PIN_List_"):
    current_file = 1
    current_file_size = 0
    if parse_arguments().file_size is None:  #Check if a file size arguement was added
        size_limit = 50 * 1024 * 1024   #Megabytes to bytes
    else:
        size_limit = parse_arguments().file_size * 1024 * 1024
        
    if parse_arguments().quick is True:    #If Quick option selected, skip the long pattern search.
        pin_lists = [find_same_number(number_list), find_sequential(number_list, min_length), find_reverse(number_list, min_length)]
    
    elif parse_arguments().all is True:  #iI All option is selected, print all numbers in the list.
        pin_lists = [number_list]
        
    else:
        pin_lists = [find_sequential(number_list, min_length), find_reverse(number_list, min_length), find_pattern(number_list)]  #Run everything
    
    file_location = parse_arguments().output_dir + "/"
    with open(f"{file_location}{filename_base}{current_file}.txt", "w") as f:
        for lists in pin_lists:      
            for item in lists:
                line = f"{item}\n"
                current_file_size += len(line.encode())
                if current_file_size > size_limit:   #Splits the output files by size
                    f.close()
                    current_file += 1
                    current_file_size = 0
                    f = open(f"{file_location}/{filename_base}{current_file}.txt", "w")
                f.write(line)

def main():
    min_length = get_min_length()
    max_length = get_max_length()
    number_list = generate_pins(min_length, max_length)
    write_list_to_files(number_list, min_length)

if __name__ == "__main__":
    main()
