# Prints the template functions for an automated test file
# with case IDs, story numbers, and the epic number
# filled in appropriately. Also prints out the case list
# to be pasted into the case list in the test file.

# Assumes continuous case IDs and story numbers
# Variables:
# num - The starting case ID
# maxid - The ending case ID
# story - The starting story number
# product - t1, cc1, t2, cc2, etc.
# epic - The epic number

num = 8316
maxid = 8340
story = 1
storystr = ""
s = "" #case list
product = "t1"
epic = "58"
      
#Prints the function templates for each test
while num <= maxid:
    if story < 10:
        storystr = "00" + str(story)
    elif story > 99:
        storystr = str(story)
    else:
        storystr = "0" + str(story)
    block = "\t# Case C" + str(num) + " - " + str(storystr) +" - UserType | \n"
    block += "\t@pytest.mark.skipif(str("+ str(num) +") not in TESTS, reason='Excluded')  # NOQA\n"
    block += "\tdef test_usertype_(self):\n"
    block += '\t\t"""Story Text.\n\n'
    block += '\t\tSteps:\n\n\n'
    block += '\t\tExpected Result:\n\n'
    block += '\t\t"""\n'
    block += "\t\tself.ps.test_updates['name'] = '"+product+"."+epic+"."+storystr+"' \\"
    block += "\n\t\t\t+ inspect.currentframe().f_code.co_name[4:]\n"
    block += "\t\tself.ps.test_updates['tags'] = [\n\t\t\t'"+product+"',\n"
    block += "\t\t\t'"+product+"."+epic+"',\n"
    block += "\t\t\t'"+product+"."+epic+"."+storystr+"',\n"

    block += "\t\t\t'"+str(num)+"'\n\t\t]"
    block += "\n\t\tself.ps.test_updates['passed'] = False\n\n"
    block += "\t\t# Test steps and verification assertions\n\n"
    block += "\t\tself.ps.test_updates['passed'] = True\n\n"
    
    s = s + str(num)
    if num != maxid:
        s = s + ", "
    
    num += 1
    story += 1
    print block

"""
    # Case CaseID - Story# - UserType |
    @pytest.mark.skipif(str(CaseID) not in TESTS, reason='Excluded')  # NOQA
    def test_usertype_story_text(self):
        Story Text.

        Steps:


        Expected Result:

        
        self.ps.test_updates['name'] = 'product.epic.story' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'product',
            'product.epic',
            'product.epic.story',
            'CaseID'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions

        self.ps.test_updates['passed'] = True
"""
    
    
    
# Prints the caselist to paste at the top of the file
print s