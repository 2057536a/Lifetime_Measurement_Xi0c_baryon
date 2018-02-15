from math import sqrt
import ROOT
from ROOT import RooRealVar, RooConstVar, RooDataSet,  RooPlot, RooFit, RooArgSet, RooArgList, RooDecay, RooLinkedList, RooDataHist,RooGlobalFunc,TH1F, TH1D,TCanvas,TGraph,RooPlot, TFile, RooUnblindOffset, RooExponential

#IMPORTING HISTOGRAM FROM FILE###
datafile1 = ROOT.TFile("myhist0.root")           # retrieve the root file where the histogram is saved
hist0 = datafile1.Get("hist0") 


####Create observable variables###
xc_tau = ROOT.RooRealVar('Xc_TAU', 'Xc_TAU', 0.0001, 0.002)


##### FITTING AN EXPONENTIAL ####
                                                                                                                    # retrieving the histogram
binnedData = ROOT.RooDataHist("binnedData", "binnedData", ROOT.RooArgList(xc_tau),ROOT.RooFit.Import(hist0))        # RooDataHist making

blinded_decay_constant = ROOT.RooRealVar("blindedConst","blindedConst", -10000.,-100000.,0.)                        # Make the blinded decay constant for blinded analysis

decayConstUnblind = ROOT.RooUnblindOffset("decayConstUnblind","Unblind decay rate","blindingString", 2000, blinded_decay_constant) #Make the unblind offset

lifetimePDF = ROOT.RooExponential("lifetimePDF","lifetimePDF", xc_tau , decayConstUnblind)

result1 = lifetimePDF.fitTo(binnedData)                                                                             # fitting the binned data


decay_constant_value = abs(blinded_decay_constant.getVal())
decay_constant_error = blinded_decay_constant.getError()
lifetime = 1/decay_constant_value
lifetime_error = decay_constant_error / (decay_constant_value**2)
percentage = (lifetime_error / lifetime)*100

print""
print "The decay constant is: " + str(decay_constant_value) + " +/- " + str(decay_constant_error)
print""
print "The lifetime is: " + str(lifetime) + " +/- " + str(lifetime_error) + " ns."
print""
print "The uncertainty in the measurement is: " + str(percentage) + " %"


lifetimePlot = xc_tau.frame()
binnedData.plotOn(lifetimePlot)      
lifetimePDF.plotOn(lifetimePlot)
lifetimePlot.Draw()

