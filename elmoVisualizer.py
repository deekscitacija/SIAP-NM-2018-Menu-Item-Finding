from allennlp.commands.elmo import ElmoEmbedder
from allennlp.modules.elmo import Elmo, batch_to_ids
from allennlp.modules.token_embedders.elmo_token_embedder import ElmoTokenEmbedder

options_file='D:/Faks/SIAP/ELMOFiles/trainPartsAll/trainedModel/options.json'
weight_file='D:/Faks/SIAP/ELMOFiles/trainPartsAll/trainedModel/weights.hdf5'

def calculate_vector():
    sent = ["Pizza", "je", "bila", "odlicna", "."]
    sentences = [sent]
    elmo = Elmo(options_file, weight_file, 1, dropout=0)

    character_ids = batch_to_ids(list(sent))
    embeddings = elmo(character_ids)
    print(embeddings)

if __name__ == "__main__":
    calculate_vector()