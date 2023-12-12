from datasets import Dataset

def tokenize_dataset_from_pandas(df, tokenizer_func, RANDOM_STATE = 0):
    raw_datasets = Dataset.from_pandas(df, preserve_index=True).train_test_split(seed=RANDOM_STATE)
    tokenized_dataset = raw_datasets.map(tokenizer_func, batched=True, remove_columns=['__index_level_0__'])
    return tokenized_dataset