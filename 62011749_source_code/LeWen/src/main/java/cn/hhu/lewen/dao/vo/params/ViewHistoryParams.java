package cn.hhu.lewen.dao.vo.params;


import lombok.Data;

import java.sql.Timestamp;

/**
 * @author Fandrew
 */
@Data
public class ViewHistoryParams {

    private String userId;
    private String newId;
    private Timestamp viewTime;
    private int viewSeconds;
}
