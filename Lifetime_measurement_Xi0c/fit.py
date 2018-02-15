from math import sqrt
import ROOT
from ROOT import RooRealVar, RooConstVar, RooDataSet,  RooPlot, RooFit, RooArgSet, RooArgList, RooDecay, RooLinkedList

datafile = ROOT.TFile("outputfile.root")
datatree = datafile.Get("WeightsTree")

#datatree.SetEntries(600000)

datatree.SetBranchStatus('*', 0)
datatree.SetBranchStatus('Xc_M', 1)
datatree.SetBranchStatus('BDT', 1)

####Create observable variables###
mass = ROOT.RooRealVar('Xc_M','Xc_M', 2420,2520)                               
bdt = ROOT.RooRealVar('BDT','BDT',-1,1)

###Create signal(gaussian) pdf###
mean = ROOT.RooRealVar('mean', 'Mean of Gaussian', 2471,2466,2478)            
sigma = ROOT.RooRealVar('sigma','Width of Gaussian',15.,0.,100.)          
gauss = ROOT.RooGaussian('gauss','Signal component',mass,mean,sigma)

###Build the Chebychev pdf with gradient parameter###
gradient = ROOT.RooRealVar('gradient','Gradient',0.,-1.,1.)
chebychev = ROOT.RooChebychev('bkg','Background', mass,RooArgList(gradient))

###Create the Roodataset###
data = ROOT.RooDataSet('data','dataset from tree', ROOT.RooArgSet(mass,bdt), ROOT.RooFit.Import(datatree),ROOT.RooFit.Cut('BDT > -0.3'))
dataentries = data.numEntries()
firstfitdata = data.reduce('BDT > 0.1')
firstfitentries = firstfitdata.numEntries()

###Build the composite of signal and background###
nsig = ROOT.RooRealVar('nsig','nsig', 0.1*dataentries, 0. , dataentries)
nbkg = ROOT.RooRealVar('nbkg','nbkg', 0.9*dataentries, 0. , dataentries)
model = ROOT.RooAddPdf('model','Sum of signal and bkg',RooArgList(chebychev,gauss),RooArgList(nbkg,nsig))

result = model.fitTo(firstfitdata)        

mean.Print()
sigma.Print()
gradient.Print()

##Setting mean, sigma and gradient contant
mean.setConstant(ROOT.kTRUE)
sigma.setConstant(ROOT.kTRUE)
gradient.setConstant(ROOT.kTRUE)

result = model.fitTo(firstfitdata,ROOT.RooFit.Minos(ROOT.kTRUE),ROOT.RooFit.PrintLevel(-1))       

xframe = mass.frame()
firstfitdata.plotOn(xframe)      
model.plotOn(xframe)
xframe.Draw()



