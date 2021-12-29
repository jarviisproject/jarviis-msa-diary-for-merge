from django.db import models
# Create your models here.
from konlpy.tag import Okt
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast
# 맞춤법 검사
from common.models import ValueObject
from hanspell import spell_checker
from writing.models_train import WritingTrain


class Writing:
    def __init__(self, vo):
        self.vo = vo

    def process(self, topic):
        return self.generate_text(topic, 50)

    def load_model(self, model_path):
        return GPT2LMHeadModel.from_pretrained(model_path)

    def load_tokenizer(self, tokenizer_path):
        return PreTrainedTokenizerFast.from_pretrained(tokenizer_path)

    def generate_text(self, sequence, max_length):
        model_path = self.vo.context
        model = self.load_model(model_path)
        tokenizer = self.load_tokenizer(model_path)
        ids = tokenizer.encode(f'{sequence},', return_tensors='pt')
        final_outputs = model.generate(
            ids,
            do_sample=True,
            max_length=max_length,
            pad_token_id=model.config.pad_token_id,
            top_k=5,
            top_p=0.95
        )
        text = tokenizer.decode(final_outputs[0], skip_special_tokens=True)
        # print(f'{"*"*20} 변경 전 {"*"*20}')
        # print(text)
        # print('*'*50)
        result = self.clean_up_text(text)
        # print(f'{"*"*20} 변경 후 {"*"*20}')
        # print(result)
        # print('*'*50)
        return result

    def clean_up_text(self, full_texts):
        okt = Okt()
        split = okt.pos(full_texts)
        # print(okt.pos(full_texts))
        ls = []
        [ls.append(i) for i, word in enumerate(split) if word[1] == 'Punctuation']
        del split[ls[-1]+1:]
        del split[:ls[0]+1]
        result = ''
        for i, word in enumerate(split):
            if word[1] == 'Josa' or word[1] == 'Punctuation':
                result = result + word[0]
            else:
                result = result + ' ' + word[0]
        return spell_checker.check(result).as_dict()['checked']

    def checking_spell(self, text):
        return spell_checker.check(text).as_dict()['checked']
