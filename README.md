This repo implements DP-GAN (https://arxiv.org/abs/1802.01345) and SeqGAN for Neural Dialogue generation (https://arxiv.org/abs/1701.06547). Additionally, we propose a new Actor Critic framework for DP-GAN which we call DPAC-GAN. This project is done for the course Information Retrieval 2 as part of the Masters in Artificial Intelligence. 

We based code for the generator on seq2seq models from IBM (https://github.com/IBM/pytorch-seq2seq) and use NLG-Eval from (https://github.com/Maluuba/nlg-eval).


Questions List:

Have been done:
1 load the parameter file. Pretraining the model, then the file would be created.
2 Padding long should be flexible and changable.
3 quliative transprant

Havn't
1 clip the gredient
2 iter problem when utilizing customer dataset(test)
3 contact problem in results quliative

Code structure

How to run the model:
1 train the model from strecth
change the setting of (), change the document file, change the setting of parameter, true both. then pretrain generator, pre-trained discriminator, then adversial training.
Python main.py

2 qulia

3 data set replace

4 SeqGAN and DPGAN
