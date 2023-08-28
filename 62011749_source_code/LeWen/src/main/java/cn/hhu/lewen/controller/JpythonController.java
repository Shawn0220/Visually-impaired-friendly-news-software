package cn.hhu.lewen.controller;

import cn.hhu.lewen.dao.vo.Result;
import cn.hhu.lewen.dao.vo.params.PhotoParams;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import org.springframework.boot.configurationprocessor.json.JSONException;
import org.springframework.web.bind.annotation.*;

//json数据进行交互
//java -> python   package
//要先导入jPython的包 网上搜一下

// 要保证环境变量中的python解释器拥有所需的包 sklearn




// my host: 10.6.138.233

/**
 * @author Fandrew
 * @RequestMapping() 括号内是访问的地址
 */
@CrossOrigin(origins = "*")
@RestController
@RequestMapping("")
public class JpythonController {

    @GetMapping("/jpython")
    public Result calljpy(){
        return Result.success("jpython called");
    }

    //------------------------------------------------------------------------------------------------------------------------------------------
    //下面是调用python的

    /**
     * 文本转语音
     * @param text
     * @return
     */
    @PostMapping("/api/text2voice")
    public Result text2voice(@RequestBody String text){
        JSONObject jsonObject = JSON.parseObject(text);
        text = (String)jsonObject.get("text");
        JSONObject data = Python.text2voice(text);
        return Result.success(data);
    }

    /**
     * 图片转语音 not used
     * @param text
     * @return
     */
    @PostMapping("/pic2voice")
    public Result picTobase64Tovoice(@RequestBody String text){
        JSONObject jsonObject = JSON.parseObject(text);
        text = (String)jsonObject.get("text");

        JSONObject data = Python.text2voice(text);
        int flag = 0;
        for(int i=1; i<=3; i++){
            data = Python.text2voice(text);
            if (data == null){
                continue;
            }else{
                flag = 1;
                break;
            }
        }
        if (flag==0){
            return Result.fail(500,"error");
        }
        return Result.success(data.getString("voice"));
    }


    @PostMapping("/photo2voice")
    public Result photo2voice(@RequestBody PhotoParams photoParams){
        System.out.println(photoParams);
        String imgbase64 = photoParams.getPhotoData();
        JSONObject textJson = Python.img2text(imgbase64);
        System.out.println("textJson is : "+textJson);
        String text = textJson.getString("text");

        JSONObject voiceJson = Python.text2voice(text);
        System.out.println("voiceJson is: "+voiceJson);
        String voice = voiceJson.getString("voice");

        JSONObject dataJson = new JSONObject();
        dataJson.put("text",text);
        dataJson.put("voice",voice);
        System.out.println("dataJson is: "+dataJson);

        return Result.success(dataJson);
    }


    @PostMapping("/photo2identify")
    public Result photo2identity(@RequestBody PhotoParams photoParams){

        String imgbase64 = photoParams.getPhotoData();
        JSONObject textandclassesJson = Python.img2textandclasses(imgbase64);
        JSONObject dataJson = new JSONObject();
        dataJson.put("text",textandclassesJson.getString("text"));
        dataJson.put("voice",textandclassesJson.getString("classes"));
        System.out.println(dataJson);

        return Result.success(dataJson);
    }

    @PostMapping("/api/text2category")
    public Result text2category(@RequestBody String text){
        JSONObject jsonObject =  Python.newsClassify(text);
        JSONObject categoryJson = new JSONObject();
        categoryJson.put("categoryName",jsonObject.getString("class"));

        String categoryName = jsonObject.getString("class");
        String[] allCategory = new String[]{"财经","体育","军事","游戏","教育","汽车","房产","科技","娱乐","其他"};
        int index=0;
        for (int i=0; i<allCategory.length; i++){
            if (categoryName.equals(allCategory[i])) {
                index = i+1;
            };
        }

        categoryJson.put("categoryId",index);
        System.out.println(categoryJson);
        return Result.success(categoryJson);
    }

    @PostMapping("/api/text2tags")
    public Result text2tags(@RequestBody String text){
        JSONObject jsonObject =  Python.newsEntities(text);
        String entities = jsonObject.getString("entities");

        //删去空格和引号
        String entitiesString = entities.replace("[","");
        entitiesString = entitiesString.replace("]","");
        entitiesString = entitiesString.replace("'","");
        entitiesString = entitiesString.replace(" ","");

        String[] entityArray = entitiesString.split(",");

        jsonObject.put("tags",entityArray);
        System.out.println(jsonObject);
        return Result.success(jsonObject);
    }
}
