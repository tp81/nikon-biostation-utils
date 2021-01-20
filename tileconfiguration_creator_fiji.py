import os
from glob import glob

#@ File(style='directory') indir
#@ Boolean doStitching
#@ Float(value=1) xmul
#@ Float(value=1) ymul
#@ Boolean(value=False) swapxy

indir = indir.getAbsolutePath()

infiles = glob(os.path.join(indir,'*.ics'))

TROW = '{}; ; ({},{})\n'

TEMPLATE = '''
# Define the number of dimensions we are working on
dim = 2

# Define the image coordinates
'''

outfile = os.path.join(indir,'TileConfiguration.txt')

with open(outfile,'w') as of:
    of.write(TEMPLATE)

    for fname in infiles:
        with open(fname,'r') as f:
            lines = f.readlines()

            for l in lines:
                #print(l.split('\t'))
                if l.split('\t')[0] == 'parameter':
                    if l.split('\t')[1] == 'origin':
                        fields = l.split('\t')
                        x0, y0, t0 = fields[-3:]

			x1 = float(x0) * xmul
			y1 = float(y0) * ymul
			if swapxy:
				x1, y1 = y1, x1
				
            of.write(TROW.format(os.path.basename(fname),str(x1),str(y1)))

with open(outfile,'r') as r:
    T = r.read()
    print(T)

print('TileConfiguration.txt saved to '+outfile+'\n')

from ij import IJ 

if doStitching:
	IJ.run("Grid/Collection stitching", "type=[Positions from file] order=[Defined by TileConfiguration] directory=["+indir+"] layout_file=TileConfiguration.txt fusion_method=[Linear Blending] regression_threshold=0.30 max/avg_displacement_threshold=2.50 absolute_displacement_threshold=3.50 computation_parameters=[Save memory (but be slower)] image_output=[Fuse and display]");

	
