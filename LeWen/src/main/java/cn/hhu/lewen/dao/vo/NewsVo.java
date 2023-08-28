package cn.hhu.lewen.dao.vo;

import com.alibaba.fastjson.JSONObject;
import com.alibaba.fastjson.annotation.JSONType;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import java.sql.Timestamp;

/*
*
* 文章内容
newId	Number	"2"
newTitle	String	"全球知名中文IT技术交流平台CSDN"
newAbstract	String	"全球知名中文IT技术交流平台CSDN"
newContent	String	"全球知名中文IT技术交流平台CSDN"
author	Json	{"writerId": "1", "writerAccount": "1141207643", "nickname": "王子潇"}
createData	String	"2009-06-26 15:58"
tags	Array	["政治", "财经", "文化", "社会"]
category	Json	{"categoryId": "1", "categoryName": "社会", }
views	Number	520
stars	Number	520
weight	0/1	权重的范围需要确定一下
titleVoice	String	一个带头部的base64字符串
ifStar	boolean
*
*
* */

/**
 * @author Fandrew
 */
@Data
@JSONType(orders={"newId","newTitle","newAbstract","newContent","author","createDate",
        "tags","category", "views","stars","weight","titleVoice","ifStar","viewTime"})
public class NewsVo {

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




}
