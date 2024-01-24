<template>
    <div class="post-list-container">
        <SfPostCard v-for="post in posts" :key="post._id" :post="post" :my-posts="myPosts"></SfPostCard>
    </div>
</template>

<script>
import SfPostCard from '../SfPostCard.vue';
import { mapActions } from 'vuex';


export default {
    name: 'SfListPosts',
    props: {
        myPosts: {
            type: Boolean,
            default: false
        }
    },
    components: {
        SfPostCard
    },
    methods: {
        ...mapActions(["getPosts"])
    },
    computed: {
        posts() {
            let data = this.$store.state.posts
            if (this.myPosts === true) {
                let userId = JSON.parse(localStorage.getItem("user")).id
                data = data.filter(post => post.author.id === userId)
            }

            return data
        }
    },
    mounted() {
        this.getPosts()
    }
}
</script>

<style scoped>
.post-list-container {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    padding-top: 2rem;
    padding-bottom: 1rem;
    margin: 0.45rem auto 0;
    height: calc(100vh - 0.45rem - 150px);
    overflow: auto;
}
</style>