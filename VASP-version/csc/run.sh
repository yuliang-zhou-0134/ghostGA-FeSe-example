#/usr/bin/bash
nohup mpirun --bind-to numa -np 4 python3 -u main.py grisb_config.toml &
