// app.js
var address = 'http://36.134.148.183:38888';

import { toJSON } from "./utils/request"

App({
  onLaunch() {
    // 登录
    wx.login({
      success (res) {
        // console.log(res.code)
        if (res.code) {
          wx.request({
            url: address + '/login',
            method: 'POST',
            data: {
              code: res.code,
            },
            header: {
              "content-type":"application/json"
            },
            success: res=> {
              var data = toJSON(res.data.data)
              getApp().globalData.userId = data.userId
            },
            fail: err=> {
              console.log(err.errMsg || "failed!")
            }
        })

        } else {
          console.log('登录失败！' + res.errMsg)
        }
      }
    })
  },
  // 设置监听器
  watch: function (ctx, obj) {
    Object.keys(obj).forEach(key => {
      this.observer(ctx.data, key, ctx.data[key], function (value) {
        obj[key].call(ctx, value)
      })
    })
  },
  // 监听属性，并执行监听函数
  observer: function (data, key, val, fn) {
    Object.defineProperty(data, key, {
      configurable: true,
      enumerable: true,
      get: function () {
        return val
      },
      set: function (newVal) {
        fn && fn(newVal)
        val = newVal
      },
    })
  },
  globalData: {
    userId: 1,
    articleData: null,
    categoryData: null,
    browseHistory:[],
    viewStartTime: null,
  },
  myAudioController: {
    audio: wx.createInnerAudioContext(),
    audioTypeOnread: "voice",
    nextAudioSrc: null,
    textStartTime: null
  }
})
