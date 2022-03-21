from imp import reload
import sys

from PySide2 import QtCore
from PySide2 import QtUiTools
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui

#HERE TO APPEND THE PATH FOR CUSTOM FUNCTIONS
sys.path.append('C:\\Users\\butto\\OneDrive\\Desktop\\Checker\\Custom_Functions')
#AND IMPORT THEM
from CheckSet import CheckMap
from CheckSet import LogList

from SceneDetection import ObjListShape
from SceneDetection import UVList
from SceneDetection import InDaScene

from CleanNode import NodeCleaner

CheckLast=[]

def maya_main_window():
    
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class DesignerUI(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(DesignerUI, self).__init__(parent)

        self.setWindowTitle("UVSET EDITOR")

        self.init_ui()
        self.create_layout()
        self.create_connections()

    def init_ui(self):
        #THE UI MUST BE CREATED IN QT INSIDE A FORM WIDGET, OTHERWISE IT WON'T BE SHOWN >> YOU'LL ONLY SE A DEFAULT WINDOW
        f = QtCore.QFile("C:\\Users\\butto\\OneDrive\\Desktop\\Checker\\UVSetCheck.ui")
        f.open(QtCore.QFile.ReadOnly)

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(f, parentWidget=self)

        f.close()

    def create_layout(self):
        print('Still working on Layout')

    #HERE CONNECTIONS FOR VARIOUS ELEMENT OF THE UI
    def create_connections(self):

        #BUTTON AT THE BOTTOM
        self.ui.Apply_Btn.clicked.connect(self.CheckUvSet)
        self.ui.Exit_Btn.clicked.connect(self.close)
        self.ui.Obj_List.itemClicked.connect(self.StartClickList)
                
        #EMPTY FOR OBJ LIST SECTION QWIDGETLIST
        if ObjListShape==[]:
            self.ui.Obj_List.addItem('EMPTY')
        else:
            for bb in ObjListShape:
                self.ui.Obj_List.insertItems(self.ui.Obj_List.count(), [bb])
        
        #EMPTY FOR UV LIST SECTION QWIDGETLIST
        if UVList==[]:
            self.ui.UvSet_List.addItem('EMPTY')
        else:
                self.ui.UvSet_List.insertItems(0,UVList[0])

    def CheckUvSet(self):

        #UPDATE MODULES >> THIS WILL ALLOW US TO HAVE SOMETHING UPDATE AT EACH CHANGE IN THE SCENE
        from imp import reload
        import SceneDetection
        reload(SceneDetection)
        from SceneDetection import ObjListShape
        from SceneDetection import UVList
        InDaScene()

        import CheckSet
        reload(CheckSet)
        from CheckSet import CheckMap
        from CheckSet import LogList
        CheckMap()

        import CleanNode
        reload(CleanNode)
        from CleanNode import NodeCleaner
        NodeCleaner()

        ListItems=[]

        #CONDITION TO UPDATE THE LOG INFO
        if LogList==[]:
            self.ui.Log_View.clear()
            self.ui.Log_View.addItem('Log con lo stato degli oggetti presenti in scena')
            self.ui.Log_View.addItem('\n')
            self.ui.Log_View.addItem('TUTTI GLI OGGETTI SONO OK')
            self.ui.Log_View.addItem('\n')
            self.ui.Log_View.addItem('HANNO UN SOLO UVSET E SI CHIAMA MAP1')
        else:
            for items in LogList:
                if items=='empty':
                    self.ui.Log_View.clear()
                    self.ui.Log_View.addItem('Ehm ... Non ci sono oggetti in scena') 
                else:
                    print LogList
                    self.ui.Log_View.clear()
                    self.ui.Log_View.addItem('Log con lo stato degli oggetti presenti in scena')
                    self.ui.Log_View.addItem('\n')
                    self.ui.Log_View.addItem('TUTTI GLI OGGETTI SONO OK')
                    self.ui.Log_View.addItem('\n')
                    self.ui.Log_View.addItem('HANNO UN SOLO UVSET E SI CHIAMA MAP1')
                    self.ui.Log_View.clear()
                    self.ui.Log_View.addItem('Log con lo stato degli oggetti presenti in scena')
                    self.ui.Log_View.addItem('\n')
                    self.ui.Log_View.addItem('ALCUNI OGGETTI SONO STATI CORRETTI')
                    #ListItems.append(items)
                    #for i in ListItems:
                        #self.ui.Log_View.addItem(i)
        
        #EMPTY FOR OBJ LIST SECTION QWIDGETLIST, CLEAR THERE FOR WHEN I ADD MULTIPLE OBJ USING THE FOR LOOP
        if ObjListShape==[]:
            self.ui.Obj_List.clear()
            self.ui.Obj_List.addItem('EMPTY')
        else:
            self.ui.Obj_List.clear()
            for bb in ObjListShape:
                self.ui.Obj_List.insertItems(self.ui.Obj_List.count(), [bb])
            

        #EMPTY FOR UV LIST SECTION QWIDGETLIST, CLEAR THERE BEACUSE THE UVSET VISUALIZED ARE RELATIVES TO THE OBJECT [I DONT WONT TO SEE ALL OF THEM LISTED]
        if UVList==[]:
            self.ui.UvSet_List.clear()
            self.ui.UvSet_List.addItem('EMPTY')
        else:
            for cc in UVList:
                self.ui.UvSet_List.clear()
                


    def StartClickList(self):

        #UPDATE MODULES >> THIS WILL ALLOW US TO HAVE SOMETHING UPDATE AT EACH CHANGE IN THE SCENE
        from imp import reload
        import SceneDetection
        reload(SceneDetection)
        from SceneDetection import ObjListShape
        from SceneDetection import UVList
        InDaScene()
        
        IndexObj=0
        
        StartClickedObj=self.ui.Obj_List.currentItem().text()
        
        #CHECK DI SICUREZZA PER EVITARE DI INSERIRE NELLA LISTA ANCHE IL PLACEHOLDER EMPTY
        if StartClickedObj!='EMPTY':
            CheckLast.append(StartClickedObj)
            if len(CheckLast)>1:
                print('Confronto OGGETTO con il precedente')
                if CheckLast[-1]==CheckLast[-2]:
                    print('OGGETTO uguale al precedente')
                    NameCheckFirst=CheckLast[-1]
                    for nn in ObjListShape:
                        if NameCheckFirst==nn:
                            IndexObjFirst=ObjListShape.index(nn)
                    UVIndexFirst=UVList[IndexObjFirst]
                    self.ui.UvSet_List.clear()
                    for uvsfirst in UVIndexFirst:
                        self.ui.UvSet_List.insertItems(self.ui.UvSet_List.count(),[uvsfirst])
                else:
                    print('OGGETTO diverso dal precedente')
                    self.ui.UvSet_List.clear()
                    NameCheckLast=CheckLast[-1]
                    #print (NameCheckLast)
                    #print (ObjectList)
                    for values in ObjListShape:
                        if NameCheckLast==values:
                            IndexObj=ObjListShape.index(values)
                            #print(IndexObj)
                    UVAtIndex=UVList[IndexObj]
                    for uvs in UVAtIndex:
                        self.ui.UvSet_List.addItem(uvs)                             
            else:
                print('Solo un OGGETTO, non posso confrontarlo con il precedente')
                #TUTTO QUESTO CHECK PERCHE DI DEFAULT NESSUN OGGETTO PARTE SELEZIONATO, SE IL PRIMO OGGETTO SELEZIONATO CON CHECKLAST==1 NON ERA IL PRIMO OGGETTO IN LISTA
                #LA SEZIONE UV LIST NON SI AGGIORNAVA CORRETTAMENTE. ALLA PRIMA SELEZIONE DEVO COMUNQUE STAMPARE UVSET RELATIVO AL PRIMO OGGETTO SELEZIONATO
                NameCheckFirst=CheckLast[0]
                for nn in ObjListShape:
                    if NameCheckFirst==nn:
                        IndexObjFirst=ObjListShape.index(nn)
                UVIndexFirst=UVList[IndexObjFirst]
                self.ui.UvSet_List.clear()
                for uvsfirst in UVIndexFirst:
                    self.ui.UvSet_List.insertItems(self.ui.UvSet_List.count(),[uvsfirst])

        else:
            pass

