package cn.hhu.lewen.service;


//import org.python.antlr.ast.Str;

import cn.hhu.lewen.dao.vo.Result;
import cn.hhu.lewen.dao.vo.params.AuthorLoginParams;
import cn.hhu.lewen.dao.vo.params.UserParams;
import org.springframework.stereotype.Service;

/**
 * @author Fandrew
 */
public interface UserService {

    /**
     * 获取用户信息
     * @param userParams
     * @return
     */
    Result getUserInfoByUserId(UserParams userParams);

    /**
     * 设置/修改用户信息
     * @param userParams
     */
    void setUserInfoByUserId(UserParams userParams);

    /**
     * 用户登录
     * @param userAccount
     * @return
     */
    String login(String userAccount);

    /**
     * 通过用户账号获取它的ID
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
}
