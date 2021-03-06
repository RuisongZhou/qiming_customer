# -*- coding: utf-8 -*-

from typing import List, Union, Tuple

import pandas as pd
# import xlrd
import random


class Dataloader:
    '''
    基础 Excel dataloader

    Note: 这里特地使用 `.xlsx` 格式数据而不选用 `.csv` 格式，因为数据中本身就可能
    带有英文逗号 `,`。

    Note: 这里没有分 batch，因为数据量本身比较小。
    '''

    @staticmethod
    def flatten_data(df: pd.DataFrame) -> List[Tuple[str, str, int]]:
        '''
        [内部方法] 将原始数据表中数据项压平

        Return:
            `[ ( 具体问法, 主问题, 答案编号 ) ]`

        Note: 主问题也算一种具体问法，加入数据中。
        '''
        retlist = []
        for row in df.itertuples():
            for ques_form in row[3:]:
                if pd.isnull(ques_form):
                    continue
                retlist.append((ques_form, row[1], row[0]))
            retlist.append((row[1], row[1], row[0]))        # 主问题也算作一种问法，加入数据中
        return retlist

    def __init__(self, filename: str, sheet_name: str):
        '''
        [构造函数]

        Args:
        - filename: Excel 数据文件路径
        - sheet_name: 数据表名称（'知识库'）
        '''
        df = pd.read_excel(filename, sheet_name=sheet_name)
        self._orig_df = df
        self._data_pool = Dataloader.flatten_data(df)
        self._answer_list = df['答案']

    def __len__(self) -> int:
        '''
        获取数据集大小
        '''
        return len(self._data_pool)

    @property
    def original_dataframe(self):
        '''
        [调试用] 获取未压平前的原始 `pd.DataFrame`
        '''
        return self._orig_df

    def sample(self, count: int=1) -> List[Tuple[str, str, str]]:
        '''
        随机获取数据

        Args:
        - count: batch 大小，默认为 1

        Return:
            `[ ( 具体问法, 主问题, 答案编号 ) ]`
        '''
        return random.sample(self._data_pool, count)

    def get_answer(self, main_ques_idx: int) -> str:
        '''
        根据 `答案编号` 获取对应答案内容
        '''
        return self._answer_list[main_ques_idx]


'''Testing and Example'''

if __name__ == '__main__':
    loader = Dataloader('../启明学院智能客服知识库.xlsx', '知识库')
    answer = loader._answer_list
    question = pd.DataFrame(loader._data_pool)
    qa = pd.concat([question,answer],axis=1)
    qa.to_csv('QA.csv',index=0,sep='\t')