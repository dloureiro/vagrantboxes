import urllib2
import argparse
from lxml import etree
import os
import sys
import subprocess
import re

def which(program):
    """
    This function is taken from http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
    """
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def printBoxes(aList,name_format, manager_format) :
    print "%3s | %-*s | %-*s" % ("Id", name_format, "Name", manager_format, "Manager")
    print "-"*(9+name_format+manager_format)
    for box in aList :
        print "%3s | %-*s | %-*s" % (box["id"], name_format, box["name"], manager_format, box["manager"])

def addBoxToVagrant(aBox, aName) :
    print "Adding box : " + aName + " from : " + aBox["url"] + " ..."
    command = "vagrant box add \"" + aName + "\" " + aBox["url"]
    #print command
    print "command executed : " + command
    #exit()
    try :
        p = subprocess.Popen(command, stdin=subprocess.PIPE, shell=True)
        #for line in iter(p.stdout.readline,''):
        #   print line.rstrip()
        p.communicate()
        print "No error found"
    except KeyboardInterrupt :
        print ""
        p.kill()
    except subprocess.CalledProcessError as err:
        print "Error : " + err.output
    #print "vagrant box add \"%s\" %s" % (aBox["name"], aBox["url"])

def printMore(aBox) :
    print """Id : %s
Name : %s
Extended : %s
Url : %s
Size : %s
Manager : %s
""" % (aBox["id"], aBox["name"], aBox["extended"], aBox["url"], aBox["size"], aBox["manager"])

def getBoxes():
    downloaded_data  = urllib2.urlopen('http://www.vagrantbox.es/')

    tree   = etree.HTML(downloaded_data.read())

    data = []

    for elementBody in tree.iter("body"):
        elementDiv  = list(elementBody.iter("div"))[0]
        elementTable = list(elementBody.iter("table"))[0]
        elementTBody = list(elementTable.iter("tbody"))[0]
        id_value = 1
        for line in elementTBody :
            elements = list(line)
            box = {}
            box["id"] = str(id_value)
            content = re.sub("\n"," ", etree.tostring(elements[0], method="text"))
            content = re.sub("\t"," ", content)
            content = re.sub("[ ]+", " ", content)
            content = content.lstrip()
            content = content.rstrip()
            contentExtended = ""
            if "(" in content :
                pos = content.find("(")
                contentExtended = content[pos:len(content)]
                content = content[0:pos]
                content = content.lstrip()
                content = content.rstrip()
            box["name"] = content
            box["manager"] = elements[1].text
            box["url"] = elements[2].text
            box["size"] = elements[3].text
            box["extended"] = contentExtended
            data.append(box)
            id_value += 1
    return data

def search(args) :
    boxes = []
    output = getBoxes()
    data = output
    max_name_format = 1
    max_manager_format = 1
    for box in data:
        if args.search.upper() in box["name"].upper() or args.search.upper() in box["extended"].upper():
            boxes.append(box)
            max_name_format = max(max_name_format,len(box["name"]))
            max_manager_format = max(max_manager_format,len(box["manager"]))
    printBoxes(boxes,max_name_format,max_manager_format)

def listAll(args) :
    boxes = []
    output = getBoxes()
    data = output
    max_name_format = 1
    max_manager_format = 1
    for box in data:
        boxes.append(box)
        max_name_format = max(max_name_format,len(box["name"]))
        max_manager_format = max(max_manager_format,len(box["manager"]))
    printBoxes(boxes,max_name_format,max_manager_format)


def add(args) :
    data = getBoxes()

    for box in data :
        if box["id"] == args.id :
            addBoxToVagrant(box, args.name)
            break

def more(args) :
    data = getBoxes()
    for box in data :
        if box["id"] == args.more :
            printMore(box)
            break

def main() :

    vagrant_path = which("vagrant")
    if not vagrant_path :
        print "vagrant executable must be in the path to be used by vagrantboxes!"
        exit()

    parser = argparse.ArgumentParser(description="Utility used to manage the installation of boxes from vagrantbox.es")

    subparsers = parser.add_subparsers()
    # create the parser for the search command
    parser_search = subparsers.add_parser("search", help="search help")
    parser_search.add_argument("search", help="A string to search for")
    parser_search.set_defaults(func=search)

    # create the parser for the add command
    parser_add = subparsers.add_parser("add", help="add a box help")
    parser_add.add_argument("id", help="The id of the box to add")
    parser_add.add_argument("name", help="The name of the registered box")
    parser_add.set_defaults(func=add)

    # create the parser for the more command
    parser_more = subparsers.add_parser("more", help="more info help")
    parser_more.add_argument("more", help="The if of the box we want more info about")
    parser_more.set_defaults(func=more)

    parser_list = subparsers.add_parser("list", help="list help")
    parser_list.set_defaults(func=listAll)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__' :

    main()