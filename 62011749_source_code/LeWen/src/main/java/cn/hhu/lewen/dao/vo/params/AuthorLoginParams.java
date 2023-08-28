package cn.hhu.lewen.dao.vo.params;

import lombok.Data;

/**
 * @author Fandrew
 */
@Data
public class AuthorLoginParams {
    private int writerId;
    private String writerAccount;
    private String writerPassword;

}
