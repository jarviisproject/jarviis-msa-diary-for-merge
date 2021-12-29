from transformers import TextDataset, DataCollatorForLanguageModeling, GPT2LMHeadModel, Trainer, TrainingArguments, PreTrainedTokenizerFast


class WritingTrain:
    def __init__(self):
        pass

    def process(self):
        train_file_path = 'data/ver3.csv'
        model_name = 'skt/kogpt2-base-v2'
        output_dir = '../machine/ver3'
        overwrite_output_dir = False
        per_device_train_batch_size = 8
        num_train_epochs = 50
        save_steps = 500
        self.train(train_file_path, model_name, output_dir, overwrite_output_dir, per_device_train_batch_size, num_train_epochs, save_steps)

    # 데이터셋 불러오기
    def load_dataset(self, file_path, tokenizer, block_size = 128):
        return TextDataset(
            tokenizer=tokenizer,
            file_path=file_path,
            block_size=block_size
        )

    # mask??
    def load_data_collator(self, tokenizer, mlm=False):
        return DataCollatorForLanguageModeling(
            tokenizer=tokenizer,
            mlm=mlm
        )

    def train(self, train_file_path,
              model_name, output_dir,
              overwrite_output_dir,
              per_device_train_batch_size,
              num_train_epochs, save_steps):
        tokenizer = PreTrainedTokenizerFast.from_pretrained(model_name,
                                                            bos_token='</s>',
                                                            eos_token='</s>',
                                                            unk_token='<unk>',
                                                            pad_token='<pad>',
                                                            mask_token='<mask>')
        train_dataset = self.load_dataset(train_file_path, tokenizer)
        data_collator = self.load_data_collator(tokenizer)

        tokenizer.save_pretrained(output_dir, legacy_format=False)
        model = GPT2LMHeadModel.from_pretrained(model_name)
        model.save_pretrained(output_dir)
        training_args = TrainingArguments(
            output_dir=output_dir,
            overwrite_output_dir=overwrite_output_dir,
            per_device_train_batch_size=per_device_train_batch_size,
            num_train_epochs=num_train_epochs,
            save_steps=save_steps
        )
        trainer = Trainer(model=model,
                          args=training_args,
                          data_collator=data_collator,
                          train_dataset=train_dataset)
        trainer.train()
        trainer.save_model()


if __name__ == '__main__':
    w = WritingTrain()
    w.process()