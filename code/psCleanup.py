# coding=utf8
############################
## Author: Mark Huberty, Mimi Tam, and Georg Zachmann
## Date Begun: 23 May 2012
## Purpose: Module to clean inventor / assignee data in the PATSTAT patent
##          database
## License: BSD Simplified
## Copyright (c) 2012, Authors
## All rights reserved.
##
## Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are met: 
## 
## 1. Redistributions of source code must retain the above copyright notice, this
##    list of conditions and the following disclaimer. 
## 2. Redistributions in binary form must reproduce the above copyright notice,
##    this list of conditions and the following disclaimer in the documentation
##    and/or other materials provided with the distribution. 
## 
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
## ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
## WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
## DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
## ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
## (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
## LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
## ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
## SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
## 
## The views and conclusions contained in the software and documentation are those
## of the authors and should not be interpreted as representing official policies, 
## either expressed or implied, of the FreeBSD Project.
############################

import re
import unicodedata

##Some subfunction stubs
def stdizeCase(string): 
    """Subfunction for string cleaning; Returns a string with all lowercase converted to uppercase characters"""
    result = string.upper()
    return result

def remDiacritics(string):
    """Subfunction for string cleaning; Returns a unicode String cleaned of accentmarks (diacritics)"""
    
    #Need to double check this "Casting" for potential problems!
    s = unicode(string)
    result = ''.join((c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c) !='Mn'))
    return result

def remTrailSpaces(string):
    """Subfunction for string cleaning; Returns a string with trailing spaces removed"""
    s = string.strip()
    return s

#a sort of main function
def masterCleanDicts(input_string, cleanup_dicts):
    for k, v in enumerate(cleanup_dicts):
        cleanup_dicts[k] = makeRegex(v)
        
    output_string = input_string
    for cleanupdict in cleanup_dicts:
        output_string = multReplace(output_string, cleanupdict)
    
    return output_string  

def multReplace(input_string, regex_dict):
    output_string = input_string
    for k, v in regex_dict.iteritems():
        output_string = v.sub(k, output_string)
    return output_string

def makeRegex(input_dict):
    regex_dict = {}
    for k, v in input_dict.iteritems():
        if isinstance(v, str):
            regex_dict[k] = re.compile(v)
        elif isinstance(v, list):
            expression = '|'.join(v)
            regex_dict[k] = re.compile(expression)
        else:
            raise ## Throw an error
    return regex_dict



#Dictionaries used for cleaning
#IMPORTANT NOTE: These all assume that case standardization has already been performed!

#Get rid of HTML tags. For extendability using dictionary. However, per Magerman et al 2006, only HTML tags were <BR>, we should validate  
convertHTML = {' ': r'<\s*BR\s*>' #break 
               }

#Get rid of SGML tags. Per Magerman et al 2006, only 7 SGML tags were identified in the data. We should validate   
convertSGML = {'&': r'&AMP;',
               'Ó': r'&OACUTE;',
               '§': r'&SECT;', 
               'Ú': r'&UACUTE;',
               ' ': r'&#8902;', 
               '.': r'&BULL;',
               '!': r'&EXCL;'
               }

commaPeriod = {'.': r'(?<=\d)(\s*\.\s*)(?=\d)', # 12345_._54321
               ',': r'(?<=\d)(\s*,\s*)(?=\d)', # 12345_,_54321  
               '. ': r'(?<=[a-zA-Z])(\s*\.\s*)(?=[a-zA-Z])', # abc_._abc
               ', ': r'(?<=[a-zA-Z])(\s*,\s*)(?=[a-zA-Z])' # abc_,_abc 
               }

cleanSymbols = {'': r'[^\s\w,.;:-]'
                }

singleSpace = {' ':r'\s+' 
               }

ampersand = { '&' : [r'\sAND\s',r'\sEN\s',r'\sDHE\s',r'\svə\s',r'\sETA\s',r'\sI\s',r'\sи\s',r'\sA\s',r'\sOG\s',r'\sKAJ\s',r'\sJA\s',r'\sAT\s',r'\sET\s',r'\sE\s',r'\sUND\s',r'\sAK\s',r'\sES\s',r'\sDAN\s',r'\sAGUS\s',r'\sUN\s',r'\sIR\s',r'\sU\s',r'\sSI\s',r'\sIN\s',r'\sY\s',r'\sNA\s', r'\sOCH\s',r'\sVE\s',r'\sVA\s', r'\sSAMT\s'] 
             }

#TEMPORARY TEST AREA
teststring10 = "500    . 19    50 <br>help me I'm a fire<br>ant 5<BR>er8<br>0<BR> < BR > <   BR > lkad </BR> < /BR > <br> <bR> <sfs  BR> <  lsks BR lls > a< Br>b abc"
teststring11 = "1 &AMP;2&aMpP; 3 & AMP ; &AMP; &aMp; &amp; &oacute; &OACUTE; &SECT; &sEcT; & s e c t;"

dictlist=[convertHTML,convertSGML]
print masterCleanDicts(teststring10, dictlist)