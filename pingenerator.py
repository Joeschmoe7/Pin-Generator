#PIN generator

while True:
     minLength = input('Enter the minimum PIN length: ')
     if minLength.isdigit():
          minLength = int(minLength)
          break
     else:
          print("That doesn't look like a number skippy")
            
while True:
     maxLength = input('Enter the maximum PIN length: ')
     if maxLength.isdigit():
          maxLength = int(maxLength)
          break
     else:
          print("That doesn't look like a number, skippy. Try again.")   

digitList = []
for digits in range(minLength, maxLength + 1):
     digitList.append(digits)
     
number_list = []

for length in digitList:
     for num in range(10**(length)):
          zeroNum = str(num).zfill(length)
          number_list.append(zeroNum)
          if num >= 10**(length):
               number_list.append(num)
          
pattern_list = []

def samenumber():
     for number in number_list:
          if len(set(number)) == 1:
               pattern_list.append(number) 
               
def sequential():
     """
     This function finds sequential numbers in a list of strings (including leading zeros).

     Args:
         number_list: A list of strings representing multi-digit numbers.

     Returns:
         A list containing numbers (strings) that are sequential.
     """

     for number in number_list:
          # Remove leading zeros if more than one
          if number.startswith("00"):
               continue

          # Calculate the length of the current number
          current_length = len(number)

          # Convert the number string to a list of digits (as strings)
          digits = list(number)

          # Check for consecutive digits throughout the number
          consecutive = True
          for i in range(1, len(digits)):
               if int(digits[i]) != int(digits[i - 1]) + 1:
                    consecutive = False
                    break

          if consecutive:
               pattern_list.append(str(number).zfill(minLength))
               
def reverse():
     """
     This function finds sequential numbers in a list of strings (including leading zeros).

     Args:
         number_list: A list of strings representing multi-digit numbers.

     Returns:
         A list containing numbers (strings) that are sequential.
     """

     for number in number_list:
          # Remove leading zeros if more than one
          if number.startswith("00"):
               continue

          # Calculate the length of the current number
          current_length = len(number)

          # Convert the number string to a list of digits (as strings)
          digits = list(number)

          # Check for consecutive digits throughout the number
          consecutive = True
          for i in range(1, len(digits)):
               if int(digits[i]) != int(digits[i - 1]) - 1:
                    consecutive = False
                    break

          if consecutive:
               pattern_list.append(str(number).zfill(minLength))
     
def patterns():
     for number in number_list:
          if len(number) == 4:
               if number[0:2] == number[-2:]:
                    pattern_list.append(number)
          if len(number) == 6:
               if number[0:3] == number [-3:]:
                    pattern_list.append(number)
               if number[0:2] ==  number[3:4]:
                    if number[3:4] == number[-2:]:
                         pattern_list.append(number)
def fileWrite():                      
     with open('pinlist.txt', 'w') as file:
          for lines in pattern_list:
               file.write(lines + '\n')

#samenumber()
#sequential()
#reverse()
patterns()  
fileWrite()
            
'''
TO DO

Test error checking for inputs
Add test to make sure max is <= min
more random patters
test to make sure file exists
add common numbers
'''
          
