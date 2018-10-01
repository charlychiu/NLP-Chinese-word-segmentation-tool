
# coding: utf-8

# In[3]:


from typing import Tuple

# ref class https://towardsdatascience.com/implementing-a-trie-data-structure-in-python-in-less-than-100-lines-of-code-a877ea23c1a1
class TrieNode(object):
    """
    Our trie node implementation. 
    """
    
    def __init__(self, char: str):
        self.char = char
        self.children = []
        # Is it the last character of the word.`
        self.word_finished = False
        # How many times this character appeared in the addition process
        self.counter = 1
    

def add(root, word: str):
    """
    Adding a word in the trie structure
    """
    node = root
    for char in word:
        found_in_child = False
        # Search for the character in the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found it, increase the counter by 1 to keep track that another
                # word has it as well
                child.counter += 1
                # And point the node to the child that contains this char
                node = child
                found_in_child = True
                break
        # We did not find it so add a new chlid
        if not found_in_child:
            new_node = TrieNode(char)
            node.children.append(new_node)
            # And then point node to the new child
            node = new_node
    # Everything finished. Mark it as the end of a word.
    node.word_finished = True


def find_prefix(root, prefix: str) -> Tuple[bool, int]:
    """
    Check and return 
      1. If the prefix exsists in any of the words we added so far
      2. If yes then how may words actually have the prefix
    """
    node = root
    # If the root node has no children, then return False.
    # Because it means we are trying to search in an empty trie
    if not root.children:
        return False, 0
    for char in prefix:
        char_not_found = True
        # Search through all the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found the char existing in the child.
                char_not_found = False
                # Assign node as the child containing the char and break
                node = child
                break
        # Return False anyway when we did not find a char.
        if char_not_found:
            return False, 0
    # Well, we are here means we have found the prefix. Return true to indicate that
    # And also the counter of the last node. This indicates how many words have this
    # prefix
    return True, node.counter


# In[4]:


import pandas as pd


# In[5]:


# read file 
file_1_path = 'data/dict_revised_2015_20160523_1.xls'
file_2_path = 'data/dict_revised_2015_20160523_2.xls'
file_3_path = 'data/dict_revised_2015_20160523_3.xls'


df1 = pd.read_excel(file_1_path)
df2 = pd.read_excel(file_2_path)
df3 = pd.read_excel(file_3_path)
frames = [df1, df2, df3]

result = pd.concat(frames)


# In[6]:


# mydict = result['字詞名']
pdSeries = result.iloc[ : , [1,2] ]


# In[7]:


mydict = pdSeries.set_index('字詞名')['字詞號'].to_dict()


# In[8]:


# processed error data i.g. &fa76._104_0.gif;
mydict = {k:v for k,v in mydict.items() if '.gif' not in k}


# In[9]:


for i in mydict.keys():
    print(i)


# In[10]:


root = TrieNode('*')
for i in mydict.keys():
    add(root, i)


# In[11]:


print(find_prefix(root, '大家好'))


# In[12]:


print(find_prefix(root, '大家'))
print(find_prefix(root, '大'))


# In[13]:


# Maximum Matching Method
def cutting_string(sentence):
    count_sentence_length = len(sentence)
    sentence_to_index_list = list()
    start_index = 0
    end_index = len(sentence)
    mark = ['，', '。', '、', '；']
    while start_index < end_index:
        if sentence[start_index:end_index] in mark:
            start_index += len(sentence[start_index:end_index])
            end_index = len(sentence)
            continue
        if sentence[start_index:end_index].isdigit():
            start_index += len(sentence[start_index:end_index])
            end_index = len(sentence)
            continue
        result, _ = find_prefix(root, sentence[start_index:end_index])
        if result:
            sentence_to_index_list.append(sentence[start_index:end_index])
#             print(sentence[start_index:end_index], start_index, end_index)
            start_index += len(sentence[start_index:end_index])
            end_index = len(sentence)
        else:
            end_index -= 1
    return sentence_to_index_list


# In[14]:


result_list = cutting_string("川普早在2016年競選總統期間就對與宣戰，認為這類多邊貿易機制導致美國製造業工作機會流失。川普也說到做到，2017年1月上任")
print('result: ',('/').join(result_list))

