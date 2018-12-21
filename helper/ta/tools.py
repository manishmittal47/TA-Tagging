"""This module provides some helper functions"""

def GetKeys(List):
    """Returns keys from list of dict""" 
    Ls = []
    for Dict in List:
        for K in Dict.keys():
            Ls.append(K)
    return Ls
