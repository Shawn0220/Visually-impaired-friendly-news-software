<template>
  <div class="className">
    <el-card class="anoCard">
      <el-table :data="tableData" border stripe :header-cell-style="{'text-align':'center'}" :cell-style="{'text-align':'center'}">>
        <el-table-column type="index" label="序号" width="60" sortable></el-table-column>
        <el-table-column prop="newId" label="文章号" width="100" sortable></el-table-column>
        <el-table-column prop="newTitle" label="标题" width="200" sortable></el-table-column>
        <el-table-column prop="newAbstract" label="摘要" width="250" sortable></el-table-column>
        <el-table-column prop="createDate" label="创建时间" width="160" sortable></el-table-column>
        <el-table-column prop="category.categoryName" label="分类" width="80" sortable></el-table-column>
        <el-table-column prop="tags" label="标签" width="170" sortable></el-table-column>
        <el-table-column prop="views" label="浏览量" width="100" sortable></el-table-column>
        <el-table-column prop="stars" label="收藏量" width="100" sortable></el-table-column>
      </el-table>
      <el-pagination background layout="total, sizes, prev, pager, next" :page-sizes="pageSizes" :page-size="pageSize"
        :current-page="currentPage" :total="total" class="fyDiv" @size-change="handleSize" @current-change="handlePage">
      </el-pagination>
    </el-card>
  </div>
</template>

<script>
import {getAuthorArticles} from "../../api/utils";
export default {
  data() {
    return {
      tableData: [],
      allList: [],
      schArr: [],
      currentPage: 1,
      pageSize: 10,
      total: 0,
      pageSizes: [10, 20, 30, 40],
    }
  },
  created() {
    this._getPageTab2()
  },
  methods: {
    handleSize(val) {
      this.pageSize = val;
      this.getPageData()
    },
    handlePage(val) {
      this.currentPage = val;
      this.getPageData()
    },
    _getPageTab2() {
      getAuthorArticles(1, 100).then(res => {
        console.log(res.data.data.data);
        this.allList = res.data.data.data;
        this.schArr = this.allList;
        this.getPageData();
        this.total = res.data.data.data.length;
      })
    },
    getPageData() {
      let start = (this.currentPage - 1) * this.pageSize;
      let end = start + this.pageSize;
      this.tableData = this.schArr.slice(start, end)
    },
  }
}
</script>
<style lang="scss" scoped>
.fyDiv {
  float: right;
  margin-top: 30px;
  padding-bottom: 20px;
}
.anoCard .el-table .el-button {
  padding: 8px 18px;
  font-size: 12px;
}
.searchDiv {
  margin-bottom: 20px;
  .el-button {
    padding: 11px 20px;
  }
}
.width1 {
  width: 180px;
  margin-right: 10px;
}
.diaForm {
  .el-input {
    width: 350px;
  }
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
.diaForm .el-form-item__label {
  padding-right: 20px;
}
.searchDiv [class^='el-icon'] {
  color: #fff;
}
</style>
