#!/usr/bin/env python
# -*- coding: utf-8 -*-

import warnings

warnings.filterwarnings('ignore')

__tool_name__='STREAM'
print('''
   _____ _______ _____  ______          __  __ 
  / ____|__   __|  __ \|  ____|   /\   |  \/  |
 | (___    | |  | |__) | |__     /  \  | \  / |
  \___ \   | |  |  _  /|  __|   / /\ \ | |\/| |
  ____) |  | |  | | \ \| |____ / ____ \| |  | |
 |_____/   |_|  |_|  \_\______/_/    \_\_|  |_|
... detect marker and transition genes                                            
''',flush=True)

import stream as st
import argparse
import multiprocessing
import os
from slugify import slugify
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import sys

mpl.use('Agg')
mpl.rc('pdf', fonttype=42)

os.environ['KMP_DUPLICATE_LIB_OK']='True'


print('- STREAM Single-cell Trajectory Reconstruction And Mapping -',flush=True)
print('Version %s\n' % st.__version__,flush=True)
    

def main():
    sns.set_style('white')
    sns.set_context('poster')
    parser = argparse.ArgumentParser(description='%s Parameters' % __tool_name__ ,formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--data-file", dest="input_filename",default = None, help="input file name, pkl format from Stream preprocessing module", metavar="FILE")
    parser.add_argument("-of","--of",dest="output_filename_prefix", default="StreamiFSOutput",  help="output file name prefix")
    parser.add_argument("-fig_width",dest="fig_width", type=int, default=8, help="")
    parser.add_argument("-fig_height",dest="fig_height", type=int, default=8, help="")
    parser.add_argument("-fig_legend_ncol",dest="fig_legend_ncol", type=int, default=None, help="")
    parser.add_argument("-percentile_expr",dest="percentile_expr", type=int, default=95, help="")
    parser.add_argument("-flag_use_precomputed",dest="flag_use_precomputed", action="store_true", help="")
    parser.add_argument("-root",dest="root", default=None, help="")
    parser.add_argument("-preference",dest="preference", default=None, help="")
    parser.add_argument("-cutoff_spearman",dest="cutoff_spearman", type=float, default=0.4, help="")
    parser.add_argument("-cutoff_logfc",dest="cutoff_logfc", type=float, default=0.25, help="")
    parser.add_argument("-num_genes",dest="num_genes", type=int, default=15, help="")

    args = parser.parse_args()
    
    workdir = "./"

    adata = st.read(file_name=args.input_filename, file_format='pkl', experiment='rna-seq', workdir=workdir)
    preference = args.preference.split(',')
    st.detect_transistion_genes(adata,cutoff_spearman=args.cutoff_spearman,cutoff_logfc=args.cutoff_logfc,percentile_expr=args.percentile_expr,n_jobs=8,
                            use_precomputed=args.flag_use_precomputed, root=args.root,preference=preference)
    st.plot_transition_genes(adata,num_genes=args.num_genes,save_fig=True,fig_path="./",fig_size=(args.fig_width, args.fig_height))
   


 
    st.write(adata,file_name=(args.output_filename_prefix + '_stream_result.pkl'),file_path='./',file_format='pkl') 

    print('Finished computation.')

if __name__ == "__main__":
    main()
