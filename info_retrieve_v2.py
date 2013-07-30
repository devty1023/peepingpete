#!/usr/bin/python

import mechanize
import sys
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def getAttr(input):
  raw = ""
  for entry in input.split('\n'):
    if "dddefault" in entry and "/TD" in entry and (entry.__len__() <= 70 or "email" in entry):
      raw += entry + "\n"
  raw = strip_tags(raw)
  #print raw

  elem = 0
  ret = []
  temp = []
  for entry in raw.split('\n'): # there are six attributes to consider
    temp.append(entry)
    elem = (elem + 1) % 7
    if(elem == 0): # section information has been processed
      ret.append(temp)
      temp = []

    
  #print ret
  return ret

      
  

def parseInput(input):
  """
  Returns a tuple of type (input_type, course dep/None, courser num/crn)  
  given a user unput, parseInput does it's best to understand what is going on

  It broadly accepst two types of input
  1: CRN
  Simple string of numbers
  2: Course Number
  e.g. cs252
  Spaces and capitalizations are okay as an input

  if not a good input, returns (-1 -1 -1)
  """


  # conver to lower case and classify
  input = input.upper(); 	# convert to lower
  input = input.replace(' ','') # remove spaces

  # if all digits are not numbers, we have a course number
  if ~input.isdigit():
    index = 0		# get division cs|252
    for char in input:
      if char.isdigit():
	break 
      index += 1

   # check 1: course number must be 3 <= digits <= 5
    if ( (input.__len__() - index) != 3 ) and ( (input.__len__() - index) != 5 ) :
      return None

    if ( (input.__len__() - index) == 3): # should add 00 at the end
      input = input + "00"

    return (0, input[0:index], input[index:input.__len__()])

  # else, we have a crn
  else:
    # check: input must have five digits
    if input.__len__() != 5:
      return None

    return (1, None, input)


def getMypurdue(input):
  """
  Returns a tupe of type (bool: availablilty, str to print if bool is true)
  accepst input returned by parseInput
  """
  if input == None:
    #print "err: bad input"
    return None


  br = mechanize.Browser()
  # set some headers
  br.set_handle_robots(False)
  br.addheaders = [('User-agent', 'Firefox')]

  # open schedule
  br.open("http://wl.mypurdue.purdue.edu/schedule")

  # select form
  br.form = list( br.forms() )[0]
  br['p_term'] = ['201410'] # 201410 = fall 2013

  # submit the form
  br.submit()			
  
  #print br.response().read()

  # Now we are in course selection mode
  br.form = list( br.forms() )[0]
  try :
    for control in br.form.controls:
      if control.name == 'sel_subj' and control.type == 'select':
        control.value = [input[1]]
      if control.name == 'sel_crse' and control.type == 'text':
        control.value = input[2]

  except:
     #print "bad input"
     return None


  br.submit()


  # STEP 1: Get all course attributes
  # PROBLEM: If html is too long (> 60000 chars) bs4 simply cuts it
  # Let's follow the following heuristic
  # 1. start at base 50000
  # 2. Find where it is "okay" to cut 
  # 3. Cut and parse
  # 4. Accumulate result
  # 5. make attr_all

  html = br.response().read() # this may be too long: FIXED
  attr_all = getAttr(html);
  #print attr_all
  # now we need to find the link to the course
  links = []
  for link in br.links():
    if (link.text is not None) and (input[1] in link.text) and (input[2] in link.text):
      # all the follwing links must be of some value
      links.append(link)
      #br.back()

  if not links:
    #print "course not found"
    return None

  # visit links and get seats/waitlist seats
  val_all = []
  for link in links:
    br.follow_link(link)
    html = br.response().read()
    val_current = getAttr(html)  # GET ALL SEAT INFORMATION
    
    # LETS CLEAN COURSE NAME HERE
    course_raw = link.text
    course_title = link.text.split(' -')[0]
    course_num = link.text.split(' -')[2]
    course = course_num + ": " + course_title
    val_current.append(course)
    val_all.append(val_current)
    br.back()

  #print val_all
  # clean up lists (parse out avaialbe seats
  vals_clean = []
  for item in val_all:
    tmp = []
    tmp.append(item[1])
    tmp.append(item[0][2])
    vals_clean.append(tmp)

  #print vals_clean
  #print len(vals_clean)

  try:
    assert len(vals_clean) == len(attr_all)
  except AssertionError:
    print "vals clean=%d attr_all=%d" % ( len(vals_clean), len(attr_all) )
    return None

  # NOW WE MERGE ATTRIBUTES AND Course Values
  ret_fin = []
  ret_temp = []
  for i in range(0, len(vals_clean)):
    ret_temp.append( vals_clean[i][0] ) # course name
    ret_temp.append( attr_all[i][1] )   # time
    ret_temp.append( attr_all[i][5] ) 	# type of section
    ret_temp.append( vals_clean[i][1])	# seats

    ret_fin.append(ret_temp)
    ret_temp=[]

  #print ret_fin
    
  return ret_fin

def getCourse(arg):
  #print 'getCourse called ' + arg
  ret = getMypurdue(parseInput(arg))
  
  if ret == None:
    return None

  if ret[0] == None: # getMypurdue couldn't find the course
    return  None

  '''
  retString = ""
  for section in ret:
    retString += section[0] + "| " + section[1] + "| " + section[2] +  ": " + str(section[3]) + "\n"
  '''

  #print retString
  return ret


if __name__ == '__main__':
  getCourse(sys.argv[1])

