#!/bin/bash
bert-serving-start -num_worker=1 -model_dir stsb_bert_base_converted/ -ckpt_name 0_BERT.ckpt
