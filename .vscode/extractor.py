import course
import assignment
import datetime
import re
import string


from robobrowser import RoboBrowser
from bs4 import BeautifulSoup

# Global variables
studentName = ""
courses = list(map(course.Course,[]))

# Body
def main():
    br = RoboBrowser(parser='html.parser')

    mainpageGrades = extractMainPage(br)


def extractMainPage(robo):
    br = robo
    br.open("https://parents.chclc.org/genesis/sis/view?gohome=true")
    form = br.get_form()
    form["j_username"] = "3010476@chclc.org"
    form["j_password"] = "y7cvmz2d"
    br.submit_form(form)

    #Converts the HTML of the grade page into a string
    src = str(br.parsed())

    #Removes initial Javascript
    src = src[src.find('<!-- Start of Header-->')+len('<!-- Start of Header-->'): len(src)]

    #Removes all HTML tags
    soup = BeautifulSoup(src,"lxml")
    src = ''.join(soup.findAll(text=True))
    
    #Removes all tabs and newlines
    src = " ".join(src.split())
    studentName = src[src.index("Select Student:")+16:src.index("Weekly Summary")-1]    

    #Cuts the string into the important parts
    notDone = True
    i = src.find('Fri')+3 #Consistent and close reference point
    while(notDone):
        i += 1
        if(ord(src[i])>=57):
            notDone = False
    src = src[i+2:src.rfind('%')+1]
    
    #Parses the text
    courseInfo = src.split('%')
    courseInfo.pop()
    for i in range(len(courseInfo)):
        courseInfo[i] = courseInfo[i].split("Email:")
        if(i != 0):
            courseInfo[i][0] = courseInfo[i][0][11:len(courseInfo[i][0])]
    
        
        # Separate info
        cInfo = courseInfo[i][0]
        cName = cInfo[0:cInfo[0:cInfo.index(",")].rfind(" ")]
        cTeacher = cInfo[cInfo[0:cInfo.index(",")].rfind(" ")+1:len(cInfo)-1]

        # Create course
        c = course.Course(cName,cTeacher,"P")
        # Add assignments from List Assignments tab (click on link) 
        # Example: c.addAssignment("a1",10,10,assignment.Category.MajorAssessment,datetime.datetime.today().date)
        courses.append(c)
        
    # Test by printing info
    print("Student: " + studentName)
    for i in range(len(courses)):
        print(str(courses[i].currentMPGrade) + " in " + courses[i].courseName 
        + " with " + courses[i].teacherName + " during " + courses[i].period)

    return courseInfo
   

if __name__ == '__main__':
    main()


