package cn.hhu.lewen.dao.vo;

import com.alibaba.fastjson.JSONObject;
import com.alibaba.fastjson.annotation.JSONType;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import java.sql.Timestamp;


/**
 * @author Fandrew
 */
@Data
@JSONType(orders={"newId","newTitle","newAbstract","newContent","author","createDate",
        "tags","category", "views","stars","weight","titleVoice","ifStar","starTime"})
public class StarVo {

    @JsonProperty(value = "newId")
    private int newId;
    @JsonProperty(value = "newTitle")
    private String newTitle;
    @JsonProperty(value = "newAbstract")
    private String newAbstract;
    @JsonProperty(value = "newContent")
    private String newContent;


    @JsonProperty(value = "author")
    private JSONObject author = new JSONObject();

    @JsonProperty(value = "createDate")
    private Timestamp createDate;




    @JsonProperty(value = "category")
    private JSONObject category = new JSONObject();
    @JsonProperty(value = "tags")
    private String[] tags;

    @JsonProperty(value = "views")
    private int views;
    @JsonProperty(value = "stars")
    private int stars;
    @JsonProperty(value = "weight")
    private int weight;
    @JsonProperty(value = "titleVoice")
    private String titleVoice;

    @JsonProperty(value = "ifStar")
    private int ifStar;

    @JsonProperty(value = "starTime")
    private Timestamp starTime;


}
