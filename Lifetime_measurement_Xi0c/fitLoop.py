from math import sqrt
import ROOT
from ROOT import RooRealVar, RooConstVar, RooDataSet,  RooPlot, RooFit, RooArgSet, RooArgList, RooDecay, RooLinkedList

datafile = ROOT.TFile("outputfile.root")
datatree = datafile.Get("WeightsTree")

#datatree.SetEntries(100000)

#datatree.SetBranchStatus('*', 0)
#datatree.SetBranchStatus('Xc_M', 1)
#datatree.SetBranchStatus('BDT', 1)

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
nsig = ROOT.RooRealVar('nsig','nsig', 0.1*firstfitentries, 0 , firstfitentries)                     
nbkg = ROOT.RooRealVar('nbkg','nbkg', 0.9*firstfitentries, 0 , firstfitentries)
model = ROOT.RooAddPdf('model','Sum of signal and bkg',RooArgList(chebychev,gauss),RooArgList(nbkg,nsig))

result = model.fitTo(firstfitdata)

mean.Print()
sigma.Print()
gradient.Print()

##Setting mean, sigma and gradient contant
mean.setConstant(ROOT.kTRUE)
sigma.setConstant(ROOT.kTRUE)
#gradient.setConstant(ROOT.kTRUE)


###LOOP FOR DIFFERENT DATASETS WITH REDUCE###


previous_data = data
BDT_value = -0.3

while BDT_value <= 0.2:
    next_data = previous_data.reduce("BDT > "+str(BDT_value))
    result = model.fitTo(next_data,ROOT.RooFit.Minos(ROOT.kTRUE),ROOT.RooFit.PrintLevel(-1))
    next_data_entries = next_data.numEntries()
    signal_number = nsig.getVal()
    bkg_number = nbkg.getVal()
    significance = (signal_number) / (sqrt(signal_number+bkg_number))

    print 'For BDT > ' + str(BDT_value) + 'the results are: '
    print 'Number of entries is: ' +str(next_data_entries)
    print 'number of signal is: ' + str(signal_number)
    print 'number of background is: ' + str(bkg_number)
    print 'The SIGNIFICANCE IS: ' + str(significance)
    print '--------------------------------------------------------------------------------------------'
    BDT_value += 0.01
    previous_data = next_data




