#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import subprocess
import sys, getopt

verbose = False

def clean_metadata(output_filename):
    if verbose:
        print "mat", output_filename
    subprocess.check_output(["mat", output_filename])

def pandoc(output_filename, input_filename, pandoc_args=None):
    """
    needs xelatex
    """
    if not isinstance(input_filename, str):
        input_filename = " ".join(input_filename)

    if pandoc_args is None:
        pandoc_args = []
    pandoc_args = " ".join(pandoc_args)
    cmd = "pandoc {pandoc_args} {input_filename} -o {output_filename}".format(pandoc_args=pandoc_args,
                                                                              input_filename=input_filename,
                                                                              output_filename=output_filename)
    if verbose:
        print cmd
    subprocess.check_output(cmd, shell=True)

def fix_filename(filename, ending):
    if not filename.endswith("." + ending):
        return filename + "." + ending
    else:
        return filename
    
    
def produce_epub(output_filename, input_filename, template_filename=None):
    if template_filename:
        raise NotImplementedError

    output_filename = fix_filename(output_filename, "epub")
    
    pandoc_args = ["-S"]

    pandoc(output_filename, input_filename, pandoc_args)

    
def produce_odt(output_filename, input_filename, template_filename=None):
    output_filename = fix_filename(output_filename, "odt")
    
    pandoc_args = ["-S",]

    if template_filename:
        pandoc_args.append("--reference-odt=%s"%template_filename)
        
    pandoc(output_filename, input_filename, pandoc_args)
    
def produce_pdf(output_filename, input_filename, template_filename=None):
    output_filename = fix_filename(output_filename, "pdf")

    pandoc_args = ["-S",
                   "--latex-engine=xelatex",
                   "-V geometry:a4paper",
                   "-V geometry:margin=1in",
                   "-V mainfont=Georgia"]

    if template_filename:
        pandoc_args.append("--template %s"%template_filename)
    
    pandoc(output_filename, input_filename, pandoc_args)
    #clean_metadata(output_filename)

def main(argv):
    input_filename  = ''
    output_filename = ''
    template_filename = None

    helpmsg = 'producer.py [-v] -i <input_filename> -t <template_filename> -o <output_filename>'
    
    try:
        opts, args = getopt.getopt(argv,"hvi:o:t:",["ifile=","ofile=", "tfile=", "verbose"])
    except getopt.GetoptError:
        print helpmsg
        sys.exit(1)
        
    global verbose
        
    for opt, arg in opts:
        if opt == '-h':
            print helpmsg
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_filename = arg
        elif opt in ("-o", "--ofile"):
            output_filename = arg
        elif opt in ("-t", "--tfile"):
            template_filename = arg
        elif opt in ("-v", "--verbose"):
            verbose=True            
         
    if input_filename == '' or output_filename == '':
        print helpmsg
        exit(1)
        
    if output_filename.endswith(".odt"):
        produce_odt(output_filename, input_filename, template_filename)
    elif output_filename.endswith(".pdf"):
        produce_pdf(output_filename, input_filename, template_filename)
    elif output_filename.endswith(".epub"):
        produce_epub(output_filename, input_filename, template_filename)
    else:
        raise NotImplementedError("output file type for file %s not understood"%output_filename)
    
if __name__ == "__main__":
   main(sys.argv[1:])

