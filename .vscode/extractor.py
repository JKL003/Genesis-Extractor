#import re
import string


from robobrowser import RoboBrowser
from bs4 import BeautifulSoup

def main():

    #Acesses Genesis
    br = RoboBrowser()
    br.open("https://parents.chclc.org/genesis/sis/view?gohome=true")
    form = br.get_form()
    form["j_username"] = "3010476@chclc.org"
    form["j_password"] = "y7cvmz2d"
    br.submit_form(form)

    #Converts the HTML of the grade page into a string
    src = str(br.parsed())

    #Removes all forms of whitespace
    src = src.translate({ord(c): None for c in string.whitespace})

    #Removes all Javascript
    src = src[src.find('<!-- Start of Header-->')+len('<!-- Start of Header-->'): len(src)]

    #Removes all HTML tags
    soup = BeautifulSoup(src)
    src = ''.join(soup.findAll(text=True))

    

    notDone = True
    i = src.find('%')-6
    while(notDone):
        i -= 1
        if(ord(src[i])>=48 and ord(src[i])<=57):
            notDone = False
    
    src = src[i+1:src.rfind('%')+1]

    print(src)
    #print(src[src.find(start)+len(start):src.find(end)+2])



    #print(re.search('%s(.*)%s' % (start, end), src))

    #result = re.search('%s(.*)%s' % (start, end), src).group(1)
    #print(result)


if __name__ == '__main__':
    main()