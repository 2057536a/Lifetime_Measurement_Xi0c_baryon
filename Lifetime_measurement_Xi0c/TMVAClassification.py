#!/usr/bin/env python
# @(#)root/tmva $Id$
# ------------------------------------------------------------------------------ #
# Project      : TMVA - a Root-integrated toolkit for multivariate data analysis #
# Package      : TMVA                                                            #
# Python script: TMVAClassification.py                                           #
#                                                                                #
# This python script provides examples for the training and testing of all the   #
# TMVA classifiers through PyROOT.                                               #
#                                                                                #
# The Application works similarly, please see:                                   #
#    TMVA/macros/TMVAClassificationApplication.C                                 #
# For regression, see:                                                           #
#    TMVA/macros/TMVARegression.C                                                #
#    TMVA/macros/TMVARegressionpplication.C                                      #
# and translate to python as done here.                                          #
#                                                                                #
# As input data is used a toy-MC sample consisting of four Gaussian-distributed  #
# and linearly correlated input variables.                                       #
#                                                                                #
# The methods to be used can be switched on and off via the prompt command, for  #
# example:                                                                       #
#                                                                                #
#    python TMVAClassification.py --methods Fisher,Likelihood                    #
#                                                                                #
# The output file "TMVA.root" can be analysed with the use of dedicated          #
# macros (simply say: root -l <../macros/macro.C>), which can be conveniently    #
# invoked through a GUI that will appear at the end of the run of this macro.    #
#                                                                                #
# for help type "python TMVAClassification.py --help"                            #
# ------------------------------------------------------------------------------ #

# --------------------------------------------
# Standard python import
import sys    # exit
import time   # time accounting
import os, ROOT

# --------------------------------------------

# # Print usage help
# def usage():
#     print " "
#     print "Usage: python %s [options]" % sys.argv[0]
#     print "  -m | --methods    : gives methods to be run (default: all methods)"
#     print "  -i | --inputfile  : name of input ROOT file (default: '%s')" % DEFAULT_INFNAME
#     print "  -o | --outputfile : name of output ROOT file containing results (default: '%s')" % DEFAULT_OUTFNAME
#     print "  -t | --inputtrees : input ROOT Trees for signal and background (default: '%s %s')" \
#           % (DEFAULT_TREESIG, DEFAULT_TREEBKG)
#     print "  -v | --verbose"
#     print "  -? | --usage      : print this help message"
#     print "  -h | --help       : print this help message"
#     print " "

# Main routine
def main():
    # Default settings for command line arguments
    DEFAULT_OUTFNAME = "TMVAXi2.root"
    DEFAULT_INFNAME  = "MC_Xic0_2015_filtered.root"
    DEFAULT_TREESIG  = "DecayTree"
    DEFAULT_TREEBKG  = "DecayTree"
    DEFAULT_METHODS  = "Cuts,CutsD,CutsPCA,CutsGA,CutsSA,Likelihood,LikelihoodD,LikelihoodPCA,LikelihoodKDE,LikelihoodMIX,PDERS,PDERSD,PDERSPCA,PDEFoam,PDEFoamBoost,KNN,LD,Fisher,FisherG,BoostedFisher,HMatrix,FDA_GA,FDA_SA,FDA_MC,FDA_MT,FDA_GAMT,FDA_MCMT,MLP,MLPBFGS,MLPBNN,CFMlpANN,TMlpANN,SVM,BDT,BDTD,BDTG,BDTB,RuleFit"

    import argparse
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-m", "--methods", default = repr(DEFAULT_METHODS.split(',')))
    argparser.add_argument("-o", "--outputfile", default = DEFAULT_OUTFNAME)
    argparser.add_argument('--variables')
    argparser.add_argument('-s', '--spectators', default = '()')
    argparser.add_argument('--signalfile', default = DEFAULT_INFNAME)
    argparser.add_argument('--signaltree', default = DEFAULT_TREESIG)
    argparser.add_argument('--signalsel', default = '')
    argparser.add_argument('--signalweight', default = '')
    argparser.add_argument('--bkgfile', default = DEFAULT_INFNAME)
    argparser.add_argument('--bkgtree', default = DEFAULT_TREEBKG)
    argparser.add_argument('--bkgsel', default = '')
    argparser.add_argument('--bkgweight', default = '')
    argparser.add_argument('--factoryname', default = "TMVAClassification")
    argparser.add_argument('-v', '--verbose', action = 'store_true', default = False)
    argparser.add_argument('--weightsdir', default = 'weights')
    argparser.add_argument('--datasetname', default = 'dataset')

    args = argparser.parse_args()

    weightsdir = args.weightsdir
    ROOT.TMVA.Config.Instance().GetIONames().fWeightFileDir = weightsdir

    # Print methods
    mlist = eval(args.methods)
    print "=== TMVAClassification: use method(s)..."
    for m in mlist:
        if m.strip() != '':
            print "=== - <%s>" % m.strip()

    # Import ROOT classes
    from ROOT import gSystem, gROOT, gApplication, TFile, TTree, TCut
    
    # check ROOT version, give alarm if 5.18 
    if gROOT.GetVersionCode() >= 332288 and gROOT.GetVersionCode() < 332544:
        print "*** You are running ROOT version 5.18, which has problems in PyROOT such that TMVA"
        print "*** does not run properly (function calls with enums in the argument are ignored)."
        print "*** Solution: either use CINT or a C++ compiled version (see TMVA/macros or TMVA/examples),"
        print "*** or use another ROOT version (e.g., ROOT 5.19)."
        sys.exit(1)
    
    # Logon not automatically loaded through PyROOT (logon loads TMVA library) load also GUI
    if os.path.exists('./TMVAlogon.C') :
        gROOT.Macro       ( "./TMVAlogon.C" )    
    
    # Import TMVA classes from ROOT
    from ROOT import TMVA

    # Output file
    outputFile = TFile( args.outputfile, 'RECREATE' )
    
    # Create instance of TMVA factory (see TMVA/macros/TMVAClassification.C for more factory options)
    # All TMVA output can be suppressed by removing the "!" (not) in 
    # front of the "Silent" argument in the option string
    factory = TMVA.Factory( args.factoryname, outputFile, 
                            "!V:!Silent:Color:!DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification" )

    # Set verbosity
    factory.SetVerbose( args.verbose )
    
    # If you wish to modify default settings 
    # (please check "src/Config.h" to see all available global options)
    #    gConfig().GetVariablePlotting()).fTimesRMS = 8.0
    #    gConfig().GetIONames()).fWeightFileDir = "myWeightDirectory"

    # Define the input variables that shall be used for the classifier training
    # note that you may also use variable expressions, such as: "3*var1/var2*abs(var3)"
    # [all types of expressions that can also be parsed by TTree::Draw( "expression" )]

    # For ROOT v6 compatibility.
    root6 = not hasattr(factory, 'AddVariable')
    if root6 :
        dataloader = ROOT.TMVA.DataLoader(args.datasetname)
    else :
        dataloader = factory

    for var in eval(args.variables) :
        if not isinstance(var, (tuple, list)) :
            var = (var,)
        try :
            dataloader.AddVariable(*var)
        except :
            print 'Failed to call dataloader.AddVariable with args', var
            raise 
    # dataloader.AddVariable( "myvar1 := var1+var2", 'F' )
    # dataloader.AddVariable( "myvar2 := var1-var2", "Expression 2", "", 'F' )
    # dataloader.AddVariable( "var3",                "Variable 3", "units", 'F' )
    # dataloader.AddVariable( "var4",                "Variable 4", "units", 'F' )

    # You can add so-called "Spectator variables", which are not used in the MVA training, 
    # but will appear in the final "TestTree" produced by TMVA. This TestTree will contain the 
    # input variables, the response values of all trained MVAs, and the spectator variables
    for var in eval(args.spectators) :
        if not isinstance(var, (tuple, list)) :
            var = (var,)
        try :
            dataloader.AddSpectator(*var)
        except :
            print 'Failed to call dataloader.AddSpectator with args', var
            raise 
    # dataloader.AddSpectator( "spec1:=var1*2",  "Spectator 1", "units", 'F' )
    # dataloader.AddSpectator( "spec2:=var1*3",  "Spectator 2", "units", 'F' )

    # Read input data
    # if gSystem.AccessPathName( infname ) != 0: gSystem.Exec( "wget http://root.cern.ch/files/" + infname )
        
    # input = TFile.Open( infname )

    # # Get the signal and background trees for training
    # signal      = input.Get( treeNameSig )
    # background  = input.Get( treeNameBkg )

    signalfile = TFile.Open(args.signalfile)
    if signalfile.IsZombie() :
        raise OSError("Couldn't find signal file " + repr(args.signalfile))
    signal = signalfile.Get(args.signaltree)
    if not signal :
        raise ValueError("Couldn't find signal TTree " + repr(args.signaltree) + " in file " + repr(args.signalfile))

    bkgfile = TFile.Open(args.bkgfile)
    if bkgfile.IsZombie() :
        raise OSError("Couldn't find bkg file " + repr(args.bkgfile))
    background = bkgfile.Get(args.bkgtree)
    if not background :
        raise ValueError("Couldn't find bkg TTree " + repr(args.bkgtree) + " in file " + repr(args.bkgfile))
        
    # Global event weights (see below for setting event-wise weights)
    signalWeight     = 1.0
    backgroundWeight = 1.0

    # ====== register trees ====================================================
    #
    # the following method is the prefered one:
    # you can add an arbitrary number of signal or background trees
    dataloader.AddSignalTree    ( signal,     signalWeight     )
    dataloader.AddBackgroundTree( background, backgroundWeight )

    # To give different trees for training and testing, do as follows:
    #    dataloader.AddSignalTree( signalTrainingTree, signalTrainWeight, "Training" )
    #    dataloader.AddSignalTree( signalTestTree,     signalTestWeight,  "Test" )
    
    # Use the following code instead of the above two or four lines to add signal and background 
    # training and test events "by hand"
    # NOTE that in this case one should not give expressions (such as "var1+var2") in the input 
    #      variable definition, but simply compute the expression before adding the event
    #
    #    # --- begin ----------------------------------------------------------
    #    
    # ... *** please lookup code in TMVA/macros/TMVAClassification.C ***
    #    
    #    # --- end ------------------------------------------------------------
    #
    # ====== end of register trees ==============================================    
            
    # Set individual event weights (the variables must exist in the original TTree)
    #    for signal    : dataloader.SetSignalWeightExpression    ("weight1*weight2");
    #    for background: dataloader.SetBackgroundWeightExpression("weight1*weight2");
    if args.signalweight :
        dataloader.SetSignalWeightExpression(args.signalweight)
    if args.bkgweight :
        dataloader.SetBackgroundWeightExpression(args.bkgweight)

    # Apply additional cuts on the signal and background sample. 
    # example for cut: mycut = TCut( "abs(var1)<0.5 && abs(var2-0.5)<1" )
    mycutSig = TCut( args.signalsel ) 
    mycutBkg = TCut( args.bkgsel ) 
    
    # Here, the relevant variables are copied over in new, slim trees that are
    # used for TMVA training and testing
    # "SplitMode=Random" means that the input events are randomly shuffled before
    # splitting them into training and test samples
    dataloader.PrepareTrainingAndTestTree( mycutSig, mycutBkg,
                                           "nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V" )

    # --------------------------------------------------------------------------------------------------

    # ---- Book MVA methods
    #
    # please lookup the various method configuration options in the corresponding cxx files, eg:
    # src/MethoCuts.cxx, etc, or here: http://tmva.sourceforge.net/optionRef.html
    # it is possible to preset ranges in the option string in which the cut optimisation should be done:
    # "...:CutRangeMin[2]=-1:CutRangeMax[2]=1"...", where [2] is the third input variable

    # Cut optimisation
    if root6 :
        # Bit of an ugly hack, but does the job.
        factory._BookMethod = factory.BookMethod
        # Don't know why 'self' isn't passed here?
        def BookMethod(*args) :
            factory._BookMethod(dataloader, *args)
        factory.BookMethod = BookMethod

    if "Cuts" in mlist:
        factory.BookMethod( TMVA.Types.kCuts, "Cuts",
                            "!H:!V:FitMethod=MC:EffSel:SampleSize=200000:VarProp=FSmart" )

    if "CutsD" in mlist:
        factory.BookMethod( TMVA.Types.kCuts, "CutsD",
                            "!H:!V:FitMethod=MC:EffSel:SampleSize=200000:VarProp=FSmart:VarTransform=Decorrelate" )

    if "CutsPCA" in mlist:
        factory.BookMethod( TMVA.Types.kCuts, "CutsPCA",
                            "!H:!V:FitMethod=MC:EffSel:SampleSize=200000:VarProp=FSmart:VarTransform=PCA" )

    if "CutsGA" in mlist:
        factory.BookMethod( TMVA.Types.kCuts, "CutsGA",
                            "H:!V:FitMethod=GA:CutRangeMin[0]=-10:CutRangeMax[0]=10:VarProp[1]=FMax:EffSel:Steps=30:Cycles=3:PopSize=400:SC_steps=10:SC_rate=5:SC_factor=0.95" )

    if "CutsSA" in mlist:
        factory.BookMethod( TMVA.Types.kCuts, "CutsSA",
                            "!H:!V:FitMethod=SA:EffSel:MaxCalls=150000:KernelTemp=IncAdaptive:InitialTemp=1e+6:MinTemp=1e-6:Eps=1e-10:UseDefaultScale" )

    # Likelihood ("naive Bayes estimator")
    if "Likelihood" in mlist:
        factory.BookMethod( TMVA.Types.kLikelihood, "Likelihood",
                            "H:!V:!TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmoothBkg[1]=10:NSmooth=1:NAvEvtPerBin=50" )

    # Decorrelated likelihood
    if "LikelihoodD" in mlist:
        factory.BookMethod( TMVA.Types.kLikelihood, "LikelihoodD",
                            "!H:!V:TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmooth=5:NAvEvtPerBin=50:VarTransform=Decorrelate" )

    # PCA-transformed likelihood
    if "LikelihoodPCA" in mlist:
        factory.BookMethod( TMVA.Types.kLikelihood, "LikelihoodPCA",
                            "!H:!V:!TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmooth=5:NAvEvtPerBin=50:VarTransform=PCA" ) 

    # Use a kernel density estimator to approximate the PDFs
    if "LikelihoodKDE" in mlist:
        factory.BookMethod( TMVA.Types.kLikelihood, "LikelihoodKDE",
                            "!H:!V:!TransformOutput:PDFInterpol=KDE:KDEtype=Gauss:KDEiter=Adaptive:KDEFineFactor=0.3:KDEborder=None:NAvEvtPerBin=50" ) 

    # Use a variable-dependent mix of splines and kernel density estimator
    if "LikelihoodMIX" in mlist:
        factory.BookMethod( TMVA.Types.kLikelihood, "LikelihoodMIX",
                            "!H:!V:!TransformOutput:PDFInterpolSig[0]=KDE:PDFInterpolBkg[0]=KDE:PDFInterpolSig[1]=KDE:PDFInterpolBkg[1]=KDE:PDFInterpolSig[2]=Spline2:PDFInterpolBkg[2]=Spline2:PDFInterpolSig[3]=Spline2:PDFInterpolBkg[3]=Spline2:KDEtype=Gauss:KDEiter=Nonadaptive:KDEborder=None:NAvEvtPerBin=50" ) 

    # Test the multi-dimensional probability density estimator
    # here are the options strings for the MinMax and RMS methods, respectively:
    #      "!H:!V:VolumeRangeMode=MinMax:DeltaFrac=0.2:KernelEstimator=Gauss:GaussSigma=0.3" );
    #      "!H:!V:VolumeRangeMode=RMS:DeltaFrac=3:KernelEstimator=Gauss:GaussSigma=0.3" );
    if "PDERS" in mlist:
        factory.BookMethod( TMVA.Types.kPDERS, "PDERS",
                            "!H:!V:NormTree=T:VolumeRangeMode=Adaptive:KernelEstimator=Gauss:GaussSigma=0.3:NEventsMin=400:NEventsMax=600" )

    if "PDERSD" in mlist:
        factory.BookMethod( TMVA.Types.kPDERS, "PDERSD",
                            "!H:!V:VolumeRangeMode=Adaptive:KernelEstimator=Gauss:GaussSigma=0.3:NEventsMin=400:NEventsMax=600:VarTransform=Decorrelate" )

    if "PDERSPCA" in mlist:
        factory.BookMethod( TMVA.Types.kPDERS, "PDERSPCA",
                             "!H:!V:VolumeRangeMode=Adaptive:KernelEstimator=Gauss:GaussSigma=0.3:NEventsMin=400:NEventsMax=600:VarTransform=PCA" )

   # Multi-dimensional likelihood estimator using self-adapting phase-space binning
    if "PDEFoam" in mlist:
        factory.BookMethod( TMVA.Types.kPDEFoam, "PDEFoam",
                            "!H:!V:SigBgSeparate=F:TailCut=0.001:VolFrac=0.0666:nActiveCells=500:nSampl=2000:nBin=5:Nmin=100:Kernel=None:Compress=T" )

    if "PDEFoamBoost" in mlist:
        factory.BookMethod( TMVA.Types.kPDEFoam, "PDEFoamBoost",
                            "!H:!V:Boost_Num=30:Boost_Transform=linear:SigBgSeparate=F:MaxDepth=4:UseYesNoCell=T:DTLogic=MisClassificationError:FillFoamWithOrigWeights=F:TailCut=0:nActiveCells=500:nBin=20:Nmin=400:Kernel=None:Compress=T" )

    # K-Nearest Neighbour classifier (KNN)
    if "KNN" in mlist:
        factory.BookMethod( TMVA.Types.kKNN, "KNN",
                            "H:nkNN=20:ScaleFrac=0.8:SigmaFact=1.0:Kernel=Gaus:UseKernel=F:UseWeight=T:!Trim" )

    # H-Matrix (chi2-squared) method
    if "HMatrix" in mlist:
        factory.BookMethod( TMVA.Types.kHMatrix, "HMatrix", "!H:!V" )

    # Linear discriminant (same as Fisher discriminant)
    if "LD" in mlist:
        factory.BookMethod( TMVA.Types.kLD, "LD", "H:!V:VarTransform=None:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=50:NsmoothMVAPdf=10" )

    # Fisher discriminant (same as LD)
    if "Fisher" in mlist:
        factory.BookMethod( TMVA.Types.kFisher, "Fisher", "H:!V:Fisher:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=50:NsmoothMVAPdf=10" )

    # Fisher with Gauss-transformed input variables
    if "FisherG" in mlist:
        factory.BookMethod( TMVA.Types.kFisher, "FisherG", "H:!V:VarTransform=Gauss" )

    # Composite classifier: ensemble (tree) of boosted Fisher classifiers
    if "BoostedFisher" in mlist:
        factory.BookMethod( TMVA.Types.kFisher, "BoostedFisher", 
                            "H:!V:Boost_Num=20:Boost_Transform=log:Boost_Type=AdaBoost:Boost_AdaBoostBeta=0.2" )

    # Function discrimination analysis (FDA) -- test of various fitters - the recommended one is Minuit (or GA or SA)
    if "FDA_MC" in mlist:
        factory.BookMethod( TMVA.Types.kFDA, "FDA_MC",
                            "H:!V:Formula=(0)+(1)*x0+(2)*x1+(3)*x2+(4)*x3:ParRanges=(-1,1)(-10,10);(-10,10);(-10,10);(-10,10):FitMethod=MC:SampleSize=100000:Sigma=0.1" );

    if "FDA_GA" in mlist:
        factory.BookMethod( TMVA.Types.kFDA, "FDA_GA",
                            "H:!V:Formula=(0)+(1)*x0+(2)*x1+(3)*x2+(4)*x3:ParRanges=(-1,1)(-10,10);(-10,10);(-10,10);(-10,10):FitMethod=GA:PopSize=300:Cycles=3:Steps=20:Trim=True:SaveBestGen=1" );

    if "FDA_SA" in mlist:
        factory.BookMethod( TMVA.Types.kFDA, "FDA_SA",
                            "H:!V:Formula=(0)+(1)*x0+(2)*x1+(3)*x2+(4)*x3:ParRanges=(-1,1)(-10,10);(-10,10);(-10,10);(-10,10):FitMethod=SA:MaxCalls=15000:KernelTemp=IncAdaptive:InitialTemp=1e+6:MinTemp=1e-6:Eps=1e-10:UseDefaultScale" );

    if "FDA_MT" in mlist:
        factory.BookMethod( TMVA.Types.kFDA, "FDA_MT",
                            "H:!V:Formula=(0)+(1)*x0+(2)*x1+(3)*x2+(4)*x3:ParRanges=(-1,1)(-10,10);(-10,10);(-10,10);(-10,10):FitMethod=MINUIT:ErrorLevel=1:PrintLevel=-1:FitStrategy=2:UseImprove:UseMinos:SetBatch" );

    if "FDA_GAMT" in mlist:
        factory.BookMethod( TMVA.Types.kFDA, "FDA_GAMT",
                            "H:!V:Formula=(0)+(1)*x0+(2)*x1+(3)*x2+(4)*x3:ParRanges=(-1,1)(-10,10);(-10,10);(-10,10);(-10,10):FitMethod=GA:Converger=MINUIT:ErrorLevel=1:PrintLevel=-1:FitStrategy=0:!UseImprove:!UseMinos:SetBatch:Cycles=1:PopSize=5:Steps=5:Trim" );

    if "FDA_MCMT" in mlist:
        factory.BookMethod( TMVA.Types.kFDA, "FDA_MCMT",
                            "H:!V:Formula=(0)+(1)*x0+(2)*x1+(3)*x2+(4)*x3:ParRanges=(-1,1)(-10,10);(-10,10);(-10,10);(-10,10):FitMethod=MC:Converger=MINUIT:ErrorLevel=1:PrintLevel=-1:FitStrategy=0:!UseImprove:!UseMinos:SetBatch:SampleSize=20" );

    # TMVA ANN: MLP (recommended ANN) -- all ANNs in TMVA are Multilayer Perceptrons
    if "MLP" in mlist:
        factory.BookMethod( TMVA.Types.kMLP, "MLP", "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:!UseRegulator" )

    if "MLPBFGS" in mlist:
        factory.BookMethod( TMVA.Types.kMLP, "MLPBFGS", "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:TrainingMethod=BFGS:!UseRegulator" )

    if "MLPBNN" in mlist:
        factory.BookMethod( TMVA.Types.kMLP, "MLPBNN", "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:TrainingMethod=BFGS:UseRegulator" ) # BFGS training with bayesian regulators

    # CF(Clermont-Ferrand)ANN
    if "CFMlpANN" in mlist:
        factory.BookMethod( TMVA.Types.kCFMlpANN, "CFMlpANN", "!H:!V:NCycles=2000:HiddenLayers=N+1,N"  ) # n_cycles:#nodes:#nodes:...  

    # Tmlp(Root)ANN
    if "TMlpANN" in mlist:
        factory.BookMethod( TMVA.Types.kTMlpANN, "TMlpANN", "!H:!V:NCycles=200:HiddenLayers=N+1,N:LearningMethod=BFGS:ValidationFraction=0.3"  ) # n_cycles:#nodes:#nodes:...

    # Support Vector Machine
    if "SVM" in mlist:
        factory.BookMethod( TMVA.Types.kSVM, "SVM", "Gamma=0.25:Tol=0.001:VarTransform=Norm" )

    # Boosted Decision Trees
    if "BDTG" in mlist:
        factory.BookMethod( TMVA.Types.kBDT, "BDTG",
                            "!H:!V:NTrees=1000:MinNodeSize=1.5%:BoostType=Grad:Shrinkage=0.10:UseBaggedGrad:GradBaggingFraction=0.5:nCuts=20:MaxDepth=2" )                        

    if "BDT" in mlist:
        factory.BookMethod( TMVA.Types.kBDT, "BDT",
                           "!H:!V:NTrees=850:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:SeparationType=GiniIndex:nCuts=20" )

    if "BDTB" in mlist:
        factory.BookMethod( TMVA.Types.kBDT, "BDTB",
                           "!H:!V:NTrees=400:BoostType=Bagging:SeparationType=GiniIndex:nCuts=20" )

    if "BDTD" in mlist:
        factory.BookMethod( TMVA.Types.kBDT, "BDTD",
                           "!H:!V:NTrees=400:MinNodeSize=5%:MaxDepth=3:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=20:VarTransform=Decorrelate" )

    # RuleFit -- TMVA implementation of Friedman's method
    if "RuleFit" in mlist:
        factory.BookMethod( TMVA.Types.kRuleFit, "RuleFit",
                            "H:!V:RuleFitModule=RFTMVA:Model=ModRuleLinear:MinImp=0.001:RuleMinDist=0.001:NTrees=20:fEventsMin=0.01:fEventsMax=0.5:GDTau=-1.0:GDTauPrec=0.01:GDStep=0.01:GDNSteps=10000:GDErrScale=1.02" )

    # --------------------------------------------------------------------------------------------------
            
    # ---- Now you can tell the factory to train, test, and evaluate the MVAs. 

    # Train MVAs
    factory.TrainAllMethods()
    
    # Test MVAs
    factory.TestAllMethods()
    
    # Evaluate MVAs
    factory.EvaluateAllMethods()    
    
    # Save the output.
    outputFile.Close()
    
    print "=== wrote root file %s\n" % outputFile.GetName()
    print "=== TMVAClassification is done!\n"
    
    # open the GUI for the result macros    
    if not ROOT.gROOT.IsBatch() :
        if hasattr(TMVA, 'TMVAGui') :
            TMVA.TMVAGui(outputFile.GetName())
            raw_input('Hit enter to quit.')
        elif 'ROOTSYS' in os.environ :
            tmvaguipath = os.path.join(os.environ['ROOTSYS'], 'tutorials', 'tmva')
            if os.path.exists(os.path.join(tmvaguipath, 'TMVAGui.C')) :
                gROOT.SetMacroPath(tmvaguipath)
                gROOT.LoadMacro   ( "TMVAGui.C" )
                try :
                    gROOT.ProcessLine( "TMVAGui(\"%s\")" % outputFile.GetName() )
                    raw_input('Hit enter to quit.')
                except RuntimeError :
                    print "Couldn't run TMVAGui!"

    outputfilename = outputFile.GetName()
    weightsfiles = dict((m, os.path.join(weightsdir, args.factoryname + '_' + m + '.weights.xml')) for m in mlist)
    classfiles = dict((m, os.path.join(weightsdir, args.factoryname + '_' + m + '.class.C')) for m in mlist)

    # keep the ROOT thread running (this makes the function hang). 
    #gApplication.Run() 

    # TMVA disables unused branches when copying the trees then doesn't change them back. 
    background.SetBranchStatus('*', 1)
    signal.SetBranchStatus('*', 1)
    if 'signalfile' in locals() :
        signalfile.Close()
    if 'bkgfile' in locals() :
        bkgfile.Close()
    return locals()

# ----------------------------------------------------------

locals().update(main())
