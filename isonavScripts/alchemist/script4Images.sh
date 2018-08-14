#!/bin/bash

echo "Hello wonderful world"'!'

myDir="myAwesomeFigures"
mkdir -p $myDir

expColFile=$myDir/expandedColorCode.png
### If starting from scratch we'll need the expanded color code from

###/home/frank/Documents/congresos/cocoyoc-2018/cocoyoc2018proc/figures/expandedColorCode.png


### in order to make the proper append etc.

timeout 4 python2 chimeraGL.py -g --eRing 1i 1e 2i 2e 3i 3e 4i 4e 5i 5e 6i 6e 7i 7e 8i 8e 9i 9e --rRing S10 S11 S12 S13 S14 S15 S16 S17 S18 S19 S20 S21 S22 S23 S24 S25 S26
convert -crop +237+0 output.png outputCrop.png 
mv outputCrop.png $myDir/chim1.png

# convert -append chim1Crop.png expandedColorCode.png appendedTest.png
# The ROI for the ground state
timeout 4 python2 chimeraGL.py -g --eRing 8i 8e 9i 9e S10 S11 S12 S13 S14 S15 S16 S17 S18
convert -crop +237+0 output.png outputCrop.png 
mv outputCrop.png $myDir/gsRings.png

#The ROI for the nine
timeout 4 python2 chimeraGL.py -g --eRing 7e 8i 8e 9i 9e S10 S11 S12 S13 S14 S15 S16 S17
convert -crop +237+0 output.png outputCrop.png 
mv outputCrop.png $myDir/nineRings.png

#The ring coins example for 4.4, maybe make an image with first just
#the blue for both cases

timeout 4 python2 chimeraGL.py -g --eRing S11
convert -crop +237+0 output.png outputCrop.png 
mv outputCrop.png $myDir/fourS11.png

timeout 4 python2 chimeraGL.py -g --eRing S11 --rRing S13
convert -crop +237+0 output.png outputCrop.png 
mv outputCrop.png $myDir/fourS11S13.png

timeout 4 python2 chimeraGL.py -g --eRing S10
convert -crop +237+0 output.png outputCrop.png 
mv outputCrop.png $myDir/fourS10.png

timeout 4 python2 chimeraGL.py -g --eRing S10 --rRing S13 S14
convert -crop +237+0 output.png outputCrop.png 
mv outputCrop.png $myDir/fourS10S13S14.png

# timeout 4 python2 chimeraGL.py -g --eRing S10 --rRing S13 S14 -t 715 794 795 796 826 827 828
# mv outputCrop.png $myDir/fourS10S13S14AndTeles1.png

timeout 4 python2 chimeraGL.py -g --eRing S10 --rRing S13 S14 -t 705 784 785 786 816 817 818
convert -crop +237+0 output.png outputCrop.png 
mv outputCrop.png $myDir/fourS10S13S14AndTeles705.png

timeout 4 python2 chimeraGL.py -g --eRing 8i --rRing S14 S15 -t 500 834 835 866 867
convert -crop +237+0 output.png outputCrop.png 
mv outputCrop.png $myDir/four8iS14S15t1.png

timeout 4 python2 chimeraGL.py -g --eRing 8i --rRing S14 S15 -t 520 847 816 879 848
convert -crop +237+0 output.png outputCrop.png 
mv outputCrop.png $myDir/four8iS14S15t2.png

# Now some heatmaps
timeout 4 python2 chimeraGL.py -c 8i 3
convert -crop +237+0 output.png outputCrop.png
f2Use=$myDir/heat8it3.png
mv outputCrop.png $f2Use
convert -append $f2Use $expColFile $f2Use

# timeout 4 python2 chimeraGL.py -c 8i 4
# convert -crop +237+0 output.png outputCrop.png 
# mv outputCrop.png $myDir/heat8i4.png
# f2Use=$myDir/heat8i4.png
# convert -append $f2Use $expColFile $f2Use

# timeout 4 python2 chimeraGL.py -c 8i 5
# convert -crop +237+0 output.png outputCrop.png 
# f2Use=$myDir/heat8it3.png
# mv outputCrop.png $myDir/heat8i5.png
# f2Use=$myDir/heat8i5.png
# convert -append $f2Use $expColFile $f2Use

# timeout 4 python2 chimeraGL.py -c 8i 6
# convert -crop +237+0 output.png outputCrop.png 
# mv outputCrop.png $myDir/heat8i6.png
# f2Use=$myDir/heat8i6.png
# convert -append $f2Use $expColFile $f2Use

# timeout 4 python2 chimeraGL.py -c 8i 7
# convert -crop +237+0 output.png outputCrop.png 
# mv outputCrop.png $myDir/heat8i7.png
# f2Use=$myDir/heat8i7.png
# convert -append $f2Use $expColFile $f2Use

timeout 4 python2 chimeraGL.py -c 9i 8
convert -crop +237+0 output.png outputCrop.png 
mv outputCrop.png $myDir/heat9i8.png
f2Use=$myDir/heat9i8.png
convert -append $f2Use $expColFile $f2Use

timeout 4 python2 chimeraGL.py -c 9i 28
convert -crop +237+0 output.png outputCrop.png 
mv outputCrop.png $myDir/heat9i28.png
f2Use=$myDir/heat9i28.png
convert -append $f2Use $expColFile $f2Use

timeout 4 python2 chimeraGL.py -c S12 20
convert -crop +237+0 output.png outputCrop.png 
mv outputCrop.png $myDir/heatS12t20.png
f2Use=$myDir/heatS12t20.png
convert -append $f2Use $expColFile $f2Use

# timeout 4 python2 chimeraGL.py -c S12 22
# convert -crop +237+0 output.png outputCrop.png 
# mv outputCrop.png $myDir/heatS12t22.png
# f2Use=$myDir/heatS12t22.png
# convert -append $f2Use $expColFile $f2Use

# timeout 4 python2 chimeraGL.py -c S25 3
# convert -crop +237+0 output.png outputCrop.png 
# mv outputCrop.png $myDir/heatS25t3.png
# f2Use=$myDir/heatS25t3.png
# convert -append $f2Use $expColFile $f2Use
