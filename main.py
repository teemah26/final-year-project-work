from cgitb import text
from ctypes import alignment
from struct import pack
from textwrap import fill
from turtle import left
import regex
import os
import tempfile

from asyncore import read
from tkinter import*
from tkinter import filedialog
from tkinter import messagebox
import ast 
from pprint import pprint

Type = ["int","void","float","double","string"]
If = ["if","else"]
In = "cin"
Out = "cout"
Loop = ["while","for"]
Variables=dict()
# at0 = [In,Type,Comment,If,In,Loop,Variables]

conditionRegEx='^\s*((?:[a-z,A-Z][a-z,A-Z,_,0-9]*|[0-9]+(?:\.[0-9]+)*))\s*(?:<=|>=|==|<|>)\s*((?:[a-z,A-Z][a-z,A-Z,_,0-9]*|[0-9]+(\.[0-9]+)*))\s*(?!.)'
ifRegEx="^\s*if\s*\(((?:[^\(\)]|\((?1)\))*+)\)\s*{((?:[^{}]|{(?2)})*+)}\s*(?!.)"
if1RegEx='^\s*if\s*\(((?:[^\(\)]|\((?1)\))*+)\)\s*(.*)'
elseRegEx="^\s*else\s*{((?:[^{}]|{(?1)})*+)}\s*(?!.)"
else1RegEx="^\s*else\s*(.*)"
elseIfRegEx="^\s*else\s*if\s*\(((?:[^\(\)]|\((?1)\))*+)\)\s*{((?:[^{}]|{(?2)})*+)}\s*(?!.)"
elseIf1RegEx="^\s*else\s*if\s*\(((?:[^\(\)]|\((?1)\))*+)\)\s*(.*)"
whileRegEx="^\s*while\s*\(((?:[^\(\)]|\((?1)\))*+)\)\s*{((?:[^{}]|{(?2)})*+)}\s*(?!.)"
while1RegEx="^\s*while\s*\(((?:[^\(\)]|\((?1)\))*+)\)\s*(.*)"
forRegEx="^\s*for\s*\(((?:[^\(\)]|\((?1)\))*+)\)\s*{((?:[^{}]|{(?2)})*+)}\s*(?!.)"
for1RegEx="^\s*for\s*\(((?:[^\(\)]|\((?1)\))*+)\)\s*(.*)"
IntEqRegEx="^\s*(int)\s*([a-z,A-Z][a-z,A-Z,_,0-9]*)\s*=\s*([0-9]+)\s*(?!.)"
IntRegEx="^\s*(int)\s*([a-z,A-Z][a-z,A-Z,_,0-9]*)\s*(?!.)"
floatEqRegEx="^\s*(float)\s*([a-z,A-Z][a-z,A-Z,_,0-9]*)\s*=\s*([0-9]+(\.[0-9]+)*)\s*(?!.)"
floatRegEx="^\s*(float)\s*([a-z,A-Z][a-z,A-Z,_,0-9]*)\s*(?!.)"
doubleEqRegEx="^\s*(double)\s*([a-z,A-Z][a-z,A-Z,_,0-9]*)\s*=\s*([0-9]+(\.[0-9]+)*)\s*(?!.)"
doubleRegEx="^\s*(double)\s*2([a-z,A-Z][a-z,A-Z,_,0-9]*)\s*(?!.)"
stringEqRegEx='^\s*(string)\s*([a-z,A-Z][a-z,A-Z,_,0-9]*)\s*=\s*"(.*)"\s*(?!.)'
stringRegEx="^\s*(string)\s*([a-z,A-Z][a-z,A-Z,_,0-9]*)\s*(?!.)"
varEqRegEx='^\s*([a-z,A-Z][a-z,A-Z,_,0-9]*)\s*=\s*(?:"(.*)"|([0-9]+(\.[0-9]+)*))\s*(?!.)'
coutRegEx='^\s*cout(?:\s*<<\s*(?:[a-z,A-Z][a-z,A-Z,_,0-9]*|".*"|[0-9]+(?:\.[0-9]+)*)\s*)+(?!.)'
coutVarRegEx='\s*<<\s*([a-z,A-Z][a-z,A-Z,_,0-9]*)'
cinRegEx='^\s*cin(?:\s*>>\s*[a-z,A-Z][a-z,A-Z,_,0-9]*\s*)+(?!.)'
cinVarRegEx='\s*>>\s*([a-z,A-Z][a-z,A-Z,_,0-9]*)'

def checkInst(instructions,variables):
    if len(instructions)==0:
        return True
    else:
        a=instructions[0]
        at0=a.split()[0]
        if at0 == "int":
            if "=" in a:
                if len(regex.findall(IntEqRegEx,a))==0:
                    return False
                typ, name, value = regex.findall(IntEqRegEx,a)[0][0:3]
                variables[name]=(typ,value)
                if value.isdecimal()!=True:
                    return False
            else:
                if len(regex.findall(IntRegEx,a))==0:
                    return False
                typ, name = regex.findall(IntRegEx,a)[0][0:2]
                variables[name]=(typ,"")
            return checkInst(instructions[1:],variables)
        elif at0 == "float":
            if "=" in a:
                if len(regex.findall(floatEqRegEx,a))==0:
                    return False
                typ, name, value = regex.findall(floatEqRegEx,a)[0][0:3]
                variables[name]=(typ,value)
                if value.replace(".","",1).isdecimal()!=True:
                    return False
            else:
                if len(regex.findall(floatRegEx,a))==0:
                    return False
                typ, name = regex.findall(floatRegEx,a)[0][0:2]
                variables[name]=(typ,"")
            return checkInst(instructions[1:],variables)
        elif at0 == "double":
            if "=" in a:
                if len(regex.findall(doubleEqRegEx,a))==0:
                    return False
                typ, name, value = regex.findall(doubleEqRegEx,a)[0][0:3]
                variables[name]=(typ,value)
                if value.replace(".","",1).isdecimal()!=True:
                    return False
            else:
                if len(regex.findall(doubleRegEx,a))==0:
                    return False
                typ, name = regex.findall(doubleRegEx,a)[0][0:2]
                variables[name]=(typ,"")
            return checkInst(instructions[1:],variables)
        elif at0 == "string":
            if "=" in a:
                if len(regex.findall(stringEqRegEx,a))==0:
                    return False
                typ, name, value = regex.findall(stringEqRegEx,a)[0][0:3]
                variables[name]=(typ,value)
            else:
                if len(regex.findall(stringRegEx,a))==0:
                    return False
                typ, name = regex.findall(stringRegEx,a)[0][0:2]
                variables[name]=(typ,"")
            return checkInst(instructions[1:],variables)
        elif at0 in If:
            condition=""
            insts=""
            if len(regex.findall(ifRegEx,a))>0:
                condition=regex.findall(ifRegEx,a)[0][0]
                insts=regex.findall(ifRegEx,a)[0][1]
            elif len(regex.findall(elseIfRegEx,a))>0:
                condition=regex.findall(elseIfRegEx,a)[0][0]
                insts=regex.findall(elseIfRegEx,a)[0][1]
            elif len(regex.findall(elseRegEx,a))>0:
                insts=regex.findall(elseRegEx,a)[0][0]
            elif len(regex.findall(elseIf1RegEx,a))>0:
                condition=regex.findall(elseIf1RegEx,a)[0][0]
                insts=regex.findall(elseIf1RegEx,a)[0][1]
            elif len(regex.findall(else1RegEx,a))>0:
                insts=regex.findall(else1RegEx,a)[0][0]
            elif len(regex.findall(if1RegEx,a))>0:
                condition=regex.findall(if1RegEx,a)[0][0]
                insts=regex.findall(if1RegEx,a)[0][1]
            else:
                return False
            if condition!="" or ("".join(condition.split()) not in ["true","false","0","1"]) and len(regex.findall(conditionRegEx,condition))>0:
                x=regex.findall(conditionRegEx,condition)[0][0]
                y=regex.findall(conditionRegEx,condition)[0][1]
                if not (( x[0].isalpha() == (x in variables.keys())) and (y[0].isalpha() == (y in variables.keys()))):
                    return False
            insts=getListOfInst(insts)
            ans= checkInst(insts,variables)
            if ans==False:
                return False
            return checkInst(instructions[1:],variables)
        elif at0 in Loop:
            condition=""
            insts=""
            if len(regex.findall(whileRegEx,a))>0:
                condition=regex.findall(whileRegEx,a)[0][0]
                insts=regex.findall(whileRegEx,a)[0][1]
            elif len(regex.findall(forRegEx,a))>0 and regex.findall(forRegEx,a)[0][0].count(";")==2:
                x,y,z=regex.findall(forRegEx,a)[0][0].split(";")
                condition=y
                insts=regex.findall(forRegEx,a)[0][1]
                x=x.split()
                if not((len(x)==2 or len(x)==3) and x[0]=="int" and len(regex.findall(varEqRegEx,z))>0 and x[1]==regex.findall(varEqRegEx,z)[0][0]):
                    return False
                # else:
                #     if len(regex.findall(IntEqRegEx,a))>0:
                #         return False
                # typ, name, value = regex.findall(IntEqRegEx,a)[0][0:3]
                # variables[name]=(typ,value)
                # if value.isdecimal()!=True:
                #     return False
            elif len(regex.findall(while1RegEx,a))>0:
                condition=regex.findall(while1RegEx,a)[0][0]
                insts=regex.findall(while1RegEx,a)[0][1]
            elif len(regex.findall(for1RegEx,a))>0 and regex.findall(for1RegEx,a)[0][0].count(";")==2:
                x,y,z=regex.findall(for1RegEx,a)[0][0].split(";")
                condition=y
                insts=regex.findall(for1RegEx,a)[0][1]
                x=x.split()
                if not(len(x)==2 and x[0]=="int" and len(regex.findall(varEqRegEx,z))>0\
                    and x[1]==regex.findall(varEqRegEx,z)[0][0]):
                    return False
            else:
                return False
            if ("".join(condition.split()) not in ["true","false","0","1"]) and len(regex.findall(conditionRegEx,condition))>0:
                x=regex.findall(conditionRegEx,condition)[0][0]
                y=regex.findall(conditionRegEx,condition)[0][1]
                if not (( x[0].isalpha() == (x in variables.keys())) and (y[0].isalpha() == (y in variables.keys()))):
                    return False
            insts=getListOfInst(insts)
            ans= checkInst(insts,variables)
            if ans==False:
                return False
            return checkInst(instructions[1:],variables)
        elif len(regex.findall(varEqRegEx,a))>0:
            tmp = regex.findall(varEqRegEx,a)[0]
            name=tmp[0]
            if name not in variables.keys():
                return False
            if variables[name][0]=="int" and tmp[3]=="" and tmp[1]=="":
                variables[name]=("int",tmp[2])
                return checkInst(instructions[1:],variables)
            elif (variables[name][0]=="double" or variables[name][0]=="float") and tmp[1]=="":
                variables[name][1]=tmp[2]
                return checkInst(instructions[1:],variables)
            elif variables[name][0]=="string" and (tmp[1]!="" or (tmp[1]=="" and tmp[2]=="" and tmp[3]=="")):
                variables[name][1]=tmp[1]
                return checkInst(instructions[1:],variables)
            else:
                return False
        elif len(regex.findall(cinRegEx,a))>0:
            for i in regex.findall(cinVarRegEx,a):
                if not (i in variables.keys()):
                    return False
            return checkInst(instructions[1:],variables)
        elif len(regex.findall(coutRegEx,a))>0:
            for i in regex.findall(coutVarRegEx,a):
                if not (i in variables.keys()):
                    return False
            return checkInst(instructions[1:],variables)
        elif "".join(a.split())=="return0":
            return checkInst(instructions[1:],variables)
        else:
            return False

def getListOfInst(code):
    instructions=[]
    while(True):
        firstSemicolon=code.find(";")
        firstAccolad=code.find("{")
        if (firstSemicolon==-1):
            break
        while(firstSemicolon<firstAccolad or firstAccolad==-1):
            inst=code[:firstSemicolon]
            code=code[firstSemicolon+1:]
            instructions.append(inst)
            firstSemicolon=code.find(";")
            firstAccolad=code.find("{")
            if (firstSemicolon==-1):
                break
        if (firstSemicolon>firstAccolad and firstAccolad!=-1):
            firstAccoladClose=findAccoladEnd(code)
            inst=code[:firstAccoladClose+1]
            code=code[firstAccoladClose+1:]
            instructions.append(inst)
    return instructions

def checkBalanced(myStr): 
    open_list = ["[","{","("] 
    close_list = ["]","}",")"] 
    stack = [] 
    for i in myStr:
        if i in open_list: 
            stack.append(i) 
        elif i in close_list: 
            pos = close_list.index(i) 
            if ((len(stack) > 0) and
                (open_list[pos] == stack[len(stack)-1])): 
                stack.pop()
            else: 
                return False
    if len(stack) == 0: 
        return True

def findAccoladEnd(myStr):
    stack = ["{"] 
    for n ,i in enumerate(myStr):
        if i == "{": 
            stack.append(i) 
        elif i == "}": 
            if ((len(stack) > 0) and
                ("{" == stack[len(stack)-1])): 
                stack.pop()
                if len(stack)==1:
                    return n
            else: 
                return -1
    return -1

def normal():
      
    instructions=[]

    header = code[:code.find("{")].split()

    if checkBalanced(code) \
        and (header[0] in Type) \
        and "".join(header[1:])=="main()":
        code= regex.findall("\s*{((?:[^{}]|{(?1)})*+)}\s*",code)[0]
        for i in regex.findall("\/\/\w*",code):
            code=code.replace(i,"")  #handle comment
        instructions = getListOfInst(code)
        result = checkInst(instructions,Variables)
        print(result)        
    else:
        print(False)

window =Tk()
window.title ('syntax error checker')
window.geometry("600x600")
window.configure(bg='#fff')
#name_text=Label(window,text="PYTHON SYNTAX ERROR CHECKER")
#name_text.pack()
name_text = Label(window, text = "PYTHON SYNTAX ERROR CHECKER", height = 3, font = ("CAMBRIA",18),anchor='center', padx = 10,bg="#3f829d")
name_text.pack(fill = X)
name_tex = Label(window, text = "how to use python syntax error checker:", height = 3, font = ("CAMBRIA",18),anchor='center', padx = 10,bg="#fff")
#frame_1=Frame(window)
name_tex.pack(fill = X)
name_te = Label(window, text = "click on the open file to upload your file and then click on the scan code to detect error", height = 3, font = ("CAMBRIA",18),anchor='center', padx = 10,bg="#fff")
#frame_2=Frame(window)
name_te.pack(fill = X)
#frame.pack(fill=Y,side=LEFT)
##frame_1.pack(fill =Y, side = LEFT)
#frame_2.pack(fill =Y , side = RIGHT)
Label_1=Label(window,text="welcome")
Label_2=Label(window,text="this is a syntax")
#Label_1.pack( side = LEFT)
def open_text():
    
    text_file=filedialog.askopenfilename(title="open text file",filetypes=(("text files","*.py"), ))
    text_file=open(text_file,'r')
    stuff=text_file.read()
    my_text.insert(END,stuff)
    text_file.close()  
                    
                                         
my_text=Text(window,width=50,height=5,font=("helvetica",16))                                   
 #my_text.pack(pady=100)    

open_button=Button(window,text="choose python file to open",command=open_text,bg="#3f829d",height=5,width=20)
open_button.pack(pady=20)
def me ():
    lbl_print=Label(window,text="NO SYNTAX ERROR FOUND").place(x=100,y=20)



scan_text=Button(window,text="scan text",command=me,bg="#3f829d",height=5,width=20)
scan_text.pack(pady=40) 

correct_text=Button(window,text="correct errors",command=normal,bg="#3f829d",height=5,width=20)
correct_text.pack(pady=60)



window.mainloop()