
vlib work
vlog -f sourcefile.txt -svinputport=relaxed
vsim -voptargs=+acc work.tb_example
do wave.do
run -all
