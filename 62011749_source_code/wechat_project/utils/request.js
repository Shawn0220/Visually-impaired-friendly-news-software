var address = 'http://36.134.148.183:38888';

export function toJSON(str) {
  if (typeof str == "String") {
    try {
      str = JSON.parse(str)
    } catch (error) {
      console.log(error)
    }
  }
  return str
}
export function getArticles(pageNumber, pageSize) {
  var res = new Promise((resolve,reject)=>{
    wx.request({
      url: address + '/new2',
      method: 'POST',
      data: {
        pageNumber: pageNumber,
        pageSize: pageSize,
        userId: getApp().globalData.userId,
      },
      header: {
        "content-type":"application/json",
      },
      success: res=> {
        var response = toJSON(res.data.data)
        for(let index = 0; index < response.data.length; index++) {
          if (response.data[index].titleVoice) {
            var codeWav = wx.env.USER_DATA_PATH + '/' + new Date().getTime() + index + '.wav';
            wx.getFileSystemManager().writeFileSync(
              codeWav,
              response.data[index].titleVoice.replace("data:audio/wav;base64,", ""),
              'base64');
            response.data[index].titleVoice = codeWav
          }
        }
        console.log(response)
        resolve(response)
      },
      fail: err=> {
        reject(err.errMsg || "failed!")
      }
    })
  }).catch((e) => {})
  return res
}
export function getVoice(text) {
  return new Promise((resolve,reject)=>{
    wx.request({
      url: address + '/text2voice',
      method: 'POST',
      data: {
        text: text.slice(0, 290),
      },
      header: {
        "content-type":"application/json",
      },
      success: res=> {
        var response = toJSON(res.data.data)
        var codeWav = wx.env.USER_DATA_PATH + '/' + new Date().getTime() + '.wav';
        wx.getFileSystemManager().writeFile({
          filePath: codeWav,
          data: response.voice.replace("data:audio/wav;base64,", ""),
          encoding: 'base64',
          success: (res) => {
            resolve(codeWav)
        }});
      },
      fail: err=> {
        reject(err.errMsg || "failed!")
      }
    })
  }).catch((e) => {})
}
// 文章还没有分段
export function getArticleDetailVoice(articleData) {
  var authorVoice = getVoice("作者：" + articleData.author.nickname + ",账号：" + articleData.author.writerAccount)
    var viewsVoice = getVoice("浏览量：" + articleData.views)
    if (articleData.ifStar) {
      var starsVoice = getVoice("收藏量：" + articleData.stars + "，您已收藏了文章，双击取消收藏")
    } else {
      var starsVoice = getVoice("收藏量：" + articleData.stars + ",双击收藏文章")
    }
    var newAbstractVoice = getVoice("新闻摘要：" + articleData.newAbstract)
    var categoryVoice = getVoice("所属分类: " + articleData.category.categoryName)
    var tagsText = "所属标签：" 
    articleData.tags.forEach(element => {
      tagsText = tagsText + element + "、"
    });
    var tagsVoice = getVoice(tagsText)
    var createDateVoice = getVoice("新闻创建时间：" + articleData.createDate)
    var newContentVoice = getVoice("新闻内容：" + articleData.newContent)

    return Promise.all([authorVoice, viewsVoice, starsVoice, newAbstractVoice, categoryVoice, tagsVoice, createDateVoice, newContentVoice])
}
export function getCategorys() {
  var res = new Promise((resolve,reject)=>{
    wx.request({
      url: address + '/categorys',
      method: 'GET',
      success: res=> {
        var response = toJSON(res.data.data)
        resolve(response)
      },
      fail: err=> {
        reject(err.errMsg || "failed!")
      }
    })
  }).catch((e) => {})
  return res
}
export function getArticlesByCategory(pageNumber, pageSize, categoryId) {
  var res = new Promise((resolve,reject)=>{
    wx.request({
      url: address + '/categoryDetails',
      method: 'POST',
      data: {
        pageNumber: pageNumber,
        pageSize: pageSize,
        categoryId: categoryId,
        userId: getApp().globalData.userId,
      },
      header: {
        "content-type":"application/json",
      },
      success: res=> {
        var response = toJSON(res.data.data)
        for(let index = 0; index < response.data.length; index++) {
          if (response.data[index].titleVoice) {
            var codeWav = wx.env.USER_DATA_PATH + '/' + new Date().getTime() + index + '.wav';
            wx.getFileSystemManager().writeFileSync(
              codeWav,
              response.data[index].titleVoice.replace("data:audio/wav;base64,", ""),
            'base64');
            response.data[index].titleVoice = codeWav
          }
        }
        resolve(response)
      },
      fail: err=> {
        reject(err.errMsg || "failed!")
      }
    })
  }).catch((e) => {})
  return res
}
export function searchArticlesByVoice(url) {
  // "data:audio/mpeg:base64," + 
  let voice = wx.getFileSystemManager().readFileSync(url, "base64",0)
  console.log(url)
  var res = new Promise((resolve,reject)=>{
  wx.request({
    url: address + '/searchByVoice',
    method: 'POST',
    data: {
      voice: voice,
      userId: getApp().globalData.userId,
    },
    header: {
      "content-type":"application/json",
    },
    success: res=> {
      var response = toJSON(res.data.data)
      for(let index = 0; index < response.data.length; index++) {
        if (response.data[index].titleVoice) {
          var codeWav = wx.env.USER_DATA_PATH + '/' + new Date().getTime() + index + '.wav';
          wx.getFileSystemManager().writeFileSync(
            codeWav,
            response.data[index].titleVoice.replace("data:audio/wav;base64,", ""),
          'base64');
        response.data[index].titleVoice = codeWav
        }
      }
      var codeWav = wx.env.USER_DATA_PATH + '/' + new Date().getTime() + response.data.length + '.wav';
      wx.getFileSystemManager().writeFileSync(
        codeWav,
        response.voice.replace("data:audio/wav;base64,", ""),
        'base64');
      response.voice = codeWav
      resolve(response)
    },
    fail: err=> {
      reject(err.errMsg || "failed!")
    }
  })
 }).catch((e) => {})
 return res
}
export function searchArticlesByText(text) {
  var res = new Promise((resolve,reject)=>{
  wx.request({
    url: address + '/searchByText',
    method: 'POST',
    data: {
      text: text,
      userId: getApp().globalData.userId,
    },
    header: {
      "content-type":"application/json",
    },
    success: res=> {
      console.log(res)
      var response = toJSON(res.data.data)
      for(let index = 0; index < response.data.length; index++) {
        if (response.data[index].titleVoice) {
          var codeWav = wx.env.USER_DATA_PATH + '/' + new Date().getTime() + index + '.wav';
          wx.getFileSystemManager().writeFileSync(
            codeWav,
            response.data[index].titleVoice.replace("data:audio/wav;base64,", ""),
          'base64');
        response.data[index].titleVoice = codeWav
        }
      }
      var codeWav = wx.env.USER_DATA_PATH + '/' + new Date().getTime() + response.data.length + '.wav';
      wx.getFileSystemManager().writeFileSync(
        codeWav,
        response.voice.replace("data:audio/wav;base64,", ""),
        'base64');
      response.voice = codeWav
      resolve(response)
    },
    fail: err=> {
      reject(err.errMsg || "failed!")
    }
  })
 }).catch((e) => {})
 return res
}
export function getVoiceByPhoto(url) {
  var photoType = url.substring(url.lastIndexOf(".") + 1);
  // "data:image/"+ photoType +";base64," + 
  var photoData = wx.getFileSystemManager().readFileSync(url, "base64")
  return new Promise((resolve,reject)=>{
    wx.request({
      url: address + '/photo2voice',
      method: 'POST',
      data: {
        photoType: photoType,
        photoData: photoData
      },
      header: {
        "content-type":"application/json",
        "userId": getApp().globalData.userId,
      },
      success: res=> {
        var response = toJSON(res.data.data)
        var codeWav = wx.env.USER_DATA_PATH + '/' + new Date().getTime() + '.wav';
          wx.getFileSystemManager().writeFileSync(
            codeWav,
            response.voice.replace("data:audio/wav;base64,", ""),
            'base64');
            response.voice = codeWav
          resolve(response)
      },
      fail: err=> {
        reject(err.errMsg || "failed!")
      }
    })
  }).catch((e) => {})
}
export function getIdentifyByPhoto(url) {
  var photoType = url.substring(url.lastIndexOf(".") + 1);
  // "data:image/"+ photoType +";base64," + 
  var photoData = wx.getFileSystemManager().readFileSync(url, "base64")
  console.log(url)
  return new Promise((resolve,reject)=>{
    wx.request({
      url: address + '/photo2identify',
      method: 'POST',
      data: {
        photoType: photoType,
        photoData: photoData
      },
      header: {
        "content-type":"application/json",
        "userId": getApp().globalData.userId,
      },
      success: res=> {
        console.log(res.data.data)
        var response = toJSON(res.data.data)
        var codeWav = wx.env.USER_DATA_PATH + '/' + new Date().getTime() + '.wav';
          wx.getFileSystemManager().writeFileSync(
            codeWav,
            response.voice.replace("data:audio/wav;base64,", ""),
            'base64');
            response.voice = codeWav
          resolve(response)
      },
      fail: err=> {
        reject(err.errMsg || "failed!")
      }
    })
  }).catch((e) => {})
}
export function getStarNews(pageNumber, pageSize) {
  var res = new Promise((resolve,reject)=>{
    wx.request({
      url: address + '/getStarNews',
      method: 'POST',
      data: {
        userId: getApp().globalData.userId,
        pageSize: pageSize,
        pageNumber: pageNumber,
      },
      header: {
        "content-type":"application/json",
      },
      success: res=> {
        console.log(res)
        var response = toJSON(res.data.data)
        for(let index = 0; index < response.data.length; index++) {
          if (response.data[index].titleVoice) {
            var codeWav = wx.env.USER_DATA_PATH + '/' + new Date().getTime() + index + '.wav';
            wx.getFileSystemManager().writeFileSync(
              codeWav,
              response.data[index].titleVoice.replace("data:audio/wav;base64,", ""),
            'base64');
            response.data[index].titleVoice = codeWav
          }
        }
        resolve(response)
      },
      fail: err=> {
        reject(err.errMsg || "failed!")
      }
    })
  }).catch((e) => {})
  return res
}
export function setStarNews(newId, ifStar, starTime) {
  var res = new Promise((resolve,reject)=>{
    wx.request({
      url: address + '/setStarNews',
      method: 'POST',
      data: {
        userId: getApp().globalData.userId,
        newId,
        ifStar: ifStar ? 1 : 0,
        starTime: starTime,
      },
      header: {
        "content-type":"application/json",
      },
      success: res=> {
        var response = toJSON(res.data.data)
        resolve(response)
      },
      fail: err=> {
        reject(err.errMsg || "failed!")
      }
    })
  }).catch((e) => {})
  return res
}
export function getUserInfo() {
  var res = new Promise((resolve,reject)=>{
    wx.request({
      url: address + '/getUserInfo',
      method: 'POST',
      data: {
        userId: getApp().globalData.userId,
      },
      header: {
        "content-type":"application/json",
      },
      success: res=> {
        var response = toJSON(res.data.data)
        response.userSex = response.userSex == 0 ? '女':'男'
        resolve(response)
      },
      fail: err=> {
        reject(err.errMsg || "failed!")
      }
    })
  }).catch((e) => {})
  return res
}
export function setUserInfo(userInfo) {
  var res = new Promise((resolve,reject)=>{
    wx.request({
      url: address + '/setUserInfo',
      method: 'POST',
      data: {
        userId: getApp().globalData.userId,
        nickname: userInfo.nickname,
        userAge: userInfo.userAge,
        userSex: userInfo.userSex == '女' ? 0 : 1,
        userTel: userInfo.userTel,
        userProvince: userInfo.userProvince,
        userCity: userInfo.userCity,
        userMail: userInfo.userMail,
      },
      header: {
        "content-type":"application/json",
        "userId": getApp().globalData.userId,
      },
      success: res=> {
        var response = toJSON(res.data.data)
        resolve(response)
      },
      fail: err=> {
        reject(err.errMsg || "failed!")
      }
    })
  }).catch((e) => {})
  return res
}
export function getBrowsingHistory(pageNumber, pageSize) {
  var res = new Promise((resolve,reject)=>{
    wx.request({
      url: address + '/getBrowsingHistory',
      method: 'POST',
      data: {
        userId: getApp().globalData.userId,
        pageNumber,
        pageSize,
      },
      header: {
        "content-type":"application/json",
      },
      success: res=> {
        var response = toJSON(res.data.data)
        for(let index = 0; index < response.data.length; index++) {
          if (response.data[index].titleVoice) {
            var codeWav = wx.env.USER_DATA_PATH + '/' + new Date().getTime() + index + '.wav';
            wx.getFileSystemManager().writeFileSync(
              codeWav,
              response.data[index].titleVoice.replace("data:audio/wav;base64,", ""),
            'base64');
            response.data[index].titleVoice = codeWav
          }
        }
        resolve(response)
      },
      fail: err=> {
        reject(err.errMsg || "failed!")
      }
    })
  }).catch((e) => {})
  return res
}
export function setBrowsingHistory(article) {
  var time = Date.now()
  var res = new Promise((resolve,reject)=>{
    wx.request({
      url: address + '/setBrowsingHistory',
      method: 'POST',
      data: {
        userId: getApp().globalData.userId,
        newId: article.newId,
        viewTime: article.viewTime,
        viewSeconds: article.viewSeconds,
      },
      header: {
        "content-type":"application/json",
      },
      success: res=> {
        var response = toJSON(res.data.data)
        resolve(response)
      },
      fail: err=> {
        reject(err.errMsg || "failed!")
      }
    })
  }).catch((e) => {})
  return res
}