import { createRouter, createWebHistory } from 'vue-router';
import translatePage from '../views/translatePage.vue';

const routes = [
    {
        path: '/',
        redirect: '/translate'  // 添加重定向，使根路径跳转到/translate
    },
    {
        path: '/translate',
        name: 'translate',
        component: translatePage,
        meta: { fullPage: true }  // 添加 meta 标记，用于全屏显示
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;