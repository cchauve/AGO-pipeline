#!/usr/bin/python

#########################################
##  Original Author:         Wandrille Duchemin
##  Modifications Author: Evan Cribbie
##  Created:        20-June-2016
##  Last modified:  26-Apr-2023
##
##  Decribes functions to transform a reconciled tree in
##  NHX format into a tree in the recPhyloXML format
##
##  requires : ete3 ( http://etetoolkit.org/ )
##             ReconciledTree , and ete3-based representation of a reconciled tree
##
#########################################

from ete3 import Tree, TreeNode
from ReconciledTree import RecEvent, ReconciledTree, myBasicTreeXMLLines


def completeTreeNames(tree, useBS = False ) :
    """
    Takes:
        - tree (ete3.Tree)
        - useBS (bool) [default = False] : uses bootstrap to name nodes

    Returns:
        (ete3.Tree) : the tree, but where the nodes without a name now have one that correspond
                    to their post-order OR their bootstrap

    """

    for i,n in enumerate(tree.traverse('postorder')):
        if n.name == "":
            #print (n.support)
            if useBS:
                n.name = str(int(n.support))
            else:
                n.name = str(i)
    return tree



def parse_node_annotation(node_annotation, isLeaf = False, isDead = False, isUndated = False):
    """
    Takes:
        - node_annotation (str): reconciliation annotation on a node

    Returns:
        (list): list of dicts coding a particular event
    """
    #print("annot : ",node_annotation , isUndated)

    l_events = []
    print(node_annotation)
    if len(node_annotation) != 0 and "|LOSS" not in node_annotation:

        if node_annotation.startswith("."):
            node_annotation = node_annotation[1:]
        tmp_ann = node_annotation.split(".")

        ##further splitting multiple transfer
        s_ann = []
        for ann in tmp_ann:

            if ann.count("@") < 1:
                s_ann.append(ann)
                continue
            ## in case of transfer and loss like: T@27|SYNP2@26|ACAM1
            new_anns = ann.split("@")

            s_ann.append("@".join(new_anns[0:2]))##first tranfer, a transfer out

            for a in new_anns[2:]:##for each transfer after that (should be only one)
                s_ann.append("@" + a)

        for ann in reversed(s_ann):
            if len(ann) == 0:
                raise Exception( "empty annotation" )

            if ann[0].isdigit(): ##starts with a number spe,dup or spe+loss
                if ann.isdigit(): ##only numbers: spe or spe+loss
                    target = ann

                    ts = int(target)

                    if isUndated:
                        ts = None

                    l_events.append( RecEvent( "S" , target , ts ) )
                    break


            if ann.startswith("T@"): ##Transfer out

                ## time slice of the source
                source_ts = None
                source_sp = None

                if isUndated:
                    ## of the shape : "T@D->A"
                    source_sp = ann[2:].partition("->")[0]
                else:
                    source_ts,junk,source_sp = ann[2:].partition("|")## partitionning something like T@22|22
                    source_ts = int(source_ts)

                ##adding the event
                l_events.append( RecEvent( "bro" , source_sp , source_ts ) )
                break

            if ann.startswith("@"): # or ann.startswith("Tb@"):##transfer in or back

                pre = 3##cropping size
                if ann.startswith("@"):
                    pre = 1

                target_ts,junk,target_sp = ann[pre:].partition("|")## partitionning something like @22|22 to get the time slice and specie

                ##adding the event
                l_events.append( RecEvent( "Tb" , target_sp, int(target_ts) ) )
                break


            if ann.startswith("Tb@"):
                l_events.append( RecEvent("Bo", "-1" ) )
                break
            if ann.startswith("D@"):##Duplication

                ts = None
                sp = None
                isUndated = True
                if isUndated:
                    sp = ann[2:]
                else:
                    ts,junk,sp = ann[2:].partition("|")## partitionning something like D@23|22
                    ts = int(ts)

                l_events.append( RecEvent( "D" , sp, ts ) )
                break

    if isLeaf and ( len(l_events)==0 or l_events[-1].eventCode !="C" ) :
        ts = 0
        if isUndated:
            ts = None
        l_events.append( RecEvent("C",None,ts) ) ##temporary placeholder for the leaf species

    if isDead: ## we start in the dead so the first event MUST be Bout or Tloss

        if not l_events[0].eventCode in ["Tb", "Bo"]:

            target_ts = l_events[0].timeSlice
            target_sp = l_events[0].species

            l_events.insert(0, RecEvent( "Tb" , target_sp , target_ts ) )

    if "|LOSS" in node_annotation:
        l_events.append(RecEvent("L",node_annotation.split("|")[0],None))

    return l_events




def separateLeafNameFromLeafAnnotation( leafName , sepSp = "_" , sepAnnot = (".","@") ):
    """
    Takes:
        - leafName (str) : name of a leaf, potentially containing reconciliation information (exemple: "g_g3.T@4|3@1|g" )
        - sepSp (str) [default = "_" ] : separator between species name and gene name
        - sepAnnot (tuple) [default = (".","@") ] : possible separators between gene name and annotations

    Returns:
        (tuple)
            (str) : gene name
            (str) : reconciliation annotation  (empty string if there is none)

    """

    spName, j , gNameAndAnnot = leafName.partition( sepSp )

    x = 0
    AnnotFound = False

    while (not AnnotFound) and (x < len(gNameAndAnnot)):

        if gNameAndAnnot[x] in sepAnnot:
            AnnotFound=True
            break

        x+=1
    #print "->", leafName[:x] , leafName[x:]
    return spName + sepSp + gNameAndAnnot[:x] , gNameAndAnnot[x:]


def getLeafSpeciesFromLeafName(leafName, sepSp = "_"):
    """
    Takes:
         - leafName (str) : name of a leaf, in the format: species separator gene
         - sepSp (str) [default = "_" ] : separator between species name and gene name

    Returns:
        (str) : species name
    """

    return leafName.partition(sepSp)[0]


def ALEtreeToReconciledTree(ALEtree, isDead = False, isUndated = False , sepSp = "_"):
    """
    Recursively builds the reconciled tree

    Takes:
        - ALEtree (ete3.TreeNode) : a tree read from a reconciled ttree in the ALE format (ie. reconciliation annotations are in the .name field)
        - isDead (bool) [default = False] : indicates whether or not this lineage starts in a dead/unsampled species

    Returns:
        (ReconciledTree)
    """

    isLeaf  = ALEtree.is_leaf()

    annotation = None
    name = ALEtree.name
    if isLeaf and "|LOSS" not in ALEtree.name:
        name , annotation = separateLeafNameFromLeafAnnotation(ALEtree.name, sepSp=sepSp)
        #print("leaf parsing :", name , annotation)
    else:
        annotation = ALEtree.name

    #print "name : ",ALEtree.name
    if "|LOSS" in ALEtree.name:
        isLeaf=False
    events = parse_node_annotation(annotation, isLeaf, isDead = isDead, isUndated = isUndated )



    if isLeaf:
        ## we specify the species of the leaf event
        events[-1].species = getLeafSpeciesFromLeafName( ALEtree.name , sepSp=sepSp )

    #print [str(e) for e in events]


    if events[-1].eventCode == "Bo":
        isDead = True ## means that both children must begin by an event in the dead


    RT = ReconciledTree()
    RT.setName(name)

    current = RT

    for e in events:
        current.addEvent(e)

    for c in ALEtree.children: ##recursion on successors
        current.add_child( ALEtreeToReconciledTree(c, isDead , isUndated , sepSp=sepSp) )

    return RT




if __name__ == "__main__":

    import sys


    ##############################################
    help =  """
                Given a file containing reconciled trees in ALE reconciled tree format,
                this script writes the trees in recPhyloXML format.

                usage : python ALEtoRecPhyloXML.py -g geneFileIn [-o fileOut -s separator]
                            -g geneFileIn       : name of the file containing NHX reconciliations
                            -o fileOut          : (optional) name of the output file (default is geneFileIn + ".xml" )
                            -s separator        : (optional) separator between species and gene name (default: "_")

               """
#                            (TODO:)
#                usage : python ALEtoRecPhyloXML.py -g geneFileIn -s speciesFileIn [-o fileOut --include.species]
#                            (-s speciesFileIn    : (optional) name of the species tree file
#                            (--include.species   : (optional) whether the species tree should be included in the XML file (using the <spTree> tag)

    OK = True

    nextKEY = None
    params = {
                            "-g"    : None ,#name of the file containing NHX reconciliations
                            "-o"    : None, #(optional) name of the output file (default is geneFileIn + ".xml" )
                            "-s"    : "_", #sepparator
                            "-st"   : None #newick species tree
            }

    flagArgs = ["--include.species"]


    for i in range(1,len(sys.argv)):

        if not nextKEY is None:
            params[nextKEY] = sys.argv[i]
            print ("argument ",nextKEY,":", sys.argv[i])
            nextKEY = None
            continue

        if sys.argv[i] in params.keys():

            if sys.argv[i] in flagArgs:
                params[sys.argv[i]] = True
                print (sys.argv[i],"flag activated")
            else:
                nextKEY = sys.argv[i]
            continue
        else:
            print ("unknown argument", sys.argv[i])

    if params["-g"] is None:
        OK = False
        print ("error: gene input file not given.")

    if OK:

        ## treating positive float options
        for pname in []:
            try:
                params[pname] = float(params[pname])
                if params[pname] < 0:
                    print ("error: ",pname ,"must be a positive number.")
                    OK = False
            except:
                print ("error:",pname,"must be a positive number.")
                OK = False

        ## treating positive int options
        for pname in []:
            try:
                params[pname] = int(params[pname])
                if params[pname] < 1:
                    print ("error: ",pname ,"must be a positive integer.")
                    OK = False
            except:
                print ("error:",pname,"must be a positive number.")
                OK = False

    if not OK:
        print (help)
        exit(1)



    defaultOutputSuffix = ".xml"
    if params["-o"] is None:
        params["-o"] = params["-g"] + defaultOutputSuffix


    OUT = open(params["-o"],"w")

    OUT.write( "<recPhylo>" + "\n" )


    indentLevel = 1
    indentChar = "  "



    print ("reading input reconciled trees.")

    spTree = params["-st"]
    isUndated = True

    if spTree != None:
        f=open(spTree,"r")
        tree_f=f.readlines()
        f.close()
        if len(tree_f)!=1:
                print("ERROR: Species Tree not one line, species tree is, ",len(tree_f)," lines" )
                exit()
        treeLine=tree_f[0]
        ## found a species tree!
        spTree = Tree(treeLine)
        spTree = completeTreeNames( spTree , True)
        OUT.write( indentLevel * indentChar + "<spTree>" + "\n")
        indentLevel += 1
        lines = myBasicTreeXMLLines(spTree)
        for xmlline in lines:
                OUT.write( indentLevel * indentChar + xmlline + "\n" )
        indentLevel -= 1
        OUT.write( indentLevel * indentChar + "</spTree>" + "\n")


    IN = open(params["-g"],"r")

    l = IN.readline()

    while l != "":

        if l != "\n":

            if l.startswith("("):##special ignore white lines

                ALEtree = Tree( l, format = 1 )
                not_done=True
                while(not_done):
                    count=0
                    for node in ALEtree.traverse("postorder"):
                        if "." in node.name and "@" not in node.name and not node.name.startswith(".") and not node.name.endswith(".c"):
                            spl=node.name.split(".")
                            tmp=node.add_child(child=node.copy())
                            locals()[''.join([node.name,".c"])] = node.add_child(name=''.join([node.name,'.c']))
                            locals()['.'.join(spl[:-1])]=locals()[''.join([node.name,".c"])].add_child(child=tmp.copy(),name='.'.join(spl[:-1]))
                            tmp.delete()
                            node.delete()
                            count=1
                            break
                    if count==0:
                        not_done=False

                while(not_done):
                    count=0
                    for node in ALEtree.traverse("postorder"):
                        if "." in node.name[1:] and "@" not in node.name and node.name.startswith(".") and not node.name.endswith(".c"):
                            spl=node.name[1:].split(".")
                            tmp=node.add_child(child=node.copy())
                            locals()[''.join([node.name,".c"])] = node.add_child(name=''.join([node.name,'.c']))
                            locals()['.'.join(spl[:-1])]=locals()[''.join([node.name,".c"])].add_child(child=tmp.copy(),name='.'.join(spl[:-1]))
                            tmp.delete()
                            node.delete()
                            count=1
                            break
                    if count==0:
                        not_done=False

                if not spTree is None:
                    sister_dict={}
                    for node_test in spTree.iter_descendants("postorder"):
                        sister_dict[node_test.name]=getattr(node_test.get_sisters()[0],"name")

                not_done=True
                while(not_done):
                    count=0
                    for node in ALEtree.traverse("postorder"):
                        if len(node.get_children())==1:
                            node.add_child(name='|'.join([sister_dict[node.name.split(".")[-3].split("|")[0]],"LOSS"]))
                            count=1
                            break
                    if count==0:
                        not_done=False


                while True:
                    try:
                        RT = ALEtreeToReconciledTree(ALEtree, isUndated = isUndated , sepSp= params["-s"])
                    except ValueError as v:
                        if not isUndated:
                            print("encountered ValueError. Trying to read in undated format.")
                            isUndated = True
                        else:
                            print("encountered ValueError even when trying to read in undated format.")
                            print("error: {0}".format(v))
                            print("abort.")
                            exit(1)
                    except Exception as e:
                        print("encountered error: {0}".format(e))
                        print("this may be due to an incorrect separator between species and gene id.")
                        print("current separator: '"+params["-s"]+"'. You can change it using option -s.")
                        exit(1)
                    else:
                        print("Reconciled tree successfuly read.")
                        break


                XMLlines = RT.getTreeRecPhyloXMLLines()

                for xmlline in XMLlines:
                    OUT.write( indentLevel * indentChar + xmlline + "\n" )


            elif l.startswith("S:"):
                ## found a species tree!
                treeLine = l[2:].strip()
                print (treeLine)

                spTree = Tree( treeLine , format = 1 )

                spTree = completeTreeNames( spTree , True)

                OUT.write( indentLevel * indentChar + "<spTree>" + "\n")

                indentLevel += 1
                lines = myBasicTreeXMLLines(spTree)
                for xmlline in lines:
                        OUT.write( indentLevel * indentChar + xmlline + "\n" )

                indentLevel -= 1
                OUT.write( indentLevel * indentChar + "</spTree>" + "\n")


            elif l.startswith("#ALE"): ## trying to recognise "#ALE****_undated " prefix
                if l.partition("_")[2].startswith("undated "):
                    isUndated = True

        l = IN.readline()

    IN.close()


    OUT.write( "</recPhylo>" + "\n" )

    OUT.close()

    print ("reconciled tree converted and written.")
