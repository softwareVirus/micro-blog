<template>
    <div>
        <div class="mode-button-container">
            <Button :class="(mode == 'all-posts' ? 'selected-mode-button ' : '') + 'mode-button'"
                @click.prevent="toggleMode('all-posts')">
                All Posts
            </Button>
            <button :class="(mode == 'feed-posts' ? 'selected-mode-button ' : '') + 'mode-button'"
                @click.prevent="toggleMode('feed-posts')">
                Feed
            </button>
        </div>
        <SfListPosts v-if="mode === 'all-posts'" mode="'all-posts'" key="all_posts" />
        <SfListPosts v-else-if="mode === 'feed-posts'" mode='feed-posts' key="feed_posts" />
    </div>
</template>

<script>
import SfListPosts from './SfListPosts.vue';

export default {
    name: "SfListPostWithToggleView",
    components: {
        SfListPosts
    },
    data() {
        return {
            mode: "all-posts",
            content: "askdjsakdjlasda ".repeat(100),
            title: "asdjhsadjaskas"
        }
    },
    methods: {
        toggleMode(mode) {
            this.mode = mode
        }
    }
}
</script>

<style scoped>
.mode-button-container {
    display: flex;
    margin: 2rem auto 0;
    width: fit-content;
    justify-content: center;
    border: 1px solid var(--primary-color);
    border-radius: 0.3rem;
    overflow: hidden;
}

.mode-button {
    font-size: 1rem;
    outline: none;
    border: none;
    padding: 0.4rem 1rem;
    font-weight: 600;
    background-color: white;
    border-radius: 0;
}

.selected-mode-button {
    background-color: var(--primary-color);
    color: white;
}
</style>