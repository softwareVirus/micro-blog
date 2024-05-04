<template>
    <form class="editor-container" @submit.prevent="handleSubmit">
        <div class="editor-header">
            <div class="editor-header-title">
                <label for="title">Title</label>
                <input type="text" name="title" minlength="2" maxlength="45" :value="title"
                    @input="$emit('update:title', $event.target.value)" />
            </div>
            <button class="create-post-button" type="submit">Create</button>
        </div>
        <div class="tag-container">
            <h4>Tags</h4>
            <div class="tag-checkbox-group">
                <div v-for="tag in tags" class="tag-checkbox" :key="tag.id">
                    <input type="checkbox" :id="tag.id"
                        :checked="selectedTags.find(item => item == tag.id) !== undefined"
                        @input="$emit('update:tags', tag.id)">
                    <label :for="tag.id">{{ tag.tag }}</label>
                </div>
                <div class="tag-checkbox" v-if="!isOpen" @click.prevent="toggleIsOpen">
                    <button id="tag-add-button" style="width: fit-content;">
                        Add Tag +
                    </button>
                </div>
                <div class="tag-input-container" v-else>
                    <input id="tag-input" style="width: fit-content;" v-model="tagInput" />
                    <button id="tag-add-button" style="width: fit-content;" @click.prevent="handleAddTag">
                        Add
                    </button>
                    <button id="tag-add-button" style="width: fit-content; background-color: red; border-color: red"
                        @click.prevent="toggleIsOpen">
                        Cancel
                    </button>
                </div>

            </div>
        </div>
        <label for="content">Content</label>
        <quill-editor class="editor" ref="myTextEditor" :value="content" :options="editorOption"
            @change="updateContent" />
    </form>
</template>

<script>
import { quillEditor } from 'vue-quill-editor'
import { mapActions } from 'vuex'

export default {
    name: 'SfEditor',
    title: 'Theme: snow',
    components: {
        quillEditor
    },
    props: {
        title: String,
        content: String,
        tags: Array,
        selectedTags: Array
    },
    data() {
        return {
            isOpen: false,
            tagInput: "",
            editorOption: {
                modules: {
                    toolbar: [
                        ['bold', 'italic', 'underline', 'strike'],
                        ['blockquote', 'code-block'],
                        [{ 'header': 1 }, { 'header': 2 }],
                        [{ 'list': 'ordered' }, { 'list': 'bullet' }],
                        [{ 'script': 'sub' }, { 'script': 'super' }],
                        [{ 'indent': '-1' }, { 'indent': '+1' }],
                        [{ 'direction': 'rtl' }],
                        [{ 'size': ['small', false, 'large', 'huge'] }],
                        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
                        [{ 'font': [] }],
                        [{ 'color': [] }, { 'background': [] }],
                        [{ 'align': [] }],
                        ['clean'],
                        ['link', 'image', 'video']
                    ],
                }
            }
        }
    },
    methods: {
        ...mapActions(["createPost", "addTag"]),
        updateContent(event) {
            this.$emit('update:content', event.html)
        },
        toggleIsOpen() {
            this.isOpen = !this.isOpen
            this.tagInput = ""
        },
        handleAddTag() {
            if (this.tagInput == "") {
                alert("input can not be empty!!")
                return;
            }
            this.addTag(this.tagInput.toLowerCase().trim())
            this.toggleIsOpen()
        },
        handleSubmit() {
            if (this.title.length < 2 || this.content.length == 0) {
                alert("Title and content can not be empty!!")
                return;
            }
            this.createPost({
                title: this.$props.title,
                content: this.$props.content,
                tags: this.$props.selectedTags
            })
        }
    },
    computed: {
        editor() {
            return this.$refs.myTextEditor.quill
        },
    },
    emits: ['update:title', 'update:content']
}
</script>

<style scoped>
.editor-header {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.tag-input-container {
    display: flex;
    max-height: 34px;
    height: 100%;
    border: 1px solid black;
    padding: 2px;
    gap: 0.25rem;
    width: fit-content
}

#tag-input {
    height: 30px;
    outline: none;
    margin: 0;
    border: none;
}

.create-post-button {
    padding: 10px;
    background-color: var(--primary-color);
    color: #fff;
    border: none;
    font-size: 1.2rem;
    border-radius: 3px;
    font-weight: 600;
    height: 100%;
    cursor: pointer;
    min-height: 3rem;
}

.editor-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    margin: 3rem auto 1rem;
    width: 80vw;
}

label[for="title"],
label[for="content"] {
    width: 100%;
    text-align: left;
    margin-bottom: 5px;
    font-weight: 700;
}

label[for="content"] {
    margin-top: 0.75rem;
}

input {
    padding: 8px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 3px;
    font-size: 1.5rem;
    width: 50vw;
}

.editor {
    width: 100%;
}

.ql-editor {
    height: 100%;
    max-height: calc(60vh) !important;
    overflow: auto;
}

.editor-header-title {
    display: flex;
    flex-direction: column;
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

#tag-add-button {

    display: block;
    border: 1px solid black;
    padding: 5px 10px;
    cursor: pointer;
    background-color: black;
    color: white;
    border-radius: 0.25rem;
    font-size: 1rem;
}

.tag-checkbox input[type="checkbox"]:checked+label {
    background-color: white;
    color: black;
}

.tag-container {
    display: flex;
    align-items: flex-start;
    flex-direction: column;
    margin-bottom: 1rem;
}

.tag-checkbox-group {
    display: flex;
    align-items: center
}

@media (max-width: 1000px) {
    .editor-container {
        width: 95vw;
    }
}
</style>
