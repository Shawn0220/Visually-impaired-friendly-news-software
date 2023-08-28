package cn.hhu.lewen.dao.pojo;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import lombok.Data;

/**
 * @author Fandrew
 */
@Data
public class Category {

    @TableId(value = "category_id",type = IdType.AUTO)

    private int categoryId;
    //id of category

    private String categoryName;
    // name of category

    private String imgUrl;
    // url of img

    private String describe;
    // description of category




}
