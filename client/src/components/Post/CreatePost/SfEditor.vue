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
        <label for="content">Content</label>
        <quill-editor class="editor" ref="myTextEditor" :value="content" :options="editorOption" @change="updateContent" />
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
        content: String
    },
    data() {
        return {
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
        ...mapActions(["createPost"]),
        updateContent(event) {
            this.$emit('update:content', event.html)
        },
        handleSubmit() {
            if (this.title.length < 2 || this.content.length == 0) {
                alert("Title and content can not be empty!!")
                return;
            }
            this.createPost({
                title: this.$props.title,
                content: this.$props.content
            })
        }
    },
    computed: {
        editor() {
            return this.$refs.myTextEditor.quill
        },
    },
    mounted() {
        console.log('this is Quill instance:', this.editor)
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

@media (max-width: 1000px) {
    .editor-container {
        width: 95vw;
    }
}
</style>

