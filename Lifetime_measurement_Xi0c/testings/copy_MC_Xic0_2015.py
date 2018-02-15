import ROOT



selectionpP = "p_P > 10000" 

selectionP = "K1_P > 1000 && K2_P > 1000 && pi_P > 1000"

selectionCHI2NDOF = "p_TRACK_CHI2NDOF < 3 && K1_TRACK_CHI2NDOF < 3 && K2_TRACK_CHI2NDOF < 3 && pi_TRACK_CHI2NDOF < 3"

selectionENDVERTEX = "Xc_ENDVERTEX_CHI2/Xc_ENDVERTEX_NDOF < 10"

selectionTAU = "1000.*Xc_TAU > 0.1" 

selectionDIRA = "Xc_DIRA_OWNPV > 0.95"  

selectionPT = "(p_PT + K1_PT + K2_PT + pi_PT) > 3000"  

selectionKPIDK = "K1_PIDK > 10 && K2_PIDK > 10"

selectionpiPIDK = "pi_PIDK < 0" 

selectionPIDp = "p_PIDp > 5"

selectionPIDpK = "(p_PIDp - p_PIDK) > 5"




inputfile = ROOT.TFile.Open('MC_Xic0_2015_prompt.root')
inputtree = inputfile.Get('DecayTree')
outputfile = ROOT.TFile.Open('MC_Xic0_2015_filtered_pP.root', 'recreate')
selection = 'p_P > 10000'
outputtree = inputtree.CopyTree(selection)
outputfile.Write()


inputfile = ROOT.TFile.Open('MC_Xic0_2015_prompt.root')
inputtree = inputfile.Get('DecayTree')
outputfile = ROOT.TFile.Open('MC_Xic0_2015_filtered_P.root', 'recreate')
selection = 'K1_P > 1000 && K2_P > 1000 && pi_P > 1000'
outputtree = inputtree.CopyTree(selection)
outputfile.Write()


inputfile = ROOT.TFile.Open('MC_Xic0_2015_prompt.root')
inputtree = inputfile.Get('DecayTree')
outputfile = ROOT.TFile.Open('MC_Xic0_2015_filtered_CHI2NDOF.root', 'recreate')
selection = 'p_TRACK_CHI2NDOF < 3 && K1_TRACK_CHI2NDOF < 3 && K2_TRACK_CHI2NDOF < 3 && pi_TRACK_CHI2NDOF < 3'
outputtree = inputtree.CopyTree(selection)
outputfile.Write()


inputfile = ROOT.TFile.Open('MC_Xic0_2015_prompt.root')
inputtree = inputfile.Get('DecayTree')
outputfile = ROOT.TFile.Open('MC_Xic0_2015_filtered_ENDVERTEX.root', 'recreate')
selection = 'Xc_ENDVERTEX_CHI2/Xc_ENDVERTEX_NDOF < 10'
outputtree = inputtree.CopyTree(selection)
outputfile.Write()


inputfile = ROOT.TFile.Open('MC_Xic0_2015_prompt.root')
inputtree = inputfile.Get('DecayTree')
outputfile = ROOT.TFile.Open('MC_Xic0_2015_filtered_TAU.root', 'recreate')
selection = '1000.*Xc_TAU > 0.1'
outputtree = inputtree.CopyTree(selection)
outputfile.Write()


inputfile = ROOT.TFile.Open('MC_Xic0_2015_prompt.root')
inputtree = inputfile.Get('DecayTree')
outputfile = ROOT.TFile.Open('MC_Xic0_2015_filtered_DIRA.root', 'recreate')
selection = 'Xc_DIRA_OWNPV > 0.95'
outputtree = inputtree.CopyTree(selection)
outputfile.Write()


inputfile = ROOT.TFile.Open('MC_Xic0_2015_prompt.root')
inputtree = inputfile.Get('DecayTree')
outputfile = ROOT.TFile.Open('MC_Xic0_2015_filtered_PT.root', 'recreate')
selection = '(p_PT + K1_PT + K2_PT + pi_PT) > 3000'
outputtree = inputtree.CopyTree(selection)
outputfile.Write()



inputfile = ROOT.TFile.Open('MC_Xic0_2015_prompt.root')
inputtree = inputfile.Get('DecayTree')
outputfile = ROOT.TFile.Open('MC_Xic0_2015_filtered_KPIDK.root', 'recreate')
selection = 'K1_PIDK > 10 && K2_PIDK > 10'
outputtree = inputtree.CopyTree(selection)
outputfile.Write()


inputfile = ROOT.TFile.Open('MC_Xic0_2015_prompt.root')
inputtree = inputfile.Get('DecayTree')
outputfile = ROOT.TFile.Open('MC_Xic0_2015_filtered_piPIDK.root', 'recreate')
selection = 'pi_PIDK < 0'
outputtree = inputtree.CopyTree(selection)
outputfile.Write()



inputfile = ROOT.TFile.Open('MC_Xic0_2015_prompt.root')
inputtree = inputfile.Get('DecayTree')
outputfile = ROOT.TFile.Open('MC_Xic0_2015_filtered_PIDp.root', 'recreate')
selection = 'p_PIDp > 5'
outputtree = inputtree.CopyTree(selection)
outputfile.Write()


inputfile = ROOT.TFile.Open('MC_Xic0_2015_prompt.root')
inputtree = inputfile.Get('DecayTree')
outputfile = ROOT.TFile.Open('MC_Xic0_2015_filtered_PIDpk.root', 'recreate')
selection = '(p_PIDp - p_PIDK) > 5'
outputtree = inputtree.CopyTree(selection)
outputfile.Write()

