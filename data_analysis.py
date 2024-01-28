import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
import numpy as np
import jieba
from wordcloud import WordCloud
from collections import Counter
import re
import july
from july.utils import date_range
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 读取CSV文件
df = pd.read_csv('你的csv文件路径')

# TODO 数据预处理（根据需求进行）
# 只保留文本聊天
df = df[df['Type'] == 1]

# 只取'IsSender','StrContent','StrTime'列
selected_columns = ['IsSender', 'StrContent', 'StrTime']  # 将要保留的列名放入一个列表中
df = df[selected_columns]
# TODO 每天聊天频率柱状图
# 将StrTime列的数据转换为日期时间格式
df['StrTime'] = pd.to_datetime(df['StrTime'])

# 创建一个新的Date列，只保留日期部分
df['Date'] = df['StrTime'].dt.date

# 根据每一天统计聊天频率
chat_frequency = df['Date'].value_counts().sort_index()

# 生成柱状图
chat_frequency.plot(kind='bar', color='#DF9F9B')
plt.xlabel('Date')
plt.ylabel('Frequency')
plt.title('Chat Frequency by Day')

# 调整刻度标签，只保留月份和日期
date_labels = [date.strftime('%m-%d') for date in chat_frequency.index]  # 格式化日期
plt.xticks(range(len(date_labels)), date_labels)  # 设置新的刻度标签
plt.xticks(fontsize=5)
plt.show()

# # TODO 制作日历热力图 （此部分需将matplotlib版本降级为3.7.0，与july兼容）
# # 将日期列转换为datetime类型
# df['Date'] = pd.to_datetime(df['Date'])
#
# # 获取日期范围
# start_date = df['Date'].min()
# end_date = df['Date'].max()
# dates = date_range(start_date, end_date)
# july.calendar_plot(dates, chat_frequency, cmap = 'Oranges')
# plt.show()


# july.month_plot(dates, chat_frequency, month=1, date_label=True)
# plt.show()

# TODO 双方信息数量对比
# 双方发送的聊天信息
sent_by_me = df[df['IsSender'] == 1]['StrContent']
sent_by_others = df[df['IsSender'] == 0]['StrContent']
# 统计数量
count_sent_by_me = len(sent_by_me)
count_sent_by_others = len(sent_by_others)
# 创建饼状图
labels = ['西红柿', '头头']
sizes = [count_sent_by_me, count_sent_by_others]
colors = ['#FF6347','#9ACD32']

explode = (0, 0.05)
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)

plt.axis('equal')
plt.title('Comparison of the number of chats')

# 添加图例
plt.legend()
# 显示图表
plt.show()


# TODO 根据一天中的每一个小时进行统计聊天频率，并生成柱状图
# 将时间字符串转换为时间类型并提取小时
df['DateTime'] = pd.to_datetime(df['StrTime'])
df['Hour'] = df['DateTime'].dt.hour

# 统计每个小时的聊天频率
hourly_counts = df['Hour'].value_counts().sort_index().reset_index()
hourly_counts.columns = ['Hour', 'Frequency']

# 绘制柱状图和数据拟合曲线
plt.figure(figsize=(10, 6))
ax = sns.barplot(x='Hour', y='Frequency', data=hourly_counts, color="#E6AAAA")

# 添加核密度估计曲线
sns.kdeplot(df['Hour'], color='#C64F4F', linewidth=1, ax=ax.twinx())

# 设置图形标题和轴标签
plt.title('Chat Frequency by Hour')
plt.xlabel('Hour of the Day')
plt.ylabel('Frequency')

# 显示图形
plt.show()
# TODO  词频分析
sent_by_me_text = ' '.join(sent_by_me.astype(str))
sent_by_others_text=' '.join(sent_by_others.astype(str))
all_text = ' '.join(df['StrContent'].astype(str))
# 使用jieba进行中文分词
words = list(jieba.cut(all_text, cut_all=False))
mywords = list(jieba.cut(sent_by_me_text, cut_all=False))
herwords = list(jieba.cut(sent_by_others_text, cut_all=False))


def is_chinese_word(word):
    for char in word:
        if not re.match(r'[\u4e00-\u9fff]', char):
            return False
    return True
with open('stopwords_hit.txt', encoding='utf-8') as f: # 可根据需要打开停用词库，然后加上不想显示的词语
    con = f.readlines()
    stop_words = set() # 集合可以去重
    for i in con:
        i = i.replace("\n", "")   # 去掉读取每一行数据的\n
        stop_words.add(i)
stop_words

def correct(a):
    b=[]
    for word in a:
        if len(word) > 1 and is_chinese_word(word) and word not in stop_words:
            b.append(word)
    return b

Words = correct(words)
Mywords = correct(words)
Herwords = correct(herwords)

words_space_split = ' '.join(Words)
print(words_space_split)
def word_fre_draw(a):
    a_counts = Counter(a)
    top_30_a= a_counts.most_common(30)
    words, frequencies = zip(*top_30_a)

    # 绘制水平柱状图
    plt.figure(figsize=(10, 15))
    plt.barh(words, frequencies, color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title('Top 30 Words in Chat Messages')
    plt.show()

word_fre_draw(Words)
word_fre_draw(Mywords)
word_fre_draw(Herwords)

# TODO 词云制作

wordcloud = WordCloud(font_path='‪C:\Windows\Fonts\STCAIYUN.TTF',  # 字体路径，例如'SimHei.ttf'
                      width=800, height=600,
                      background_color='white',  # 背景颜色
                      max_words=200,  # 最大显示的词数
                      max_font_size=100,  # 字体最大值
                      ).generate(words_space_split)

# 使用Matplotlib展示词云图
plt.figure(figsize=(10, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # 关闭坐标轴
plt.show()

#TODO 一周贡献率
df['Weekday'] = df['StrTime'].dt.day_name()

# 计算每天的消息数量
weekday_counts = df['Weekday'].value_counts().reindex([
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
])

# 找出频率最高的那天
max_day = weekday_counts.idxmax()

# 制作饼状图
plt.figure(figsize=(8, 8))
explode = [0.1 if day == max_day else 0 for day in weekday_counts.index]  # 突出显示频率最高的那天
plt.pie(weekday_counts, labels=weekday_counts.index, explode=explode, autopct='%1.1f%%',
        startangle=140, colors=plt.cm.Paired.colors)
plt.title('Distribution of Messages During the Week')
plt.show()

# TODO 最多的天数及月份
df['Date'] = pd.to_datetime(df['Date'])

# 提取年月日
df['YearMonth'] = df['Date'].dt.to_period('M')
df['Day'] = df['Date'].dt.date

# 计算每天的消息数量
daily_counts = df['Day'].value_counts()

# 找出消息最多的那一天
max_day = daily_counts.idxmax()
max_day_count = daily_counts.max()

# 计算每月的消息数量
monthly_counts = df['YearMonth'].value_counts()

# 找出消息最多的那个月
max_month = monthly_counts.idxmax()
max_month_count = monthly_counts.max()

# 打印结果
print(f"最多消息的一天是 {max_day}，共有 {max_day_count} 条消息。")
print(f"最多消息的一个月是 {max_month}，共有 {max_month_count} 条消息。")


# 计算消息总数
total_messages = len(df)

# 打印消息总数
print(f"一共聊了 {total_messages} 条消息。")