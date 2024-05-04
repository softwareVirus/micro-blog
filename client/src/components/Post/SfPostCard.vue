<template>
    <router-link class="post-card-link" :to="'/post/' + post.id">
        <div class="post-card-container">
            <div class="post-card">
                <h3 class="post-card-title">{{ post.title }}</h3>
                <p class="post-card-content" v-html="post.content"></p>
                <p class="post-card-author">
                    Author By {{ post.author.firstName + " " + post.author.lastName }}
                    <span id="dot">·</span>
                    {{ formattedDate }}
                </p>
                <button class="delete-button" v-if="myPosts" @click.prevent="handleDeletePost">Delete</button>
            </div>
            <div class="post-card-tags">
                <div class="tag-container">
                    <h4>Tags</h4>
                    <div class="tag-link-group" v-if="post.tags && post.tags.length > 0">
                        <route-link v-for="tag in post.tags" class="tag-link" :key="tag.id">
                            {{ tag.tag }}
                        </route-link>
                    </div>
                    <h4 v-else style="margin: 0; margin-left: 0.5rem;">No Tags</h4>
                </div>
            </div>
        </div>
    </router-link>
</template>

<script>
import moment from 'moment'
import { mapActions } from 'vuex';

export default {
    name: "SfPostCard",
    props: {
        post: {
            type: Object,
            required: true
        },
        myPosts: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            posts: [
                {
                    _id: "1",
                    title: "Hello World",
                    content: "Lorem Impus Lorem Impus Lorem Impus Lorem Impus Lorem Impus Lorem Impus Lorem Impus Lorem Impus Lorem Impus Lorem Impus Lorem Impus",
                    author: {
                        _id: "u1",
                        firstName: "İbrahim Halil",
                        lastName: "Sakli",
                        email: "ibrahimsdakli52@hotmail.com",
                    },
                    vote: 12,
                    created_at: new Date(),
                    updated_at: new Date()
                }
            ]
        }
    },
    methods: {
        ...mapActions(["deletePost"]),
        handleDeletePost() {
            this.deletePost(this.post.id)
        }
    },
    computed: {
        formattedDate() {
            return moment(this.post.created_at).format('MMM DD, YYYY');
        },
    },
}
</script>

<style scoped>
.post-card-container {
    width: 100%;
    text-align: left;
    /*border: 0.15rem solid #00000040;*/
    border-radius: 1rem;
    padding: 1rem 2rem;
    box-shadow: rgba(0, 0, 0, 0.16) 0px 3px 6px, rgba(0, 0, 0, 0.23) 0px 3px 6px;
    transition: all 0.2s ease-out;
    cursor: pointer;
    display: flex;
}

.post-card-link {
    width: 100%;
    max-width: 960px;
    text-decoration: none;
    color: inherit;
}

.post-card-container:hover {
    transform: translateY(-2px);
    box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px, rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
}

.post-card-author {
    font-size: 0.75rem;
}

.post-card-content {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    font-size: 0.95rem;
}

#dot {
    padding: 0 0.35rem;
}

.delete-button {
    padding: 10px;
    background-color: red;
    color: #fff;
    border: none;
    border-radius: 3px;
    font-weight: 600;
    cursor: pointer;
    width: 100%;
}

.post-card {
    width: 80%;
}

.post-card-tags {
    width: 20%;
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
    flex-flow: wrap;
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