package cn.hhu.lewen.service;

import cn.hhu.lewen.dao.vo.Result;
import cn.hhu.lewen.dao.vo.params.PageParams;

public interface CategoryService {

    /**
     * 获取服务器所有分类
     * @return
     */
    Result getAllCategory();

    /**
     *  按 id 找分类
     * @param id
     * @return
     */
    Result getCategoryById(int id);

    /**
     * 按分类id找文章简介
     * @param pageParams
     * @return
     */
    Result getCategoryDetailsByCategoryId(PageParams pageParams);
}
