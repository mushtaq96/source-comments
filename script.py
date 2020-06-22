from googletrans import Translator
import re
import os
import fnmatch #to remove unwanted files
import time # to find runtime
start_time = time.time()

eng_list_of_translated_comments = []
total_comment_count = 0

#extracting comments from the source file
def sourceComments(filename,string):
    file_lines =[]
    with open(filename,'r',encoding='utf-8')as ro:
        #traverse each line for Japanese
        for eachline in ro.readlines():
            if isRegionJapanese(eachline) or isCommentJapanese(eachline,string):
                string_to_add = translateToEnglish(eachline)#english translation for line
                eng_list_of_translated_comments.append(string_to_add)
                removeNewlineChar = eachline.rstrip()
                addNewLine = ' '.join([removeNewlineChar,string_to_add,'\n'])
                file_lines.append(addNewLine)
                global total_comment_count 
                total_comment_count += 1

            elif containsJapaneseRandomly(eachline):
                addString = translateToEnglish(eachline)
                removenewlinechar = eachline.rstrip()
                removenewlinecharUpdate = removenewlinechar+'//'
                addLine = ' '.join([removenewlinecharUpdate, addString,'\n'])
                file_lines.append(addLine)
                                                         
            else:
                file_lines.append(eachline) 
                               
        

    with open(filename,'w',encoding='utf-8')as wo:
        wo.writelines(file_lines)
        return True
    return False

def containsJapaneseRandomly(string):
    clean_string = string.strip()
    clean_string = clean_string.strip('//')
    pattern = r'.*[\u3040-\u309f\u30a0-\u30ff\uff66-\uff9f\u4e00-\u9faf]+.*' #match jpn characters in between english
    if re.match(pattern,clean_string):
        return True
    return False


def isCommentJapanese(single_line,string):
    #is a comment
    if string in single_line:
        #is it japanese
        if(containsJapanese(single_line)):
            return True
    return False

def isRegionJapanese(single_line):
    find = '#region'
    if find in single_line:
        #this is region code
        if(containsJapanese(single_line)):
            return True
    return False    


#valuidate if japanese character exists
def containsJapanese(string):
    clean_string = string.strip()#no use as of now
    clean_string = clean_string.strip('//')#
    #pattern = r'\s{0,}/{2,}\s{0,}[\u3040-\u309f\u30a0-\u30ff\uff66-\uff9f\u4e00-\u9faf]+'
    ##pattern = r'\s{0,}/{2,}\s{0,}.*[\u3040-\u309f\u30a0-\u30ff\uff66-\uff9f\u4e00-\u9faf]+.*' #match jpn characters in between english
    pattern = r'.*[\u3040-\u309f\u30a0-\u30ff\uff66-\uff9f\u4e00-\u9faf]+.*' #match jpn characters in between english
    if re.match(pattern,clean_string):
        return True
    return False

#language conversion of comments to english
def translateToEnglish(jpn_input):
    translator = Translator()
    clean_jpn_input = jpn_input.strip()
    clean_jpn_input = clean_jpn_input.strip('// ')
    clean_jpn_input = clean_jpn_input.rstrip('・・')
    pattern = '[\u3040-\u309f\u30a0-\u30ff\uff66-\uff9f\u4e00-\u9faf]+'
    divideJpn = re.findall(pattern,clean_jpn_input) 
    #join it as one string of jpn
    if(len(divideJpn)>=1):
        divideJpnString = ''.join(divideJpn)
        eng_output = translator.translate(divideJpnString).text
    else:
        eng_output = translator.translate(clean_jpn_input).text
    return eng_output

#ignore files which end with .cs yet irrelevant
def fnmatching(filename):        
    if fnmatch.fnmatch(filename,'*.Designer.cs'):
        return False
    elif fnmatch.fnmatch(filename,'Temp*.cs'):
        return False
    return True

counter = []
#entry point of the program
def startProgram(path,string):
    
    for ROOT,DIR,FILES in os.walk(path):
        for file in FILES:
            if file.endswith(('cs')) and fnmatching(file):
                
                absolute_path = os.path.join(ROOT,file) 
                if sourceComments(absolute_path,string):
                    counter.append(file)
    return counter
        
##Workaround to solve the daily limit() Json decode error on accessing the google translate api 
## - manually update a single root folder and expect .cs files to be translated 


### code for individual files
# file_path = '/home/mushtaq/Projects/uploadedFiles'
# if  sourceComments(file_path,'//'):
#     print('\n Comments found')
#     print("Total comments in this iteration -"+str(total_comment_count))
#     store_comment_count_location = 'C:\\Users\\b.mushtaq\\Code\\TotalComments.txt'
#     with open(store_comment_count_location,'r+',encoding='utf-8')as fo:
#         all_lines = fo.readlines()
#         last_line = all_lines[-1]
#         updated_total_value = total_comment_count+int(last_line)
#         fo.write('\n%d' % updated_total_value)
#     end_time = time.time()
#     print("\n Time in seconds"+str(end_time-start_time))
# else:
#     print('\n Try again')


