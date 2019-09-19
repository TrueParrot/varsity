'''
Add before command handlers & event handlers but after definitions.
Then add our code under the on_message(message) event handler to yours

'''
def filter(message):
    '''
    Advanced Message Filtering System; Accounts for usual types of bypasses such as using formatting and spacing out characters
    Has some flaws such as being able to bypass by typing like th is

    '''
    cFilter = False
    textFilter = ["WORDS", "TO", "FILTER"]
    contents = message.content.translate({ord(i): None for i in '"`_*~.?!-<>[\/()]{}'}).split() #Makes things a tad bit more tricky to bypass, also ignore formatting
    index = 0
    for word in contents:
        if word.upper() in textFilter:
            cFilter = True
        if len(word) == 1: #Assume they're doing this space by space
            reconstructing = True
            adder = 1
            string = "" + word
            while reconstructing:
                try:
                    string = string + contents[index+adder]
                    if len(contents[index+adder]) == 1:
                        adder = adder + 1
                    else:
                        reconstructing = False
                except IndexError:
                    reconstructing = False
            if string.upper() in textFilter:
                cFilter = True
        index = index + 1
    return cFilter
    
@client.event()
def on_message(message):
    isFiltered = filter(message) #Returns true for is filtered; False for not filtered;
    if isFiltered: #If the result is True then
        await message.delete(delay=None) #Delete the message instantly
    #Rest of your code below here
