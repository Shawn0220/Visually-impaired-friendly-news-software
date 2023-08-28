package cn.hhu.lewen.dao.vo;

import lombok.Data;

/**
 * @author Fandrew
 */
@Data
public class AuthorVo {

    private int writerId;

    private String writerAccount;

    private String writerPassword;

    private String nickname;

    private int writer_age;

    private int writerSex;

    private String writerTel;

    private String writerProvince;

    private String writerCity;

    private String writerMail;


}
