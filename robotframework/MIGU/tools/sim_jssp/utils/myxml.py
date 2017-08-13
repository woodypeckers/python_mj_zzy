# -*- coding:utf-8 -*-
'''自定义一个xml类，使得可以增加节点，
修改节点的值，删除节点等操作，最后可以生成xmlstr
这个主要是为老严的接口设计的，所以可以根据接口定义简化
2015.9.23: 增加namespaces参数，以方便处理多个xmlns的指向问题（参考misc的soap接口中的多个url定义）
'''
import lxml
from lxml import etree
import copy

class MyXml( object ):
    def __init__( self, source = None ):
        self.root = None
        self.encoding = 'utf-8'
        if source != None:
            if source.find('<?') != -1:
                self.root = etree.fromstring( source )               
            else:
                self.root = etree.fromstring( open( source, 'r+' ).read() )

    def setRoot( self, rootName ):
        if self.root == None:
            self.root = etree.Element( rootName )

    def addNode( self, parent_xpath, nodename, nodevalue = None, parent_namespaces = None ):
        parents = self._get_elements( parent_xpath, parent_namespaces )
        # print parent
        for parent in parents:
            if nodevalue != None:
                lxml.etree.SubElement( parent, nodename ).text = nodevalue
            else:
                lxml.etree.SubElement( parent, nodename )
            # print dir( parent )
            # print lxml.etree.tostring( parent )
            # print lxml.etree.tostring( self.root )

    def addNode_Once( self, parent_xpath, nodename, nodevalue = None, parent_namespaces = None ):
        parents = self._get_elements( parent_xpath, parent_namespaces )
        parent = parents[-1]
        if nodevalue != None:
            lxml.etree.SubElement( parent, nodename ).text = nodevalue
        else:
            lxml.etree.SubElement( parent, nodename )

    def setNodesValue( self, xpath, nodevalue, namespaces = None ):
        elements = self._get_elements( xpath, namespaces )
        for element in elements:
            element.text = nodevalue

    def setNodeValue( self, xpath, nodevalue, namespaces = None ):
        element = self._get_elements( xpath, namespaces )[0]
        element.text = nodevalue
    
    def getNodeValue( self, xpath, namespaces = None ):
        elements = self._get_elements( xpath, namespaces )
        return elements[0].text

    def removeNode( self, xpath ):
        nodes = self.root.xpath( xpath )
        # print nodes
        # print dir( self.root )
        for node in nodes:
            node.clear()

    def toString( self, encoding = 'UTF-8' ):
        xmlstr = lxml.etree.tostring( self.root, encoding = encoding, xml_declaration = True, pretty_print = True, )
        # if not xmlstr.startswith( '<?' ):
        #    xmlstr = '<?xml version="1.0" encoding="UTF-8"?>\n%s' % xmlstr
        return xmlstr

    def setNodeAttribute( self, xpath, name, value ):
        element = self._get_elements( xpath )[0]
        element.attrib[name] = value

    # PRIVATE
    def _get_elements( self, xpath, namespaces = None ):
        '''获取xpath指定的所有节点'''
        # 如果获取的是root,直接返回self.root
        if len( xpath.split( '/' ) ) == 2 and xpath.split( '/' )[1] == self.root.tag:
            return [self.root, ]
        return self.root.xpath( xpath, namespaces=namespaces )

    def _get_element( self, xpath, namespaces = None ):
        '''获取xpath指定第一个节点'''
        elements = self._get_elements( xpath, namespaces )
        return elements[0]

    def _copy_element( self, xpath ):
        return copy.deepcopy( self._get_element( xpath ) )

def main():
    xmlobj = MyXml( './nosetests.xml' )
    xmlobj.addNode( '//testcase', 'chenzw', u'testcase陈振武' )
    xmlobj.addNode( '/testsuite', 'chenzw', u'testsuite陈振武' )
    xmlobj.setNodeValue( '/testsuite/chenzw', u'testsuite陈振武Modify' )
    xmlobj.setNodesValue( '//testcase/chenzw', u'testcase陈振武Modify' )
    # xmlobj.removeNode( '//testcase[@name="testcase2"]/chenzw' )
    xmlobj.setNodeAttribute( '//testcase[@name="testcase2"]', 'classname', 'somevalue' )
    # xmlobj.setNodesValue( '/testsuite/chenzw', u'陈振武' )
    # xmlobj = MyXml()
    # xmlobj.setRoot( 'root' )
    # xmlobj.addNode( '/', 't1' )
    print xmlobj.toString()
    open( 'nosetests2.xml', 'w+' ).write( xmlobj.toString( encoding = 'GB2312' ) )

if __name__ == "__main__":
    main()
