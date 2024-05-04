<template>
    <div id="message-history-box">
        <h1>Messages</h1>
        <div id="message-history-list">
            <SfMessageCard v-for="userId in user.conversations" :key="userId" :userId="userId"/>
        </div>
    </div>
</template>

<script>
import SfMessageCard from './SfMessageCard.vue';
export default {
    components: {
        SfMessageCard
    },
    computed: {
        user() {
            return this.$store.state.user
        }
    }
}
</script>

<style scoped>
#message-history-list {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
    width: 100%;
    height: calc(100vh - 60px - 42.880px - 37px - 8rem);
    overflow: auto;
    box-sizing: border-box;
    padding-bottom: 2rem;
}

#message-history-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    max-width: 1280px;
    margin: 0 auto;
    padding: 1rem;
    border-radius: 2rem;
    margin-bottom: 2rem;
    border: 2px solid black;    
    margin-top: 2rem;
}
</style>