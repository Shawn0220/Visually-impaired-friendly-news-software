package cn.hhu.lewen.dao.vo;

import com.alibaba.fastjson.annotation.JSONType;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

/**
 * @author Fandrew
 */
@Data
@JSONType(orders = {"categoryId", "categoryName", "imgUrl", "describe"})
public class CategoryVo {

    @JsonProperty(value = "categoryId")
    private int categoryId;

    @JsonProperty(value = "categoryName")
    private String categoryName;

    @JsonProperty(value = "imgUrl")
    private String imgUrl;

    @JsonProperty(value = "describe")
    private String describe;




}
