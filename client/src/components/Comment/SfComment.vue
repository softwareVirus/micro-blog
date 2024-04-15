<template>
    <div style="min-width: 100%;">

        <div class="comment-box">
            <div class="comment-author">
                <p class="author-name">
                    {{ comment.author.firstName + " " + comment.author.lastName }}
                </p>
                <p class="comment-date">
                    {{ formattedDate }}
                </p>
            </div>
            <p class="comment-content">
                &nbsp;&nbsp;&nbsp;&nbsp;{{ comment.content }}
            </p>
            <button v-if="comment.parentComment === null" @click.prevent="toggleReplyMode" class="reply-comment-button">
                Reply
            </button>
        </div>
        <SfCreateComment style="width: calc(100% - 1.5rem); margin-left: 1.5rem;" v-if="isReplyComment"
            :viewReplyButton="comment.depth !== 3" :isReplyComment="isReplyComment" :parentComment="comment.id"
            @update="newValue => isReplyComment = newValue" />
        <div style="width: calc(100% - 1.5rem); margin-left: 1.5rem;">
            <SfComment v-for="comment in (comment.childComments ? comment.childComments : [])" :comment="comment"
                :key="comment.id" :class="'depth-' + comment.depth" />
        </div>
        <p class="view-more-text"
            v-if="(comment.childComments !== undefined && comment.totalNumberOfChildComment > comment.childComments.length) && comment.totalNumberOfChildComment !== 0"
            style="margin-left: 1.5rem;" @click.prevent="handleGetChildComments">
            View Comments {{ comment.totalNumberOfChildComment }}
        </p>

    </div>
</template>

<script>
import moment from 'moment';
import SfCreateComment from './SfCreateComment.vue';
import { mapActions } from 'vuex';

export default {
    name: "SfComment",
    props: {
        comment: {
            type: Object,
            default: () => { }
        }
    },
    components: {
        SfCreateComment
    },
    data() {
        
        return {
            isReplyComment: false
        }
    },
    methods: {
        ...mapActions(["getComments"]),
        toggleReplyMode() {
            this.isReplyComment = !this.isReplyComment
        },
        handleGetChildComments() {
            this.getComments({
                postId: this.$route.params.id,
                commentId: this.comment.id
            })
        }
    },
    computed: {
        formattedDate() {
            return moment(this.comment.created_at).format('MMM DD, YYYY');
        },
        remainUnviewedChildComment() {/*
            if (this.comment.childComments.length !== 0) {
                return this.comment.totalNumberOfChildComments - this.comment.childComments.length;
            }*/
            return ""
        },
        checkMoreChildComment() {
            //return this.comment.childComments.length < this.comment.totalNumberOfChildComments
            return ""
        }
    },
    mounted() {
        
    }
}
</script>

<style scoped>
.comment-box {
    box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 2px 6px 2px;
    border-radius: 0.5rem;
    padding: 0.8rem;
    margin: 1rem 0;
}

.comment-content {
    text-align: left;
}

.comment-author {
    display: flex;
    gap: 1rem;
    align-items: center;
    justify-content: space-between;
}

.author-name {
    font-weight: 600;
}

.comment-date {
    font-size: 0.8rem;
}

.view-more-text {
    text-align: left;
    margin-bottom: 0;
    font-weight: bold;
    cursor: pointer;
}

.view-more-text:hover {
    text-decoration: underline;
}


.reply-comment-button {
    padding: 10px;
    background-color: var(--primary-color);
    color: #fff;
    border: none;
    border-radius: 3px;
    font-weight: 600;
    cursor: pointer;
}
</style>