package cn.hhu.lewen.service;

import cn.hhu.lewen.dao.pojo.ForSearch;
import cn.hhu.lewen.dao.pojo.News;
import cn.hhu.lewen.dao.vo.NewsVo;
import cn.hhu.lewen.dao.vo.Result;
import cn.hhu.lewen.dao.vo.params.IfStarParams;
import cn.hhu.lewen.dao.vo.params.PageParams;
import cn.hhu.lewen.dao.vo.params.ViewHistoryParams;
import com.alibaba.fastjson.JSONObject;

import java.util.List;

/**
 * @author Fandrew
 */
public interface NewsService {

    /**
     * getArticles 获取文章列表
     * @param pageParams
     * @return
     */
    Result getArticles(PageParams pageParams);

    /**
     * 获取浏览记录
     * @param pageParams
     * @return
     */
    Result getBrowsingHistoryByUserId(PageParams pageParams);

    /**
     * 获取收藏记录
     * @param pageParams
     * @return
     */
    Result getStarNewsByUserId(PageParams pageParams);

    /**
     * 新增浏览记录
     * @param viewHistoryParams
     */
    void addNewViewItem(ViewHistoryParams viewHistoryParams);

    /**
     * 更新浏览记录 暂不用
     * @param viewHistoryParams
     */
    void updateViewItem(ViewHistoryParams viewHistoryParams);


    /**
     * 通过作者名模糊搜索文章
     * @param forSearch
     * @return
     */
    List<NewsVo> getArticlesByWriterName(ForSearch forSearch);

    /**
     * 搜索文章  自己看impl
     * @param forSearch
     * @return
     */
    List<NewsVo> searchArticles(ForSearch forSearch);

    /**
     * 收藏与取消收藏
     * @param ifStarParams
     */
    void setStarNews(IfStarParams ifStarParams);

    /**
     * 新增收藏项，即收藏
     * @param ifStarParams
     */
    void addStarItem(IfStarParams ifStarParams);

    /**
     * 删除收藏项，即取消收藏
     * @param ifStarParams
     */
    void deleteStarItem(IfStarParams ifStarParams);

    /**
     * 插入news表中的 tags  暂未用
     * @param entitiesString
     * @param newId
     */
    void insertEntities(String entitiesString, String newId);

    /**
     * 插入新闻实体对照表
     * @param entity
     * @param newId
     */
    void insertEntity2New(String entity,String newId);

    /**
     * 通过新闻实体对照表找文章
     * @param forSearch
     * @return
     */
    List<NewsVo> getEntity2New(ForSearch forSearch);

    /**
     * 通过作者Id 获取它的文章
     * @param pageParams
     * @return
     */
    Result getArticlesByWriterId(PageParams pageParams);

    /**
     * 通过分类ID获取文章
     * @param pageParams
     * @return
     */
    Result getArticlesByCategoryId(PageParams pageParams);

    /**
     * 作者ID的浏览收藏发布排名
     * @param writerId
     * @return
     */
    Result getWriterData(int writerId);

    /**
     * 上传  返回主键newId 用于后续操作
     * @param news
     * @return
     */
    int uploadArticles(News news);

    /**
     * 按月份获取作者浏览收藏发布排名
     * @param writerId
     * @return
     */
    JSONObject getAuthorMonthData(int writerId);


}
