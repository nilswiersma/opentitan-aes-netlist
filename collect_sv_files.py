#!/usr/bin/python3
from pathlib import Path

with open('sv_files.mk', 'w') as outf:
	print('# generated bui build_sv_files.py', file=outf)
	print('AES_SOURCES += prim_clock_gating.sv', file=outf)
	for x in Path('lowrisc_dv_verilator_aes_tb_0/src').glob('**/*.sv'):
		print('AES_SOURCES +=', x, file=outf)
