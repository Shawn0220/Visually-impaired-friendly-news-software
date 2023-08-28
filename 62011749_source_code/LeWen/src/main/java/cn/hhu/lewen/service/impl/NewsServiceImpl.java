package cn.hhu.lewen.service.impl;

import cn.hhu.lewen.controller.Python;
import cn.hhu.lewen.dao.mapper.NewsMapper;
import cn.hhu.lewen.dao.pojo.ForSearch;
import cn.hhu.lewen.dao.pojo.News;
import cn.hhu.lewen.dao.vo.BrowsingHistoryVo;
import cn.hhu.lewen.dao.vo.NewsVo;
import cn.hhu.lewen.dao.vo.Result;
import cn.hhu.lewen.dao.vo.StarVo;
import cn.hhu.lewen.dao.vo.params.IfStarParams;
import cn.hhu.lewen.dao.vo.params.PageParams;
import cn.hhu.lewen.dao.vo.params.ViewHistoryParams;
import cn.hhu.lewen.service.NewsService;
import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;

//import org.springframework.data.domain.Page;
//import org.springframework.data.domain.PageImpl;

@Service("NewsService")
public class NewsServiceImpl implements NewsService {

    @Autowired
    private NewsMapper newsMapper;


    @Override
    public Result getArticles(PageParams pageParams){
//        System.out.println(((String[]) Python.recmd(pageParams.getUserId(),"10").get("array")).toString());

        pageParams.setRmdArray((String[]) Python.recmd(pageParams.getUserId(),"10").get("array"));

        String[] t = pageParams.getRmdArray();
        System.out.println("rmdArray is :");
        for (String s : t) {
            System.out.println(s);
        }

        Page<News> page = new Page<>(pageParams.getPageNumber(),pageParams.getPageSize());
        //IPage<News> iPage = new Page<>()
//        LambdaQueryWrapper<News> queryWrapper = new LambdaQueryWrapper<>();
        LambdaQueryWrapper<News> queryWrapper = new LambdaQueryWrapper<>();

        //是否置顶进行排序,        //时间倒序进行排列相当于order by create_data desc
        //queryWrapper.orderByAsc(News::getRecmd);





        IPage<News> newsPage = newsMapper.getArticles(page,queryWrapper,pageParams.getUserId());
        //分页查询用法 https://blog.csdn.net/weixin_41010294/article/details/105726879
        List<News> records = newsPage.getRecords();

        records.addAll(0, newsMapper.getArticlesByNewId(pageParams.getUserId(),pageParams.getRmdArray()));

        //        records.addAll(0, )
//        String[] r = new String[]{"12","9","1","3","7","2","4","5","6","8"};
//        System.out.println("get by newId: "+newsMapper.getArticlesByNewId("1",r));

        //打印测试
//        for (News record : records) {
//            System.out.println(record);
//            System.out.println("--------------------------------------------");
//        }


        // 要返回我们定义的vo数据，就是对应的前端数据，不应该只返回现在的数据需要进一步进行处理
        List<NewsVo> newsVoList =copyListForNew(records);

//        System.out.println(newsVoList);

//        for (NewsVo newsVo : newsVoList) {
//            System.out.println(newsVo);
//            System.out.println("----------------------------------");
//        }
//        return Result.success(records);

        JSONObject jsonObject = new JSONObject();
        jsonObject.put("data",newsVoList);

        return Result.success(jsonObject);

    }

    @Override
    public Result getBrowsingHistoryByUserId(PageParams pageParams){
        Page<News> page = new Page<>(pageParams.getPageNumber(),pageParams.getPageSize());

        LambdaQueryWrapper<News> queryWrapper = new LambdaQueryWrapper<>();

        IPage<News> newsPage = newsMapper.getBrowsingHistoryByUserId(page,queryWrapper,pageParams.getUserId());

        List<News> records = newsPage.getRecords();


        List<BrowsingHistoryVo> browsingHistoryVoList = copyListForBrowsingHistory(records);

        JSONObject jsonObject = new JSONObject();
        jsonObject.put("data",browsingHistoryVoList);


        return Result.success(jsonObject);
    }

    @Override
    public Result getStarNewsByUserId(PageParams pageParams){
        Page<News> page = new Page<>(pageParams.getPageNumber(),pageParams.getPageSize());

        LambdaQueryWrapper<News> queryWrapper = new LambdaQueryWrapper<>();

        IPage<News> newsPage = newsMapper.getStarNewsByUserId(page,queryWrapper,pageParams.getUserId());

        List<News> records = newsPage.getRecords();


        List<StarVo> starVoList = copyListForStar(records);

        JSONObject jsonObject = new JSONObject();
        jsonObject.put("data",starVoList);

        return Result.success(jsonObject);
    }
    @Override
    public void addNewViewItem(ViewHistoryParams viewHistoryParams){
        newsMapper.addNewViewItem(viewHistoryParams);
    }
    @Override
    public void updateViewItem(ViewHistoryParams viewHistoryParams){
        newsMapper.updateViewItem(viewHistoryParams);
    }

    @Override
    public void setStarNews(IfStarParams ifStarParams){
        if(ifStarParams.getIfStar()==1){
            addStarItem(ifStarParams);
        }else if (ifStarParams.getIfStar() == 0){
            deleteStarItem(ifStarParams);
        }
    }

    @Override
    public void addStarItem(IfStarParams ifStarParams) {
        newsMapper.addStarItem(ifStarParams);
    }

    @Override
    public void deleteStarItem(IfStarParams ifStarParams) {
        newsMapper.deleteStarItem(ifStarParams);
    }

    @Override
    public void insertEntities(String entitiesString, String newId) {
        newsMapper.insertEntities(entitiesString,newId);
    }

    @Override
    public void insertEntity2New(String entity, String newId) {
        newsMapper.insertEntity2New(entity,newId);
    }

    @Override
    public List<NewsVo> searchArticles(ForSearch forSearch){

        List<NewsVo> searchList = new ArrayList<>();

       searchList.addAll(getEntity2New(forSearch));
       searchList.addAll(getArticlesByWriterName(forSearch));

        System.out.println("the searchList is: "+searchList);

//        JSONObject jsonObject = new JSONObject();
//        jsonObject.put("list",searchList);


        return searchList;
    }


    //搜索含有entity的
    @Override
    public List<NewsVo> getEntity2New(ForSearch forSearch) {
//        System.out.println("getentity2new called");
//        ForSearch forSearch = new ForSearch();
//        forSearch.setEntities(entities);
//        forSearch.setUserId(userId);

        List<NewsVo> newsVoList = copyListForNew(newsMapper.getEntity2New(forSearch));

        return newsVoList;
    }

    //按作者名模糊搜索
    @Override
    public List<NewsVo> getArticlesByWriterName(ForSearch forSearch) {
//        Page<News> page = new Page<>(1,10);

//        LambdaQueryWrapper<News> queryWrapper = new LambdaQueryWrapper<>();

        List<News> records = newsMapper.getArticlesByWriterName(forSearch);

//         = newsPage.getRecords();


        List<NewsVo> newsVoList = copyListForNew(records);

//        JSONObject jsonObject = new JSONObject();
//        jsonObject.put("data",newsVoList);

        return newsVoList;
    }

    //-----下面是为web端准备的------------------------------------------------------------------------------------

    @Override
    public Result getArticlesByWriterId(PageParams pageParams){
        Page<News> page = new Page<>(pageParams.getPageNumber(),pageParams.getPageSize());

        LambdaQueryWrapper<News> queryWrapper = new LambdaQueryWrapper<>();

        IPage<News> newsPage = newsMapper.getArticlesByWriterId(page,queryWrapper,pageParams.getWriterId());

        List<News> records = newsPage.getRecords();

        // 要返回我们定义的vo数据，就是对应的前端数据，不应该只返回现在的数据需要进一步进行处理
        List<NewsVo> newsVoList =copyListForNew(records);


        JSONObject jsonObject = new JSONObject();
        jsonObject.put("data",newsVoList);

        return Result.success(jsonObject);

    }
    @Override
    public Result getArticlesByCategoryId(PageParams pageParams){
        Page<News> page = new Page<>(pageParams.getPageNumber(),pageParams.getPageSize());

        LambdaQueryWrapper<News> queryWrapper = new LambdaQueryWrapper<>();

        IPage<News> newsPage = newsMapper.getArticlesByCategoryId(page,queryWrapper,pageParams.getCategoryId());

        List<News> records = newsPage.getRecords();

        // 要返回我们定义的vo数据，就是对应的前端数据，不应该只返回现在的数据需要进一步进行处理
        List<NewsVo> newsVoList =copyListForNew(records);


        JSONObject jsonObject = new JSONObject();
        jsonObject.put("data",newsVoList);

        return Result.success(jsonObject);

    }

    @Override
    public Result getWriterData(int writerId){
        JSONObject jsonObject = new JSONObject();
        int views = newsMapper.getViewsByWriterId(writerId);
        int stars = newsMapper.getStarsByWriterId(writerId);
        int release = newsMapper.getPublishByWriterId(writerId);
        int rank = newsMapper.getRankByWriterId(writerId);
        System.out.println(views+"aa"+stars+"aa"+release+"aa"+rank);
        jsonObject.put("views",views);
        jsonObject.put("stars",stars);
        jsonObject.put("release",release);
        jsonObject.put("rank",rank);

        return Result.success(jsonObject);
    }

    @Override
    public int uploadArticles(News news) {

        newsMapper.uploadArticles(news);
        int newId = news.getNewId();

        return newId;
    }


    @Override
    public JSONObject getAuthorMonthData(int writerId) {
        JSONObject jsonObject = new JSONObject();
        int[] views = new int[6];
        int[] stars = new int[6];

        for(int i=5; i>=0; i--){
            views[5-i] = newsMapper.getViewMonthData(writerId,i);
            stars[5-i] = newsMapper.getStarMonthData(writerId,i);
        }

        jsonObject.put("views",views);
        jsonObject.put("stars",stars);




        return jsonObject;
    }

    //------下面是辅助工具方法-----------------------------------------------------------------------------------
    private List<StarVo> copyListForStar(List<News> records) {
        List<StarVo> starVoList = new ArrayList<>();
        for (News record : records) {
            starVoList.add(copyForStar(record));
        }

        return starVoList;
    }

    private StarVo copyForStar(News news) {
        StarVo starVo = new StarVo();
//        BeanUtils.copyProperties(news,newsVo);
        starVo.setNewId(news.getNewId());
        starVo.setNewTitle(news.getNewTitle());
        starVo.setNewAbstract(news.getNewAbstract());
        starVo.setNewContent(news.getNewContent());

        // 加入new LinkedHashMap<>()  可以保证put进去是什么顺序，显示就是什么顺序
        JSONObject t1 = new JSONObject(new LinkedHashMap<>());
        t1.put("writerId",news.getWriterId());
        t1.put("writerAccount",news.getWriterAccount());
        t1.put("nickname",news.getNickname());
        starVo.setAuthor(t1);

        starVo.setCreateDate(news.getCreateDate());

        String temptags = news.getTags();
        String[] temp = temptags.split(",");
        starVo.setTags(temp);

        JSONObject t2 = new JSONObject(new LinkedHashMap<>());
        t2.put("categoryId",news.getCategoryId());
        t2.put("categoryName",news.getCategoryName());
        starVo.setCategory(t2);

        starVo.setViews(news.getViews());
        starVo.setStars(news.getStars());
        starVo.setWeight(news.getWeight());
        starVo.setTitleVoice(news.getTitleVoice());

        starVo.setIfStar(news.getIfStar());


//        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");//格式化为一个固定格式的字符串
//        Date date = news.getStarTime();
//        String text = sdf.format(date);

        starVo.setStarTime( news.getStarTime());







        //调整时间格式
        //newsVo.setWdate(new DateTime(newsVo.getWdate()).toString("yyyy-MM--dd HH:mm"));
        //tag数组化


        return starVo;
    }

    private List<NewsVo> copyListForNew(List<News> records) {
        List<NewsVo> newsVoList = new ArrayList<>();
        for (News record : records) {
            newsVoList.add(copyForNew(record));
        }

        return newsVoList;
    }

    private List<BrowsingHistoryVo> copyListForBrowsingHistory(List<News> records) {
        List<BrowsingHistoryVo> browsingHistoryVoList = new ArrayList<>();
        for (News record : records) {
            browsingHistoryVoList.add(copyForBrowsingHistory(record));
        }

        return browsingHistoryVoList;
    }



    private NewsVo copyForNew(News news){
        NewsVo newsVo = new NewsVo();
//        BeanUtils.copyProperties(news,newsVo);
        newsVo.setNewId(news.getNewId());
        newsVo.setNewTitle(news.getNewTitle());
        newsVo.setNewAbstract(news.getNewAbstract());
        newsVo.setNewContent(news.getNewContent());

        // 加入new LinkedHashMap<>()  可以保证put进去是什么顺序，显示就是什么顺序
        JSONObject t1 = new JSONObject(new LinkedHashMap<>());
        t1.put("writerId",news.getWriterId());
        t1.put("writerAccount",news.getWriterAccount());
        t1.put("nickname",news.getNickname());
        newsVo.setAuthor(t1);

        newsVo.setCreateDate(news.getCreateDate());

        String temptags = news.getTags();
        String[] temp = temptags.split(",");
        newsVo.setTags(temp);

        JSONObject t2 = new JSONObject(new LinkedHashMap<>());
        t2.put("categoryId",news.getCategoryId());
        t2.put("categoryName",news.getCategoryName());
        newsVo.setCategory(t2);

        newsVo.setViews(news.getViews());
        newsVo.setStars(news.getStars());
        newsVo.setWeight(news.getWeight());
        newsVo.setTitleVoice(news.getTitleVoice());

        newsVo.setIfStar(news.getIfStar());







        //调整时间格式
        //newsVo.setWdate(new DateTime(newsVo.getWdate()).toString("yyyy-MM--dd HH:mm"));
        //tag数组化


        return newsVo;
    }


    private BrowsingHistoryVo copyForBrowsingHistory(News news){
        BrowsingHistoryVo browsingHistoryVo = new BrowsingHistoryVo();
//        BeanUtils.copyProperties(news,newsVo);
        browsingHistoryVo.setNewId(news.getNewId());
        browsingHistoryVo.setNewTitle(news.getNewTitle());
        browsingHistoryVo.setNewAbstract(news.getNewAbstract());
        browsingHistoryVo.setNewContent(news.getNewContent());

        // 加入new LinkedHashMap<>()  可以保证put进去是什么顺序，显示就是什么顺序
        JSONObject t1 = new JSONObject(new LinkedHashMap<>());
        t1.put("writerId",news.getWriterId());
        t1.put("writerAccount",news.getWriterAccount());
        t1.put("nickname",news.getNickname());
        browsingHistoryVo.setAuthor(t1);

        browsingHistoryVo.setCreateDate(news.getCreateDate());

        String temptags = news.getTags();
        String[] temp = temptags.split(",");
        browsingHistoryVo.setTags(temp);

        JSONObject t2 = new JSONObject(new LinkedHashMap<>());
        t2.put("categoryId",news.getCategoryId());
        t2.put("categoryName",news.getCategoryName());
        browsingHistoryVo.setCategory(t2);

        browsingHistoryVo.setViews(news.getViews());
        browsingHistoryVo.setStars(news.getStars());
        browsingHistoryVo.setWeight(news.getWeight());
        browsingHistoryVo.setTitleVoice(news.getTitleVoice());

        browsingHistoryVo.setIfStar(news.getIfStar());
        browsingHistoryVo.setViewTime(news.getViewTime());







        //调整时间格式
        //newsVo.setWdate(new DateTime(newsVo.getWdate()).toString("yyyy-MM--dd HH:mm"));
        //tag数组化


        return browsingHistoryVo;
    }


}
