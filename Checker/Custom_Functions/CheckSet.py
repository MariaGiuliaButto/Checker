#SECTION TO CONTROL AND CORRECT THE UV SET THAT ARE WRONG
import maya.cmds as cmds

#TELLING WHERE THE SCRIPT IS IF WE CHOOSE TO MOVE IT
import sys
sys.path.append('C:\\Users\\butto\\OneDrive\\Desktop\\Checker\\Custom_Functions')

#HERE WE IMPORT THE GLOBAL VARIABLES THAT WE NEED TO RETRIEVE FROM THE SCENE ANALYSIS
from SceneDetection import ObjListShape
from SceneDetection import LogList
from SceneDetection import UVList

#GLOBAL VARIABLES
Map1Obj=[]
list_changed=[]

#DICTIONARY WITH EVERYTHING INSIDE
complete_dictionary=dict(object=ObjListShape,uvset=UVList)

#FUNCTIONS
def difference_uv(list_uv,string):
    if string in list_uv:
        list_uv.remove(string)
        return list_uv

#TO SUBTRACT AN OBJECT FROM A LIST, INPUT LIST AND ITEM
def difference_list(ls,value):
    if ls==[]:
       LogList.append('Nessuna correzione')
       print('First list is empty') 
    elif value==[]:
        print ('List to subtract is empty')
        return ls
    elif ls==value:
        print('The two list are equal, difference will be empty')
    else:
        #FOR CICLES USEFUL IN THE CASE THE UVSET IS MORE THAN 1 [REMEMBER THAT WE HAVE A LIST INSIDE A LIST FOR THE UVSET]
        for ii in value:
            if ii in ls:
                ls.remove(ii)
                return ls
            else:
                print('Check:value not in the list')


#NOW I NEED TO CREATED A LIST OF ALL NOT CORRECT OBJECT BEACUSE THIS LIST WILL BE USED FOR SOME FURTHER CONDITION
list_to_be_scanned=[]

def to_be_changed(items_list):
    if items_list==[]:
        print(LogList)
    else:
        list_to_be_scanned.append(items_list)
        return list_to_be_scanned


#FUCTION TO HAVE A LOG TO USE IN THE WINDOW
def CustomLog(ls):
    if ls==[]:
        print('No object changed')
    else:
        for items_corretti in ls:
            LogList.append(items_corretti)
        return LogList 

def CheckMap():

    #WE NEED TO ANALIZE THE COMBO >> OBJECT + UVSET

    #LIST OBJ AND UVLIST HAS ALWAYS THE SAME LENGHT, SO WE NEED JUST TO OBTAIN THE LENGHT OF ONE OF THEM
    lengthlist=len(ObjListShape)
    #THE RIGHT CORRISPONDECE BETWEEN ELEMENTS IS THE ONE LINKED BY INDEX OBJ[0] >> UVSET[0]
    for index in range(0,lengthlist):
        
        divided_dictionary=dict(object=ObjListShape[index],uvset=UVList[index])

        #FROM THE DICTIONARY WE FILTERED ONLY THE ITEMS WITH THE KEY UVSET
        uvset_filtered= dict((key,divided_dictionary[key]) for key in ['uvset'] if key in divided_dictionary)
        
        #NOW THAT WE HAVE EVERYTHING WE NEED >> WE COULD START CHECKING THE CONDITION ON THE UVSET
        #CORE OF THE CODE

        for sets in uvset_filtered:
            #HERE WE TOOK ONLY THE VALUES FROM THE KEY
            key_uv=uvset_filtered[sets]
            #AND THE LENGHT OF THIS LIST TO CREATE SOME CONDITIONS BASED ON THE NUMBER OF OBJECTS THAT WE HAVE ON THE LIST
            key_uv_lenght=len(key_uv)

            for jj in key_uv:
                #FIRST CONDITION -- FIRST ELEMENT CALLED MAP1, HERE IN THIS BLOCK WE ASSUME THAT MAP1 EXISTS
                if jj=='map1':
                #IS THE ONLY ONE IN THE LIST OR THERE ARE OTHERS?
                    if key_uv_lenght ==1:
                        #print ('CORRETTO DI PARTENZA') + '\n' + ObjListShape[index]
                        #NOW WE KNOW THAT THIS OBJ IS ALL RIGHT >> SO WE NEED TO DELETE IT FROM THE DICTIONARY TO START ANALIZING THE OTHERS REMAINING
                        del divided_dictionary['object']
                        del divided_dictionary['uvset']
                        to_be_changed(ObjListShape[index])
                        Map1Obj.append(ObjListShape[index])
                    #THEN IF WE HAVE MORE THAN ONE OBJ, IN WHICH POSITION IS MAP1 IN THE LIST [IS THE STANDARD SET THAT WE NEED TO KEEP]
                    else:
                        if key_uv[0]=='map1':
                            #print('IL PRIMO E GIUSTO, CANCELLA GLI ALTRI') + ' ' + ObjListShape[index]
                            #WHEN WE FIND AN OBJECT WITH THESE SPECS WE NEED TO DELETE FROM THE DICTIONARY AS ABOVE
                            del divided_dictionary['object']
                            del divided_dictionary['uvset']
                            #WE CREATE A LIST OF ALL UVS WITHOUT MAP1 INSIDE FOR THIS REASON WE USE THE FUNCION DIFFERENCE_LIST
                            other_uv=difference_uv(key_uv,jj)
                            #HERE WE ARE CHECKING THIS: WHAT HAPPENS IF MAP1 IS AT THE FIRST PLACE BUT THERE ORE OTHER ELEMENTS OTHER THAN MAP1
                            for uvset_to_change in other_uv:
                                if uvset_to_change !=0:
                                    #CORRECTION > WE DELETE ALL THE OTHER UVSET
                                    cmds.polyUVSet(ObjListShape[index],uvSet=uvset_to_change,delete=True)
                                    #WE SAVE THE NAME OF THE OBJECT THAT HAS TO BE CORRECTED HERE, FOR DEBUG
                                    to_be_changed(ObjListShape[index])
                        
                        #IF MAP 1 IS NOT THE FIRST ELEMENT
                        else:
                            #print 'MAP1 EXISTS BUT IS NOT THE 1ST ITEM' + ' ' + ObjListShape[index]

                            #FOR SOME MAYA RULES >> YOU CAN'T DELETE THE 1ST SET IN THE LIST
                            #SO >> WE NEED TO MOVE MAP1 TO THE 1ST PLACE AND THEN DELETE OTHERS
                            #THE SAME AS UP >> THE PLUS STEP IS JUST TO MOVE MAP1

                            #again we clean from the dictionary and the uv list to be corrected the object that have 
                            #already been corrected from the code above
                            del divided_dictionary['object']
                            del divided_dictionary['uvset']
                            other_uv=difference_uv(key_uv,jj)
                            
                            #move uvset map1 to the first place, delete other sets
                            cmds.polyUVSet(ObjListShape[index],reorder=True,nuv=other_uv[0],uvSet='map1')
                            for uvset_to_change in other_uv:
                                cmds.polyUVSet(ObjListShape[index],uvSet=uvset_to_change,delete=True)
                                #add it to the debug list
                                to_be_changed(ObjListShape[index])

        
        #NOW >> AS WE HAVE DELETED FROM THE DICTIONARY THE OBJECTS THAT HAVE ALREADY BY ANALIZED WE CAN PROCEED WITH THE REMAINING ONES
        #HERE CORRECTION OF THE OBJECTS THAT HAVENT MAP1 AT ALL IN THEIR UVSET

        if divided_dictionary=={}:
            print('ALREADY CORRECT IN THE CODE ABOVE' + ' ' + ObjListShape[index])
        else:
            #print 'TO CORRECT' + ObjListShape[index]
            #print divided_dictionary
            #print uvset_filtered
            #print key_uv
            #print key_uv_lenght
            if key_uv_lenght == 1:

                del divided_dictionary['object']
                del divided_dictionary['uvset']
                other_uv=difference_uv(key_uv,jj)

                cmds.polyUVSet(ObjListShape[index],rename=True,newUVSet='map1')
                to_be_changed(ObjListShape[index])
            
            else:
                #DEBUG >> HERE WE COULD PRINT THE NAME OF THE REMAINING OBJECT
                #print(ObjListShape[index])
                #print uvset_filtered

                del divided_dictionary['object']
                del divided_dictionary['uvset']

                list_index=[]

                for jj in key_uv:
                    list_index.append(key_uv.index(jj))
                for number in list_index:
                    if number==0:
                        cmds.polyUVSet(ObjListShape[index],rename=True,uvSet=key_uv[number],newUVSet='map1')
                    else:
                        cmds.polyUVSet(ObjListShape[index],uvSet=key_uv[number],delete=True)
                        to_be_changed(ObjListShape[index])


    #Delete History at the end just to clean up what we have done
    for obj in ObjListShape:
        cmds.delete(obj,constructionHistory=True)

    #a list with all the object scanned
    #print list_to_be_scanned

    #we have to subtract the already ok obj >> stored in the list Map1Obj
    if list_to_be_scanned == Map1Obj:
        print('list_changed remain empty, the two list to subtract are equal') 
    else:
        #using set to avoid duplicate objects
        list_changed.extend(list(set(difference_list(list_to_be_scanned,Map1Obj))))

    CustomLog(list_changed)

#DEBUG >> EXC THE FUNCTION
#CheckMap()
#print(LogList)

#OUR AIM IS TO OBTAIN THE CORRECT VALUES INSIDE THE LOGLIST LIST: ACTIVATE THIS PRINT TO CHECK THE VALUE
#print LogList
# 3 CASES >> 1. EMPTY + NESSUNA CORREZIONE --- 2. NESSUNA CORREZIONE, TUTTI GLI OGGETTI CHE C ERANO IN SCENA ERANO OK ----- 3. ELENCO OGGETTI CORRETTI
                
                



                














                    
        
    
    


