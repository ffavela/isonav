# isonav

A command line tool for making quick and easy nuclear reactions
calculator.

## About

`isonav` (formerly isotope-navigator) is intended to be a command line
interface program for making calculations for nuclear reactions.

As any other command line software, the main advantage is that the
program is callable either from a user or from another program. This
is very attractive for various applications. See the "isonavScripts/"
directory for just a few script examples made for BaSH.

Works with python 3.x python 2.x support has been dropped.

INSTALLATION:

The installation process was tested only on Ubuntu 24.04 machines.

Requirements:

The python package docopt is REQUIRED. In ubuntu the package can be
installed via (for the moment this is the only package that needs sudo
powers):

```bash
$ sudo apt install python3-docopt
```

Or for linux in general via:

```bash
$ pip install docopt==0.6.2
```

To install;

    mkdir -p $HOME/.myPrograms
    cd $HOME/.myPrograms
    ln -s route/directory/for/isonav.py isonav #PAY ATTENTION HERE!

Add the following line at the end of your .bashrc (or .zshrc ...):

    export PATH=$PATH:$HOME/.myPrograms

To uninstall simply remove the symlink. In case the is empty then you
can remove it too as well as the export on your `rc` file.

If there is a previous installation and it was done via the deprecated
installScript.sh please review [LEGACY](LEGACY.md) for instructions to
uninstall it and some reasons for deprecating that method. TLDR: If
there is a legacy install present then run `sudo ./uninstallLegacy.sh`
to remove it.

Resources:

The program is far from finished, here are some resources online that
where partially used for building it.

The Isotope Explorer:
http://ie.lbl.gov/isoexpl/isoexpl.htm

Main inspiration for the program, the main problem with it is that is
only for windows, isonav does not do everything isotope explorer does
nor is it the intention.

Most of the data of isonav was taken from the ENSDF data files that the
isotope explorer uses.

TUNL:

http://www.tunl.duke.edu/

Provides an easy to use webapp for accessing nuclear data.

NNDC:

http://www.nndc.bnl.gov/

Another important resource.

USAGE:

The typical abbreviations for some isotopes can be used:

```console
1n==n  #neutron
1H==p
2H==d
3H==t
4He==a
```

Examples:

Note: All energies are in MeV The next gives a printout of the general
usage (not all functions have been implemented yet). The -v option can
be used in almost all cases (verbose).

```bash
$ isonav
Usage:
  isonav <number> [-v] (-s|--symbol)
  isonav <symbol> [-v] ([-p|--protons])
  isonav <symbol> [-v] (--name)
  isonav <iso> [-v] [-n|--neutrons] [[-i|--isotopes] [-m --amu]]
  isonav <iso> [-v] ([-m|--mass]|--compton) [--amu --liquidDrop]
  isonav <iso> [-v] --mirror
  isonav <iso> [-v] ([-r | --radius]|[(-l|--levels) [--limit=val]])
  isonav <iso> [-v] --Elab=val (--deBroglie | --redDeBroglie)
  isonav <iso> [-v] --Elab=val --L4TOF=L
  isonav <iso> [-v] --decay [--Ex=val]
  isonav <iso> [-v] (--alpha | --nEmission | --pEmission ) [--num=val]
  isonav <iso> [-v] --Emission=val [--num=val]
  isonav <iso> [-v] (--BE | --BEperNucleon) [--liquidDrop]
  isonav <iso1> <iso2> [-v] (--coulomb | --reactions [--latex] )
  isonav <iso1> <iso2> [-v] (--gamowEnergy | --T=temp --gamowPeak )
  isonav <iso1> <iso2> [-v] --fussion [--Elab=val]
  isonav <iso1> <iso2> [-v] --Elab=val --angle=val [[--xTreme|-x] --latex]
  isonav <iso1> <iso2> [-v] --scatE=val --angle=val
  isonav <isop> <isot> <isoEject> <isoRes> [-v] (-q|--QVal) [--amu]
  isonav <isop> <isot> <isoEject> <isoRes> [-v] --Elab=val --maxAng
  isonav <isop> <isot> <isoEject> <isoRes> [-v] --Elab=val --angle=val ([--xEje=val] [--xRes=val])
  isonav <isop> <isot> <isoEject> <isoRes> [-v] --Elab=val --angle=val [(-x|--xTreme) [--xF1=xFileEject.txt] [--xF2=xFileRes.txt]]
  isonav <ion> [-v] --material=matName --Elab=val (--thickness=val [--depositedE] | --range) [--bloch] [--density=dens]
  isonav [-v] --listMaterials [--material=matName]
  isonav -h | --version
```

```bash
$ isonav 22 -s
Ti
```

```bash
$ isonav Au --protons #A value can be ommited here
79
```

```bash
$ isonav Ag --name
Silver
```

```bash
$ isonav 195Au --neutrons
116
```

```bash
$ isonav Pb -i
178Pb
179Pb
180Pb
181Pb
182Pb
183Pb
184Pb
185Pb
186Pb
187Pb
188Pb
189Pb
190Pb
...
215Pb
216Pb
217Pb
218Pb
219Pb
220Pb
```

Being verbose:

```bash
$ isonav Pb -iv
Isotopes and masses, in MeV by default
178Pb
179Pb
180Pb
181Pb
182Pb
183Pb
184Pb
185Pb
186Pb
...
216Pb
217Pb
218Pb
219Pb
220Pb
```

Getting the masses and forcing to display in amu (not MeVs):

```bash
$ isonav Au -im --amu
169Au   168.99808
170Au   169.995972
171Au   170.991875791
172Au   171.989942284
173Au   172.986240924
174Au   173.984717
175Au   174.981303712
...
206Au   205.98474
207Au   206.9884
208Au   207.99345
209Au   208.99735
210Au   210.0025
```

```bash
$ isonav 22Ne --mass
20484.845484518828
```

```bash
$ isonav 22Ne --mass --liquidDrop #Using the LD model
20477.90454623588
```

```bash
$ isonav 22Ne --mirror
22Mg
```

```bash
$ isonav 40Ca -r #Nuclear radius in fm
4.103942272024073
```

```bash
$ isonav 12C --levels --limit=10
1       0.0
2       4.43891
3       7.6541999999999994
4       9.641
5       10.3
6       10.844
7       11.16
8       11.828
9       12.71
10      13.352
```

```bash
$ isonav 12C --Elab=2.0 --redDeBroglie
9.332022523394577e-06
```

These next parts are useful for identifying particles in terms of
their energy in a nuclear scattering experiment.

```bash
$ isonav d 14N a 12C --Elab=3.0 --angle=35
4He     12C
13.929  -130.521        2.645

12C     4He
5.881   -132.566        10.693
```

```bash
$ isonav d 14N a 12C --Elab=3.0 --angle=35 --xTreme
*4He    12C
1       0.000           13.929  -130.521        2.645

4He     *12C
1       0.000           13.929  -130.521        2.645
2       4.439           10.341  -127.323        1.794
3       7.654           7.710   -123.304        1.210
4       9.641           6.061   -119.175        0.872
5       10.300          5.509   -117.282        0.765
6       10.844          5.051   -115.418        0.679
7       11.160          4.784   -114.177        0.630
8       11.828          4.216   -111.055        0.531
9       12.710          3.456   -105.431        0.408
10      13.352          2.896   -99.612 0.326
11      14.083          2.245   -89.914 0.246
12      15.110          1.293   -65.497 0.171
13      15.440          0.969   -53.181 0.166
14      16.106          0.198   -16.445 0.271

14      16.106          0.003   -1.617  0.465

*12C    4He
1       0.000           5.881   -132.566        10.693
2       4.439           4.507   -130.226        7.628
3       7.654           3.478   -127.424        5.442
4       9.641           2.819   -124.675        4.114
5       10.300          2.595   -123.450        3.679
6       10.844          2.407   -122.262        3.323
7       11.160          2.297   -121.480        3.118
8       11.828          2.060   -119.539        2.687
9       12.710          1.737   -116.108        2.127
10      13.352          1.493   -112.597        1.729
11      14.083          1.200   -106.670        1.291
12      15.110          0.737   -89.285 0.728
13      15.440          0.556   -77.047 0.578

12      15.110          0.000   -0.625  1.464
13      15.440          0.016   -6.794  1.118

12C     *4He
1       0.000           5.881   -132.566        10.693
```

It can also see Coulomb excitations

```bash
$ isonav d 14N d 14N --Elab=5.5 --angle=25 --xTreme
*2H     14N
1       0.000           5.354   -75.758 0.146
2       2.225           3.116   -45.059 0.160

2H      *14N
1       0.000           5.354   -75.758 0.146
2       2.313           3.024   -43.689 0.163
3       3.948           1.267   -19.738 0.285

*14N    2H
1       0.000           1.987   -123.078        3.513
2       2.313           1.342   -108.138        1.845
3       3.948           0.513   -51.516 1.039

2       2.313           0.063   -9.113  3.124
3       3.948           0.481   -48.333 1.071

14N     *2H
1       0.000           1.987   -123.078        3.513
2       2.225           1.371   -109.124        1.905

2       2.225           0.057   -8.519  3.219
```

```bash
$ isonav d 14N --reactions -v
#Given two isotopes it returns the coulomb energy barrier
#Or the possible reactions.
#Eject  Residue Thres   QValue  coulombE
0None   16O     None    20.74   None
4He     12C     0.00    13.57   3.71
1H      15N     0.00    8.61    2.42
8Be     8Be     0.00    6.12    4.80
1n      15O     0.00    5.07    0.00
2H      14N     0.00    0.00    2.29
3He     13C     2.35    -2.06   3.80
3H      13N     4.91    -4.30   2.21
5Li     11B     4.97    -4.35   4.58
5He     11C     6.73    -5.88   3.66
6Li     10B     11.60   -10.14  4.53
7Be     9Be     12.72   -11.12  4.81
7Li     9B      12.95   -11.32  4.51
6Be     10Be    17.14   -14.98  4.83
6He     10C     19.78   -17.29  3.63
4Li     12B     25.95   -22.69  4.64
4H      12N     29.69   -25.96  2.17
8Li     8B      31.87   -27.87  4.50
3Li     13B     33.42   -29.23  4.74
9Li     7B      41.89   -36.63  4.51
...
```

```bash
$ isonav p 14N  --fussion
15O	7	7.276	0.021
```

```bash
$ isonav p 14N --fussion --Elab=0.1 -v
#Prints the fused element, if isotope exists.
#Max populated level, and energy, and remaining KE in lab
15O	7	7.276	0.121
```

```bash
$ isonav d 14N --Elab=3.0 --angle=35
4He     12C
13.929  -130.521        2.645

12C     4He
5.881   -132.566        10.693

1H      15N
11.351  -99.191 0.257

15N     1H
1.576   -118.695        10.032

8Be     8Be
5.910   -128.846        3.205

8Be     8Be
5.910   -128.846        3.205

1n      15O
7.896   -84.863 0.176

15O     1n
1.197   -112.642        6.875

2H      14N
2.848   -70.134 0.152

14N     2H
0.885   -101.910        2.115

3He     13C
0.772   -35.903 0.171

13C     3He
0.280   -50.709 0.663

0.143   -30.168 0.800
```

Where the first row after the expression is when the ejectile is
expected at the given angle and the recond is when the residual is
expected.

```bash
$ isonav d 14N --Elab=3.0 --angle=35 --xTreme
*4He    12C
1       0.000           13.929  -130.521        2.645

4He     *12C
1       0.000           13.929  -130.521        2.645
2       4.439           10.341  -127.323        1.794
3       7.654           7.710   -123.304        1.210
4       9.641           6.061   -119.175        0.872
5       10.300          5.509   -117.282        0.765
6       10.844          5.051   -115.418        0.679
7       11.160          4.784   -114.177        0.630
8       11.828          4.216   -111.055        0.531
9       12.710          3.456   -105.431        0.408
10      13.352          2.896   -99.612 0.326
11      14.083          2.245   -89.914 0.246
12      15.110          1.293   -65.497 0.171
13      15.440          0.969   -53.181 0.166
14      16.106          0.198   -16.445 0.271

14      16.106          0.003   -1.617  0.465

*12C    4He
1       0.000           5.881   -132.566        10.693
2       4.439           4.507   -130.226        7.628
...
*1H     15N
1       0.000           11.351  -99.191 0.257

1H      *15N
1       0.000           11.351  -99.191 0.257
2       5.270           6.190   -73.974 0.148
3       5.299           6.162   -73.766 0.148
4       6.324           5.148   -65.626 0.137
5       7.155           4.321   -57.981 0.133
6       7.301           4.175   -56.542 0.133
...
*15O    1n
1       0.000           1.197   -112.642        6.875
2       5.183           0.478   -80.290 2.411
3       5.241           0.466   -79.106 2.365

2       5.183           0.080   -21.882 2.810
3       5.241           0.085   -22.900 2.746

15O     *1n
1       0.000           1.197   -112.642        6.875

*2H     14N
1       0.000           2.848   -70.134 0.152
2       2.225           0.570   -21.267 0.205

2H      *14N
1       0.000           2.848   -70.134 0.152
2       2.313           0.468   -18.499 0.220

*14N    2H
1       0.000           0.885   -101.910        2.115
...
.............. You get the idea.
```

```bash
$ isonav 235U --decay
76Zn	159Sm		111.947	53.485	165.431
77Zn	158Sm		110.923	54.037	164.960
75Zn	160Sm		111.483	52.232	163.714
74Zn	161Sm		111.932	51.417	163.349
73Zn	162Sm		111.038	50.006	161.044
72Zn	163Sm		110.853	48.933	159.786
75Cu	160Eu		108.181	50.692	158.872
74Cu	161Eu		108.753	49.966	158.718
73Cu	162Eu		109.351	49.252	158.603
76Cu	159Eu		106.871	51.069	157.940
72Cu	163Eu		109.153	48.190	157.343
71Cu	164Eu		109.562	47.404	156.965
.
.Lots of stuff
.
```

```bash
$ isonav 151Lu --pEmission
1(1H)   150Yb           1.241
```

```bash
$ isonav 13Be --nEmission
1(1n)   12Be            0.510
```

```
#Double proton emission
$ isonav 45Fe --pEmission --num=2
2(1H)	43Cr		1.154
```

```bash
$ isonav n --compton -v
#The compton wavelength in fm
1.3195908515350636
```

The --xTreme cases can take some time and the outputs can become very
large, here is an example of one case:

```bash
$ isonav 14N 167Yb --Elab=5.5 --angle=20 --xTreme>14N167YbxTreme5p5MeVAngle20.txt
```

Note the redirection `>` you may want to use it in order to save long
outputs.

#This took about 80 min in my computer
