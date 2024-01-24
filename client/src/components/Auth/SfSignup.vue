<template>
    <div class="signup-container">
        <div class="signup-box">
            <h2>Sign Up</h2>
            <form @submit.prevent="handleSignup" class="signup-form">
                <label class="signup-label" for="first-name">First Name</label>
                <input type="text" id="first-name" v-model="user.firstName" required />

                <label class="signup-label" for="last-name">Last Name</label>
                <input type="text" id="last-name" v-model="user.lastName" required />

                <label class="signup-label" for="email">Email</label>
                <input type="email" id="email" v-model="user.email" required />

                <label class="signup-label" for="password">Password</label>
                <input type="password" id="password" v-model="user.password" required />

                <button class="signup-submit-button" type="submit">Sign Up</button>
            </form>
        </div>
    </div>
</template>
    
<script>
import { mapActions } from 'vuex';

export default {
    name: 'SfSignup',
    data() {
        return {
            user: {
                firstName: '',
                lastName: '',
                email: '',
                password: '',
            }
        };
    },
    methods: {
        ...mapActions(["signup"]),
        handleSignup() {
            this.signup(this.user)
        }
    },
};
</script>
    
<style scoped>
.signup-container {
    height: calc(100vh - 64px);
    display: flex;
    align-items: center;
    justify-content: Center;
}

.signup-box {
    max-width: 400px;
    margin: auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    width: 100%;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.signup-form {
    display: flex;
    flex-direction: column;
}

.signup-label {
    width: 100%;
    text-align: left;
    margin-bottom: 5px;
    font-size: 0.75rem;
    font-weight: 600;
}

input {
    padding: 8px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 3px;
}

.signup-submit-button {
    padding: 10px;
    background-color: var(--primary-color);
    color: #fff;
    border: none;
    border-radius: 3px;
    font-weight: 600;
    cursor: pointer;
    text-transform: uppercase;
}

.signup-submit-button:hover {
    background-color: var(--primary-color);
}
</style>
    