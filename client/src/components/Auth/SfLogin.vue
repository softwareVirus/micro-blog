<template>
  <div class="login-container">
    <div class="login-box">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin" class="login-form">
        <label class="login-label" for="email">Email</label>
        <input type="text" id="email" v-model="user.email" required />

        <label class="login-label" for="password">Password</label>
        <input type="password" id="password" v-model="user.password" required />

        <button class="login-submit-button" type="submit">Login</button>
      </form>
    </div>
  </div>
</template>
  
<script>
import { mapActions } from 'vuex';

export default {
  name: 'SfLogin',
  data() {
    return {
      user: {
        email: '',
        password: '',
      }
    };
  },
  methods: {
    ...mapActions(["login"]),
    handleLogin() {
      this.login(this.user);
      this.$router.push({ name: "list-posts" })
    }
  },
};
</script>
  
<style scoped>
.login-container {
  height: calc(100vh - 64px);
  display: flex;
  align-items: center;
  justify-content: Center;
}

.login-box {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 100%;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.login-form {
  display: flex;
  flex-direction: column;
}

.login-label {
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

.login-submit-button {
  padding: 10px;
  background-color: var(--primary-color);
  color: #fff;
  border: none;
  border-radius: 3px;
  font-weight: 600;
  cursor: pointer;
  text-transform: uppercase;
}

.login-submit-button:hover {
  background-color: var(--primary-color);
}
</style>
  