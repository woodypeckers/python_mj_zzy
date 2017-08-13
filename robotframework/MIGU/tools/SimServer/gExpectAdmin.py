# -*- coding: utf-8 -*-

'''
Created on 2015-6-4

@author: wangmianjie
'''


global G_ExpectMsg_List
G_ExpectMsg_List=[]


def removeExpMsgByGlob(expMsg):
    for msg in G_ExpectMsg_List:
        if msg.equal(expMsg) :
            G_ExpectMsg_List.remove(msg)
            

def setExpMsgMatchStatus(expMsg):
    for msg in G_ExpectMsg_List:
        if msg.equal(expMsg) :
            msg.setMatchStatus()
            
