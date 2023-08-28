package cn.hhu.lewen.dao.vo.params;

import lombok.Data;

/**
 * @author Fandrew
 */
@Data
public class PageParams {

    private int pageNumber;
    private int pageSize ;
    private String categoryId;
    private String userId;
    private String writerId;
    private String[] rmdArray;

}
