package cn.hhu.lewen.dao.pojo;

import lombok.Data;

import java.sql.Timestamp;


/**
 * @author Fandrew
 */
@Data

public class StarItem {

    private int userId;
    private int newId;
    private int ifStar;
    private Timestamp starTime;

}
