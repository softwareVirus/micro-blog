<template>
    <router-link :to="`/chat/${currentUser.id}/${userId}`" class="message-card">
        <h1>{{ user.firstName + " " + user.lastName }}</h1>
    </router-link>
</template>

<script>
import { mapActions } from 'vuex';
export default {
    props: {
        userId: {
            type: String,
        }
    },
    data() {
        return {
            user: null,
        }
    },
    methods: {
        ...mapActions(["getProfile"])
    },
    computed: {
        currentUser() {
            return this.$store.state.user
        }
    },
    async mounted() {
        this.user = await this.getProfile(this.userId)
    }
}
</script>

<style scoped>
.message-card {
    width: 100%;
    max-width: 960px;
    box-shadow: rgba(0, 0, 0, 0.16) 0px 3px 6px, rgba(0, 0, 0, 0.23) 0px 3px 6px;
    border-radius: 2rem;
    display: flex;
    flex-direction: column;
    padding: 1rem 2.5rem;
    cursor: pointer;
    transition: all 0.2s ease-out;

}

.message-card>h1,
.message-card>p {
    text-align: left;
}

.message-card>caption {
    text-align: right;
}

.message-card:hover {
    transform: translateY(-2px);
}

a{
    text-decoration: none;
    color: inherit
}
</style>