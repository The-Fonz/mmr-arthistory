#
# Calculates feature vector for all paintings, stores it in extracted.json
#

import cv2
from features import color
from utils import get_tree, save_tree
import os
import time
c = time.clock

from features import EHD, GF, GLCM

save_every_n = 100

if __name__ == '__main__':
    t = get_tree()

    for i, painting in enumerate(t):
        painting['features'] = {}
        fn = painting['afbeelding']

        # Always run from repo root dir
        path = os.path.abspath(os.path.join('.', 'data', *fn.split('/')))
        print("\nGetting painting {}".format(path))
        cvim = cv2.imread(path)

        cfe = color.ColorFeatureExtracter(cvim)


        t1 = c()
        colorfeats = cfe.ComputeFeatures()
        t2 = c()
        print("Extracting color features took {:.6f}s".format(t2-t1))

        t1 = c()
        ehdfeat = EHD.EHDFeatures(cvim)
        t2 = c()
        gfeat = GF.GaborFeatures().feats_gabor(cvim)
        t3 = c()
        glcmfeat = GLCM.GLCMFeatures(cvim)
        t4 = c()

        print("Extracting texture features took {:.6f}s for EHD,\
 {:.6f}s for GF, {:.6f}s for GLCM".format(t2-t1, t3-t2, t4-t3))

        # Add feature vect
        painting['features'] = {
            'RgbHist': colorfeats['RgbHist'],
            'ColorBitmap': colorfeats['ColorBitmap'],
            'EHD': ehdfeat,
            'GLCM': glcmfeat,
        }

        if not i % save_every_n:
            # Save tree with feature vects
            t1 = c()
            save_tree(t)
            t2 = c()
            print("\n\nSAVED TREE in {:.6f}s, doing this every {} paintings"
            .format(t2-t1, save_every_n))
