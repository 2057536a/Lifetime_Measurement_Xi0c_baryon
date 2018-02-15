# read a Tree with a style specific to Python and then thin it
# this means keeping all the branches of the tree but only for some events
# we can select the events by asking a cut, or by throwing a random number
# either way, for each event keep all the branches without the code needing to know
# what all those branches are. it means the code can be short even for trees 
# with many many branches
# ex: exThinTree("file1.root","tree1","rPt",10.0,18.0,"thinned_file1.root",False)

def exThinTree(fileName,treeName,variableName,cut_low,cut_high,outfileName,debug=False):

   # open file
    file=TFile(fileName,"READ")
    if not file.IsOpen():
        print "File",fileName,"does not exist, so will abort"
        return False

    # open tree
    tree=file.Get(treeName)
    if not exists(tree,treeName,debug):
        print "Tree",treeName,"does not exist, so will abort"
        return False

    # create the output file
    outfile=TFile(outfileName,"RECREATE")

    # create the output tree as a clone of the initial tree
    # as we create it after the outfile is created
    # it will be owned by outfile and it will be saved to outfile when outfile will be closed
    outtree=tree.CloneTree(0)

    # notice the much easier to loop over the events and retrieve the variables
    # without needing the number of entries, without setting the branch addresses first,
    # without needing the type of the variable and without needing the command of GetEntry
    for event in tree:
        value=getattr(tree,variableName)

        # now we can use the value to apply a cut on event based on this value
        if cut_low <= value <= cut_high:
            outtree.Fill()
        if debug:
            # in this simple example simply print them
            print "current value is",value,"cut_low",cut_low,"cut_high",cut_high

    # after the event loop, save the outtree (it will be saved to the outfile)
    outtree.AutoSave()
    return True
# ended function
