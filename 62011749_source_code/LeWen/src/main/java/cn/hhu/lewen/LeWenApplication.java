package cn.hhu.lewen;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;

/**
 * @author Fandrew
 */
@SpringBootApplication
@MapperScan(basePackages = "cn.hhu.lewen.dao.mapper")
public class LeWenApplication extends SpringBootServletInitializer {

    public static void main(String[] args) {
        SpringApplication.run(LeWenApplication.class, args);
    }

//    @Override
//    protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
//        return application.sources(LeWenApplication.class);
//    }
}
