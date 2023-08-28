package cn.hhu.lewen.dao.mapper;


import cn.hhu.lewen.dao.pojo.ForSearch;
import cn.hhu.lewen.dao.pojo.News;
import cn.hhu.lewen.dao.vo.params.IfStarParams;
import cn.hhu.lewen.dao.vo.params.ViewHistoryParams;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

/**
 * @author Fandrew
 */
@Mapper
public interface NewsMapper extends BaseMapper<News> {

    /**
     * 获取首页向该用户展示的文章
     * @param page
     * @param lambdaQueryWrapper
     * @param userId
     * @return
     */
    IPage<News> getArticles(Page<News> page, LambdaQueryWrapper<News> lambdaQueryWrapper, String userId);

    /**
     * 获取该用户的浏览记录
     * @param page
     * @param lambdaQueryWrapper
     * @param userId
     * @return
     */
    IPage<News> getBrowsingHistoryByUserId(Page<News> page, LambdaQueryWrapper<News> lambdaQueryWrapper,String userId);

    /**
     * 获取该用户的收藏记录
     * @param page
     * @param lambdaQueryWrapper
     * @param userId
     * @return
     */
    IPage<News> getStarNewsByUserId(Page<News> page, LambdaQueryWrapper<News> lambdaQueryWrapper,String userId);

    /**
     * 添加一项新的浏览记录
     * @param viewHistoryParams
     */
    void addNewViewItem(ViewHistoryParams viewHistoryParams);

    /**
     * 更新一项浏览记录 （暂不用
     * @param viewHistoryParams
     */
    void updateViewItem(ViewHistoryParams viewHistoryParams);

    /**
     * 新增一项收藏记录
     * @param ifStarParams
     */
    void addStarItem(IfStarParams ifStarParams);

    /**
     * 取消收藏
     * @param ifStarParams
     */
    void deleteStarItem(IfStarParams ifStarParams);

    /**
     * 向新闻表中插入tags
     * @param entitiesString
     * @param newId
     */
    void insertEntities(String entitiesString,String newId);

    /**
     * 向新闻实体对照表中添加新的项
     * @param entity
     * @param newId
     */
    void insertEntity2New(String entity,String newId);

    /**
     * 通过到新闻实体对照表中检索文章
     * @param forSearch
     * @return
     */
    List<News> getEntity2New(ForSearch forSearch);

    /**
     * 通过作者名 模糊搜索 文章
     * @param forSearch
     * @return
     */
    List<News> getArticlesByWriterName(ForSearch forSearch);

//    List<News> getArticlesByAbstract(ForSearch forSearch);

    /**
     * 通过新闻id数组来搜索文章  用于推荐系统
     * @param userId
     * @param rmdArray
     * @return
     */
    List<News> getArticlesByNewId(String userId, String[] rmdArray);

    //下面的方法用于web端

    /**
     * 通过作者id获取他的文章
     * @param page
     * @param lambdaQueryWrapper
     * @param writerId
     * @return
     */
    IPage<News> getArticlesByWriterId(Page<News> page, LambdaQueryWrapper<News> lambdaQueryWrapper,String writerId);

    /**
     * 通过分类id来获取它的文章
     * @param page
     * @param lambdaQueryWrapper
     * @param categoryId
     * @return
     */
    IPage<News> getArticlesByCategoryId( Page<News> page, LambdaQueryWrapper<News> lambdaQueryWrapper,String categoryId);

    /**
     * 上传文章  返回主键newId在news.getNewId() 用于后续操作
     * @param news
     * @return
     */
    int uploadArticles(News news);

    /**
     * web端的作者Id的浏览 收藏 发布  排名
     * @param writerId
     * @return
     */
    int getViewsByWriterId(int writerId);

    /**
     * 收藏量
     * @param writerId
     * @return
     */
    int getStarsByWriterId(int writerId);

    /**
     * 发布量
     * @param writerId
     * @return
     */
    int getPublishByWriterId(int writerId);

    /**
     * 作者排名  暂时以发布量来排名
     * @param writerId
     * @return
     */
    int getRankByWriterId(int writerId);

    /**
     * 传入writerId 和往前推subMonth的月数 0为当前月
     * @param writerId
     * @param subMonth
     * @return
     */
    int getViewMonthData(int writerId, int subMonth);

    /**
     * 获取六个月的文章被收藏量
     * @param writerId
     * @param subMonth
     * @return
     */
    int getStarMonthData(int writerId, int subMonth);

}
