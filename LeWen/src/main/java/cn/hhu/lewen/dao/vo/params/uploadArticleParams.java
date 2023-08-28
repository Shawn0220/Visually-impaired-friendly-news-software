package cn.hhu.lewen.dao.vo.params;

import lombok.Data;

/**
 * @author Fandrew
 */
@Data
public class uploadArticleParams {



    private String newTitle;

    private String newAbstract;

    private String newContent;

    private int writerId;
    //上传的时候会给



    private int categoryId;
    //上传时用选择框给还是识别？


    private String[] tags;
    //手动可以给
    private String tagsString;



}
