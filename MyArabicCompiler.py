from tkinter import *
from tkinter import messagebox
import tkinter as tk
letter = {'ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ز', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك',
          'ل', 'م', 'ن', 'ه', 'و', 'ى', 'ي'}
digit = ['0','1','2','3','4','5','6','7','8','9','٩','٨','٧','٦','٥','٤','٣','٢','١','٠']

symbols={'+':'رمز جمع','-':'رمز طرح','*':'رمز ضرب','/':'رمز قسمه','>':'اصغر من','<':'اكبر من',
         '{':'قوس مجموعه مغتوح','}':'قوس مجموعه مغلق','[':'قوس مربع مفتوح ',']':'قوس مربع مغلق',
         '(':'قوس مفتوح',')':'قوس مغلق','،':'فاصله','؛':'فاصله منقوطه'}
compare_symbols={'=!':'رمز لا يساوي','==':'رمز يساوي','=<':'رمز اكبر من او يساوي ','=>':'رمز اصغر من او يساوي'
                 ,'=':'يعادل'}
key_words=['خالي','صحيح','حقيقي','بينما','اخر','اذا','ارجع']

#Errors
Param_err="Parameter Error "
Dec_err="Declaration Error "
Var_err='Variable Error'
Opr_err='Bad Operator'
Com_err='Comparision Error'
Ret_err='Return Error'
Fac_err='Factor Error'
Cal_err='Call Error'
Arg_err='Arguments Error'
Ter_err='Term Error'
Add_err='Additive Error'
Exp_err='Expression Error'
Stm_err="Statement Error"
Pro_err='Program Error'
##tokens#
class Token:
    def __init__(self ,type_,value=None):
        self.type=type_
        self.value=value
    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'
###lexer##
class Scaner:
    def __init__(self, text):
        self.text=text
        self.pos=-1
        self.current_char= None
        self.advance()
    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len (self.text) else '%'


    def make_token(self):

        tokens = []
        while self.current_char != '%':
            if self.current_char in ' ' or self.current_char == '\n':
                self.advance ()
            elif self.current_char in digit:
                returned,pos=self.make_numbers()
                if returned=="Lexer Error":
                    return [],"Lexer Error at "+str(pos)
                else:
                    tokens.append (returned)
                    self.advance()
            elif self.current_char in letter:
                tokens.append (self.make_letter ())
                self.advance()
            elif self.current_char in list(symbols.keys())or self.current_char in list(compare_symbols.keys())or self.current_char=='!':
                returned ,pos= self.make_symbol ()
                if returned == "Lexer Error":
                    return [], "Lexer Error at "+str(pos)
                else:
                    tokens.append (returned)
                    self.advance ()
            else:
                return [],"Lexer Error"

        return tokens, None
    def make_numbers(self):
            num_str =''
            dot_count =0
            while self.current_char != '%' and self.current_char in digit or self.current_char =='.':
                if self.current_char=='.':
                    if dot_count ==1:
                        break
                    dot_count+=1
                    num_str+='.'
                else:
                    num_str+= self.current_char
                self.advance ()
            if self.current_char in letter:
                return "Lexer Error",self.pos
            if dot_count ==0:
                return Token('صحيح',int(num_str))
            else :
                return Token('حقيقي',float(num_str))
    def make_letter(self):
            str=''
            while self.current_char !='%' and self.current_char in letter or self.current_char in digit:
                str+=self.current_char
                self.advance()
            if str in key_words:
                return Token('جمله',str)
            return Token('متغير',str)
    def make_symbol(self):
        str=''
        if self.current_char=='!':
            str+=self.current_char
            self.advance()
            if self.current_char=='=':
                str+=self.current_char
                return Token(compare_symbols['=!'],str)
            else:
                return "Lexer Error",self.pos
        elif self.current_char=='>':
            str+=self.current_char
            self.advance()
            if self.current_char=='=':
                str+=self.current_char
                return Token(compare_symbols['=>'],str)
            else:
                return Token(symbols['>'],str)
        elif self.current_char=='<':
            str+=self.current_char
            self.advance()
            if self.current_char=='=':
                str+=self.current_char
                return Token(compare_symbols['=<'],str)
            else:
                return Token(symbols['<'],str)
        elif self.current_char=='=':
            str+=self.current_char
            self.advance()
            if self.current_char=='=':
                str+=self.current_char
                return Token(compare_symbols['=='],str)
            else:
                return Token(compare_symbols['='],str)
        else:
            str+=self.current_char
            return Token(symbols[str],str)


class Sentence:
    def __init__(self,tpe ,left_node,right_node ,op_tok=None,Endsentence=None ):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        self.end_sentence=Endsentence
        self.tpe=tpe
    def __repr__(self):
        return f'{self.tpe}({self.right_node}, {self.op_tok}, {self.left_node})'




class Parser:

    def __init__(self,tokens):
        self.tokens=tokens
        self.current_tok=''
        self.tok_idx =-1
        self.AssignmentToken=[]
        self.advance()
    def advance(self):
        self.tok_idx+=1
        #print(self.tok_idx)
        if self.tok_idx<len(self.tokens):
            self.current_tok=self.tokens[self.tok_idx]
        else :self.current_tok=None
        #print(self.current_tok)
#done
    def program(self):
        dec=self.declaration_list()
        if dec==Dec_err:
            return Pro_err
        else:
            return dec

#done
    def declaration_list(self):
        declarations=[]
        str=''
        dec=self.declaration()
        while True:
            if type(dec)=='Sentence':
                declarations.append(dec)
                self.advance()
                dec=self.declaration()
            else:
                break
        for d in declarations:
            if d==Dec_err:
                return Dec_err
            else:
                str+=d
        return Sentence("Declaration_list",str,'')


#done
    def declaration(self):
        var=self.var_declaration()
        fun=self.fun_declaration()
        if type(var)=='Sentence':
            return var
        elif type(fun)=='Sentence':
            return fun
        else:
            return Dec_err

#done
    def type_specifier(self):
        if self.current_tok.value in key_words[0:3]:
            return self.current_tok.value
        else:
            return 'error'
    def var_declaration(self):
        right=''
        left=dec_type=self.type_specifier()
        if left=='error':
            return Dec_err+"Unknown DataType"
        self.advance()
        if self.current_tok.type=='متغير':
            right+=self.current_tok.value
            self.advance()
            if self.current_tok.value=='؛':
                right+=self.current_tok.value
                return Sentence("Variable Declaration",left,right,Endsentence="؛")
            elif self.current_tok.value==']':
                right+=self.current_tok.value
                self.advance()
                if self.current_tok.type in ['صحيح','حقيقي']:
                    if self.current_tok.type==dec_type:
                        right+=self.current_tok.value
                        self.advance()
                        if self.current_tok.value=='[':
                            right+=self.current_tok.value
                            self.advance()
                            if self.current_tok.value=='؛':
                                right+=self.current_tok.value
                                return Sentence("Array Declaration",left,right,Endsentence='؛')
                            else:
                                return Dec_err+"Missing ؛"
                        else:
                            return Dec_err+"Missing ["
                    else:
                        return Dec_err+"wrong types"
                else:
                    return Dec_err+"Undefended Type"
            else:
                return Dec_err
        return Dec_err

    def local_declaration(self):
       pass
#done
    def param(self):
        right = ''
        left = self.type_specifier ()
        if left == 'error':
            return Dec_err + "Unknown DataType"
        else:
            self.advance ()
            if self.current_tok.type == 'متغير':
                right += self.current_tok.value
                self.advance ()
                if self.current_tok.value == ']':
                    right += self.current_tok.value
                    self.advance ()
                    if self.current_tok.value == '[':
                        right+=self.current_tok.value
                        return Sentence("Array Parameter",left,right)
                    else:
                        return Param_err+" Missing ["
                else:
                    return Sentence("Variable Parameter",left,right)
            else:
                return Param_err
#done
    def params(self):
        str=''
        paras=self.param_list()
        if paras==Param_err:
            return None
        else:
            for par in paras:
                str+=" ، "+par
            return Sentence("Parameters",str[3:],'')



#done
    def param_list(self):
        parameters=[]

        left=self.param()
        if type(left)!='Sentence':
            return Param_err
        else:
            parameters.append(left)
            self.advance()
            while self.current_tok.value=='،':
                par=self.param()
                if type(par)=='Sentence':
                    parameters.append(par)
                    self.advance()
                else:
                    return Param_err
            return parameters
#done
    def expression_statement(self):
        str=''
        exp=self.expression()
        if self.current_tok.value=='؛':
            return self.current_tok.value
        elif type(exp)=='Sentence':
            str+=exp
            self.advance()
            if self.current_tok.value=='؛':
                return Sentence('',str,self.current_tok.value)
            else:
                return Exp_err
        else:
            return Exp_err
#done
    def simple_expression(self):

        left=self.additive_expression()
        if type(left)=='Sentence':
            self.advance()
            op=self.relOp()
            if op!=Com_err:
                self.advance()
                right=self.additive_expression()
                if type(right)=='Sentence':
                    return Sentence("Simple Expression",left,right,op)
                else:
                    return Com_err
            else:
                return Sentence("One Comparision",left,'')
        else:
            return Com_err
#done
    def additive_expression(self):
        adds = []
        strr = ''
        ad = self.term ()
        while type (ad) == 'Sentence':
            self.advance ()
            add = self.addOp ()
            if add != Opr_err:
                adds.append (str (add) + str (ad))
                self.advance ()
                ad = self.term ()
            else:
                adds.append (str (ad))
                break
        else:
            return Add_err
        for a in adds:
            strr += a
        return Sentence ('', strr, '')

#done
    def relOp(self):
        if self.current_tok.value in ['=!','==','=<','=>','<','>']:
            return self.current_tok.value
        else:
            return Com_err
#done
    def addOp(self):
        if self.current_tok.value in ['+','-']:
            return self.current_tok.value
        else:
            return Opr_err
#done
    def mulOp(self):
        if self.current_tok.value in ['*','/']:
            return self.current_tok.value
        else:
            return Opr_err
#done
    def expression_statment(self):
        expres=[]
        ex=self.expression()
        while type(ex)=='Sentence':
            self.advance()
            if self.current_tok.value=="؛":
                expres.append(ex)
                self.advance()
                ex=self.expression()
            else:
                return expres
        else:
            if self.current_tok.value:
                return self.current_tok.value


#done
    def expression(self):
        st=''
        sim=self.simple_expression()
        va=self.var()
        if type(sim)=='Sentence':
            return Sentence('Expression',str(sim))
        if type(va)=='Sentence':
            self.advance()
            if self.current_tok.value=='=':
                st+=self.current_tok.value
                self.advance()


#done
    def var(self):
        left=''
        right=''
        if self.current_tok.type=='متغير':
            left+=self.current_tok.value
            self.advance()
            if self.current_tok.value==']':
                left+=self.current_tok.value
                self.advance()
                exp=self.expression()
                if type(exp)=='Sentence':
                    right+=exp
                    self.advance()
                    if self.current_tok.value=='[':
                        right+=self.current_tok.value
                        return Sentence("Array Variable",left,right)
                    else:
                        return Var_err+" Missing ["
                else:
                    return Var_err+" Expression Error"

            else:
                return Sentence("ID",left,'')
        else:
            return Var_err

#done
    def return_statement(self):
        left=''
        right=''
        if self.current_tok.value=='ارجع':
            left+=self.current_tok.value
            self.advance()
            va=self.current_tok.value
            exp=self.expression()
            if va=='؛':
                right+=va
                return Sentence("Simple return",left,right,Endsentence='؛')
            elif type(exp)=='Sentence':
                right+=exp
                self.advance()
                if self.current_tok.value=='؛':
                    right+=self.current_tok.value
                    return Sentence("Expression return",left,right,Endsentence='؛')
                else:
                    return Ret_err+" Missing ؛"
            else:
                return Ret_err
        else:
            return Ret_err+" Missing ارجع"
    def statemenet(self):
        pass
#done
    def selection_statement(self):
        left=''
        right=''
        if self.current_tok.value=='اذا':
            left=+self.current_tok.value
            self.advance()
            if self.current_tok.value==")":
                left+=self.current_tok.value
                self.advance()
                ex=self.expression()
                if type(ex)=='Sentence':
                    left+=ex
                    self.advance()
                    if self.current_tok.value=='(':
                        left+=self.current_tok.value
                        self.advance()
                        st=self.statemenet()
                        if type(st)=='Sentence':
                            left+=st
                            self.advance()
                            if self.current_tok.value=='اخر':
                                right+=self.current_tok.value
                                self.advance()
                                st2=self.statemenet()
                                if type(st2)=='Sentence':
                                    right+=st2
                                    return Sentence("selection",left,right)
                                else:
                                    return Stm_err
                            else:
                                return Sentence("simple selection",left,right)
                        else:
                            return Stm_err
                    else:
                        return Stm_err
                else:
                    return Stm_err
            else:
                return Stm_err
        else:
            return Stm_err
#done
    def iteration_statement(self):
        left=''
        right=''
        if self.current_tok.value=='بينما':
            left+=self.current_tok.value
            self.advance()
            if self.current_tok.value==")":
                left+=self.current_tok.value
                self.advance()
                ex=self.expression()
                if type(ex)=='Sentence':
                    left+=ex
                    self.advance()
                    if self.current_tok.value=='(':
                        left+=self.current_tok.value
                        self.advance()
                        st=self.statemenet()
                        if type(st)=='Sentence':
                            right+=st
                            return Sentence("iteration",left,right)
                        else:
                            return Stm_err
                    else:
                        return Stm_err
                else:
                    return Stm_err
            else:
                return Stm_err
        else:
            return Stm_err




    def statement_list(self):
        pass







#done
    def compound_statement(self):
        left=''
        right=''
        if self.current_tok.value=="}":
            Left=self.current_tok.value
            self.advance()
            lo= self.local_declaration ()
            if type(lo)=='Sentence':
                left+=lo
                sts=self.statement_list()
                if type(sts)=='Sentence':
                    right+=sts
                    self.advance()
                    if self.current_tok.value=='{':
                        right+=self.current_tok.value
                        return Sentence("",left,right)
                    else:
                        return Stm_err
                else:
                    return Stm_err
            else:
                return Stm_err
        else:
            return Stm_err

#done
    def call(self):
        left=''
        right=''
        if self.current_tok.type=='متغير':
            left+=self.current_tok.value
            self.advance()
            if self.current_tok.value==')':
                left+=self.current_tok.value
                self.advance()
                args=self.args()
                if type(args)=='Sentence':
                    right+=args
                    self.advance()
                    if self.current_tok.value=='(':
                        right+=self.current_tok.value
                        return Sentence("Call",left,right)
                else:
                    return Cal_err
            else:
                return Cal_err
        else:
            return Cal_err

#done
    def term(self):
        terms=[]
        strr=''
        tr=self.factor()
        while type(tr)=='Sentence':
            self.advance()
            mul=self.mulOp()
            if mul!=Opr_err:
                terms.append(str(mul)+str(tr))
                self.advance()
                tr=self.factor()
            else:
                terms.append(str(tr))
                break
        else:
            return Ter_err
        for t in terms:
            strr+=t
        return Sentence('',strr,'')

#done
    def args(self):
        str=''
        args=self.args_list()
        if args==Arg_err:
            return Arg_err
        else:
            for arg in args:
                str+=" ، "+arg
        return Sentence("Arguments",str[3:],'')
#done
    def args_list(self):
        argument=[]
        arg=self.expression()
        while type(arg)=='Sentence':
            self.advance()
            if self.current_tok.value=='،':
                argument.append(arg)
                self.advance()
                arg=self.expression()
            else:
                argument.append(arg)
                return argument
        return Arg_err

#done
    def factor(self):
        var=self.var()
        cal=self.call()
        right=''
        left=''
        if self.current_tok.value==')':
            left+=self.current_tok.value
            self.advance()
            exp=self.expression()
            if type(exp)=='Sentence':
                right+=exp
                self.advance()
                if self.current_tok.value=='(':
                    right+=self.current_tok.value
                    return Sentence('Factor',left,right)
                else:
                    return Fac_err+" Missing ("
            else:
                return Fac_err
        if self.current_tok.type in ['حقيقي','صحيح']:
            return Sentence('Number',self.current_tok.value,'')
        if type(var)=='Sentence':
            return Sentence('',var,'')
        if type(cal)=='Sentence':
            return Sentence('',cal,'')




    def fun_declaration(self):
        left=self.type_specifier()
        if left=='error':
            return Dec_err+"Functions must have Output DataType"

        right=''
        self.advance()
        if self.current_tok.type=='متغير':
            right+=self.current_tok.value
            self.advance()
            if self.current_tok.value==')':
                right+=self.current_tok.value
                self.advance()
                fun_para=self.params()
                for par in fun_para:
                    right+=par
                if self.current_tok.valu=='(':
                    right+=self.current_tok.value
                    self.advance()
                    statments=compound_statement()




    def parse(self):
        res = []
        while (self.current_tok != None):
            res.append (self.program ())
        return (res)


def CodeCompile():
    result = textBox.get ("0.0", tk.END + "-1c")
    lines = result.split ("\n")
    print(lines)
    ###scanner
    sScaner = Scaner (result)
    tokens, er = sScaner.make_token ()
    print (tokens)
    print (er)
    parser = Parser (tokens)
    res=parser.parse()
    print(res)
    if er =="Lexer Error":
        messagebox.showerror ("Lexer Error", "There is no Tokens ")
    else:
        output=''
        for tok in tokens:
            output+=tok.value+'\n'
        messagebox.showinfo ("Compiled Successfully", "Tokens are " + "\n" + output)


#GUI
rootWidget = Tk(screenName="Arabic Compiler")
rootWidget.configure(background='black')
rootWidget.geometry("940x500")
# Code to add widgets will go here..
# .
firstLabel= Label(rootWidget,text= "Type your Code Here ",fg="#ADF70E",bg="black")

firstLabel.grid(row=0,column=0)
textBox = Text(rootWidget,width=100,height=25,borderwidth=5)

textBox.grid(row=1,column=0)
compileButton=Button(rootWidget,text="Compile",bg="black",fg="#ADF70E",command=CodeCompile,padx=20,pady=20)
compileButton.grid(row=2,column=1)

#Continue running
rootWidget.mainloop()