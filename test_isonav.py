from isonav import main
from docopt import DocoptExit
from pytest import raises
import io
from contextlib import redirect_stdout


def test_help():
    usageStr = """Usage:
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
"""
    with raises(DocoptExit):
        isoHelpOutput = main([])
        assert isoHelpOutput == usageStr


def get_output(argv):
    f = io.StringIO()
    with redirect_stdout(f):
        main(argv)
    return f.getvalue().rstrip('\n')


def test_symbols():
    argv = ['-s', '22']
    out = get_output(argv)
    assert 'Ti' == out
    #Put more here


def test_protons():
    argv = ['--protons', 'Au']
    out = get_output(argv)
    assert '79' == out
    argv = ['--protons', 'Ag']
    out = get_output(argv)
    assert '47' == out
    # Put more here


def test_neutrons():
    argv = ['--neutrons', '195Au']
    out = get_output(argv)
    assert '116' == out
    # Put more here


def test_isotopes():
    argv = ['-i', 'Pb']
    out = get_output(argv)
    isos = """178Pb
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
191Pb
192Pb
193Pb
194Pb
195Pb
196Pb
197Pb
198Pb
199Pb
200Pb
201Pb
202Pb
203Pb
204Pb
205Pb
206Pb
207Pb
208Pb
209Pb
210Pb
211Pb
212Pb
213Pb
214Pb
215Pb
216Pb
217Pb
218Pb
219Pb
220Pb"""
    assert isos == out


def test_isomasses():
    argv = ['-im', 'Au', '--amu']
    out = get_output(argv)
    iso_masses = """169Au\t168.99808
170Au\t169.995972
171Au\t170.991875791
172Au\t171.989942284
173Au\t172.986240924
174Au\t173.984717
175Au\t174.981303712
176Au\t175.980250432
177Au\t176.976870439
178Au\t177.97603192
179Au\t178.973173654
180Au\t179.972523397
181Au\t180.970079047
182Au\t181.969617874
183Au\t182.967590635
184Au\t183.967451524
185Au\t184.965789569
186Au\t185.965952703
187Au\t186.964543155
188Au\t187.965349392
189Au\t188.963948286
190Au\t189.96469839
191Au\t190.963702248
192Au\t191.964813694
193Au\t192.964137257
194Au\t193.965417754
195Au\t194.965035225
196Au\t195.966569908
197Au\t196.966568786
198Au\t197.96824242
199Au\t198.968765282
200Au\t199.970756456
201Au\t200.971657484
202Au\t201.973856
203Au\t202.975154446
204Au\t203.977831
205Au\t204.97985
206Au\t205.98474
207Au\t206.9884
208Au\t207.99345
209Au\t208.99735
210Au\t210.0025"""
    assert iso_masses == out
