<template>
    <div class="navbar-container">
        <nav class="navbar">
            <div class="navbar-logo">
                <router-link to="/">Micro Blog</router-link>
            </div>
            <div class="navbar-items" v-if="user">
                <router-link to="/list-posts">List Posts</router-link>
                <router-link to="/create-post">Create Post</router-link>
            </div>
            <div class="navbar-auth-items">
                <template v-if="!user">
                    <router-link to="/login">Log In</router-link>
                    <router-link to="/signup">Sign Up</router-link>
                </template>
                <template v-else>
                    <SfNotificationBox />
                    <router-link to="/chat_history" style="background-color: white; border: 1px solid black;">
                        <SfMessageIcon />
                    </router-link>
                    <router-link :to="'/profile/' + user.id">{{ user.firstName + " " + user.lastName }}</router-link>
                    <button class="logout-button" @click.prevent="logout">Logout</button>
                </template>
            </div>
        </nav>
    </div>
</template>

<script>
import { mapActions } from 'vuex'
import SfMessageIcon from './SfMessageIcon.vue'
import SfNotificationBox from './Notification/SfNotificationBox.vue'
export default {
    name: "SfNavbar",
    components: {
        SfMessageIcon,
        SfNotificationBox
    },
    data() {
        return {
            isOpenProfileDialog: false,
            isOpenMenuDialog: false
        }
    },
    methods: {
        ...mapActions(["logout"]),
        toggleOpenProfileDialog() {
            this.isOpenProfileDialog = !this.isOpenProfileDialog
        },
        toggleOpenMenuDialog() {
            this.isOpenMenuDialog = !this.isOpenMenuDialog
        }
    },
    computed: {
        user() {
            //let user = JSON.parse(localStorage.getItem("user"))
            return this.$store.state.user
        }
    }
}
</script>

<style scoped>
.navbar-container {
    width: 100%;
    box-shadow: rgba(0, 0, 0, 0.15) 0px 3px 3px 0px;
}

.navbar {
    width: 100%;
    max-width: 1280px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-sizing: border-box;
    padding: 0.5rem;
    min-height: 4rem;
}

.navbar-items,
.navbar-auth-items {
    display: flex;
    gap: 1rem;
}

a {
    text-decoration: none;
    color: var(--primary-color);
    font-weight: 600;
}

.navbar-auth-items>a {
    min-height: 2.5rem;
    padding: 0.25rem 1rem;
    display: flex;
    align-items: center;
    border-radius: 0.35rem;
}

.navbar-auth-items>a:nth-child(1) {
    color: white;
    background-color: var(--primary-color);
}

.navbar-auth-items>a:nth-child(2) {
    color: var(--primary-color);
    border: 1px solid var(--primary-color);
    background-color: white;
}

.logout-button {
    padding: 10px;
    background-color: black;
    color: #fff;
    border: none;
    border-radius: 3px;
    font-weight: 600;
    cursor: pointer;
}
</style>