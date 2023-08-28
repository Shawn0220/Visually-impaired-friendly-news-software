package cn.hhu.lewen.controller;

import cn.hhu.lewen.dao.pojo.ForSearch;
import cn.hhu.lewen.dao.pojo.News;
import cn.hhu.lewen.dao.vo.NewsVo;
import cn.hhu.lewen.dao.vo.Result;
import cn.hhu.lewen.dao.vo.params.*;
import cn.hhu.lewen.service.CategoryService;
import cn.hhu.lewen.service.NewsService;
import cn.hhu.lewen.service.UserService;
import com.alibaba.fastjson.JSONException;
import com.alibaba.fastjson.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.*;
import org.springframework.http.converter.StringHttpMessageConverter;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import javax.servlet.http.HttpServletResponse;
import javax.sound.sampled.UnsupportedAudioFileException;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.text.ParseException;
import java.util.List;

//json数据进行交互
//java -> python   package
//要先导入jPython的包 网上搜一下

// 要保证环境变量中的python解释器拥有所需的包 sklearn




// my host: 10.6.138.233

/**
 * @RequestMapping() 括号内是访问的地址
 */
@CrossOrigin(origins = "*")
@RestController
@RequestMapping("")
public class NewsController {


    @Autowired
    private NewsService newsService;

    @Autowired
    private CategoryService categoryService;
//
    @Autowired
    private UserService userService;

    @Autowired
    private HttpServletResponse response;

    @GetMapping("/test")
    public Result test(){

        return Result.success("test");
    }

    /**
//     * getArticles 获取文章列表
//     * @param pageParams
//     * @return
//     */
    @PostMapping("/new2")
    public Result getArticles(@RequestBody PageParams pageParams){
        response.setHeader("Access-Control-Allow-Origin", "*");

        System.out.println(pageParams);


        System.out.println("getArticles called!!!!");
        return newsService.getArticles(pageParams);
//        return Result.success();
    }

    /**
     * getCategorys  获取所有分类信息
     * @return
     */
    @GetMapping("/categorys")
    public Result getCategorys(){
        System.out.println("getAllCategory used !!");
        Result allCategory = categoryService.getAllCategory();
        return allCategory;
    }

    /**
     * 获取某一分类的具体文章
     * @param pageParams
     * @return
     */
    @PostMapping("/categoryDetails")
    public Result getNewsDetailByCategoryId(@RequestBody PageParams pageParams){

        System.out.println(pageParams);
        System.out.println("getNewsDetailByCategoryId used!!!");

        Result newsDetailByCategoryIdResult = categoryService.getCategoryDetailsByCategoryId(pageParams);

        return newsDetailByCategoryIdResult;
    }


    /**
     * 登录
     * @param loginParams
     * @return
     * @throws JSONException
     */
    @PostMapping("/login")
    public Result login(@RequestBody LoginParams loginParams) throws JSONException {
        String code = loginParams.getCode();
        System.out.println(code);
        //请求地址  GET https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code
        RestTemplate restTemplate = new RestTemplate();
        restTemplate.getMessageConverters().set(1,new StringHttpMessageConverter(StandardCharsets.UTF_8));
        String uri = "https://api.weixin.qq.com/sns/jscode2session?appid=wx9733e30bf9f4d11e&secret=cb8b03be006bb8c9ed888c2151939715&js_code="+code+"&grant_type=authorization_code";
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.parseMediaType("application/json;charset=UTF-8"));
        HttpEntity<String> entity = new HttpEntity<String>(headers);
        ResponseEntity<String> response = restTemplate.exchange(uri, HttpMethod.GET, entity, String.class);
        JSONObject jsonObject = (JSONObject) JSONObject.parse( response.getBody());

        System.out.println(response.getBody());
        String userAccount = jsonObject.getString("openid");
        String userId = userService.login(userAccount);

        System.out.println(userService.getUserIdByUserAccount(userAccount));


        JSONObject jsonObject1 = new JSONObject();
        jsonObject1.put("userId",userId);

        return Result.success(jsonObject1);



    }


    /**
     * 获取用户个人信息
     * @param userParams
     * @return
     */
    @PostMapping("/getUserInfo")
    public Result getUserInfoByUserId(@RequestBody UserParams userParams){
        System.out.println("getUserInfo:"+userParams.getUserId());


        Result userInfoResult =  userService.getUserInfoByUserId(userParams);


        System.out.println(userInfoResult);



        return userInfoResult;
    }

    /**
     * 修改个人信息
     * @param userParams
     * @return
     */
    @PostMapping("/setUserInfo")
    public Result setUserInfoByUserId(@RequestBody UserParams userParams){
        System.out.println(userParams);
        userService.setUserInfoByUserId(userParams);
        return Result.success(getUserInfoByUserId(userParams));
    }

    /**
     * 获取浏览记录
     * @param pageParams
     * @return
     */
    @PostMapping("/getBrowsingHistory")
    public Result getBrowsingHistoryByUserId(@RequestBody PageParams pageParams){


        Result BrowsingHistoryResult = newsService.getBrowsingHistoryByUserId(pageParams);
        System.out.println(BrowsingHistoryResult);

        return BrowsingHistoryResult;
    }

    /**
     * 增加浏览记录
     * @param viewHistoryParams
     * @return
     * @throws ParseException
     */
    @PostMapping("/setBrowsingHistory")
    public Result setBrowsingHistory(@RequestBody ViewHistoryParams viewHistoryParams) throws ParseException {
        System.out.println(viewHistoryParams);

        newsService.addNewViewItem(viewHistoryParams);
        PageParams pageParams = new PageParams();
        pageParams.setPageSize(1);
        pageParams.setPageNumber(10);

        pageParams.setUserId(viewHistoryParams.getUserId());
//        return getBrowsingHistoryByUserId(pageParams);
        return Result.success("setBrowsingHistory done!");
    }


    /**
     * 获取收藏记录
     * @param pageParams
     * @return
     */
    @PostMapping("/getStarNews")
    public Result getStarNewsByUserId(@RequestBody PageParams pageParams){
        System.out.println("getStarNews:"+pageParams);

        System.out.println(pageParams);

        Result StarNewsResult = newsService.getStarNewsByUserId(pageParams);
        System.out.println(StarNewsResult);



        return StarNewsResult;
    }

    /**
     * 增加收藏记录
     * @param ifStarParams
     * @return
     */
    @PostMapping("/setStarNews")
    public Result setStarNewsByUserId(@RequestBody IfStarParams ifStarParams){

        System.out.println(ifStarParams);

        newsService.setStarNews(ifStarParams);
//        System.out.println(StarNewsResult);



        return Result.success("setStarNews");
    }


    /**
     * 通过文本搜索
     * @param searchParams
     * @return
     */
    @PostMapping("/searchByText")
    public Result searchByText(@RequestBody SearchParams searchParams){

        String temp = searchParams.getText();
        System.out.println("in searchByText");
        System.out.println("searchParams is : "+searchParams);
        JSONObject jsonObject =  Python.newsEntities(searchParams.getText());
        /*
         * 用途：对上传的文章进行实体分析，并将实体存进tags
         * */
        System.out.println("jsonobject of newsEntities :"+jsonObject);
        //{"entities":array"}

        String entities = jsonObject.getString("entities");
        entities = entities+","+temp;
        System.out.println("temp is: "+temp);
        System.out.println("entities is : "+entities);
        //删去空格和引号
        String entitiesString = entities.replace("[","");
        entitiesString = entitiesString.replace("]","");
//        System.out.println(entitiesString);
        entitiesString = entitiesString.replace("'","");
        entitiesString = entitiesString.replace(" ","");
        System.out.println("entitiesString is: "+entitiesString);

        //此时得到的entitiesString就是   "fdr,wzx,qx,gsn"  这样的字符串
        //下面利用split将其转换为数组
        //先添加temp
        System.out.println(temp);

        String[] entityArray = entitiesString.split(",");

        //制作一个ForSearch
        ForSearch forSearch = new ForSearch();
        forSearch.setEntities(entityArray);
        forSearch.setUserId(searchParams.getUserId());
        //获取返回的搜索到的文章列表
        List<NewsVo> searchArticles = newsService.searchArticles(forSearch);


        JSONObject dataObject = new JSONObject();
        dataObject.put("data",searchArticles);
        dataObject.put("text",entitiesString);

        String text1 = "正在为您展示"+entitiesString+"的搜索结果";

        System.out.println("搜到的list是"+dataObject.getString("data"));
        System.out.println("text1"+text1);

        JSONObject data = Python.text2voice(text1);

        dataObject.put("voice",data.getString("voice"));



        return Result.success(dataObject);
    }


    /**
     * 通过语音搜索
     * @param searchParams
     * @return
     * @throws UnsupportedAudioFileException
     * @throws IOException
     */
    @PostMapping("/searchByVoice")
    public Result searchByVoice(@RequestBody SearchParams searchParams) throws UnsupportedAudioFileException, IOException {

        //把语音转为文本，然后和文本搜索一致
        System.out.println("searchParams is :"+searchParams.getVoice());
        JSONObject textObject =  Python.voice2text(searchParams.getVoice());
//        String temp = "audio/mpeg:base64,GkXfo59ChoEBQveBAULygQRC84?????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";

        searchParams.setText( textObject.getString("text"));


        JSONObject jsonObject =  Python.newsEntities(searchParams.getText());
        /*
         * 用途：对上传的文章进行实体分析，并将实体存进tags
         * */
        System.out.println("this jsonobject is :"+jsonObject);
        //{"entities":array"}
        String entities = jsonObject.getString("entities");
//        System.out.println("entitiesArray:"+entities);
        String entitiesString = entities.replace("[","");
        entitiesString = entitiesString.replace("]","");
//        System.out.println(entitiesString);
        entitiesString = entitiesString.replace("'","");
        entitiesString = entitiesString.replace(" ","");
        System.out.println(entitiesString);

        //此时得到的entitiesString就是   "fdr,wzx,qx,gsn"  这样的字符串
        //下面利用split将其转换为数组
        String[] entityArray = entitiesString.split(",");

        //制作一个ForSearch
        ForSearch forSearch = new ForSearch();
        forSearch.setEntities(entityArray);
        forSearch.setUserId(searchParams.getUserId());
        //获取返回的搜索到的文章列表
        List<NewsVo> searchArticles = newsService.searchArticles(forSearch);


        JSONObject dataObject = new JSONObject();
        dataObject.put("data",searchArticles);
        dataObject.put("text",entitiesString);

        String text1 = "正在为您展示"+entitiesString+"的搜索结果";
        System.out.println("text1 :"+text1);

        JSONObject data = Python.text2voice(text1);

        dataObject.put("voice",data.getString("voice"));



        return Result.success(dataObject);
    }


    /**
     * 语音输入转为文本
     * @param searchParams
     * @return
     * @throws UnsupportedAudioFileException
     * @throws IOException
     */
    @PostMapping("/voice2text")
    public Result voice2text(@RequestBody SearchParams searchParams) throws UnsupportedAudioFileException, IOException {

        //把语音转为文本，然后和文本搜索一致
        System.out.println("searchParams is :"+searchParams.getVoice());
        JSONObject textObject =  Python.voice2text(searchParams.getVoice());
//        String temp = "audio/mpeg:base64,GkXfo59ChoEBQveBAULygQRC84?????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";

        searchParams.setText( textObject.getString("text"));



        JSONObject dataObject = new JSONObject();

        dataObject.put("text",searchParams.getText());


        System.out.println("voice2text datajson :"+dataObject);


        return Result.success(dataObject);
    }

    /**
     * 获取该作者的文章被浏览、收藏等数据  总量
     * @param jsonObject
     * @return
     */
    @PostMapping("/api/authorPreview")
    public Result getAuthorPreviewByWriterId(@RequestBody JSONObject jsonObject){
        String writerId = jsonObject.getString("writerId");

        System.out.println(writerId);
//        System.out.println(newsService.getWriterData(writerId));
        return newsService.getWriterData(Integer.parseInt( writerId));

    }


    /**
     * 获取该作者写的文章
     * @param pageParams
     * @return
     */
    @PostMapping("/api/authorArticles")
    public Result getArticlesByWriterId(@RequestBody PageParams pageParams){


        return newsService.getArticlesByWriterId(pageParams);
    }

    /**
     * 上传文章
     * @param uploadArticleParams
     * @return
     */
    @PostMapping("/api/addNews")
    public Result uploadArticles(@RequestBody uploadArticleParams uploadArticleParams){

        News uploadNew = new News();
        uploadNew.setNewTitle(uploadArticleParams.getNewTitle());
        uploadNew.setNewAbstract(uploadArticleParams.getNewAbstract());
        uploadNew.setNewContent(uploadArticleParams.getNewContent());
        uploadNew.setWriterId(uploadArticleParams.getWriterId());
        uploadNew.setCategoryId(uploadArticleParams.getCategoryId());

        String[] temp = uploadArticleParams.getTags();
        String tagsString = String.join(",",temp);

        uploadArticleParams.setTagsString(tagsString);

        System.out.println("tagsstring: "+tagsString );

        uploadNew.setTags(tagsString);

        System.out.println("uploadNew is"+uploadNew);
//        System.out.println("uploadnew : "+uploadNew);

        //向实体表中添加这个新闻的实体
        //先获取主键
        int newId = newsService.uploadArticles(uploadNew);
        System.out.println("newId is : "+newId);
        //tags数组一个个加进实体识别表中，明天测试！！！

        for (String s : temp) {
            newsService.insertEntity2New(s,String.valueOf(newId));
        }



        return Result.success("upload done");
    }

    /**
     * 作者登录服务端
     * @param authorLoginParams
     * @return
     */
    @PostMapping("/api/authorLogin")
    public Result authorLogin(@RequestBody AuthorLoginParams authorLoginParams){

        System.out.println(authorLoginParams);
        int writerId =  userService.authorLogin(authorLoginParams);

        System.out.println("writerId:"+writerId);
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("writerId",writerId);

        return Result.success(jsonObject);
    }


    /**
     * 按月获取作者数据
     * @param authorLoginParams
     * @return
     */
    @PostMapping("/api/authorMonthData")
    public Result getAuthorMonthData(@RequestBody AuthorLoginParams authorLoginParams){
        JSONObject jsonObject = newsService.getAuthorMonthData(authorLoginParams.getWriterId());
        System.out.println("authorMonthData:"+jsonObject);
        return Result.success(jsonObject);
    }





}
