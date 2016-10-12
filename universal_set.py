import logging
import inspect
import operator

import pandas as pd

class UniversalSet(object):

    def __init__(self, words_set=None):
        
        if words_set is None:
            words_set = set()

        self._index_to_words = []
        self._words_to_index = {}

        self._add(words_set)

    def __eq__(self, other):

        if isinstance(other, UniversalSet):
            return self._index_to_words == other._index_to_words and \
                   self._words_to_index == other._words_to_index
        else:
            raise ValueError('Comparing (%s) with (%s)'
                             % (type(self), type(other)))

    def __len__(self):
        return len(self._index_to_words)

    def __getitem__(self, idx):
         return self._index_to_words[idx]

    def to_csv(self, file_name, index=True):

        col = ['word']
        report_df = pd.DataFrame(columns=col, index=['id'])

    def indices(self):
        return range(len(self._index_to_words))

    def indices_generator(self):
        for idx in range(len(self._index_to_words)):
            yield idx

    def add(self, words_set, return_flag=None):
        words = words_set - set(self._index_to_words)
        self._add(words)

        if return_flag == 'length':
            return len(words)
        elif return_flag == 'set':
            return words
        elif return_flag is None:
            return None
        else:
            raise AttributeError('Incorrect index flag: %s in the \
            add function' % return_flag)

    def _add(self, words):

        next_idx = len(self._index_to_words)
        for w in words:
            self._words_to_index[w] = next_idx
            self._index_to_words.append(w)
            next_idx += 1

    def get_index(self, word, default=None):
        return self._words_to_index.get(word, default)

    def get_word(self, idx, default=None):
        
        return default if idx > len(self._index_to_words) \
                       else self._index_to_words[idx]

    def characteristic_indices(self, words):

        indices = set([self.get_index(w, None) for w in words])
        indices.discard(None)
        return indices

    def check_consistancy(self):

        msg = 'The universal set is consistant'
        result = True

        if len(self._words_to_index) != len(self._index_to_words):
            result = False
            msg = ('Inconsistant correspondance of the length of \
            indexes and words')

        logging.info(msg)
        return result

        for w, idx in self._words_to_index.iteritems():
            if w != self._index_to_words[idx]:
                result = False
                msg = ('Inconsistant universal set at word: %s, \
                idx: %i' % (w, idx))

                break

        logging.info(msg)
        return result

    def length(self):
        return len(self._index_to_words)

    def empty(self):
        return (len(self._index_to_words) == 0)

    def set_universe(self,
                     index_to_words=[],
                     words_to_index={},
                     rhs=None,
                     copy_op=lambda x: x):
        """Sets the universal set through the corresponding index_to_words
        (The words of the universe have to be ordered and there fore they
        posses an index in this ordering) or words_to_index.

        Attributes
        ----------
        index_to_words : list with the words, occuring by their corresponding
        order
        words_to_index : dictionary with the words as keys and their
        corresponding values
        copy_op : Operation that determines how the universal set to be stored.
        It can be stored as a hard/deep/ copy into the member variables of
        self /the current class/ or the corresponding member variable can
        point to the universal set from outside.
        """
        if rhs is not None:
            index_to_words = rhs._index_to_words
            words_to_index = rhs._words_to_index

        if (len(index_to_words) == 0 and len(words_to_index) == 0):
            raise AssertionError('Function takes index_to_words or \
            words_to_index and exactly one of them!')
        elif (len(index_to_words) > 0 and len(words_to_index) > 0):
            if len(index_to_words) != len(words_to_index):
                raise AssertionError('Input attributes should have the same \
                                     length')
            else:  # if the lengths are equal
                # Chek the input attributes for consistency
                for word, idx in words_to_index.iteritems():
                    if word != index_to_words[idx]:
                        raise AssertionError('Input attributes are \
                        inconsistent!')
                self._index_to_words = copy_op(index_to_words)
                self._words_to_index = copy_op(words_to_index)

        elif len(words_to_index) > 0:
            self._words_to_index = copy_op(words_to_index)
            sorted_by_index = sorted(words_to_index.items(),
                                     key=operator.itemgetter(1))
            self._index_to_words = [item[0] for item in sorted_by_index]

        elif len(index_to_words) > 0:
            self._index_to_words = copy_op(index_to_words)
            self._words_to_index = dict((w, idx)
                                        for idx, w in range(index_to_words))
        else:
            raise AssertionError('Unhandled case in function: %s'
                                 % inspect.stack()[0][3])
