# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np

ADD = u'E:\\最近任务\\实习资料\\姚老师\\2.7_consulting_agreement_info\\start_end_date\\begin_end_date.csv'
ORIGIN = U'E:\\最近任务\\实习资料\\姚老师\\2.7_consulting_agreement_info\\independent_contractor\\merge_8info.csv'

# read
df_ori = pd.read_csv(ORIGIN)
df_add = pd.read_csv(ADD)

# write
df = pd.merge(df_ori, df_add, on='exfilename')
merge = df.to_csv('merge_9info.csv')
print 'OK'