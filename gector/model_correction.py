import os
from gector.gec_model import GecBERTModel
from pyinflect import getAllInflections, getInflection

class GectorCorrector:

    def __init__(self, weight_path):
          
        self.model = GecBERTModel(vocab_path=os.path.join(os.path.dirname(__file__), 'data', 'output_vocabulary'),
                                  model_paths=[weight_path],
                                  max_len=100, min_len=3,
                                  iterations=10,
                                  min_error_probability=0,
                                  lowercase_tokens=0,
                                  model_name='roberta',
                                  special_tokens_fix=1,
                                  log=False,
                                  confidence=0,
                                  del_confidence=0,
                                  is_ensemble=0,
                                  weigths=None)


    def predict(self, text):
        preds, _, edits = self.model.handle_batch([text['text'].split()])

        text['corrected_text'] = preds[0]

        # save transformation to words 
        for edit in edits:
            if 'append' in edit[1].lower():
                text['words'].insert(edit[0][0], {'text': edit[0][2], 'transformation': '', 'mistake': '', 'appended': True, 'append_index': None})
                text['words'][edit[0][0] - 1]['transformation'] = '__append'
                text['words'][edit[0][0] - 1]['append_index'] = edit[0][0]
            if 'replace' in edit[1].lower():
                if text['words'][edit[0][0]]['text'].lower() == edit[2].lower():
                    text['words'][edit[0][0]]['transformation'] = edit[0][2]
                if text['words'][edit[0][1]]['text'].lower() == edit[2].lower():
                    text['words'][edit[0][1]]['transformation'] = edit[0][2]
                if text['words'][edit[0][0]]['transformation'].lower() == edit[2].lower():
                    text['words'][edit[0][0]]['transformation'] = edit[0][2]
                if text['words'][edit[0][1]]['transformation'].lower() == edit[2].lower():
                    text['words'][edit[0][1]]['transformation'] = edit[0][2]
            if  'transform' in edit[1].lower():
                if 'vbd' in edit[1].lower():
                    change_word = getAllInflections(edit[2])['VBD'][0]
                elif 'vbn' in edit[1].lower():
                    change_word = getAllInflections(edit[2])['VBN'][0]
                else:
                    change_word = edit[2]

                print(edit[1].lower())

                if text['words'][edit[0][0]]['text'].lower() == edit[2].lower():
                    text['words'][edit[0][0]]['transformation'] = change_word
                if text['words'][edit[0][1]]['text'].lower() == edit[2].lower():
                    text['words'][edit[0][1]]['transformation'] = change_word
                if text['words'][edit[0][0]]['transformation'].lower() == edit[2].lower():
                    text['words'][edit[0][0]]['transformation'] = change_word
                if text['words'][edit[0][1]]['transformation'].lower() == edit[2].lower():
                    text['words'][edit[0][1]]['transformation'] = change_word

        return text