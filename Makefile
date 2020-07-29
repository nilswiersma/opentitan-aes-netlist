.PHONY: all
	all: aes.v

include sv_files.mk

aes.v: $(AES_SOURCES)
	sv2v --verbose -D=VERILATOR -I./lowrisc_dv_verilator_aes_tb_0/src/lowrisc_prim_assert_0.1/rtl/ $^ > $@


