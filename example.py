from model_correction import GectorCorrector

cg = GectorCorrector('roberta_1_gectorv2.th')
text = {}

text['text'] = """
 Hello, my name is Irina, I am 20 years old. I live in St.P. since my birthday, since 2020. I study at Swae, St. Petersburg University, I don't know. I study at Frontend Developer. I work at the University of St. Petersburg University, I don't know. I have students in my course. I teach Russian language and digital skills for students at 8-11 grade. That's all. Yesterday I have my boyfriend and I have breakfast, I bet, how it will be, have dinner in Guzhuan. And you from some Czech restaurant? Polish? It's Czech national restaurant. Then I go to my university and sit at university for 4 hours. Then I go home. That's all.
"""

text['words'] = [{'text': word, 'transformation': '', 'mistake': '', 'appended': False} for word in text['text'].split()]

cg.predict(text)