import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

from sympy import *
from sympy.solvers.solveset import linsolve
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application


# Tamanho da janela
Window.size = (400,200)
t, s = symbols('t, s')

class LbTxt(BoxLayout):
    """Layout class"""
    from kivy.properties import ObjectProperty
    theTxt = ObjectProperty(None)

class MyLayout(BoxLayout):
    """Layout class"""

    def generateLine(self, x, y, z):
        """Line calculations"""
        transformations = (standard_transformations+ (implicit_multiplication_application,))
        x = parse_expr(x, transformations=transformations)
        y = parse_expr(y, transformations=transformations)
        z = parse_expr(z, transformations=transformations)

        a = x.subs(t, 0)
        b = y.subs(t, 0)
        c = z.subs(t, 0)
        p1 = Point3D(a, b, c)

        a = x.subs(t, 1)
        b = y.subs(t, 1)
        c = z.subs(t, 1)
        p2 = Point3D(a, b, c)

        return Line3D(p1, p2)

    def compute(self):
        """Button method"""
        x1 = self.ids.sec1.eq1.theTxt.text
        y1 = self.ids.sec2.eq1.theTxt.text
        z1 = self.ids.sec3.eq1.theTxt.text

        x2 = self.ids.sec1.eq2.theTxt.text
        y2 = self.ids.sec2.eq2.theTxt.text
        z2 = self.ids.sec3.eq2.theTxt.text

        reta1 = self.generateLine(x1, y1, z1);
        reta2 = self.generateLine(x2, y2, z2);

        # try:
        if Line3D.is_parallel(reta1, reta2): self.lTxt = 'As retas sao [color=33ff33]PARALELAS[/color]'
        elif Line3D.are_concurrent(reta1, reta2): self.lTxt = 'As retas sao [color=33ff33]CONCORRENTES[/color]'
        else: self.lTxt = 'As retas sao [color=33ff33]REVERSAS[/color]'
        # except: self.lTxt = '[color=ff3333]ERRO[/color]'

class MyApp(App):
    """"Classe do app"""

    def build(self):
        """Contrutor"""
        self.root = Builder.load_file('kwindow.kv')
        return self.root

if __name__ == '__main__':
    MyApp().run()
