#SECTION TO CONTROL AND CORRECT THE UV SET THAT ARE WRONG
import maya.cmds as cmds

#TELLING WHERE THE SCRIPT IS IF WE CHOOSE TO MOVE IT
import sys
sys.path.append('C:\\Users\\butto\\OneDrive\\Desktop\\Checker\\Custom_Functions')

from CheckSet import list_changed
#from CheckSet import CheckMap

#CheckMap()
#print(list_changed)


shapeparent=[]
attributeshape=[]
attrtodelete=[]
attributename=[]

def NodeCleaner():

    if list_changed==[]:
        print ('list empty no change to look in the NODE EDITOR')
    else:
        print('Checking NODE EDITOR')
        for ii in list_changed:
            attributeshape.append(cmds.listAttr(ii + '.uvSet', multi=True,st='uvSet'))

    for attribute in attributeshape:
        for set in attribute:
            if set != 'uvSet[0]':
                attrtodelete.append(set)

    for ii in list_changed:
        for deletable in attrtodelete:      
            cmds.removeMultiInstance(ii +'.' + deletable)



    




    



