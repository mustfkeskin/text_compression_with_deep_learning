# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 20:39:30 2017

@author: Mustafa
"""

# 
# Compression application using adaptive arithmetic coding
# 
# Usage: python adaptive-arithmetic-compress.py InputFile OutputFile
# Then use the corresponding adaptive-arithmetic-decompress.py application to recreate the original input file.
# Note that the application starts with a flat frequency table of 257 symbols (all set to a frequency of 1),
# and updates it after each byte encoded. The corresponding decompressor program also starts with a flat
# frequency table and updates it after each byte decoded. It is by design that the compressor and
# decompressor have synchronized states, so that the data can be decompressed properly.
# 
# Copyright (c) Project Nayuki
# 
# https://www.nayuki.io/page/reference-arithmetic-coding
# https://github.com/nayuki/Reference-arithmetic-coding
# 

import sys
import arithmeticcoding
python3 = sys.version_info.major >= 3


# Command line main application function.
def main():
	inputfile  = "C:\\Users\\Mustafa\\Desktop\\txt\\alice.txt"
	outputfile = "C:\\Users\\Mustafa\\Desktop\\txt\\alice_compress.txt"
	
	# Perform file compression
	with open(inputfile, "rb") as inp:
		bitout = arithmeticcoding.BitOutputStream(open(outputfile, "wb"))
		try:
			compress(inp, bitout)
		finally:
			bitout.close()


def compress(inp, bitout):
	initfreqs = arithmeticcoding.FlatFrequencyTable(257)
	freqs = arithmeticcoding.SimpleFrequencyTable(initfreqs)
	enc = arithmeticcoding.ArithmeticEncoder(bitout)
	while True:
		# Read and encode one byte
		symbol = inp.read(1)
		if len(symbol) == 0:
			break
		symbol = symbol[0] if python3 else ord(symbol)
		enc.write(freqs, symbol)
		freqs.increment(symbol)
	enc.write(freqs, 256)  # EOF
	enc.finish()  # Flush remaining code bits


# Main launcher
if __name__ == "__main__":
	main()
