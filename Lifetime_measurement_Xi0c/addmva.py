from xml.etree import ElementTree
from argparse import ArgumentParser
import ROOT
from array import array

class TreeFormula(object) :
    __slots__ = ('formula', 'tree', 'ttform')

    def __init__(self, formula, tree) :
        self.formula = formula
        self.tree = tree
        self.ttform = ROOT.TTreeFormula(formula, formula, tree)

    def get_entry(self, i) :
        self.tree.LoadTree(i)
        self.ttform.GetNdata()

    def evaluate(self) :
        return self.ttform.EvalInstance()

    def evaluate_entry(self, i) :
        self.get_entry(i)
        return self.evaluate()

def main() :
    ROOT.gROOT.SetBatch(True)
    argparser = ArgumentParser()
    argparser.add_argument('--inputfile')
    argparser.add_argument('--inputtree')
    argparser.add_argument('--outputfile')
    argparser.add_argument('--outputtree')
    argparser.add_argument('--weightsfile')
    argparser.add_argument('--weightsvar')
    argparser.add_argument('--maxentries', default = -1, type = int)

    args = argparser.parse_args()

    inputfile = ROOT.TFile.Open(args.inputfile)
    inputtree = inputfile.Get(args.inputtree)
    
    weightstree = ElementTree.parse(args.weightsfile)
    weightsroot = weightstree.getroot()

    reader = ROOT.TMVA.Reader('Silent')
    treevars = {}
    tmvavararrays = {}

    weightvars = weightsroot.findall('Variables')[0].findall('Variable')
    for v in weightvars :
        # This will only work when the formula corresponds to a branch, 
        # and not a combination of branches. 
        form = v.get('Expression')
        vtype = v.get('Type')

        tmvavararrays[form] = array(vtype.lower(), [0])
        reader.AddVariable(form, tmvavararrays[form])

        #treetype = inputtree.GetBranch(form).GetLeaf(form).GetTypeName()
        #treevararrays[form] = array(treetype[0].lower(), [0])
        treevars[form] = TreeFormula(form, inputtree)
        #inputtree.SetBranchAddress(form, treevararrays[form])

    spectatorvars = weightsroot.findall('Spectators')[0].findall('Spectator')
    for v in spectatorvars :
        form = v.get('Expression')
        vtype = v.get('Type')
        tmvavararrays[form] = array(vtype.lower(), [0])
        reader.AddSpectator(form, tmvavararrays[form])

        #treetype = inputtree.GetBranch(form).GetLeaf(form).GetTypeName()
        #treevararrays[form] = array(treetype[0].lower(), [0])
        treevars[form] = TreeFormula(form, inputtree)
        #inputtree.SetBranchAddress(form, treevararrays[form])

    reader.BookMVA(args.weightsvar, args.weightsfile)

    outputfile = ROOT.TFile.Open(args.outputfile, 'recreate')
    outputtree = ROOT.TTree(args.outputtree, args.outputtree)
    mvavar = array('f', [0])
    outputtree.Branch(args.weightsvar, mvavar, args.weightsvar + '/F')

    if args.maxentries == -1 :
        args.maxentries = inputtree.GetEntries()

    for i in xrange(min(args.maxentries, inputtree.GetEntries())) :
        #inputtree.GetEntry(i)
        #for key, treeval in treevararrays.iteritems() :
        #    for j in xrange(len(treeval)) :
        #        tmvavararrays[key][j] = treeval[j]
        for key, treeval in treevars.iteritems() :
            tmvavararrays[key][0] = treeval.evaluate_entry(i)

        mvavar[0] = reader.EvaluateMVA(args.weightsvar)
        outputtree.Fill()
    outputtree.Write()
    outputfile.Close()

if __name__ == '__main__' :
    main()
