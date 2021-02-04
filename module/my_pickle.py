'''
pickleを利用して
ファイルの読み込みや書き込みを行う
関数が定義されている
'''

#モジュールのインクルード
import pickle

#ファイルの読み込みをする関数
def pickle_load(file_name):
    with open(f'./pickle/{file_name}.pickle', mode='rb') as f:
        data = pickle.load(f)
        return data

#ファイルの書き込みをする関数
def pickle_dump(obj, file_name):
    with open(f'./pickle/{file_name}.pickle', mode='wb') as f:
        pickle.dump(obj,f)