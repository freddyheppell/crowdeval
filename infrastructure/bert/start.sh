#!/bin/bash
bert-serving-start -num_worker=1 -pooling_layer=-1 -model_dir stsb-bert-base-tf/
