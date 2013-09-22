import mechanize
import bs4
import sys


def parseInput(input):
  """
  Returns a tuple of type (input_type, course dep/None, courser num/crn)  
  given a user unput, parseInput does it's best to understand what is going on

  Simple string of numbers
  : Course Number
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

    print "err: bad input"
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
<<<<<<< HEAD
     #print "bad input"
     return None
=======
     print "bad input"
     return []
>>>>>>> a21a10adc91ca2db5da0ec14b8c4623d04365874


  br.submit()

  #print br.response().read()

  # now we need to find the link to the course
  links = []
  for link in br.links():
    if (link.text is not None) and (input[1] in link.text) and (input[2] in link.text):
      # all the follwing links must be of some value
      links.append(link)
      #br.back()

  if not links:
<<<<<<< HEAD
    #print "course not found"
=======
    print "course not found"
>>>>>>> a21a10adc91ca2db5da0ec14b8c4623d04365874
    return None

  # visit links and get seats/waitlist seats
  val_all = []
  for link in links:
    val_current = []
    val_current.append(link.text)
    br.follow_link(link)
    html = br.response().read()
    soup = bs4.BeautifulSoup(html)
    for entry in soup.find_all('td'):
      if "dddefault" in str(entry) and str(entry).__len__() < 30:
	# really weird criteria, but it works
	val_current.append(int(entry.string))
    br.back()
    val_all.append(val_current)

  # clean up lists (parse out avaialbe seats
  vals_clean = []
  for item in val_all:
    tmp = []
    tmp.append(item[0])
    tmp.append(item[3])
    vals_clean.append(tmp)

  return vals_clean

def getCourse(arg):
  print 'getCourse called ' + arg
  ret = getMypurdue(parseInput(arg))

  if ret[0] == None: # getMypurdue couldn't find the course
    return  None

  retString = ""
  for section in ret:
    retString += section[0] + ": " + str(section[1]) + "\n"

  #print retString
  return retString


if __name__ == '__main__':
  getCourse(sys.argv[1:])
