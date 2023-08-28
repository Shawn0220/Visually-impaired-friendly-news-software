<template>
  <div class="className">
    <el-card class="anoCard">
      <el-form class="input-form" ref="input-form" :model="newData" :rules="rules" label-position="right" label-width="150px">
        <el-form-item prop="newTitle" class="newTitle">
          <label slot="label" class="label-text"> 新闻标题： </label>
          <el-input class="title-input" maxlength="50" v-model="newData.newTitle" show-word-limit clearable
                    placeholder="请输入新闻标题..." type="text"/>
          <el-button type="primary" size="small" class="my-button" @click="getTitleVoice()" :loading="titleLoading">试听标题语音</el-button>
        </el-form-item>
        <el-form-item prop="newAbstract">
          <label slot="label" class="label-text"> 新闻摘要： </label>
          <el-input class="abstract-input" maxlength="100" v-model="newData.newAbstract" show-word-limit clearable
                    placeholder="请输入新闻摘要..." type="textarea" rows="3" resize="none"/>
          <el-button type="primary" size="small" class="my-button" @click="getAbstractVoice()" :loading="abstractLoading">试听摘要语音</el-button>
        </el-form-item>
        <el-form-item prop="newContent">
          <label slot="label" class="label-text"> 新闻内容： </label>
          <el-input class="content-input" v-model="newData.newContent" show-word-limit clearable
                    placeholder="请输入新闻内容..." type="textarea" :autosize="{minRows:6 }" resize="none"/>
          <el-button type="primary" size="small" class="my-button" @click="getContentVoice()" :loading="contentLoading">试听内容语音</el-button>
        </el-form-item>
        <el-form-item prop="category">
          <label slot="label" class="label-text"> 所属分类： </label>
          <el-tag class="my-tags" type="success" effect="dark" style="margin-left: 1%">{{ newData.category.categoryName ? newData.category.categoryName: '请获取' }}</el-tag>
          <el-button type="primary" size="small" class="my-button" @click="getTheCategory()" :loading="categoryLoading">获取所属分类</el-button>
        </el-form-item>
        <el-form-item prop="tags">
          <label slot="label" class="label-text"> 所属标签： </label>
          <el-tag class="my-tags" type="success" closable effect="dark" style="margin-left: 1%" v-for="(item, index) in newData.tags" @close="removeTags(index)"> {{ item }} </el-tag>
          <el-input class="input-new-tag" v-if="inputVisible" v-model="inputValue" ref="saveTagInput" size="small" @keyup.enter.native="handleInputConfirm" @blur="handleInputConfirm">
          </el-input>
          <el-button v-else class="button-new-tag" size="small" @click="showInput">+ 自定义标签</el-button>
        </el-form-item>
        <el-form-item prop="getTags">
          <label slot="label" class="label-text"> 推荐标签： </label>
          <el-tag class="my-tags" type="success" effect="dark" style="margin-left: 1%" v-for="(item, index) in getTags" @click="addTags(index)"> {{ item }} </el-tag>
          <el-button type="primary" size="small" class="my-button" @click="getTheTags()" :loading="tagsLoading">识别推荐标签</el-button>
        </el-form-item>
      </el-form>
      <div class="submit-button">
        <el-button type="warning" @click="onSubmit()">发布新闻</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
  import {getVoice, getCategory, getTags, addNews} from "../../api/utils";

export default {
  data() {
    return {
      titleLoading: false,
      abstractLoading: false,
      contentLoading: false,
      categoryLoading: false,
      tagsLoading: false,
      inputVisible: false,
      inputValue: '',
      getTags: [],
      newData: {
        newTitle: null,
        newAbstract: null,
        newContent: null,
        category: {
          categoryId: null,
          categoryName: null,
        },
        tags: [],
      },
      rules: {
        newTitle: [
          {required: true, message: '请输入文章标题...', trigger: 'blur'},
          {max: 50, message: '不能大于50个字符!', trigger: 'blur'},
        ],
        newAbstract: [
          {required: true, message: '请输入文章摘要...', trigger: 'blur'},
          {max: 100, message: '不能大于100个字符!', trigger: 'blur'},
        ],
        newContent: [
          {required: true, message: '请输入文章内容...', trigger: 'blur'},
        ]
      }
    }
  },
  created() {},
  filters: {},
  methods: {
    getTitleVoice() {
      if (this.newData.newTitle) {
        this.titleLoading = true;
        getVoice("文章标题：" + this.newData.newTitle).then(res=> {
          this.audioRead(res.data.data.voice);
          this.titleLoading = false;
        })
      } else {
        this.$notify({
          title: '提示',
          message: '获取语音需要您先输入文字',
          iconClass: 'el-icon-s-opportunity'
        })
      }
    },
    getAbstractVoice() {
      if (this.newData.newAbstract) {
        this.abstractLoading = true;
        getVoice("文章摘要：" + this.newData.newAbstract).then(res=> {
          this.audioRead(res.data.data.voice);
          this.abstractLoading = false;
        })
      } else {
        this.$notify({
          title: '提示',
          message: '获取语音需要您先输入文字',
          iconClass: 'el-icon-s-opportunity'
        })
      }
    },
    getContentVoice() {
      if (this.newData.newContent) {
        this.contentLoading = true;
        getVoice("文章内容：" + this.newData.newContent).then(res=> {
          this.audioRead(res.data.data.voice);
          this.contentLoading = false;
        })
      } else {
        this.$notify({
          title: '提示',
          message: '获取语音需要您先输入文字',
          iconClass: 'el-icon-s-opportunity'
        })
      }
    },
    getTheCategory() {
      if (this.newData.newContent) {
        this.categoryLoading = true;
        getCategory(this.newData.newContent.split().join('')).then(res=> {
          this.newData.category = res.data.data;
          this.categoryLoading = false;
        })
      } else {
        this.$notify({
          title: '提示',
          message: '获取分类需要您先输入新闻内容',
          iconClass: 'el-icon-s-opportunity'
        })
      }
    },
    getTheTags() {
      if (this.newData.newTitle || this.newData.newContent || this.newData.newAbstract) {
        this.tagsLoading = true;
        const text = (this.newData.newTitle + this.newData.newAbstract + this.newData.newContent).split().join('');
        getTags(text).then(res=> {
          this.getTags = res.data.data.tags;
          this.tagsLoading = false;
        })
      } else {
        this.$notify({
          title: '提示',
          message: '获取标签需要您先输入文字',
          iconClass: 'el-icon-s-opportunity'
        })
      }
    },
    addTags(index) {
      if (!this.newData.tags.includes(this.getTags[index])) {
        this.newData.tags.push(this.getTags[index])
      }
    },
    removeTags(index) {
      this.newData.tags.splice(index, 1)
    },
    showInput() {
      this.inputVisible = true;
      this.$nextTick(_ => {
        this.$refs.saveTagInput.$refs.input.focus();
      });
    },
    handleInputConfirm() {
      if (this.inputValue) {
        this.newData.tags.push(this.inputValue);
      }
      this.inputVisible = false;
      this.inputValue = '';
    },
    onSubmit() {
      if (!this.newData.category) {
        this.$notify({
          title: '提示',
          message: '请获取所属分类后再发布文章',
          iconClass: 'el-icon-s-opportunity'
        });
        return;
      } else if (this.newData.tags.length === 0) {
        this.$notify({
          title: '提示',
          message: '请设置文章标签后再发布文章',
          iconClass: 'el-icon-s-opportunity'
        });
        return;
      }
      for (let i = 0; i < this.getTags.length; i++) {
        if (!this.newData.tags.includes(this.getTags[i])) {
          this.newData.tags.push(this.getTags[i])
        }
      }
      let that = this;
      this.$refs['input-form'].validate((valid) => {
          if (valid) {
          addNews(that.newData).then(res => {
            that.$notify({
              title: '提示',
              message: '发布成功！',
              iconClass: 'el-icon-s-opportunity'
            })
          });
            that.$refs['input-form'].resetFields();
            that.getTags = [];
        } else {
          return false;
        }
      });
    }
  }
}
</script>

<style scoped>
  .anoCard{
    padding: 8px 18px;
    font-size: 12px;
  }
  .label-text {
    font-size: 20px;
    font-weight: bold;
    width: 300px;
  }
  .newTitle >>> .el-input__inner {
    height: 60px;
  }
  .title-input {
    width: 800px;
    margin-left: 1%;
    font-size: 30px;
    font-weight: bold;
  }
  .abstract-input {
    width: 500px;
    margin-left: 1%;
    white-space:pre-line;
  }
  .content-input {
    width: 500px;
    margin-left: 1%;
    white-space:pre-line;
  }
  .my-button {
    margin-left: 2%;
  }
  .my-tags {
    margin-left: 1%;
  }
  .submit-button {
    width: 100%;
    display: flex;
    justify-content: center;
  }
  .button-new-tag {
    margin-left: 1%;
    height: 32px;
    line-height: 30px;
    padding-top: 0;
    padding-bottom: 0;
  }
  .input-new-tag {
    width: 90px;
    margin-left: 1%;
    vertical-align: bottom;
  }
</style>
<style lang="scss">
  .anoCard {
    .el-card__body:after {
      content: '';
      clear: both;
      width: 0;
      height: 0;
      visibility: hidden;
      display: block;
    }
  }
</style>
