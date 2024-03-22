<template>
    <div class="post-list-container">
        <div class="user-info-container">
            <div class="user-name-box">
                <h1>
                    {{ profile.firstName }} {{ profile.lastName }}
                </h1>
                <button :class="'follow-button' + (isFollowing ? ' unfollow' : '')" @click.prevent="followUser">
                    {{ isFollowing ? "Unfollow" : "Follow" }}
                </button>
            </div>
            <div class="user-follow-info">
                <p>
                    {{ profile.followers.length }} Followers
                </p>
                <p>
                    {{ profile.following.length }} Following
                </p>
            </div>
        </div>
        <div class="tag-container">
            <h4>Tags</h4>
            <div class="tag-checkbox-group">
                <div v-for="tag in tags" class="tag-checkbox" :key="tag.id">
                    <input type="checkbox" :id="tag.id" :value="tag.id" v-model="selectedTags">
                    <label :for="tag.id">{{ tag.tag }}</label>
                </div>
            </div>
        </div>
        <div v-if="posts.length === 0">
            <h1>
                There is no post yet
            </h1>
        </div>
        <SfPostCard v-for="post in posts" :key="post._id" :post="post" :my-posts="myPosts"></SfPostCard>
    </div>
</template>

<script>
import SfPostCard from '../Post/SfPostCard.vue';
import { mapActions } from 'vuex';


export default {
    name: 'SfListPosts',
    props: {
        myPosts: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            selectedTags: [],
            profile: null
        }
    },
    components: {
        SfPostCard
    },
    methods: {
        ...mapActions(["follow", "unfollow", `getProfile`, "getPosts", "getUserPosts"]),
        async followUser() {
            if (this.isFollowing) {
                const result = await this.unfollow(this.userId)
                if (result) {
                    this.profile.followers = this.profile.followers.filter(item => item !== this.user.id)
                }
            } else {
                const result = await this.follow(this.userId)
                if (result) {
                    this.profile.followers.push(this.user.id)
                }
            }
        }
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
        },
        user() {
            return this.$store.state.user
        },
        userId() {
            return this.$route.params.id
        },
        isFollowing() {
            return this.$store.state.user?.following.includes(this.userId) === true
        }
    },
    watch: {
        async selectedTags(newValue, oldValue) {
            console.log(newValue, oldValue)
            await this.getUserPosts({
                userId: this.userId,
                tags: newValue
            })
        }
    },
    async mounted() {
        this.profile = await this.getProfile(this.userId)
        await this.getUserPosts({
            userId: this.userId
        })
        console.log(this.profile, this.tags)
    }
}
</script>

<style scoped>
.unfollow {
    background-color: white !important;
    color: black !important
}

.follow-button {
    display: block;
    border: 1px solid black;
    padding: 5px 10px;
    cursor: pointer;
    max-height: 40px;
    background-color: black;
    color: white;
    font-size: 1.25rem;
    min-width: 6rem;
    border-radius: 0.25rem;
}

.user-info-container {
    width: 100%;
    max-width: 960px;
    padding: 1rem 2rem;
    border-radius: 1rem;
    border: 2px black solid;
}

.user-name-box {
    display: flex;
    align-items: center;
    gap: 1rem
}

.user-follow-info {
    display: flex;
    gap: 1rem;
}

.user-follow-info>p {
    font-weight: bold;
}

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