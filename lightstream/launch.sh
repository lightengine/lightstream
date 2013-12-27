#!/bin/bash
export DISPLAY=:0
git pull private master
python emulator.py
