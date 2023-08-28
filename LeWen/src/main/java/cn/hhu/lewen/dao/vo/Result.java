package cn.hhu.lewen.dao.vo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.Getter;
import lombok.Setter;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * @author Fandrew
 */
@Data
@AllArgsConstructor
@Getter
@Setter
public class Result {

    @Autowired
    private boolean success;
    @Autowired
    private int code;
    @Autowired
    private String msg;
    @Autowired
    private Object data;


    public static Result success(Object data){

        return new Result(true,200,"success",data);
    }

    public static Result fail(int code, String msg){
        return new Result(false,code,msg,null);
    }
}
