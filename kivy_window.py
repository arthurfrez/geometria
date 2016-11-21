import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window

from sympy import *
from sympy.solvers.solveset import linsolve
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application

# http://www.im.ufrj.br/dmm/projeto/projetoc/precalculo/sala/conteudo/capitulos/cap91s7.html
# dando errado

# Tamanho da janela
Window.size = (400,200)
t, s = symbols('t, s')

from kivy.uix.boxlayout import BoxLayout

class LbTxt(BoxLayout):
    # Atributos
    from kivy.properties import ObjectProperty
    theTxt = ObjectProperty(None)

class MyLayout(BoxLayout):
    eq1 = []
    eq2 = []
    vec1 = []
    vec2 = []

    # Metodo para achar o valor do t
    def find_between(self, s, first, last):
        return s[s.rfind(first):-len(last)]

    # Metodo para ignorar divisao por 0
    def div0(self, a, b):
        if b == 0: return 0
        return a/b

    # Metodo para achar o t no vetor
    def theT(self, s):
        i = s.find('t')
        t1 = s.rfind('+')
        t2 = s.rfind('-')

        if i == 0: return 1
        elif not t1 == -1:
            if s[t1+1] == 't': return 1
            else: return self.find_between(s, '+', 't')
        elif (not t2 == -1) and ((s.count('-') == 2) and (not t2 == 0)):
            if s[t2+1] == 't': return -1
            else: return self.find_between(s, '-', 't')
        elif (not t2 == -1) and (s.count('-') == 1):
            if s[t2+1] == 't': return -1
            else: return self.find_between(s, '-', 't')
        elif not i == -1: return s[0:-len('t')]
        return 0

    # Metodo para gerar os vetores
    def genVectors(self):
        if not self.vec1:
            self.vec1.append(int(self.theT(self.eq1[0])))
            self.vec1.append(int(self.theT(self.eq1[1])))
            self.vec1.append(int(self.theT(self.eq1[2])))

            self.vec2.append(int(self.theT(self.eq2[0])))
            self.vec2.append(int(self.theT(self.eq2[1])))
            self.vec2.append(int(self.theT(self.eq2[2])))
        else:
            self.vec1[0] = int(self.theT(self.eq1[0]))
            self.vec1[1] = int(self.theT(self.eq1[1]))
            self.vec1[2] = int(self.theT(self.eq1[2]))

            self.vec2[0] = int(self.theT(self.eq2[0]))
            self.vec2[1] = int(self.theT(self.eq2[1]))
            self.vec2[2] = int(self.theT(self.eq2[2]))

        print self.vec1[0], self.vec1[1], self.vec1[2]
        print self.vec2[0], self.vec2[1], self.vec2[2]

    # Metodo para checkar se os vetores sao paralelos
    def isParallel(self):
        v = 0
        if self.div0(self.vec1[0], self.vec2[0]) == 0: v = self.div0(self.vec1[0], self.vec2[0])
        elif self.div0(self.vec2[0], self.vec1[0]) == 0: v = self.div0(self.vec2[0], self.vec1[0])
        else: return False

        if (not self.div0(self.vec1[1], self.vec2[1]) == v) and (not self.div0(self.vec2[1], self.vec1[1]) == v):
            return False
        if (not self.div0(self.vec1[2], self.vec2[2]) == v) and (not self.div0(self.vec2[2], self.vec1[2] )== v):
            return False

        return True

    # Checka se as retas sao concorrentes
    def isConcorrente(self):
        self.eq2[0] = self.eq2[0].replace('t', 's')
        self.eq2[1] = self.eq2[1].replace('t', 's')
        self.eq2[2] = self.eq2[2].replace('t', 's')

        transformations = (standard_transformations+ (implicit_multiplication_application,))
        a = parse_expr(self.eq1[0], transformations=transformations)
        b = parse_expr(self.eq2[0], transformations=transformations)
        r1 = Eq(a, b)

        c = parse_expr(self.eq1[1], transformations=transformations)
        d = parse_expr(self.eq2[1], transformations=transformations)
        r2 = Eq(c, d)

        sol = linsolve((r1, r2), [t, s])
        if sol == EmptySet(): return False

        e = parse_expr(self.eq1[2], transformations=transformations)
        f = parse_expr(self.eq2[2], transformations=transformations)
        r3 = Eq(e, f)
        pset = next(iter(sol))

        if solve(r3.subs(t, pset[0])) == pset[1]: return True
        return False

    # Metodo do botao
    def compute(self):
        if not self.eq1:
            self.eq1.append(self.ids.sec1.eq1.theTxt.text)
            self.eq1.append(self.ids.sec2.eq1.theTxt.text)
            self.eq1.append(self.ids.sec3.eq1.theTxt.text)
        else:
            self.eq1[0] = self.ids.sec1.eq1.theTxt.text
            self.eq1[1] = self.ids.sec2.eq1.theTxt.text
            self.eq1[2] = self.ids.sec3.eq1.theTxt.text

        if not self.eq2:
            self.eq2.append(self.ids.sec1.eq2.theTxt.text)
            self.eq2.append(self.ids.sec2.eq2.theTxt.text)
            self.eq2.append(self.ids.sec3.eq2.theTxt.text)
        else:
            self.eq2[0] = self.ids.sec1.eq2.theTxt.text
            self.eq2[1] = self.ids.sec2.eq2.theTxt.text
            self.eq2[2] = self.ids.sec3.eq2.theTxt.text

        self.genVectors()
        b = self.isParallel()
        c = self.isConcorrente()
        if b: self.lTxt = 'As retas sao [color=33ff33]PARALELAS[/color]'
        elif c: self.lTxt = 'As retas sao [color=33ff33]CONCORRENTES[/color]'
        else: self.lTxt = 'As retas sao [color=33ff33]REVERSAS[/color]'

class MyApp(App):
    # Construtor
    def build(self):
        self.root = Builder.load_file('kwindow.kv')
        return self.root

if __name__ == '__main__':
    MyApp().run()
