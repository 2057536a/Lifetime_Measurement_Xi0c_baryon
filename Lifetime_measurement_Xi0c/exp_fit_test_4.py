from math import sqrt
import ROOT
from ROOT import RooRealVar, RooConstVar, RooDataSet,  RooPlot, RooFit, RooArgSet, RooArgList, RooDecay, RooLinkedList, RooDataHist,RooGlobalFunc,TH1F, TH1D,TCanvas,TGraph,RooPlot, TFile, RooUnblindOffset, RooExponential

#IMPORTING HISTOGRAM###
datafile1 = ROOT.TFile("myhist2.root")                                                                                      # fetching the root file where the histogram is saved
hist2 = datafile1.Get("hist2") 


####Create observable variables###
xc_tau = ROOT.RooRealVar('Xc_TAU', 'Xc_TAU', 0.0001, 0.002)


##### FITTING AN EXPONENTIAL ####
                                                                                                                               # retrieving the histogram
binnedData = ROOT.RooDataHist("binnedData", "binnedData", ROOT.RooArgList(xc_tau),ROOT.RooFit.Import(hist2))                  # RooDataHist making

blinded_decay_constant = ROOT.RooRealVar("blindedConst","blindedConst", -10000.,-100000.,0.)                                       # Make the blinded decay constant for blinded analysis

decayConstUnblind = ROOT.RooUnblindOffset("decayConstUnblind","Unblind decay rate","blindingString", 2000, blinded_decay_constant) #Make the unblind offset

lifetimePDF = ROOT.RooExponential("lifetimePDF","lifetimePDF", xc_tau , decayConstUnblind)

result1 = lifetimePDF.fitTo(binnedData)                                                                                            # fitting the binned data

print "The decay rate is: " + str(blinded_decay_constant.getVal()) + " +/- " + str(blinded_decay_constant.getError())

print "The blinded lifetime is: " + str(1 / blinded_decay_constant.getVal()) + " and the error in the lifetime is: " + str(blinded_decay_constant.getError() / (blinded_decay_constant.getVal())**2)


lifetimePlot = xc_tau.frame()
binnedData.plotOn(lifetimePlot)      
lifetimePDF.plotOn(lifetimePlot)
lifetimePlot.Draw()

