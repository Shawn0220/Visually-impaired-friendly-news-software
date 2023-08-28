package cn.hhu.lewen.dao.mapper;

import cn.hhu.lewen.dao.pojo.User;
import cn.hhu.lewen.dao.vo.params.AuthorLoginParams;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;

/**
 * @author Fandrew
 */
@Mapper
public interface UserMapper extends BaseMapper<User> {

    /**
     * 获取用户个人信息
     * @param userId
     * @return
     */
    User getUserInfoByUserId(String userId);

    /**
     * 修改用户个人信息
     * @param user
     */
    void setUserInfoByUserId(User user);

    /**
     * 用户登录
     * @param userAccount
     */
    void login(String userAccount);

    /**
     * 通过用户账号获取用户id
     * @param userAccount
     * @return
     */
    String getUserIdByUserAccount(String userAccount);

    /**
     * 判断用户是否存在
     * @param userAccount
     * @return
     */
    int isExist(String userAccount);

    /**
     * 作者登录
     * @param authorLoginParams
     * @return
     */
    int authorLogin(AuthorLoginParams authorLoginParams);

    /**
     * 通过作者账号获取作者id
     * @param writerAccount
     * @return
     */
    int getAuthorId(String writerAccount);

}
