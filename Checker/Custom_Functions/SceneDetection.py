#SECTION TO CHECK THE OBJECT IN THE SCENE

import maya.cmds as cmds

#GLOBAL VARIABLE TO CONTAIN THE FINAL CORRECT LIST
ObjListShape=[]
LogList=[]
UVList=[]

#FUNCTIONS
#THIS ONE TO SUBTRACT ELEMENT FROM A LIST IF THEY ARE INSIDE THE LIST, INPUT ARE 2 LISTS
def RemoveFromList(startinglist,subtractlist):
    for element in subtractlist:
        if element in startinglist:
            startinglist.remove(element)
    return startinglist

'''-------------------------------------------------------------------------------------------------------------'''

#HERE WE NEED TO CHECK ALL THE ELEMENTS INSIDE THE SCENE
#OBJ TO AVOID >> GROUPS, CAMERAS [_GRP IS THE STANDARD FOR GROUPS NAME]

def InDaScene():

    #1 OBTAIN ALL THE OBJECT IN THE SCENE
    cmds.select(allDagObjects=True)
    list_scene=cmds.ls(orderedSelection=True)

    #3 OBTAIN A LIST OF GROUPS
    suffix='_GRP'
    list_groups=[]

    for element in list_scene:
        if suffix in element:
            list_groups.append(element)

    #JUST SUBTRACTING THE TWO LIST WITH THE FUNCTION CREATED ABOVE
    ObjListShape.extend(RemoveFromList(list_scene,list_groups))

    #IF EMPTY >> I ADD THE VALUE TO THE LOGLIST 
    #ELSE WE WILL CREATE A SEPARATE LIST FOR OBJ AND UVSET THAT WE WILL USE INTO ANOTHER FUNCTION >> THE ONE THAT WILL CORRECT THE UVS IF WRONG
    if ObjListShape==[]:
        LogList.append('empty')    
    else:
        for obj in ObjListShape:
            cmds.select(obj,add=True)
            UVList.append(cmds.polyUVSet(obj,query=True,allUVSets=True))

    return ObjListShape,LogList,UVList

#HERE WE EXCUTE THE FUNCTION TO GAVE THE RESULT TO ANOTHER MODULE
#InDaScene()