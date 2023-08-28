import {creatTouchController,CONTROLSTATUS } from "../../utils/touch"
import { readController, contentStart, contentStop, contentReset, initAudioController } from "../../utils/audio.js"
import { getArticleDetailVoice, setStarNews, getVoice, setBrowsingHistory } from "../../utils/request"
import { formatTime } from "../../utils/time"
// pages/articleView/articleView.js
const app = getApp()
Page({
  data: {
    articleData: {type: Object, value: {
      newId: String,	      // 文章唯一标识符
      newTitle: String,	    // 标题
      newAbstract: String,  // 摘要
      newContent: String,   // 文章内容
      author: {             // 作者信息
        writerId: String,
        writerAccount: String,
        nickname: String,
      },
      createDate: String,   // 文章的创建时间
      tags: Array,          // 标签数组
      category: {           // 分类
        categoryId: String,
        categoryName: String
      },
      views: Number,	      // 浏览量
      stars: Number,	      // 收藏量
      weight: Number,       // 推荐度
      titleVoice: String,   // 标题语音文件
      ifStar: Boolean,      // 用户是否收藏文章
    }},
    articleVoice: {type: Object, value: {
      titleVoice: String,   // 标题语音文件
      authorVoice: String,  // 作者
      viewVoice: String,         // 浏览量
      starsVoice: String,        // 收藏量
      newAbstractVoice: String,  // 新闻摘要
      categoryVoice: String,
      tagsVoice: String,
      createDateVoice: String,
      newContentVoice: String
    }},
    controlStatus: null,
    activeId: 0,
    dataList: ["newTitle", "author", "views", "stars", "newAbstract", "category", "tags", "createDate", "newContent"],
    loading: true,
    stopContent: false,
  },

  /* 生命周期函数--监听页面加载 */
  onLoad(options) {
    // 初始化播放器
    initAudioController()
    readController("voice/doubleTapArticle.mp3","control")
    this.setData({loading: true, articleData: app.globalData.articleData, })
    getArticleDetailVoice(app.globalData.articleData).then(values=> {
      var articleVoice = {
        titleVoice: app.globalData.articleData.titleVoice,   // 标题语音文件
      }
      articleVoice.authorVoice = values[0]; articleVoice.viewsVoice = values[1]; articleVoice.starsVoice = values[2];
      articleVoice.newAbstractVoice = values[3]; articleVoice.categoryVoice = values[4]; articleVoice.tagsVoice = values[5];
      articleVoice.createDateVoice = values[6]; articleVoice.newContentVoice = values[7];
      this.setData({
        articleVoice: articleVoice,
        loading: false
      })
      readController("voice/articleView/loadedView.mp3", "control")
      this.singleTap(this.data.dataList[this.data.activeId])
    })
    creatTouchController(this, 'touchEvent', 'controlStatus')
    // 监控 controlStatus 的变化
    app.watch(this, {
      controlStatus: function(newVal) {
        if (newVal == CONTROLSTATUS.left || newVal == CONTROLSTATUS.right) {
          wx.navigateBack({
            success: res=>{
              readController("voice/return.mp3","control")
            }
          })
        } else if (this.data.loading) {
          readController("voice/home/loading.mp3", "control")
        } else if (newVal == CONTROLSTATUS.up) {
          if (this.data.activeId == 0) {
            this.setData({activeId: 0})
          } else {
            this.setData({activeId: this.data.activeId - 1})
          }
        } else if (newVal == CONTROLSTATUS.down) {
          if (this.data.activeId == this.data.dataList.length - 1) {

          } else {
            this.setData({activeId: this.data.activeId + 1})
          }
        } else if (newVal == CONTROLSTATUS.singleTap) {
          this.singleTap(this.data.dataList[this.data.activeId])
        } else if (newVal == CONTROLSTATUS.doubleTap) {
          this.doubleTap(this.data.dataList[this.data.activeId])
        } else if (newVal == CONTROLSTATUS.longTapStart) {
          if (this.data.dataList[this.data.activeId] != "newContent") {
            contentStart(this.data.articleVoice.newContentVoice, 0)
            this.setData({activeId: 8})
          } else {
            contentReset()
          }
        } else if (newVal == CONTROLSTATUS.longTapEnd) {

        } else if (newVal == CONTROLSTATUS.cancel) {

        }
      },
      activeId: function(newVal) {
        wx.pageScrollTo({
          selector: "#" + this.data.dataList[newVal],
          offsetTop: -300,
        })
        this.singleTap(this.data.dataList[newVal])
        if (this.data.dataList[newVal] == "newContent") {
          this.setData({stopContent: true})
        }
      }
    })
  },
  /* 生命周期函数--监听页面初次渲染完成 */
  onReady() {},
  /* 生命周期函数--监听页面显示 */
  onShow() {
    app.globalData.viewStartTime = new Date()
  },
  /* 生命周期函数--监听页面隐藏 */
  onHide() {},
  /* 生命周期函数--监听页面卸载 */
  onUnload() {
    var viewSeconds = (Date.now() - app.globalData.viewStartTime.getTime()) / 1000
    if ( viewSeconds > 30) {
      setBrowsingHistory({
        "newId": this.data.articleData.newId,
        "viewTime": app.globalData.viewStartTime.getTime(),
        "viewSeconds": viewSeconds,
      })
    } else {
      app.globalData.viewStartTime = null
    }
  },
  /* 用户点击右上角分享 */
  onShareAppMessage() {},
  singleTap(item) {
    if (item == 'newTitle') {
      readController(this.data.articleVoice.titleVoice, "voice")
    } else if (item == 'author') {
      readController(this.data.articleVoice.authorVoice, "voice")
    } else if (item == 'views') {
      readController(this.data.articleVoice.viewsVoice, "voice")
    } else if (item == 'stars') {
      readController(this.data.articleVoice.starsVoice, "voice")
    } else if (item == 'newAbstract') {
      readController(this.data.articleVoice.newAbstractVoice, "voice")
    } else if (item == 'category') {
      readController(this.data.articleVoice.categoryVoice, "voice")
    } else if (item == 'tags') {
      readController(this.data.articleVoice.tagsVoice, "voice")
    } else if (item == 'createDate') {
      readController(this.data.articleVoice.createDateVoice, "voice")
    } else if (item == 'newContent') {
      readController("voice/articleView/newContentInfo.mp3", "voice")
    }
  },
  doubleTap(item) {
    if (item == 'newTitle') {

    } else if (item == 'author') {

    } else if (item == 'views') {

    } else if (item == 'stars') {
      var newIfStar = this.data.articleData.ifStar == 1 ? 0 : 1
      setStarNews(this.data.articleData.newId, newIfStar, Date.now()).then(res=>{
        var article = this.data.articleData
        var voice = this.data.articleVoice
        article.ifStar = newIfStar
        if (newIfStar == 1) {
          article.stars = article.stars + 1
          getVoice("收藏量：" + this.data.articleData.stars + "，您已收藏了文章，双击取消收藏").then(res=>{
            voice.starsVoice = res
            this.setData({articleData: article, articleVoice: voice})
            readController("voice/articleView/starTrue.mp3", "control")
          })
        } else {
          article.stars = article.stars - 1
          getVoice("收藏量：" + this.data.articleData.stars + ", 双击收藏文章").then(res=>{
            voice.starsVoice = res
            this.setData({articleData: article, articleVoice: voice})
            readController("voice/articleView/starFalse.mp3", "control")
          })
        }
      })
    } else if (item == 'newAbstract') {

    } else if (item == 'category') {

    } else if (item == 'tags') {

    } else if (item == 'createDate') {

    } else if (item == 'newContent') {
      if (this.data.stopContent) {
        contentStart(this.data.articleVoice.newContentVoice, app.myAudioController.textStartTime)
      } else {
        contentStop()
      }
      this.setData({stopContent: !this.data.stopContent})
    }
  }
})