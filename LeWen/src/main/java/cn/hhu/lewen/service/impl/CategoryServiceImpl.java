package cn.hhu.lewen.service.impl;

import cn.hhu.lewen.dao.mapper.CategoryMapper;
import cn.hhu.lewen.dao.pojo.Category;
import cn.hhu.lewen.dao.pojo.News;
import cn.hhu.lewen.dao.vo.CategoryVo;
import cn.hhu.lewen.dao.vo.NewsVo;
import cn.hhu.lewen.dao.vo.Result;
import cn.hhu.lewen.dao.vo.params.PageParams;
import cn.hhu.lewen.service.CategoryService;
import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;

@Service("CategoryService")
public class CategoryServiceImpl implements CategoryService {
    @Autowired
    private CategoryMapper categoryMapper;

//    @Autowired
//    private RedisTemplate redisTemplate;


    @Override
    public Result getAllCategory() {
        List<Category> categories = categoryMapper.getAllCategories();

        List<CategoryVo> categoryVoList = copyCategoryList(categories);

        JSONObject jsonObject = new JSONObject();
        jsonObject.put("data",categoryVoList);
        return Result.success(jsonObject);
    }

    @Override
    public Result getCategoryById(int id) {
        Category category = categoryMapper.selectCategoryById(id);
        System.out.println(category);
        return Result.success(category);
    }

    @Override
    public Result getCategoryDetailsByCategoryId(PageParams pageParams) {
        Page<News> page = new Page<>(pageParams.getPageNumber(),pageParams.getPageSize());
        LambdaQueryWrapper<News> queryWrapper = new LambdaQueryWrapper<>();

        IPage<News> newsIPage = categoryMapper.getCategoryDetailsByCategoryId(pageParams.getCategoryId(),pageParams.getUserId(),page,queryWrapper);

        List<News> records = newsIPage.getRecords();

        List<NewsVo> newsVoList =copyList(records);
        System.out.println(newsVoList);

        JSONObject jsonObject = new JSONObject();
        jsonObject.put("data",newsVoList);
        return Result.success(jsonObject);
    }


    private List<CategoryVo> copyCategoryList(List<Category> records) {
        List<CategoryVo> categoryVoList = new ArrayList<>();
        for (Category record : records) {
            categoryVoList.add(copyCategory(record));
        }

        return categoryVoList;
    }

    private CategoryVo copyCategory(Category category){
       CategoryVo categoryVo = new CategoryVo();
       categoryVo.setCategoryId(category.getCategoryId());
       categoryVo.setCategoryName(category.getCategoryName());
       categoryVo.setImgUrl(category.getImgUrl());
       categoryVo.setDescribe(category.getDescribe());


        //调整时间格式
        //newsVo.setWdate(new DateTime(newsVo.getWdate()).toString("yyyy-MM--dd HH:mm"));
        //tag数组化


        return categoryVo;
    }

    private List<NewsVo> copyList(List<News> records) {
        List<NewsVo> newsVoList = new ArrayList<>();
        for (News record : records) {
            newsVoList.add(copy(record));
        }

        return newsVoList;
    }

    private NewsVo copy(News news){
        NewsVo newsVo = new NewsVo();
        BeanUtils.copyProperties(news,newsVo);
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

}
