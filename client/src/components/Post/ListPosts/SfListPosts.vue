<template>
    <div class="post-list-container">
        <div class="tag-container">
            <h4>Tags</h4>
            <div class="tag-checkbox-group">
                <div v-for="tag in tags" class="tag-checkbox" :key="tag.tag">
                    <input type="checkbox" :id="tag.id" :value="tag.id" v-model="selectedTags">
                    <label :for="tag.id">{{ tag.tag }}</label>
                </div>
            </div>
        </div>
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
        },
        mode: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            selectedTags: []
        }
    },
    components: {
        SfPostCard
    },
    methods: {
        ...mapActions(["getFeedPosts", "getPosts"])
    },
    computed: {
        posts() {
            let data = this.$store.state.posts
            if (this.myPosts === true) {
                let userId = JSON.parse(localStorage.getItem("user")).id
                data = data.filter(post => post.author.id === userId)
            }

            return data
        },
        tags() {
            return this.$store.state.tags
        }
    },
    watch: {
        selectedTags(newValue) {
            if (this.mode == "feed-posts")
                this.getFeedPosts(newValue)
            else
                this.getPosts(newValue)
        }
    },
    mounted() {
        if (this.mode == "feed-posts")
            this.getFeedPosts(this.selectedTags)
        else
            this.getPosts(this.selectedTags)
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


.tag-checkbox {
    display: inline-block;
    margin: 5px;
}

.tag-checkbox input[type="checkbox"] {
    display: none;
}

.tag-checkbox label {
    display: block;
    border: 1px solid black;
    padding: 5px 10px;
    cursor: pointer;
    background-color: black;
    color: white;
    border-radius: 0.25rem;
}

.tag-checkbox input[type="checkbox"]:checked+label {
    background-color: white;
    color: black;
}

.tag-container {
    width: 100%;
    max-width: 960px;
    display: flex;
    align-items: flex-start;
    flex-direction: column;
    margin-bottom: 1rem;
}

.comment-container>h1 {
    text-align: left;
}
</style>