package cn.hhu.lewen.dao.pojo;

import lombok.Data;

/**
 * @author Fandrew
 */
@Data
public class User {

    private int userId;

    private String userAccount="*****";

    private String userPassword;

    private String nickname;

    private int userAge;

    private int userSex;

    private String userTel;

    private String userProvince;

    private String userCity;

    private String userMail;

}
