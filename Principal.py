import sys
from PyQt5 import uic 
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen

import Genetico as Gnetics

class View_GUI(QMainWindow):

    Poblacion_inicial = 0
    Poblacion_maxima = 0
    Minimo_x = 0
    Minimo_y = 0
    Maximo_x = 0
    Maximo_y = 0
    Prob_mutacion = 0
    num_iter = 0
    error_x = 0
    
    def __init__(self):
        super().__init__()
        uic.loadUi("Gnectis.ui", self)
        self.Btn_init.clicked.connect(self.validAttributes)


    def getAttributes(self):
        #Detalles sobre población
        self.Poblacion_inicial = self.Pob_initial.text()
        self.Poblacion_maxima = self.Pob_max.text()

        #Detalles sobre abcisa y ordenada
        self.Minimo_x = self.min_x.text()
        self.Maximo_x = self.max_x.text()
        self.Maximo_y = self.max_y.text()
        self.Minimo_y = self.min_y.text()

        #PARAMETROS
        self.Prob_mutacion = self.prob_mutacion.text()
        self.num_iter = self.num_iter.text()
    
        #ERROR PERMISIBLE
        self.errorx = self.error_x.text()


    def validAttributes(self):
        self.getAttributes()
        if not self.Poblacion_inicial or not self.Poblacion_maxima:
            self.alert_pob.setText("Se necesitan detalles de la población.")
        
        if not self.Minimo_x or not self.Minimo_y or not self.Maximo_x or not self.Maximo_y:
            self.alert_rango.setText("Se necesitan detalles sobre abcisa y ordenada.")
        
        if not self.Prob_mutacion or not self.num_iter:
            self.alert_param.setText("Se necesitan detalles sobre los parametros.")
        
        if not self.errorx:
            self.alert_error.setText("Se necesitan detalles sobre el error permisible.")
        
        else:
            self.run_algorith()

    
    def run_algorith(self):
        Gnetics.main(self.Prob_mutacion ,  self.Poblacion_inicial , self.num_iter , 
        self.Poblacion_maxima , self.Minimo_x , self.Maximo_x , self.Minimo_y , self.Maximo_y , 
        self.errorx)


#Main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = View_GUI()
    GUI.show()
    app.exec_()


# CREDITS
__author__ = "Alexis Roque"
__copyright__ = "Copyright (C) 2021 Author Alexis Roque"
__program__ = "Algoritmo Genetico (IA)"
__date__ = "May 17. 16:20 hrs."
__version__ = "Final 1.0"