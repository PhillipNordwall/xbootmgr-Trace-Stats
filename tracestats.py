"""@package tracestats calculates mean and stddev on multiple windows xbootmgr
trace runs.

.xml files in the current directory are treated as being from the same series
of runs and mean and stddev of the duration are calculated on the intervals in
them. These XML files are generated via "xperf -i boot_x.etl -o boot_x.xml -a
boot".
"""
import os
import xml.dom.minidom
import sys
import getopt

def main(argv=None):
    """main is the entrance to the program.
    
    -h or --help displays usage information from the docstring.
    """
    if argv is None:
        argv = sys.argv
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print msg
	print "for help use --help"
	sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
	    sys.exit(0)
    print tracestats()

def tracestats(directory='.', ext='.xml', tagname='interval'):
    """tracestats takes calculates mean and stddev on multiple windows
    xbootmgr trace runs.
    @param directory the directory to look for files with extension ext
    @param ext the extension of the xml file
    @param tagname the tag in the xml file to look for name,duration attributes
    @returns stats dictionary
    
    .xml files in the current directory are treated as being from the same
    series of runs and mean and stddev of the duration are calculated on the
    intervals in them. These XML files are generated via
    "xperf -i boot_x.etl -o boot_x.xml -a boot".
    """
    # get the list of files ending in ext
    files=[a for a in os.listdir(directory) if ext == a[-1*len(ext):]]
    info = dict()
    for file in files:
        filedom = xml.dom.minidom.parse(directory+file)
        attributes = dict()
        # add name: duration entries to the attributes dictionary for tags
        # that match tagname
        for node in filedom.getElementsByTagName(tagname):
            name = node.getAttribute('name')
            dur = node.getAttribute('duration')
            attributes[name]=int(dur)
        # add filename: attributesdict to the info dictionary
        info[file] = attributes
    # gather the name of all the attributes in the info dicts
    keys = set()
    for entry in info:
        keys.update(info[entry].keys())
    stats = dict()
    # calculate mean and stddev for each name that exists in attributes
    for key in keys:
        selection = [info[entry][key] for entry in info]
        sellen = len(selection)
        m = sum(selection)/sellen
        s = int((sum([(entry - m)**2 for entry in selection])/sellen)**0.5)
        stats[key] = (m/1000.0, s/1000.0)
    return stats

if __name__ =="__main__":
    main()
