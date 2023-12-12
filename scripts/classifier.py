from transformers import create_optimizer, DataCollatorWithPadding, TFAutoModelForSequenceClassification

from transformers.keras_callbacks import PushToHubCallback, KerasMetricCallback
from keras.callbacks import TensorBoard

def train_classifier_tf_model(batch_size, num_epochs, dataset, tokenizer, model_checkpoint, n_label, genre_index, compute_metrics, hub_output):
    batches_per_epoch = len(dataset["train"]) // batch_size
    total_train_steps = int(batches_per_epoch * num_epochs)
    optimizer, schedule = create_optimizer(init_lr=2e-5, num_warmup_steps=0, num_train_steps=total_train_steps)
    
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer, return_tensors="tf")

    id2label = {id:genre_index[id] for id in range(n_label)}
    label2id = {genre_index[id]:id for id in range(n_label)}

    model_clf = TFAutoModelForSequenceClassification.from_pretrained(
    model_checkpoint, num_labels=n_label, id2label=id2label, label2id=label2id
    )

    tf_train_set = model_clf.prepare_tf_dataset(
    dataset["train"],
    shuffle=True,
    batch_size=batch_size,
    collate_fn=data_collator,
    )

    tf_validation_set = model_clf.prepare_tf_dataset(
        dataset["test"],
        shuffle=False,
        batch_size=batch_size,
        collate_fn=data_collator,
    )

    model_clf.compile(optimizer=optimizer)

    metric_callback = KerasMetricCallback(metric_fn=compute_metrics, eval_dataset=tf_validation_set)

    push_to_hub_callback = PushToHubCallback(
        output_dir=hub_output,
        tokenizer=tokenizer,
    )

    tensorboard_callback = TensorBoard(log_dir= f"./{hub_output}/logs")

    callbacks = [metric_callback, tensorboard_callback, push_to_hub_callback]

    model_clf.fit(x=tf_train_set, validation_data=tf_validation_set, epochs=3, callbacks=callbacks)