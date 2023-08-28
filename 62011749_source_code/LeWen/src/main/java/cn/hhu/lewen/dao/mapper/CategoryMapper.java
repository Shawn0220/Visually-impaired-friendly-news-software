package cn.hhu.lewen.dao.mapper;

import cn.hhu.lewen.dao.pojo.Category;
import cn.hhu.lewen.dao.pojo.News;
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
public interface CategoryMapper extends BaseMapper<Category> {
    /**
     * 获取数据库中文章的所有分类名
     * @return
     */
    List<Category> getAllCategories();

    /**
     * 通过id获取分类信息
      * @param id
     * @return
     */
    Category selectCategoryById(int id);

    /**
     * 通过分类id获取该分类文章
     * @param categoryId
     * @param userId
     * @param page
     * @param lambdaQueryWrapper
     * @return
     */
    IPage<News> getCategoryDetailsByCategoryId(String categoryId, String userId, Page<News> page, LambdaQueryWrapper<News> lambdaQueryWrapper);
}
