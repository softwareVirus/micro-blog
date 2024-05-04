<template>
    <div class="comment-list">
        <SfComment v-for="comment in comments" :comment="comment" :key="comment.id"
            :class="'depth-' + comment.depth" />
    </div>
</template>

<script>
import SfComment from './SfComment.vue';

export default {
    name: "SfCommentList",
    components: {
        SfComment
    },
    computed: {
        comments() {
            return this.$store.state.currentPost.comments
        }
    }
}
</script>

<style scoped>
.comment-list {
    min-width: 100%;
    display: flex;
    flex-direction: column;
}
</style>