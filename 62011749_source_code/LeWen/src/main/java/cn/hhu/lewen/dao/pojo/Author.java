package cn.hhu.lewen.dao.pojo;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import lombok.Data;
import org.springframework.stereotype.Component;

/**
 * @author Fandrew
 */
@Data
public class Author {
    @TableId(value = "writer_id", type = IdType.AUTO)

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
