# Get a string of text and turn it into sound
from scamp import *
from os import path
from sys import argv
from sys import exit
from hashlib import sha256

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
    if len(argv) > 1:  # Different ways to get the same output
        
        numbers = workWithArgs()
        
    else:
        numbers = workWithFile()
        
    # Get sha256 hash for title
    content = ''
    for num in numbers:  # Grab the list of ordinal char values
        content += str(num)  # Create a single string of numbers

    shaHash = sha256(bytes(content, 'utf-8')).hexdigest()
    half = int(len(shaHash) / 2)
    hex1 = shaHash[0:half]
    hex2 = shaHash[half:]
    
    print(f'[i] Content: {content}\n[i] SHA256 digest: {hex1 + hex2}')

    # Play sound 
    s = Session()
    clarinet = s.new_part('clarinet')
    violin = s.new_part('violin')
    
    s.start_transcribing()  # This will record the performance as it's played
    for x, pitch in enumerate(numbers):
        if x % 2:
            clarinet.play_note(pitch, 1, .2)
        else:
            violin.play_note(pitch, 1, .2)
    s.wait(1)
    recording = s.stop_transcribing()
    
    recording.to_score(title=hex1, composer=hex2).show()  # This will open the performance's pdf sheet music
    recording.to_score(title=hex1, composer=hex2).export_music_xml(f'ciphText-{shaHash[-4:]}.musicxml')
    recording.to_score(title=hex1, composer=hex2).export_pdf(f'ciphText-{shaHash[-4:]}.pdf')