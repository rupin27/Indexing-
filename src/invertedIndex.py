import json, os, sys, re, time
from collections import OrderedDict

class Inverted():
    def __init__(self, file):
        self.start_time = time.time()
        self.fileName = file
        self.tokens = []
        self.dict = {}
        self.sId_cnt = {}
        self.sId_loc = {}
        self.query_dict = {}


    def getInput(self):
        json_file = open(os.path.join(sys.path[0], self.fileName), 'r')
        self.dict = json.load(json_file)
        self.dict = self.dict['corpus']
        #self.dict = json.dumps(self.dict)
        json_file.close()

    #Makes a dictionary with format {word: [[playId, sceneId, sceneNum, count], ....]}
    def terms_Loc_Count(self):
        for items in self.dict:
            text = items['text']
            self.tokens.extend(text.split(' '))
        self.tokens = list(set(self.tokens))
        self.tokens.remove('')
        for word in self.tokens:
            self.sId_cnt[word] = []
            for items in self.dict:
                if word in items['text']:
                    if word not in self.sId_cnt:
                        self.sId_cnt[word].append([items['playId'], items['sceneId'], items['sceneNum'], items['text'].count(word)])
                    else:
                        if items['sceneId'] not in self.sId_cnt[word]:
                            self.sId_cnt[word].append([items['playId'], items['sceneId'], items['sceneNum'], items['text'].count(word)])

    #Makes a dictionary with format {word: [[playId, sceneId, sceneNum, location], ....]}
    def terms_Loc_Pos(self):
        for items in self.dict:
            text = items['text']
            self.tokens = text.split(' ')
            self.tokens.remove('')
            for loc, word in enumerate(self.tokens):
                if word not in self.sId_loc:
                    self.sId_loc[word] = []
                    self.sId_loc[word].append([items['playId'], items['sceneId'], items['sceneNum'], loc])
                else:
                    self.sId_loc[word].append([items['playId'], items['sceneId'], items['sceneNum'], loc])

    def prcs_query(self):
        #result_dict['type'] = scene(s) or play(s)
        #           ['words'] = ['word1', 'word2']
        #           ['comp']  = ['word3]

        input_file = open(os.path.join(sys.path[0], 'input.txt'), 'r')
        str = input_file.readline()
        list = str.split(' ')
        l = ['words', 'word', 'names', 'name']
        l2 = ['is', 'are']
        unwanted = ['', 'or']
        result_dict = {}
        if 'frequently' in list:
            result1 = re.search('Find (.*) where',str)
            result2 = re.search('words (.*) are', str)
            result3 = re.search('frequently than (.*)', str)
            outputType = result1.group(1).replace('the ', '')
            words1 = result2.group(1).split(' ')
            for elem in words1:
                if elem in unwanted:
                    words1.remove(elem)
            words2 = result3.group(1).split(' ')
            words2 = words2[-1:]
            for elem in words2:
                word3 = elem.replace('.', '')
            result_dict['type'] = outputType 
            result_dict['words'] = words1
            result_dict['comp'] = word3

        if 'mentioned.' in list:
            result1 = re.search('Find (.*) where ',str) 
            outputType = result1.group(1).replace('the ', '')
            word = 'where'
            for elem in l:
                if elem in list:
                    word = elem
            for elem in l2:
                if elem in list:
                    word2 = elem
            result2 = re.search(word + '(.*)' + word2, str)
            words1 = result2.group(1).split(' ')
            words2 = ''
            for elem in words1:
                if '\"' in elem:
                    words2 = "combined"
            words1 = [word.replace(",", "") for word in words1]
            words1 = [word.replace("\"", "") for word in words1]
            for elem in words1:
                if elem in unwanted:
                    words1.remove(elem)
            result_dict['type'] = outputType 
            result_dict['words'] = words1
            if words2 != '':
                result_dict['comp'] = words2

        self.query_dict = result_dict

    def checkIfCons(self, n, l, list_word_loc, word_set): 
        # l: [('play/scene', [1, 2, 3, 4])
        # list_word_loc: ['play/scene', location, 'word']
        li_st = []
        boolVal = False
        for elem in l:
            for elem in l[1]:
                i = 1
                while(i != n):
                    if elem + i in l[1]:
                        i+= 1
                    else:
                        break
                if (i == n):
                    boolVal = True
                    for x in range(n):
                        li_st.append((l[0], elem + x ))
                    break
        set_wrds = {}
        if (li_st != []):
            for elem1 in li_st:
                for elem2 in list_word_loc:
                    if (elem1[0] == elem2[0]) and (elem1[1] == elem2[1]):
                        set_wrds[elem2[2]] = elem1[1]
            low = 100000
            new_set_wrds = {}
            for k, v in set_wrds.items():
                if (v < low):
                    low = v
            for k, v in set_wrds.items():
                new_set_wrds[k] = v - low
            if new_set_wrds != word_set:
                boolVal = False
        return boolVal
    

    def term_based_queries(self):
        terms0 = open(os.path.join(sys.path[0].replace('/src', ''), 'terms0.txt'), 'w')   
        if (len(self.query_dict) == 3):
            result = []
            if self.query_dict['comp'] == 'combined':
                init_list = []
                word_set = {}
                for i in range(len(self.query_dict['words'])):
                    word_set[self.query_dict['words'][i]] = i

                for elem in self.query_dict['words']:
                    if self.sId_loc.has_key(elem):
                        wrd = self.sId_loc[elem]
                        for item in wrd:
                            if self.query_dict['type'] == 'scene(s)':
                                init_list.append([item[1], item[3], elem])
                            else:
                                init_list.append([item[0], item[3], elem])

                d = OrderedDict()
                for elem in init_list:
                    d.setdefault(elem[0], []).append(elem[1])
                loc_list = list(d.items())
                for elem in loc_list: 
                    if self.checkIfCons(len(self.query_dict['words']), elem, init_list, word_set) == True:
                        result.append(str(elem[0]))
                result = list(set(result))
                result.sort()
                for items in result:
                    terms0.write(str(items) + '\n')

            else:   
                cmp = self.query_dict['comp']
                for elem in self.query_dict['words']:
                    wrd = self.sId_cnt[elem]
                    if self.sId_cnt[cmp]:
                        cmp_wrd = self.sId_cnt[cmp]
                    for item1 in wrd:
                        for item2 in cmp_wrd:
                            if item1[1] == item2[1] and item1[3] > item2[3]:
                                if self.query_dict['type'] == 'scene(s)':
                                    result.append(str(item1[1]))
                                else:
                                    result.append(str(item1[0])) 
                result = list(set(result))
                result.sort()
                for items in result:
                    terms0.write(str(items) + '\n')

        if (len(self.query_dict) == 2):
            result2 = []
            for elem in self.query_dict['words']:
                if self.sId_cnt[elem]:
                    for val in self.sId_cnt[elem]:
                        if self.query_dict['type'] == 'scene(s)':
                            result2.append(str(val[1]))
                        else:
                            result2.append(str(val[0]))                           
                            
            result2 = list(set(result2))
            result2.sort()
            for items in result2:
                terms0.write(str(items) + '\n')    

    def info_averageLen(self):
        listLen = []
        for items in self.dict:
            text = items['text'] 
            tokens = text.split(' ')
            tokens.remove('')
            listLen.append(len(tokens))
        listLen.sort()
        longest = listLen[-1]
        smallest = listLen[0]
        shortList_plays = []
        shortList_scenes = []
        longList_plays = []
        longList_scenes = []
        for items in self.dict:
            text = items['text'] 
            tokens = text.split(' ')
            tokens.remove('')
            length = len(tokens)  
            if (length == longest):
                longList_scenes.append(items['sceneId'])
                longList_plays.append(items['playId'])
            if (length == smallest):
                shortList_scenes.append(items['sceneId'])
                shortList_plays.append(items['playId'])            
        sum = 0
        count = len(listLen)
        for item in listLen:
            sum += item
        return [shortList_plays, shortList_scenes, longList_plays, longList_scenes, int((sum / count))]
           

if __name__ == '__main__':
    file = "shakespeare-scenes.json"
    I = Inverted(file)
    I.getInput()
    I.terms_Loc_Count()
    I.terms_Loc_Pos()
    I.prcs_query()
    I.term_based_queries()
    '''
    x = I.info_averageLen()
    print('Average length of a scene: {}'.format(x[4]))
    print('Shortest scenes, Longest scenes: {}, {}, Shortest plays, Longest plays: {}, {}'.format(x[1], x[3], x[0], x[2]))
    '''
    print("{} seconds".format(time.time() - I.start_time))
