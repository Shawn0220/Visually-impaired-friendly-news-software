import math
import pymysql
import pandas as pd

sql_connection = pymysql.connect(host='localhost', user='root', password='qx01030011',
                                 db='cnsoft', port=3306, autocommit=False, charset='utf8mb4')


# 新闻结构体：编号 + 相似度
class news2W(object):
    def __init__(self, news_id, news_W):
        self.news_id = news_id
        self.news_W = news_W

    def __str__(self):
        return "{news_id:<}\t{news_W:}".format(news_id=self.news_id, news_W=self.news_W)


# 打印新闻结构体的列表
def show_news_list(news_list):
    for news in news_list:
        print(news)
    print("\n=====")


# 获取新闻总收藏量
def get_news_stars(newsid):
    sql = "select count(*) from cnsoft.starinformation where new_id=" + str(newsid)
    df_sql = pd.read_sql(sql, sql_connection)  # 参数：查询语句+连接配置
    return df_sql.loc[0][0]


# 获取所有新闻编号
def get_all_news():
    sql = "select * from cnsoft.news"
    df_sql = pd.read_sql(sql, sql_connection)  # 参数：查询语句+连接配置
    newsArr = []
    for news in df_sql['new_id']:
        # print(news)
        newsArr.append(news)
    return newsArr


# 获取用户收藏的新闻
def get_user_star(userid):
    sql = "select * from cnsoft.starinformation where user_id=" + str(userid)
    df_sql = pd.read_sql(sql, sql_connection)  # 参数：查询语句+连接配置
    newsArr = []
    for news in df_sql['new_id']:
        # print(news)
        newsArr.append(news)
    return newsArr


# 求Wij值
def get_news_W(newsi, newsj):
    sql = "select a.user_id from (select * from cnsoft.starinformation where new_id=" + str(newsi) + \
          ") a,(select * from cnsoft.starinformation where new_id=" + str(newsj) + ") b where a.user_id = b.user_id"
    df_sql = pd.read_sql(sql, sql_connection)
    userArr = []
    # 求式Wij分子项
    # 获取新闻i和j的共同阅读者
    for index, user in df_sql.iterrows():
        # print(user['user_id'])
        userArr.append(user['user_id'])
    # 获取共同阅读者 每个人的收藏总量
    union_reader_starcnt = []
    for user in userArr:
        # print(user)
        sql = "select count(*) from cnsoft.starinformation where user_id=" + str(user)
        df_sql = pd.read_sql(sql, sql_connection)
        # print(df_sql)
        union_reader_starcnt.append(df_sql.loc[0][0])
    # print(union_reader_starcnt)
    # 求得和式分子
    numerator = 0
    for counts in union_reader_starcnt:
        numerator = 1 / math.log(1 + counts, 2)
    # 求得分母
    denominator = 0
    X = get_news_stars(newsi)
    Y = get_news_stars(newsj)
    denominator = math.sqrt(X * Y)
    # 得到Wij
    if denominator != 0:
        Wij = numerator / denominator
    else:
        Wij = 0
    return Wij


# 求S(j,k)
def getSjk(j, k):
    all_news = get_all_news()
    # print(all_news)
    news_W_list = []
    # print(news_W_list)
    for news in all_news:
        if get_news_W(news, j) != 0 and news != j:
            # print(news2W(news, get_news_W(news, j)))
            news_W_list.append(news2W(news, get_news_W(news, j)))
    # print(news_W_list)
    sorted_news_list = sorted(news_W_list, key=lambda x: x.news_W, reverse=True)
    # 求 与新闻j相似度排前K个的新闻
    topK_news = []
    for news in sorted_news_list[:k]:
        topK_news.append(news)

    return topK_news

# 获取新闻推荐度
def getPuj(u,j,k):
    Puj = 0
    starArr = get_user_star(u)
    Sjk = getSjk(j,k)
    for star_news in starArr:
        for news in Sjk:
            if star_news == news.news_id:
                Puj += news.news_W
    return Puj

# 推荐系统 用户ID + 推荐量
def myrecommender(u,howmany):
    all_news = get_all_news()
    recommended_news = []
    for news in all_news:
        Puj = getPuj(u,news,3)
        # print(Puj)
        recommended_news.append(news2W(news,Puj))
    sorted_news_list = sorted(recommended_news, key=lambda x: x.news_W, reverse=True)
    newsid_list = []
    for news in sorted_news_list[:howmany]:
        newsid_list.append(news.news_id)
    return str(newsid_list)

# 测试
if __name__ == '__main__':
    '''e = get_news_stars(2)
    print(e)'''

    '''sql = "select * from cnsoft.starinformation where new_id=1 "
    df_sql = pd.read_sql(sql, sql_connection)
    x = get_news_W(1,6)
    print(x)'''
    #x = news2W(1, 20)
    #x = getSjk(2,2)
    #print(x)
    '''all_news = get_all_news()
    for news in all_news:
        x = getPuj(1,news,10)
        print(x)'''
    x = myrecommender(7, 5)
    print(x)