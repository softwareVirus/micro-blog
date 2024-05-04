<template>
  <div class="notification-container">
    <div
      class="notification-icon-box"
      @mouseover="showNotifications = true"
      @mouseleave="showNotifications = false"
    >
      <SfNotificationIcon />
      <!-- Change the icon as per your choice -->
    </div>
    <div
      class="notification-box"
      @mouseover="showNotifications = true"
      @mouseleave="showNotifications = false"
      v-show="showNotifications"
    >
      <template v-if="notifications.length !== 0">
        <div
          v-for="(notification, index) in notifications"
          :key="index"
          class="notification-card"
        >
          <p>{{ notification.message }}</p>
        </div></template>
      <template v-else>
        <h3>There is no notification</h3>
      </template>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import SfNotificationIcon from "./SfNotificationIcon.vue";
import io from "socket.io-client";
export default {
  components: {
    SfNotificationIcon,
  },
  data() {
    return {
      showNotifications: false,
      notifications: [],
      socket: null,
    };
  },
  methods: {
    ...mapActions(["getNotifications"]),
  },
  async mounted() {
    const notifications = await this.getNotifications();
    this.notifications = notifications.data;
    const token = localStorage.getItem("access_token");

    this.socket = io("http://127.0.0.1:5000", {
      extraHeaders: {
        Authorization: "Bearer " + token,
      },
    }); // Replace with your server URL
    this.socket.emit("join_notification", { current_user_id: "alfa" });

    this.socket.on("notification", (notification) => {
      console.log("here", this.notifications);
      this.notifications.unshift(notification);
    });
  },
};
</script>

<style>
.notification-container {
  position: relative;
}

.notification-icon-box {
  cursor: pointer;
  border: solid 1px black;
  border-radius: 0.35rem;
  padding: 0.25rem 0.75rem;
}

.notification-box {
  position: absolute;
  top: 100%;
  left: 0;
  width: 300px; /* Adjust as needed */
  background-color: #fff;
  border: 1px solid #ccc;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 999;
}

.notification-card {
  padding: 10px;
  border-bottom: 1px solid #ccc;
}

.notification-card:last-child {
  border-bottom: none;
}
</style>
