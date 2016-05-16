#!/usr/bin/python
# - python version 2.7 - #
# -*- coding: utf-8 -*- #

def GetJavaType(dbType):
  import ConfigParser
  import string, os, sys, re
  if dbType == "":
    return "NoneType"
  strinfo = re.compile(r'\(.*\)')
  dbType = strinfo.sub('',dbType)
  cf = ConfigParser.ConfigParser()
  cf.read("datatype.ini")
  return cf.get("MYSQL2JAVA", dbType)


def Convert2ClassStyle(oriStr, splitStr):
  if len(oriStr) > 1:
    oriStr = oriStr[0].upper() + oriStr[1:]
  return Convert2FieldStyle(oriStr, splitStr)


def Convert2FieldStyle(oriStr, splitStr):  
  str_list = oriStr.split(splitStr)
  if len(str_list) > 1:
    for index in range(1, len(str_list)):
      if str_list[index] != '':
        str_list[index] = str_list[index][0].upper() + str_list[index][1:]
      else:
        continue
    return ''.join(str_list)
  else:
    return oriStr


from PDMHandler import PDMHandler
if __name__ == '__main__' :
  import sys, time, string, re
  reload(sys)
  sys.setdefaultencoding("utf-8")
  if len(sys.argv) <= 1:
    print "USAGE:   ",sys.argv[0],"<filename>","[tablename]"
    print "EXAMPLE 1: ",sys.argv[0],"data/Consol.pdm"
    print "EXAMPLE 2: ",sys.argv[0],"data/Consol.pdm","UserTable"
    sys.exit(1)
  else:
    filename = sys.argv[1]
    if len(sys.argv) >= 3:
      tablename = sys.argv[2]
    else:
      tablename = ""
  try:
    ph = PDMHandler.parse(filename)
  except:
    sys.exit(1)

  filename = "dbentity.jh"
       
  output=sys.stdout
  outputfile=open("src/"+filename,'w')
  sys.stdout=outputfile
  x = time.localtime() 
  print "/*"
  print "*",filename
  print "*"
  print "* Created Date:",time.strftime('%Y-%m-%d %H:%M:%S',x)
  print "*"	
  print "* Copyright (c)  Centling Technologies Co., Ltd."
  print "*"
  print "* This software is the confidential and proprietary information of"
  print "* Centling Technologies Co., Ltd. (\"Confidential Information\"). You shall not"
  print "* disclose such Confidential Information and shall use it only in accordance"
  print "* with the terms of the license agreement you entered into with"
  print "* Centling Technologies Co., Ltd."
  print "*/"
  print ""        
  print "/**"       
  print "* @author garfield.yue"
  print "* @version 0.1<br>"
  print "*/"
  
  for pkg in PDMHandler.getPkgNodes(ph):
    pkg_attrs = PDMHandler.getPkgAttrs(pkg)
    #print "P:", pkg_attrs["Name"],pkg_attrs["Code"],pkg_attrs["Creator"]
    for tbl in PDMHandler.getTblNodesInPkg(pkg) : 
      tbl_attrs = PDMHandler.getTblAttrs(tbl)
      if tablename == "" or tablename.lower() == tbl_attrs["Name"].lower():
        genTableName = tbl_attrs["Name"]
        tmpObjTableName = genTableName.replace("cs_", "")
        #tmpRe = re.compile('^mcc_')
        #tmpObjTableName = tmpRe.sub('',genTableName)
        objTableName = Convert2ClassStyle(tmpObjTableName,'_')

        print ""
        print "entity",objTableName,"{"        
        
        colList = PDMHandler.getColNodesInTbl(tbl)
        colLen = len(colList)
        index = 0
        for col in colList :          
          col_attrs = PDMHandler.getColAttrs(col)
          dbType = GetJavaType(col_attrs["DataType"])
          objColName = Convert2FieldStyle(col_attrs["Name"],"_")
          objClassName = Convert2ClassStyle(col_attrs["Name"],"_")
          length = col_attrs["Length"]
          
          hasLen = ""
          if dbType == "String" :
            hasLen = "" if (length<=0 or length=="") else ("maxlength("+length+")")
            
          isNullable = ("required" if col_attrs["Column.Mandatory"] else "")
          
          
          if index < (colLen-1) :
            print "    "+objColName,dbType,isNullable,hasLen+","
          else:
            print "    "+objColName,dbType,isNullable,hasLen
            
          index = index + 1          
        
        
        print "  }"
        print ""
  outputfile.close()
  sys.stdout=output
print "Generate finished !!"
print "please check the socure codes : src/"+filename

