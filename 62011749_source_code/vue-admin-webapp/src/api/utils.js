// import $axios from './index'
import axios from "axios";
import Vue from 'vue'

const $axios = axios.create({
    // 设置超时时间
    timeout: 30000,
    // 基础url，会在请求url中自动添加前置链接
    baseURL: "http://36.134.148.183:38888/api",
    // baseURL: "http://10.11.12.220:38888/api"
})
export function getVoice(text) {
    const url = '/text2voice';
    return $axios.post(url, {
        text: text,
    })
}
export function getCategory(text) {
    const url = '/text2category';
    return $axios.post(url, {
        text: text,
    })
}
export function getTags(text) {
    const url = '/text2tags';
    return $axios.post(url, {
        text: text,
    })
}
export function addNews(newData) {
    console.log(Vue.prototype.$writerId);
    const url = '/addNews';
    return $axios.post(url, {
        writerId: Vue.prototype.$writerId,
        newTitle: newData.newTitle,
        newAbstract: newData.newAbstract,
        newContent: newData.newContent,
        categoryId: newData.category.categoryId,
        tags: newData.tags,
    })
}
export function getAuthorPreview() {
    const url = '/authorPreview';
    return $axios.post(url, {
        writerId: Vue.prototype.$writerId,
    })
}
export function getAuthorArticles(pageNumber, pageSize) {
    const url = '/authorArticles';
    return $axios.post(url, {
        writerId: Vue.prototype.$writerId,
        pageNumber: pageNumber,
        pageSize: pageSize,
    })
}
export function getlogin(writerData) {
    const url = '/authorLogin';
    return $axios.post(url, {
        writerAccount: writerData.writerAccount,
        writerPassword: writerData.writerPassword,
    })
}
export function getMonthData() {
    const url = '/authorMonthData';
    return $axios.post(url, {
        writerId: Vue.prototype.$writerId
    })
}