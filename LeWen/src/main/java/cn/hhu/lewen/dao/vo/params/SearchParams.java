package cn.hhu.lewen.dao.vo.params;

import lombok.Data;

/**
 * @author Fandrew
 */
@Data
public class SearchParams {

    private String text;
    private String userId;
    private String voice;
    private String nickname;
}
