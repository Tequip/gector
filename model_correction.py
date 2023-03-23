import re
import spacy

from gector.gec_model import GecBERTModel
from pyinflect import getAllInflections, getInflection

class GectorCorrector:

    def __init__(self, weight_path):
          
        self.model = GecBERTModel(vocab_path='data/output_vocabulary',
                                model_paths=[weight_path],
                                max_len=100, min_len=3,
                                iterations=10   ,
                                min_error_probability=0,
                                lowercase_tokens=0,
                                model_name='roberta',
                                special_tokens_fix=1,
                                log=False,
                                confidence=0,
                                del_confidence=0,
                                is_ensemble=0,
                                weigths=None)
        
        self.nlp = spacy.load('en_core_web_sm')

    def _calculate_deleted_appended_words(self, text, index):
        deleted, appended, curr_index = 0, 0, 0
        for i, word in enumerate(text['words']):
            if curr_index == index:
                break
#             if 'appended' in word.keys() and word['appended'] == True:
#                 appended += 1
#                 continue
            if 'transform_into' in word.keys() and word['transform_into'] == '__delete':
                deleted += 1
                continue
                
            curr_index += 1
            
        return appended, deleted
            
        
    def predict(self, text):
        preds, _, edits = self.model.handle_batch([re.sub('[0-9]', '', text['text']).split()])

        text['corrected_text'] = preds[0]

        deleted_items = 0
        appended_items = 0

        # save transformation to words 
        for edit in edits:
            try:
                try:
                    edit[0] = (edit[0][0] + sum(self._calculate_deleted_appended_words(text, edit[0][0])),
                                edit[0][1] + sum(self._calculate_deleted_appended_words(text, edit[0][1])), edit[0][2])
                    print(edit, 'CONTEXT ', text['words'][edit[0][0]]['text'], text['words'][edit[0][1]]['text'])
                    
                    if 'append' in edit[1].lower():
                        if edit[0][2] in [',', '.']:
                            text['words'].insert(edit[0][0], {'text': edit[0][2], 'transform_into': '', 'mistake': None, 'appended': False, 'append_index': None})
                        else:
                            text['words'][edit[0][0] - 1]['transform_into'] = '__append'
                            text['words'][edit[0][0] - 1]['append_index'] = edit[0][0]
                            text['words'].insert(edit[0][0], {'text': edit[0][2], 'transform_into': None, 'mistake': None, 'appended': True, 'append_index': None})

                        # appended_items += 1
                    elif 'replace' in edit[1].lower():
                        if text['words'][edit[0][0]]['text'].lower() == edit[2].lower():
                            text['words'][edit[0][0]]['transform_into'] = edit[0][2]
                        elif text['words'][edit[0][1]]['text'].lower() == edit[2].lower():
                            text['words'][edit[0][1]]['transform_into'] = edit[0][2]
                        elif text['words'][edit[0][0]]['transform_into'].lower() == edit[2].lower():
                            text['words'][edit[0][0]]['transform_into'] = edit[0][2]
                        elif text['words'][edit[0][1]]['transform_into'].lower() == edit[2].lower():
                            text['words'][edit[0][1]]['transform_into'] = edit[0][2]
                    elif 'merge_space' in edit[1].lower():
                        text['words'][edit[0][1] - 1]['transform_into'] = text['words'][edit[0][1] - 1]['text'] + \
                                 text['words'][edit[0][1]]['text']
                        
                        text['words'][edit[0][1]]['transform_into'] = '__delete'
                        deleted_items += 1

                    elif 'transform' in edit[1].lower():

                        doc = self.nlp(u"{}".format(edit[2]))

                        base_word = doc[0].lemma_

                        if 'vbd' in edit[1].split('_')[-1].lower():
                            change_word = getAllInflections(base_word)['VBD'][0]
                        elif 'vbn' in edit[1].split('_')[-1].lower():
                            change_word = getAllInflections(base_word)['VBN'][0]
                        elif 'vbz' in edit[1].split('_')[-1].lower():
                            change_word = getAllInflections(base_word)['VBZ'][0]
                        elif 'vbg' in edit[1].split('_')[-1].lower():
                            change_word = getAllInflections(base_word)['VBG'][0]
                        elif 'vb' in edit[1].split('_')[-1].lower():
                            change_word = getAllInflections(base_word)['VB'][0]
                        elif 'agreement_plural' in edit[1].lower():
                            inflections = getAllInflections(base_word)
                            if edit[2] == inflections['NN'][0]:
                                change_word = inflections['NNS'][0]
                            else:
                                change_word = inflections['NN'][0]
                        else:
                            change_word = edit[2]

                        # print(change_word)

                        if text['words'][edit[0][0]]['text'].lower() == edit[2].lower():
                            text['words'][edit[0][0]]['transform_into'] = change_word
                        elif text['words'][edit[0][1]]['text'].lower() == edit[2].lower():
                            text['words'][edit[0][1]]['transform_into'] = change_word
                        elif text['words'][edit[0][0]]['transform_into'].lower() == edit[2].lower():
                            text['words'][edit[0][0]]['transform_into'] = change_word
                        elif text['words'][edit[0][1]]['transform_into'].lower() == edit[2].lower():
                            text['words'][edit[0][1]]['transform_into'] = change_word

                    elif 'delete' in edit[1].lower():
                        text['words'][edit[0][0]]['transform_into'] = '__delete'
                        deleted_items += 1
                    else:
                        print(edit)
                except Exception as e:
                    print('EXCEPTION', str(e))
                    print('EXCEPTION ON', edit, 'CONTEXT ', text['words'][edit[0][0]]['text'], text['words'][edit[0][1]]['text'])
                    continue
            except:
                continue

        return text