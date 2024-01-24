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
            <SfEditor 
                v-if="mode == 'editor'" 
                :title="title" 
                :content="content" 
                @update:title="newValue => title = newValue"
                @update:content="newValue => content = newValue" 
            />
            <SfDisplayPost v-else :title="title" :content="content"/>
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
            title: ""
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