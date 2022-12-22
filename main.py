# Get a string of text and turn it into sound
from scamp import *
from os import path
from sys import argv
from sys import exit


def listToString(targetList):
    string = ''
    for item in targetList:
        string += str(item)
    return string


def convertToNumbers(message):
    numbers = []
    note = []
    
    # 1. If input is a list, use the words in list
    if message == type(list):
        target = message
    
    else:  # Otherwise make a list and have the message be the only elem
        target = []
        target.append(message)
        
    # 2. Proceed to convert to numbers
    for word in message:
        for letter in word:
            numbers.append(ord(letter))
        
    return numbers  
  
  
def workWithArgs():
    return convertToNumbers(argv[1:])
     
     
def workWithFile():
    if path.exists('./message.txt'):
        with open('./message.txt') as file:
            nums = convertToNumbers(file.read())
        return nums
        
    else:
        print('Fill in messages.txt or enter text through commmand line')
        with open('./message.txt', 'w') as file: file.write('Enter stuff here')
        exit(2)
    
            
if __name__ == '__main__':
    
    # Get pitch
    if len(argv) > 1:
        
        numbers = workWithArgs()
        
    else:
        numbers = workWithFile()
        
    # Play sound 
    s = Session()
    clarinet = s.new_part('clarinet')
    violin = s.new_part('violin')
    s.start_transcribing()
    for x, pitch in enumerate(numbers):
        if x % 2:
            clarinet.play_note(pitch, 1, .2)
        else:
            violin.play_note(pitch, 1, .2)
    s.wait(1)
    s.stop_transcribing().to_score(title='Message In a Composition').show()
