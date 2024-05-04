<template>
    <div class="display-post-container" v-if="title !== null || post !== undefined">
        <div class="display-post-box">
            <h1 class="display-post-title">
                {{ post.title }}
            </h1>
            <p class="post-card-content" v-html="post.content">
            </p>
        </div>
        <div class="comment-container">
            <h1>
                Authored By
                <router-link :to="'/profile/' + post.author.id">
                    {{ post.author.firstName + " " + post.author.lastName }}
                </router-link>
            </h1>
            <div style="display: flex; width: 100%; justify-content: space-between; ">
                <p class="post-card-author" style="margin: 0">
                    {{ formattedDate }}
                </p>
                <div style="display: flex; align-items: center; gap: 0.5rem"
                    v-if="!title && !content && tags.length == 0">
                    <SfHeartIcon />
                    {{ post.votes.length }}
                </div>
            </div>
            <div class="tag-container" v-if="title !== null">
                <h4>Tags</h4>
                <div class="tag-link-group" v-if="tags && tags.length > 0">
                    <route-link v-for="tag in tags" class="tag-link" :key="tag.tag">
                        {{ tag.tag }}
                    </route-link>
                </div>
                <h4 v-else style="margin: 0; margin-left: 0.5rem;">No Tags</h4>
            </div>
            <div class="tag-container" v-else>
                <h4>Tags</h4>
                <div class="tag-link-group" v-if="post.tags && post.tags.length > 0">
                    <route-link v-for="tag in post.tags" class="tag-link" :key="tag.tag">
                        {{ tag.tag }}
                    </route-link>
                </div>
                <h4 v-else style="margin: 0; margin-left: 0.5rem;">No Tags</h4>
            </div>
            <h1>
                Comments
            </h1>
            <template v-if="!title && !content">
                <SfCreateComment />
                <SfCommnetList />
            </template>
        </div>
    </div>
</template>

<script>
import moment from 'moment'
import SfCommnetList from '../Comment/SfCommentList'
import SfCreateComment from '../Comment/SfCreateComment.vue'
import SfHeartIcon from '../SfHeartIcon.vue'
import { mapActions } from 'vuex'

export default {
    components: {
        SfCommnetList,
        SfCreateComment,
        SfHeartIcon
    },
    props: {
        title: {
            type: String,
            default: null
        },
        content: {
            type: String,
            default: null
        },
        tags: {
            type: Array,
            default: () => []
        }
    },
    methods: {
        ...mapActions(["getPost", "removeCurrentPost"])
    },
    computed: {
        formattedDate() {
            return moment(this.post.created_at).format('MMM DD, YYYY');
        },
        post() {
            if (this.title !== null && this.content !== null) {
                return {
                    title: this.title,
                    content: this.content,
                    created_at: new Date(),
                    author: {
                        firstName: this.$store.state.user.firstName,
                        lastName: this.$store.state.user.lastName
                    }
                }
            }
            return this.$store.state.currentPost
        }
    },
    async mounted() {
        await this.getPost(this.$route.params.id)
    },
    beforeDestroy() {
        this.removeCurrentPost()
    }
}
</script>

<style scoped>
.display-post-container {
    display: flex;
    width: 95%;
    margin: 0 auto;
    justify-content: space-between;
}

.display-post-box {
    width: 65%;
}

.comment-container {
    width: 30%;
    margin-top: 3rem;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.display-post-title {
    font-size: 6rem;
    margin-bottom: 0.25rem;
    word-wrap: break-word;
}

.post-card-author {
    font-size: 1rem;
    margin-top: 0;
    margin-bottom: 2.5rem;
    text-align: left
}

#dot {
    padding: 0 0.35rem;
}

.post-card-content {
    text-align: left;
}

.tag-link {
    display: block;
    border: 1px solid black;
    padding: 5px 10px;
    cursor: pointer;
    background-color: black;
    color: white;
    border-radius: 0.25rem;
}

.tag-link-group {
    display: flex;
    gap: 0.25rem;
    padding: 0.25rem;
}

.tag-container {
    display: flex;
    align-items: flex-start;
    flex-direction: column;
    margin-bottom: 0.5rem;
}

.comment-container>h1 {
    text-align: left;
}
</style>
