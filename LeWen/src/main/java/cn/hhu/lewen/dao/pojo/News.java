package cn.hhu.lewen.dao.pojo;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import lombok.Data;

import java.sql.Timestamp;

/**
 * 对于数据库，这里的约定有个很sb的东西，就是数据库中的下划线他会合并成大写字母，这里我还没找到别的修改方法
 * 例如，数据库中  data_apple  这里必须是  dataApple    反之，你数据库是dataApple，你这里必死无疑。
 *
 *即  数据库中少用驼峰命名
 */

@Data
public class News {

    @TableId(value = "new_id",type = IdType.AUTO)

    private int newId;

    private String newTitle;

    private String newAbstract;

    private String newContent;

    private int writerId;
    private String writerAccount;
    private String nickname;

    private Timestamp createDate;


    private int categoryId;
    private String categoryName;

    private String tags;

    private int views;

    private int stars;

    private int weight;

    private String titleVoice;

    //用于多表查询
    private int ifStar;
    private Timestamp viewTime;
    private Timestamp starTime;

}
