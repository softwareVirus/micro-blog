<template>
    <form class="comment-type-container" @submit.prevent="handleCreateComment">
        <textarea class="comment-input" placeholder="Type comment..." maxlength="200" v-model="comment"></textarea>
        <div :class="isReplyComment ? 'button-container' : ''">
            <button class="create-comment-button failed-color" v-if="viewReplyButton"
                @click="$emit('update', false)">Close</button>
            <button class="create-comment-button" type="submit">Publish</button>
        </div>
    </form>
</template>

<script>
import { mapActions } from 'vuex';

export default {
    props: {
        isReplyComment: {
            type: Boolean,
            default: false
        },
        viewReplyButton: {
            type: Boolean,
            default: false
        },
        parentComment: {
            type: String,
            default: null
        }
    },
    data() {
        return {
            comment: ""
        }
    },
    methods: {
        ...mapActions(["createComment"]),
        handleCreateComment() {
            console.log(this.parentComment)
            this.createComment({
                content: this.comment,
                postId: this.$route.params.id,
                parentComment: this.parentComment
            })
        }
    },
}
</script>

<style scoped>
.button-container {
    width: 100%;
    display: flex;
    justify-content: space-between;
}

.comment-input {
    width: 100%;
    border-radius: 0.5rem;
    border: none;
    resize: none;
    outline: none !important;
    font-family: inherit;
    font-size: 1rem;
}

.comment-input:focus {
    height: 10rem;
}

.comment-type-container {
    width: 100%;
    border-radius: 0.5rem;
    box-sizing: border-box;
    padding: 0.75rem 0.5rem;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    box-shadow: rgba(0, 0, 0, 0.16) 0px 3px 6px, rgba(0, 0, 0, 0.23) 0px 3px 6px;
}

.failed-color {
    background-color: red !important;
}

.create-comment-button {
    padding: 10px;
    background-color: var(--primary-color);
    color: #fff;
    border: none;
    border-radius: 3px;
    font-weight: 600;
    cursor: pointer;
}
</style>