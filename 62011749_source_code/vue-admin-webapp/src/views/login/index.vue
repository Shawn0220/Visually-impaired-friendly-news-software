<template>
  <div class="login">
    <div class="loginBox">
      <h2 class="loginH2"><strong>乐闻</strong> 后台管理系统 - 作者端</h2>
      <div class="loginCon">
        <div class="titleDiv">
          <h3>Sign up now</h3>
          <p>Enter your username and password to log on:</p>
          <i class="el-icon-key"></i>
        </div>
        <el-form ref="loginForm" :rules="rules" :model="ruleForm">
          <el-form-item prop="writerAccount">
            <el-input placeholder="请输入账号" prefix-icon="el-icon-writerAccount" v-model="ruleForm.writerAccount"></el-input>
          </el-form-item>
          <el-form-item prop="writerPassword">
            <el-input placeholder="请输入密码" prefix-icon="el-icon-lock" v-model="ruleForm.writerPassword" show-password></el-input>
          </el-form-item>
          <el-button type="primary" class="loginBtn" @click="loginLw('loginForm')">登录</el-button>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
import SlideVerify from '@/components/SlideVerify'
import {getlogin} from "../../api/utils";
import  {Message} from "element-ui";
import Vue from "vue";
export default {
  data() {
    return {
      notifyObj: null,
      text: '向右滑动',
      ruleForm: {
        writerAccount: '',
        writerPassword: ''
      },
      rules: {
        writerAccount: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
        ],
        writerPassword: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      }
    }
  },
  mounted() {
    this.shopTip()
  },
  methods: {
    refresh() {
      this.$refs.slideDiv.reset()
    },
    loginLw(form) {
      let that = this;
      this.$store.dispatch('user/_login', {user:'admin',password:'123456'})
      getlogin(this.ruleForm).then(res => {
        if (!res.data.data.writerId) {
          Message.error("登录失败！");
          that.refresh();
        } else {
          Vue.prototype.$writerId = res.data.data.writerId;
          that.$router.push('/');
          Message.success("登录成功！");
          if (that.notifyObj) {
            that.notifyObj.close()
          }
          that.notifyObj = null
        }
      }).catch(error => {
        that.refresh();
        Message.error("登录失败！");
      })
    },
    shopTip() {
      this.notifyObj = this.$notify({
        title: '提示',
        message:
          '可用作者账号为：admin,密码为：123456',
        iconClass: 'el-icon-s-opportunity'
      })
    }
  },
  components: {
    SlideVerify
  }
}
</script>
<style scoped lang="scss">
.login {
  height: 100%;
  width: 100%;
  background: url(../../assets/pageBg/loginBg.jpg) no-repeat center center;
  background-size: 100% 100%;
  overflow: hidden;
}
.loginBox {
  height: 455px;
  width: 550px;
  margin: 0 auto;
  position: relative;
  top: 50%;
  margin-top: -287px;
}
.loginH2 {
  font-size: 38px;
  color: #fff;
  text-align: center;
}
.loginCon {
  margin-top: 30px;
  background: #eee;
  border-radius: 4px;
  .titleDiv {
    padding: 0 28px;
    background: #fff;
    position: relative;
    height: 120px;
    border-radius: 4px 4px 0 0;
    h3 {
      font-size: 22px;
      color: #555;
      font-weight: initial;
      padding-top: 23px;
    }
    p {
      font-size: 16px;
      color: #888;
      padding-top: 12px;
    }
    i {
      font-size: 65px;
      color: #ddd;
      position: absolute;
      right: 27px;
      top: 29px;
    }
  }
  .el-form {
    padding: 25px 25px 30px 25px;
    background: #eee;
    border-radius: 0 0 4px 4px;
  }
}
.loginBtn {
  width: 100%;
  background: #19b9e7;
}
.slideShadow {
  position: fixed;
  z-index: 999;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
}
.slideSty {
  position: absolute;
  width: 380px;
  height: 311px;
  background: #e8e8e8;
  border: 1px solid #dcdcdc;
  left: 50%;
  top: 50%;
  margin-left: -188px;
  margin-top: -176px;
  z-index: 99;
  border-radius: 5px;
}
.iconBtn {
  padding: 9px 0 0 19px;
  color: #5f5f5f;
  border-top: 1px solid #d8d8d8;
  margin-top: 17px;
  i {
    font-size: 22px;
    cursor: pointer;
  }
  i:last-child {
    margin-left: 7px;
  }
}
</style>
<style>
.slideSty .slide-verify {
  margin: 13px auto 0 auto;
  width: 350px !important;
}
.slideSty .slide-verify-slider {
  width: 100% !important;
}
.slideSty .slide-verify-refresh-icon {
  display: none;
}
</style>
