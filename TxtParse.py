import re
import sys
import os.path
import pandas as pd
import numpy as np
import copy

"""
The purpose of this program was to parse through data from the website Realtor.com
and then put it into a textfile so I could perform data analysis.
"""


def Alltext_to_String()-> {str:str}:
    """This will read the textfile. It will search for relevant information about
    houses and put it into a dictionary"""
    filename= input("What file do you want to read? ")
    #filename= "Houses5.txt"
    filename+= add_txt_ext(filename)   
    house_text= HTML_list(filename)
    return Only_House(house_text)


def add_txt_ext(file:str)-> str:
    return '.txt' if file[-4:] != '.txt' else ""


def HTML_list(file:str)-> [str]:
    """It reads the text file into a list"""
    try:
        with open(file, 'r', encoding= 'utf-8') as infile:
            return [line.strip() for line in infile if line.strip() != "" ]
    except (FileExistsError , Exception) as e:
        print(e)
        sys.exit()


def Only_House(all_html:[str])-> [str]:
    """It removes non relevant house information"""
    position= Position_Address(all_html)
    house_total= Add_Info(position, all_html)
    return Remove_Duplicates(house_total, 'Brokered')


def Position_Address(all_html:[str])-> [str]:
    """This will look at a line and see if there is something resembling an address.
    For this website, The general pattern for an address is 4-5 numbers followed by a 
    capital letter. It will find the index from html and append it to a new list"""
    position= []
    for line in all_html:
        if re.findall(r'\d{4,5} [A-Z]', line[:150]) != []:
            position.append(all_html.index(line))
    return position


def Add_Info(position:[int], all_html:[str])-> [str]:
    """Puts all house info on one line so it would be easier to organize"""
    house_total= []
    for count, start in enumerate(position):
        end = len(all_html) if count == len(position) - 1 else position[count + 1]
        info = " ".join(all_html[num].rstrip() for num in list(range(start,end)))
        house_total.append(info[:1000])
        
    if len(house_total[len(house_total)-1])> 1000:
        house_total.pop(len(house_total)-1)
    return house_total


def Remove_Duplicates(long_list:[str], string:str)-> [str]:
    """Removes duplicate information if it has a certain string"""
    return [item for item in long_list if string in item]


def Break_Houses(house_unsep:{str:str})-> [{str:str}, {str:str}]:
    """It separates all house information into values in a dictionary. 
    house has all the features unchaged while house_num has integers
    when they are supposed to be ints."""
    house= {}
    Make_Keys(house, house_unsep)
    house_num= Give_Values(house, house_unsep)
    return [house, house_num]


def Make_Keys(house:{}, house_unsep:{str:str})-> None:
    """It makes the address the key to the dictionary"""
    for i in range(len(house_unsep)):
        if 'CA' in house_unsep[i]:
            full_addr= re.findall(r'\d{2,5} .+? CA \d*', house_unsep[i])
            house[full_addr[0]]= [full_addr[0]]
        
        
def Give_Values(house:{str:[str]}, house_unsep:{str:str})-> {str:[str]}:
    """This will make all the details of the house into values"""
    type_house= ['House for Sale', 'Condo/Townhome', 'Mfd/Mobile Home']
    house_RE= [r'House for Sale', r'Condo/Townhome', r'Mfd/Mobile Home']
    short_details= ['$', ('bd', 'bed'), 'ba', 'sqft', 'lot', 'car']
    list_RE= [r'\$\S*', (r'\d* bd', r'\d* bed'), r'\S* ba', r'\S* sqft',
              r'\S* \S* lot', r'\w* car']
    
    for count, type_h in enumerate(type_house):
        Type_of_House(house, house_unsep, type_h, house_RE[count])
    house_num= copy.deepcopy(house)

    for count, deets in enumerate(short_details):
        Value_to_Dict(house, house_num, house_unsep, deets, list_RE[count], True, count)
    return house_num


def Type_of_House(house:{str:str}, house_unsep:{str:str}, detail:str, RE:str)-> None:
    """It will put type of house in the dictionary"""
    for count, key in enumerate(house):
        if detail in house_unsep[count]:
            value= re.findall(RE, house_unsep[count])[0].split()
            if 'Home' in value:
                house[key].append('Mobile Home')
            else:
                house[key].append(value[0])


def Value_to_Dict(house:{str:[str]}, house_num:{str:[str]}, house_unsep:{str:str}, 
                  detail:str or (str), RE:str or (str), param:bool, Cou:int)-> None:
    """It will put details into the dictionary."""
    if type(RE)== tuple:
        Is_Tuple(house, house_num, house_unsep, detail, RE, param, Cou)
        return
    
    for count, key in enumerate(house):
        if detail in house_unsep[count]:
            value= re.findall(RE, house_unsep[count])
            house[key].append(value[0])
            num_value= re.findall(r'\d', value[0])
            string= ''.join([num for num in num_value])
            string= Exceptions(value, string)
            if house_num[key] != string:
                house_num[key].append(string)
        else:
            if param:
                try:
                    house[key][Cou+2]
                    """If it isn't able to index it, it will give an error
                    Plus 2 because we already start with
                    the address and the type of house in the dictionary """
                except:
                    house[key].append('No ' + detail)
                    house_num[key].append('-')
        

def Is_Tuple(house:{str:[str]}, house_num:{str:[str]}, house_unsep:{str:str}, 
             detail:(str), RE:(str), param:bool, Cou:int)-> None:
    """If detail is a tuple, it will run thought Value_to_Dict again but specifically
    for every value in the tuple instead of the tuple as a whole.
    This solves the problem of bedroom being defined as 'bd' or 'bed'."""
    count= 0
    for every_type in RE:
        param= False
        if every_type== RE[-1]:
            param= True
        Value_to_Dict(house, house_num, house_unsep, detail[count], RE[count], param, Cou)
        count+= 1
    return


def Exceptions(value:[str], string:str)-> str:
    """It will look at the reason why it is difficult to look for a
    specific item."""
    if '+' in value[0]:
        string= int(string) + .5
    if 'yes' in value[0]:
        string= 1
    if 'lot' in value[0]:
        if 'sqft' in value[0]:
            string= int(string)/43560
        if 'acres' in value[0]:
            string= string[:1] + '.' + string[1:]
    return string


def Output_File(house:{str:[str]}, house_num:{str:[str]})-> None:
    """It takes the information from the dictionary and either writes or appends
    it into two textfiles. The first textfile is either to read and the second
    does not have the units."""
    filename= input("What should the output file be called? ")
    filenum= filename + "_num"
    filename= add_txt_ext(filename)
    filenum= add_txt_ext(filenum)
    #filename= "all_houses.txt"
    #filenum= filename + "_num.txt"
    filename += add_txt_ext(filename)
    filenum += add_txt_ext(filenum)
    headers = ['Address', 'TypeOfHouse', 'Price$','Bedrooms',
               'Bathrooms', 'SqftHome', 'AcresLot', 'CarSpace']
    head= '\t'.join(headers)
    
    if os.path.exists(filename):
        House_app = Text_to_Dict(filename)
        House_num_app= Text_to_Dict(filenum)
        Add_Dict(house, House_app)
        Add_Dict_num(house_num, House_num_app)
        Save_Text(House_app, filename, head)
        Save_Text(House_num_app, filenum, head)
    else:
        Save_Text(house, filename, head)
        Save_Text(house_num, filenum, head)


def Text_to_Dict(filename:str)-> {str:[str]}:
    """It reads the textfile and puts the information into a dictionary."""
    text_house= {}
    f= open(filename, 'r')
    next(f)
    for line in f:
        file_list= re.split(r'\t', line.rstrip("\n"))
        text_house[file_list[0]] = [item for item in file_list]
    f.close()
    return text_house


def Add_Dict(house:{str:[str]}, house_app:{str:[str]})-> None:
    """It combines the information of the new dictionary and the textfile we are
    appending to. We are adding it to House_app."""
    for line in house:
        if line in house_app:
            for value in house[line]:
                if value not in house_app[line]:        
                    del(house_app[line])
                    house_app[line]= house[line]
                    break
        else:
            house_app[line]= house[line]


def Add_Dict_num(house_num:{str:[str]}, house_num_app:{str:[str]})-> None:
    """It combines the information of the num dictionary with the num textfile we
    are appending to."""
    for line in house_num:
        if line in house_num_app:
            for count, value in enumerate(house_num[line]):
                value= str(value)
                if value not in house_num_app[line][count]:
                    del(house_num_app[line])
                    house_num_app[line]= house_num[line]
                    break
        else:
            house_num_app[line]= house_num[line]


def Save_Text(D:{str:[str]}, filename:str, head:str)-> None:
    """It converts the dictionary into a data frame and then into a text file"""
    d= {k:v for k, v in D.items() if len(v) == 8}
    df= pd.DataFrame(d).T
    np.savetxt(filename, df.values, delimiter= '\t',
               fmt= '%s', header= head)


def main():
    houses= Alltext_to_String()
    [house, house_num]= Break_Houses(houses)
    Output_File(house, house_num)


main()












