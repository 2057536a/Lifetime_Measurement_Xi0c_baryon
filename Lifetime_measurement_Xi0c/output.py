import ROOT


datafile = ROOT.TFile("outputfile.root")
datatree = datafile.Get("WeightsTree")


#datatree.Scan()
#datatree.Print()
datatree.Show(34)
entries = datatree.GetEntries()
#print entries


#datatree.Draw("Xc_M")
#datatree.Draw("BDT")
#datatree.Draw("Xc_M >> h(300)","BDT > -0.1")
#datatree.Draw("Xc_M >> h(300,2420,2520)" , "BDT > -0.1")
'''
mylist = []
for jentry in xrange(entries):
    nb = datatree.GetEntry(jentry)
    if nb <= 0:
        continue
    myvalue = datatree.Xc_TAU
    #myvalue = datatree.Xc_IPCHI2_OWNPV
    #if myvalue <= 9:
        #print myvalue

    if myvalue >= 0.0009:
        print myvalue
    else:
        print 'no value greater than that'



    #mylist.append(myvalue)

#mylist.min()
#mylist.max()
'''
