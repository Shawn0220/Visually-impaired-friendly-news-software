package cn.hhu.lewen.dao.vo.params;


import lombok.Data;

import java.sql.Timestamp;

/**
 * @author Fandrew
 */
@Data
public class IfStarParams {

    private String userId;
    private String newId;
    private int ifStar;
    private Timestamp starTime;
}
