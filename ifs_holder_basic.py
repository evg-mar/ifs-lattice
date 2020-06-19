import numpy as np
import pandas as pd
import ntpath

import os


def split_path_name(path):
#     print(ntpath.split(path))
    head, tail = ntpath.split(path)
    if tail == '':
        return ntpath.split(head)
    else:
        return head, tail
        

class IfsHolderBasic(object):
    
    def __init__(self, path_file_csv, path_file_config=None):
        self.df_ifs = pd.read_csv(path_file_csv)
#                             names=['id', 'label', 'mu', 'nu'],
#                             index_col='id')
        self.base_path, self.file_name = split_path_name(path_file_csv)
        self.full_path = os.path.join(self.base_path, self.file_name)
        if path_file_config is not None:
            self.df_config = pd.read_csv(path_file_config, 
                                         index_col=False)
#         self.mus = np.asarray(df_ifs['mu'], dtype=float)
#         self.nus = np.asarray(df_ifs['nu'], dtype=float)
#         self.id  = np.asarray(df_ifs['id'], dtype=int)
        
    @property
    def get_mus(self):
        return np.asarray(self.df_ifs['mu'].astype(float), dtype=float)
    
    @property
    def get_nus(self):
        return np.asarray(self.df_ifs['nu'].astype(float), dtype=float)
    
    @property
    def get_idx(self):
        return np.asarray(self.df_ifs.index.astype(int), dtype=int)

        
    def set_ifs(self, mus, nus, idx, path_file=None):
#         path = path_file if path_file is not None else self.full_path
        assert(len(idx)==len(mus)==len(nus))
        dic = {'mu': np.asarray(mus, dtype=float),
               'nu': np.asarray(nus, dtype=float)}
        self.df_ifs = pd.DataFrame(dic, index=idx)
        
        if path_file is not None:
            self.df_ifs.to_csv(path_file, sep=',', index=True)
    
    def set_conf(self, dic, path_config):
        self.df_config.to_csv(dic)



if __name__ == '__main__':
#     from ifs_holder_basic import IfsHolderBasic
    filepath = os.path.join(os.getcwd() , 'ifsholder/ifs_holder.csv')

    ifs_basic = IfsHolderBasic(filepath,
                              None)
    print(ifs_basic.get_mus)
#     print(ifs_basic.df_ifs)