import ROOT


inputfile = ROOT.TFile.Open('MC_Xic0_2015_prompt.root')
inputtree = inputfile.Get('DecayTree')
outputfile = ROOT.TFile.Open('MC_Xic0_2015_filtered.root', 'recreate')
selection = 'p_P > 10000 && K1_P > 1000 && K2_P > 1000 && pi_P > 1000 && p_TRACK_CHI2NDOF < 3 && K1_TRACK_CHI2NDOF < 3 && K2_TRACK_CHI2NDOF < 3 && pi_TRACK_CHI2NDOF < 3 && Xc_ENDVERTEX_CHI2/Xc_ENDVERTEX_NDOF < 10 && 1000.*Xc_TAU > 0.1 && Xc_DIRA_OWNPV > 0.95 && (p_PT + K1_PT + K2_PT + pi_PT) > 3000 && K1_PIDK > 10 && K2_PIDK > 10 && pi_PIDK < 0 && p_PIDp > 5 && (p_PIDp - p_PIDK) > 5'
outputtree = inputtree.CopyTree(selection)
outputfile.Write()
