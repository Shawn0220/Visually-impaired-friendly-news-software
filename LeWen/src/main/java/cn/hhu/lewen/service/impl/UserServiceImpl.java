package cn.hhu.lewen.service.impl;


import cn.hhu.lewen.dao.mapper.UserMapper;
import cn.hhu.lewen.dao.pojo.User;
import cn.hhu.lewen.dao.vo.Result;
import cn.hhu.lewen.dao.vo.UserVo;
import cn.hhu.lewen.dao.vo.params.AuthorLoginParams;
import cn.hhu.lewen.dao.vo.params.UserParams;
import cn.hhu.lewen.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service("UserService")
public class UserServiceImpl implements UserService {
    @Autowired
    private UserMapper userMapper;


    @Override
    public int authorLogin(AuthorLoginParams authorLoginParams) {
        int flag =  userMapper.authorLogin(authorLoginParams);
        int writerId = userMapper.getAuthorId(authorLoginParams.getWriterAccount());

        return writerId;
    }

    @Override
    public Result getUserInfoByUserId(UserParams userParams) {

        User user =  userMapper.getUserInfoByUserId(userParams.getUserId());

        UserVo userVo = copyUser(user);


        return Result.success(userVo);
    }

    @Override
    public void setUserInfoByUserId(UserParams userParams) {
        User user = copyUserParams(userParams);

        userMapper.setUserInfoByUserId(user);

        System.out.println("userParams"+userParams);
        System.out.println("user"+user);


    }

    @Override
    public int isExist(String userAccount){

        return userMapper.isExist(userAccount);
    }

    @Override
    public String login(String userAccount) {
        if (userMapper.isExist(userAccount)==1){
            return getUserIdByUserAccount(userAccount);
        }else{
            userMapper.login(userAccount);
            return getUserIdByUserAccount(userAccount);
        }

    }

    @Override
    public String getUserIdByUserAccount(String userAccount) {


        return userMapper.getUserIdByUserAccount(userAccount);
    }


    public UserVo copyUser(User user){
        UserVo userVo = new UserVo();
        userVo.setUserId(String.valueOf(user.getUserId()));//类型转换
        userVo.setUserPassword(user.getUserPassword());
        userVo.setNickname(user.getNickname());
//        userVo.setUserAge(Integer.parseInt( user.getUserAge()));//类型转换
        userVo.setUserAge( user.getUserAge());
        userVo.setUserSex(user.getUserSex());
        userVo.setUserTel(user.getUserTel());
        userVo.setUserProvince(user.getUserProvince());
        userVo.setUserCity(user.getUserCity());
        userVo.setUserMail(user.getUserMail());

        return userVo;


    }

    public User copyUserParams(UserParams userParams){
        User user = new User();
        user.setUserId(Integer.parseInt(userParams.getUserId()));
        user.setNickname(userParams.getNickname());
        user.setUserAge(userParams.getUserAge());
        user.setUserSex(userParams.getUserSex());
        user.setUserTel(userParams.getUserTel());
        user.setUserProvince(userParams.getUserProvince());
        user.setUserCity(userParams.getUserCity());
        user.setUserMail(userParams.getUserMail());
        user.setUserPassword(userParams.getUserPassword());

        return user;




    }
}
