#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, getopt, os
from producer import produce_pdf, produce_odt, produce_epub

verbose = False

def main(argv):
    input_dir  = ''
    output_dir = ''
    template_dir = None
    
    helpmsg = 'produce_all.py [-v] -i <input_dir> -t <template_dir> -o <output_dir>'
    
    try:
        opts, args = getopt.getopt(argv,"hvi:o:t:",["idir=", "odir=", "tdir=", "verbose"])
    except getopt.GetoptError:
        print helpmsg
        sys.exit(1)
        
    global verbose
        
    for opt, arg in opts:
        if opt == '-h':
            print helpmsg
            sys.exit()
        elif opt in ("-i", "--idir"):
            input_dir = arg
        elif opt in ("-t", "--tdir"):
            template_dir = arg
        elif opt in ("-o", "--odir"):
            output_dir = arg
        elif opt in ("-v", "--verbose"):
            verbose=True            
         
    if input_dir == '' or output_dir == '':
        print helpmsg
        exit(1)

    for book in ("volume-1", "volume-2", "volume-3"):
        full_dir = os.path.sep.join([input_dir, book])
        for root, dirs, files in os.walk(full_dir):
            for f in files:
                if f.endswith(".md"):
                    input_filename = full_dir + os.path.sep + f

                    if not f.startswith("index"):
                        output_filename = output_dir + os.path.sep + book + "-" + f.replace(".md","")
                    else:
                        output_filename = output_dir + os.path.sep + book

                if verbose:
                    print "producing", output_filename, "from", input_filename,
                    sys.stdout.flush()

                
                    
                produce_pdf(output_filename, input_filename,  template_filename = template_dir + os.path.sep + "template.tex" if template_dir else None)
                produce_odt(output_filename, input_filename,  template_filename = template_dir + os.path.sep + "template.odt" if template_dir else None)
                produce_epub(output_filename, input_filename)
                if verbose:
                    print "."
                    
if __name__ == "__main__":
   main(sys.argv[1:])
        
