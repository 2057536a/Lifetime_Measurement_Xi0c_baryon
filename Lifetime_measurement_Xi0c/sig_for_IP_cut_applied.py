from math import sqrt
import ROOT
from ROOT import RooRealVar, RooConstVar, RooDataSet,  RooPlot, RooFit, RooArgSet, RooArgList, RooDecay, RooLinkedList, RooDataHist,RooGlobalFunc,TH1F, TH1D,TCanvas,TGraph,RooPlot, TFile, RooUnblindOffset, RooExponential

datafile = ROOT.TFile("outputfile.root")
datatree = datafile.Get("WeightsTree")

#datatree.SetEntries(100000)

datatree.SetBranchStatus('*', 0)
datatree.SetBranchStatus('Xc_M', 1)
datatree.SetBranchStatus('BDT', 1)
datatree.SetBranchStatus('Xc_TAU', 1)
datatree.SetBranchStatus('Xc_IPCHI2_OWNPV', 1)


####Create observable variables###
mass = ROOT.RooRealVar('Xc_M','Xc_M', 2420.0,2520.0)                               
bdt = ROOT.RooRealVar('BDT','BDT',-1.0,1.0)
xc_tau = ROOT.RooRealVar('Xc_TAU', 'Xc_TAU', 0.0001, 0.002)
xc_ipchi2 = ROOT.RooRealVar('Xc_IPCHI2_OWNPV','Xc_IPCHI2_OWNPV', 0.0, 9.)


###Create signal(gaussian) pdf###
mean = ROOT.RooRealVar('mean', 'Mean of Gaussian', 2471.0,2466.0,2478.0)            
sigma = ROOT.RooRealVar('sigma','Width of Gaussian',15.,0.,100.)          
gauss = ROOT.RooGaussian('gauss','Signal component',mass,mean,sigma)

###Build the Chebychev pdf with gradient parameter###
gradient = ROOT.RooRealVar('gradient','Gradient',0.,-1.,1.)
chebychev = ROOT.RooChebychev('bkg','Background', mass,RooArgList(gradient))


###Create the Roodataset###
data = ROOT.RooDataSet('data','dataset from tree', ROOT.RooArgSet(mass,bdt,xc_tau,xc_ipchi2), ROOT.RooFit.Import(datatree),ROOT.RooFit.Cut('BDT > 0.01 && Xc_IPCHI2_OWNPV < 9'))
dataEntries = data.numEntries()



###Build the composite of signal and background###
nsig = ROOT.RooRealVar('nsig','nsig', 0.1*dataEntries, 0. , dataEntries)                     
nbkg = ROOT.RooRealVar('nbkg','nbkg', 0.9*dataEntries, 0. , dataEntries)
model = ROOT.RooAddPdf('model','Sum of signal and bkg',RooArgList(chebychev,gauss),RooArgList(nbkg,nsig))


#Apply model to firstfitdata
result = model.fitTo(data)

#Prints out the shape parameters
mean.Print()
sigma.Print()
gradient.Print()


#xframe = mass.frame()
#data.plotOn(xframe)      
#model.plotOn(xframe)
#xframe.Draw()


##Setting shape parameters as contants
mean.setConstant(ROOT.kTRUE)
sigma.setConstant(ROOT.kTRUE)
gradient.setConstant(ROOT.kTRUE)

signal_number = nsig.getVal()
background_number = nbkg.getVal()


print""
print "For Xc_IPCHI2_OWNPV < 9 and BDT > 0.01 the signal is: " + str(signal_number)
print""
print".....and the background is : " + str(background_number)
print""

   
