import ROOT


inputfile = ROOT.TFile.Open('outputfile.root')
inputtree = inputfile.Get('WeightsTree')
outputfile = ROOT.TFile.Open('outputfile_copy.root', 'recreate')
outputtree = inputtree.CopyTree("")
outputfile.Write()
