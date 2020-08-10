tools used:

- sv2v
- yosys
- verilator

To also pull in opentitan, be sure to use `git clone --recursive ...`

# AES testbench

Build
```
cd submodules/opentitan
fusesoc --cores-root=. run --setup --build lowrisc:dv_verilator:aes_tb
```

Run once with default key and input, no traces
```
./build/lowrisc_dv_verilator_aes_tb_0/default-verilator/Vaes_tb
```

Run with key DEADBEEFCAFEBABEC001DAADB01AD01A and input 000102030405060708090A0B0C0D0E0F, collect trace
```
./build/lowrisc_dv_verilator_aes_tb_0/default-verilator/Vaes_tb -kDEADBEEFCAFEBABEC001DAADB01AD01A -i000102030405060708090A0B0C0D0E0F -t
```

Run multiple times with random key and input (requires requires [cryptography package](https://pypi.org/project/cryptography/))

```
python3 hw/ip/aes/pre_dv/aes_tb/python/aes_tb.py
```

# Run through sv2v

Make a copy of the relevant files
```
cd ../..
cp -rv submodules/opentitan/build/lowrisc_dv_verilator_aes_tb_0 ./
python3 collect_sv_files.py
```

Run it through sv2v
```
make aes.v
```

Run through verilator and build simulation
```
cd lowrisc_dv_verilator_aes_tb_0/default-verilator

verilator ../../aes.v --Mdir . --cc +incdir+../src/lowrisc_dv_verilator_simutil_verilator_0/cpp -CFLAGS -I../src/lowrisc_dv_verilator_simutil_verilator_0/cpp +incdir+../src/lowrisc_prim_assert_0.1/rtl -CFLAGS -I../src/lowrisc_prim_assert_0.1/rtl ../src/lowrisc_lint_comportable_0.1/tools/verilator/comportable.vlt ../src/lowrisc_lint_common_0.1/tools/verilator/common.vlt ../src/lowrisc_prim_generic_clock_mux2_0/lint/prim_generic_clock_mux2.vlt ../src/lowrisc_prim_generic_pad_wrapper_0/lint/prim_generic_pad_wrapper.vlt ../src/lowrisc_prim_xilinx_clock_mux2_0/lint/prim_xilinx_clock_mux2.vlt ../src/lowrisc_prim_xilinx_pad_wrapper_0/lint/prim_xilinx_pad_wrapper.vlt ../src/lowrisc_prim_all_0.1/lint/prim.vlt ../src/lowrisc_tlul_common_0.1/lint/tlul_common.vlt ../src/lowrisc_tlul_adapter_reg_0.1/lint/tlul_adapter_reg.vlt ../src/lowrisc_tlul_adapter_sram_0.1/lint/tlul_adapter_sram.vlt ../src/lowrisc_tlul_socket_1n_0.1/lint/tlul_socket_1n.vlt ../src/lowrisc_tlul_socket_m1_0.1/lint/tlul_socket_m1.vlt ../src/lowrisc_tlul_sram2tlul_0.1/lint/tlul_sram2tlul.vlt ../src/lowrisc_ip_aes_0.6/lint/aes.vlt --top-module aes_tb --exe ../src/lowrisc_dv_verilator_simutil_verilator_0/cpp/verilator_sim_ctrl.cc ../src/lowrisc_dv_verilator_simutil_verilator_0/cpp/verilated_toplevel.cc ../src/lowrisc_dv_verilator_aes_tb_0/cpp/aes_tb.cc  --trace-fst --trace-structs --trace-params --trace-max-array 1024 -CFLAGS "-std=c++11 -Wall -DVM_TRACE_FMT_FST -DTOPLEVEL_NAME=aes_tb -g -O0" -LDFLAGS "-pthread -lutil -lelf" -Wall -Wno-fatal

make -f Vaes_tb.mk
```

Run once with default key and input
```
./Vaes_tb
```

# Run through yosys

```
cd ../..
yosys
read_verilog aes.v
```

Will produce an error: `aes.v:XXXX: ERROR: Condition for generate if is not constant`. `LfsrType` is defined as `"GAL_XOR"`, so simply comment out the other if branch.

```
yosys
read_verilog aes.v
synth -top aes_tb
dfflibmap -liberty cmos_cells.lib
abc -liberty cmos_cells.lib
clean
write_verilog aes_synth.v
<Ctrl-D>
```

To run through verilator
```
cd lowrisc_dv_verilator_aes_tb_0/default-verilator

verilator ../../aes_synth.v ../../cmos_cells.v --Mdir . --cc +incdir+../src/lowrisc_dv_verilator_simutil_verilator_0/cpp -CFLAGS -I../src/lowrisc_dv_verilator_simutil_verilator_0/cpp +incdir+../src/lowrisc_prim_assert_0.1/rtl -CFLAGS -I../src/lowrisc_prim_assert_0.1/rtl ../src/lowrisc_lint_comportable_0.1/tools/verilator/comportable.vlt ../src/lowrisc_lint_common_0.1/tools/verilator/common.vlt ../src/lowrisc_prim_generic_clock_mux2_0/lint/prim_generic_clock_mux2.vlt ../src/lowrisc_prim_generic_pad_wrapper_0/lint/prim_generic_pad_wrapper.vlt ../src/lowrisc_prim_xilinx_clock_mux2_0/lint/prim_xilinx_clock_mux2.vlt ../src/lowrisc_prim_xilinx_pad_wrapper_0/lint/prim_xilinx_pad_wrapper.vlt ../src/lowrisc_prim_all_0.1/lint/prim.vlt ../src/lowrisc_tlul_common_0.1/lint/tlul_common.vlt ../src/lowrisc_tlul_adapter_reg_0.1/lint/tlul_adapter_reg.vlt ../src/lowrisc_tlul_adapter_sram_0.1/lint/tlul_adapter_sram.vlt ../src/lowrisc_tlul_socket_1n_0.1/lint/tlul_socket_1n.vlt ../src/lowrisc_tlul_socket_m1_0.1/lint/tlul_socket_m1.vlt ../src/lowrisc_tlul_sram2tlul_0.1/lint/tlul_sram2tlul.vlt ../src/lowrisc_ip_aes_0.6/lint/aes.vlt --top-module aes_tb --exe ../src/lowrisc_dv_verilator_simutil_verilator_0/cpp/verilator_sim_ctrl.cc ../src/lowrisc_dv_verilator_simutil_verilator_0/cpp/verilated_toplevel.cc ../src/lowrisc_dv_verilator_aes_tb_0/cpp/aes_tb.cc  --trace-fst --trace-structs --trace-params --trace-max-array 1024 -CFLAGS "-std=c++11 -Wall -DVM_TRACE_FMT_FST -DTOPLEVEL_NAME=aes_tb -g -O0" -LDFLAGS "-pthread -lutil -lelf" -Wall -Wno-fatal

make -f Vaes_tb.mk

./Vaes_tb
```

# Flatten

```
yosys
read_verilog aes.v
synth -top aes_tb
flatten
dfflibmap -liberty cmos_cells.lib
abc -liberty cmos_cells.lib
clean
write_verilog aes_synth_flat.v
<Ctrl-D>
``` 

```
cd lowrisc_dv_verilator_aes_tb_0/default-verilator

verilator ../../aes_synth_flat.v ../../cmos_cells.v --Mdir . --cc +incdir+../src/lowrisc_dv_verilator_simutil_verilator_0/cpp -CFLAGS -I../src/lowrisc_dv_verilator_simutil_verilator_0/cpp +incdir+../src/lowrisc_prim_assert_0.1/rtl -CFLAGS -I../src/lowrisc_prim_assert_0.1/rtl ../src/lowrisc_lint_comportable_0.1/tools/verilator/comportable.vlt ../src/lowrisc_lint_common_0.1/tools/verilator/common.vlt ../src/lowrisc_prim_generic_clock_mux2_0/lint/prim_generic_clock_mux2.vlt ../src/lowrisc_prim_generic_pad_wrapper_0/lint/prim_generic_pad_wrapper.vlt ../src/lowrisc_prim_xilinx_clock_mux2_0/lint/prim_xilinx_clock_mux2.vlt ../src/lowrisc_prim_xilinx_pad_wrapper_0/lint/prim_xilinx_pad_wrapper.vlt ../src/lowrisc_prim_all_0.1/lint/prim.vlt ../src/lowrisc_tlul_common_0.1/lint/tlul_common.vlt ../src/lowrisc_tlul_adapter_reg_0.1/lint/tlul_adapter_reg.vlt ../src/lowrisc_tlul_adapter_sram_0.1/lint/tlul_adapter_sram.vlt ../src/lowrisc_tlul_socket_1n_0.1/lint/tlul_socket_1n.vlt ../src/lowrisc_tlul_socket_m1_0.1/lint/tlul_socket_m1.vlt ../src/lowrisc_tlul_sram2tlul_0.1/lint/tlul_sram2tlul.vlt ../src/lowrisc_ip_aes_0.6/lint/aes.vlt --top-module aes_tb --exe ../src/lowrisc_dv_verilator_simutil_verilator_0/cpp/verilator_sim_ctrl.cc ../src/lowrisc_dv_verilator_simutil_verilator_0/cpp/verilated_toplevel.cc ../src/lowrisc_dv_verilator_aes_tb_0/cpp/aes_tb.cc  --trace-fst --trace-structs --trace-params --trace-max-array 1024 -CFLAGS "-std=c++11 -Wall -DVM_TRACE_FMT_FST -DTOPLEVEL_NAME=aes_tb -g -O0" -LDFLAGS "-pthread -lutil -lelf" -Wall -Wno-fatal

make -f Vaes_tb.mk

./Vaes_tb
```








cmos_cells files from https://raw.githubusercontent.com/YosysHQ/yosys/master/examples/cmos/
