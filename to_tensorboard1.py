import tensorflow as tf


import numpy as np
import os
# https://gist.github.com/nlothian/0cd4540389f7091717ece6f4b89b6604

meta_file = "f_metadata.tsv"
vec_file = "f_vectors.tsv"
output_path = "./tensorboard/projections"

# read embedding file into list and get the size
with open('./GloVe-1.2/female/vectors.txt', 'r') as embedding_file:
    embedding_content = embedding_file.readlines()
    embedding_content = [x.strip() for x in embedding_content] 
    #print(embedding_content[1].split())

    num_lines = len(embedding_content)  - 1 # skip the header
    num_dims = len(embedding_content[1].split()) - 1 # -1 because of the label column
    print("Detected dimensions:", num_lines, " X ", num_dims)

    placeholder = np.zeros((num_lines, num_dims))

    print(placeholder.shape)


    z = 0
    with open(os.path.join(output_path, meta_file), 'w') as file_metadata:
        out_v = open(os.path.join(output_path, vec_file), 'w')

        i = 0
        for line in embedding_content [1:]:  # skip the header line
            values = line.split()
            raw_label = values[0]
            #print(label)
            col = 0
            vec = values[1:]
            out_v.write('\t'.join([str(x) for x in vec])+'\n')
            for val in values[1:]: # skip the label
                placeholder[i][col] = val
                z = i + col
                col = col + 1
            i = i + 1

            if raw_label == '':
                file_metadata.write("<Empty Line>\n")
            else:
                label = raw_label
                file_metadata.write(label + "\n")

        print("z = ", z)

meta_file = "m_metadata.tsv"
vec_file = "m_vectors.tsv"


# read embedding file into list and get the size
with open('./GloVe-1.2/male/vectors.txt', 'r') as embedding_file:
    embedding_content = embedding_file.readlines()
    embedding_content = [x.strip() for x in embedding_content] 
    #print(embedding_content[1].split())

    num_lines = len(embedding_content)  - 1 # skip the header
    num_dims = len(embedding_content[1].split()) - 1 # -1 because of the label column
    print("Detected dimensions:", num_lines, " X ", num_dims)

    placeholder = np.zeros((num_lines, num_dims))

    print(placeholder.shape)


    z = 0
    with open(os.path.join(output_path, meta_file), 'w') as file_metadata:
        out_v = open(os.path.join(output_path, vec_file), 'w')

        i = 0
        for line in embedding_content [1:]:  # skip the header line
            values = line.split()
            raw_label = values[0]
            #print(label)
            col = 0
            vec = values[1:]
            out_v.write('\t'.join([str(x) for x in vec])+'\n')
            for val in values[1:]: # skip the label
                placeholder[i][col] = val
                z = i + col
                col = col + 1
            i = i + 1

            if raw_label == '':
                file_metadata.write("<Empty Line>\n")
            else:
                label = raw_label
                file_metadata.write(label + "\n")

        print("z = ", z)