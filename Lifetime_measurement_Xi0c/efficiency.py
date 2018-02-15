import ROOT


datafileNo = ROOT.TFile("MC_Xic0_2015_prompt.root")
datatreeNo = datafileNo.Get("DecayTree")

datafileYes = ROOT.TFile("MC_Xic0_2015_filtered.root")
datatreeYes = datafileYes.Get("DecayTree")


htotal = ROOT.TH1F('htotal','',100, -1.,4.)
datatreeNo.Draw('Xc_TAU*1000. >> htotal')

hselected = ROOT.TH1F('hselected','',100,-1.,4.)
datatreeYes.Draw('Xc_TAU*1000. >> hselected')

heff = ROOT.TEfficiency(hselected,htotal)

heff.Draw('AP')
