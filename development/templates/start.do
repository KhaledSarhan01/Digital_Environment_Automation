vlib work
vlog -f sourcefile.txt -svinputport=relaxed
vsim -voptargs=+acc work.$tb_name
add wave *
run -all
