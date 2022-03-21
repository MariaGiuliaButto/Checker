import sys

sys.path.append('C:\\Users\\butto\\OneDrive\\Desktop\\Checker\\Custom_Functions')
from SceneDetection import InDaScene
InDaScene()

sys.path.append('C:\\Users\\butto\\OneDrive\\Desktop\\Checker')

from UVSetCheck_Script import DesignerUI

if __name__ == "__main__":


    try:
        designer_ui.close() # pylint: disable=E0601
        designer_ui.deleteLater()
    except:
        pass

designer_ui=DesignerUI()
designer_ui.show()


