<template>
    <div>
        <div class="mode-button-container">
            <Button :class="(mode == 'editor' ? 'selected-mode-button ' : '') + 'mode-button'"
                @click.prevent="toggleMode('editor')">
                Editor
            </Button>
            <button :class="(mode == 'display' ? 'selected-mode-button ' : '') + 'mode-button'"
                @click.prevent="toggleMode('display')">
                Display
            </button>
        </div>
        <div>
            <SfEditor v-if="mode == 'editor'" :title="title" :content="content" :tags="tags"
                @update:title="newValue => title = newValue" @update:content="newValue => content = newValue"
                @update:tags="newValue => {
                if (selectedTags.includes(newValue)) {
                    selectedTags = selectedTags.filter(item => item != newValue)
                } else {
                    selectedTags.push(newValue)
                }
            }" :selectedTags="selectedTags" />
            <SfDisplayPost v-else :title="title" :content="content" :tags="selectedTags" />
        </div>
    </div>
</template>

<script>
import SfEditor from './SfEditor.vue';
import SfDisplayPost from '../SfDisplayPost.vue';

export default {
    name: "CreatePost",
    components: {
        SfEditor,
        SfDisplayPost
    },
    data() {
        return {
            mode: "editor",
            content: "",
            title: "",
            selectedTags: []
        }
    },
    methods: {
        toggleMode(mode) {
            this.mode = mode
        }
    },
    computed: {
        tags() {
            return this.$store.state.tags
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