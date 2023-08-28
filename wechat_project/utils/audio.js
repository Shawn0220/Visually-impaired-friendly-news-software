const app = getApp()

const base_url = 'http://eos-wuxi-1.cmecloud.cn/spencer/'

export function readController(src, type) {
  if (app.myAudioController.audioTypeOnread == "content") {
    contentStop()
  }
  if (type == "control") {
    initAudioController()
    app.myAudioController.audio.onEnded(()=>{
      app.myAudioController.audioTypeOnread = "voice"
    })
    if (src.indexOf('voice') != -1) {
      app.myAudioController.audio.src = base_url + src;
    } else {
      app.myAudioController.audio.src = src;
    }
    app.myAudioController.audio.play();
    app.myAudioController.audioTypeOnread = "control";
  } else if (app.myAudioController.audioTypeOnread == "control") {
    app.myAudioController.nextAudioSrc = src;
    app.myAudioController.audio.onEnded(()=>{
      app.myAudioController.audio.offEnded(()=>{})
      if (src.indexOf('voice') != -1) {
        app.myAudioController.audio.src = base_url + app.myAudioController.nextAudioSrc;
      } else {
        app.myAudioController.audio.src = app.myAudioController.nextAudioSrc;
      }
      app.myAudioController.audio.play();
      app.myAudioController.audioTypeOnread = "voice";
    })
  } else {
    if (src.indexOf('voice') != -1) {
      app.myAudioController.audio.src = base_url + src;
    } else {
      app.myAudioController.audio.src = src;
    }
    app.myAudioController.audio.play();
    app.myAudioController.audioTypeOnread = "voice";
  }
  // app.globalData.myAudio.();
  // console.log(app.globalData.myAudio.src)
}

export function contentStart(src, time) {
  app.myAudioController.audio.onEnded(()=>{
    app.myAudioController.audioTypeOnread = "voice"
  })
  if (src.indexOf('voice') != -1) {
    app.myAudioController.audio.src = base_url + src;
  } else {
    app.myAudioController.audio.src = src;
  }
  if (time) {
    app.myAudioController.audio.seek(time)
  }
  app.myAudioController.audio.play()
  app.myAudioController.audioTypeOnread = "content"
}

export function contentStop() {
  app.myAudioController.audio.pause()
  app.myAudioController.audioTypeOnread = "voice"
  app.myAudioController.textStartTime = app.myAudioController.audio.currentTime
}

export function contentReset() {
  app.myAudioController.audio.onEnded(()=>{
    app.myAudioController.audioTypeOnread = "voice"
  })
  app.myAudioController.audio.seek(0)
  app.myAudioController.audio.play()
  app.myAudioController.audioTypeOnread = "content"
}

export function initAudioController() {
  app.myAudioController.audio.destroy()
  app.myAudioController.audio = wx.createInnerAudioContext()
}

