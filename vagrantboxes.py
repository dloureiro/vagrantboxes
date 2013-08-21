import urllib2
import argparse
from lxml import etree

def printBoxes(aList,name_format, manager_format) :
    print "%3s\t %*s\t %*s" % ("Id", name_format, "Name", manager_format, "Manager")
    for box in aList :
        print "%3s\t %*s\t %*s" % (box["id"], name_format, box["name"], manager_format, box["manager"])

def addBoxToVagrant(aBox) :
    print "vagrant box add \"%s\" %s" % (aBox["name"], aBox["url"])

def printMore(aBox) :
    print """Id : %s
Name : %s
Url : %s
Size : %s
Manager : %s
""" % (aBox["id"], aBox["name"], aBox["url"], aBox["size"], aBox["manager"])

def main() :

    parser = argparse.ArgumentParser(description="Utility used to manage the installation of boxes from vagrantbox.es")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-s", "--search", dest="search", help="A string to search for")
    group.add_argument("-a", "--add", dest="add", help="The id of the box to add")
    group.add_argument("-m", "--more", dest="more", help="The id of the box we want more info about")

    args = parser.parse_args()

    downloaded_data  = urllib2.urlopen('http://www.vagrantbox.es/')

    tree   = etree.HTML(downloaded_data.read())

    data = []

    max_name_format = 1
    max_manager_format = 1

    for elementBody in tree.iter("body"):
        elementDiv  = list(elementBody.iter("div"))[0]
        elementTable = list(elementBody.iter("table"))[0]
        elementTBody = list(elementTable.iter("tbody"))[0]
        id_value = 1
        for line in elementTBody :
            elements = list(line)
            box = {}
            box["id"] = str(id_value)
            box["name"] = elements[0].text
            box["manager"] = elements[1].text
            box["url"] = elements[2].text
            box["size"] = elements[3].text
            data.append(box)
            id_value += 1
            max_name_format = max(max_name_format,len(box["name"]))
            max_manager_format = max(max_manager_format,len(box["manager"]))

    if args.search :
        boxes = []
        for box in data :
            if args.search.upper() in box["name"].upper() :
                boxes.append(box)
        printBoxes(boxes,max_name_format,max_manager_format)
    elif args.add :
        for box in data :
            if box["id"] == args.add :
                addBoxToVagrant(box)
                break
    elif args.more :
        for box in data :
            if box["id"] == args.more :
                printMore(box)
                break
    else :
        parser.print_help()

if __name__ == '__main__' :

    main()