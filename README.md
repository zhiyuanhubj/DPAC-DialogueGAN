This repo implements DP-GAN (https://arxiv.org/abs/1802.01345) and SeqGAN for Neural Dialogue generation (https://arxiv.org/abs/1701.06547). Additionally, we propose a new Actor Critic framework for DP-GAN which we call DPAC-GAN. This project is done for the course Information Retrieval 2 as part of the Masters in Artificial Intelligence. 

We based code for the generator on seq2seq models from IBM (https://github.com/IBM/pytorch-seq2seq) and use NLG-Eval from (https://github.com/Maluuba/nlg-eval).


## Questions List:

## Have been done:
- load the parameter file. Pretraining the model, then the file would be created.

- Padding long should be flexible and changable.

- quliative transprant

-- definition of 'GEN_MLE_LR'

## Havn't
- clip the gredient
- iter problem when utilizing customer dataset(test)
- contact problem in results quliative

## Code structure

- generator structure

initial generator(generator.py-->Seq2Seq/Seq2Seq.py--> EncoderRNN and DecoderRNN)

- pretrain the generator

- intial discriminator

- pretrain discriminator

- adversial training

4 SeqGAN and DPGAN


## Get Start

### Requirements

### Train and evaluate

```bash
python main.py
```
change the setting of (), change the document file, change the setting of parameter, true both. then pretrain generator, pre-trained discriminator, then adversial training.

data set replace

### Test
```bash
python qualitive_analysis.py
```
