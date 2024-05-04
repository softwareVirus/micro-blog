<template>
    <div id="message-box">
        <div id="user-info-box">
            <h2>{{ recipientUser.firstName }} {{ recipientUser.lastName }}</h2>
            <caption :style="{ color: recipientStatus === 'online' ? 'green' : 'red' }">
                {{ recipientStatus === 'online' ? '🟢 Active' : '🔴 Offline' }}
            </caption>
        </div>
        <div id="message-dialog">
            <div id="message-content">
                <div v-for="message in messages" :key="String(message.timestamp)" :class="(message.sender == currentUser.id ? 'self' : 'user') + '-box'">
                    {{ message.content }}
                </div>
            </div>
            <div id="message-input">
                <textarea v-model="messageInput" @keydown.enter.prevent="sendMessage" maxlength="250"></textarea>
                <button @click="sendMessage">Send</button>
            </div>
        </div>
    </div>
</template>

<script>
import io from 'socket.io-client';
import { mapActions } from 'vuex';

export default {
    props: ['cid', 'rid'],
    data() {
        return {
            socket: null,
            recipientStatus: 'online',
            messageInput: '',
            messages: [],
            recipientUser: null,
            interval: null
        };
    },
    async mounted() {
        this.recipientUser = await this.getProfile(this.$route.params.rid)
        this.messages = await this.fetchConversation(this.$route.params.rid)
        // Connect to the socket server
        const token = localStorage.getItem('access_token');

        this.socket = io('http://127.0.0.1:5000', {
            extraHeaders: {
                "Authorization": "Bearer " + token
            }
        }); // Replace with your server URL
        this.interval = setInterval(() => {
            
            this.socket.emit('user_status', {
                recipient_ids: [this.recipientUser.id]
            })
            // Handle user status updates
            this.socket.on('user_status', (users) => {
                
                const recipient = users[this.recipientUser.id];
                
                if (recipient) {
                    this.recipientStatus = recipient.status;
                }
            });
        }, 1000 * 10)

        // Join the private chat room
        this.socket.emit('join_private_chat', { current_user_id: this.currentUser.id });

        // Handle private messages
        this.socket.on('private_message', message => {
            
            this.messages.push(message);
            
        });
    },
    methods: {
        ...mapActions(["getProfile", "fetchConversation"]),
        sendMessage() {
            if(this.messageInput.trim() === "") {
                alert("You can not send empty message")
                return;
            }
            // Send the message to the recipient
            this.socket.emit('private_message', { recipient_id: this.recipientUser.id, message: this.messageInput });

            // Add the message to the local messages array
            this.messages.push(
                {
                    sender: this.currentUser.id,
                    recipient: this.recipientUser.id,
                    content: this.messageInput,
                    timestamp: new Date()
                }
            );

            // Clear the message input
            this.messageInput = '';
        }
    },
    computed: {
        currentUser() {
            return this.$store.state.user
        },
    },
    beforeDestroy() {
        // Leave the private chat room when the component is destroyed
        clearInterval(this.interval)
        this.socket.emit('leave_private_chat', { recipient_id: this.recipientUser.id });
    }
};
</script>

<style scoped>
#message-box {
    width: 90%;
    max-width: 1280px;
    margin: 0 auto;
}

#message-dialog {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    flex-direction: column;
    padding: 1rem;
    border: 2px solid black;
    border-radius: 2rem;
    width: 95%;
    height: calc(100vh - 12rem);
}

#message-input {
    width: 100%;
    margin-top: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
}

#message-input>textarea {
    border-radius: 1rem;
    padding: 0.25rem 1rem;
    width: 80%;
    resize: none;
    font-family: inherit
}

#message-input>button {
    color: white;
    font-size: 1rem;
    padding: 0.5rem 1rem;
    background-color: black;
    border-radius: 1rem;
    width: 15%;
    cursor: pointer;
}

#message-input>button:hover {
    opacity: 0.6;
}

.self-box,
.user-box {
    padding: 1rem;
    min-width: 20rem;
    border-radius: 1rem;
    width: fit-content;
    max-width: 50vw;
}

.self-box {
    align-self: flex-end;
    text-align: right;
    background-color: #59B4C3;
}

.user-box {
    align-self: flex-start;
    text-align: left;
    background-color: bisque;
}

#user-info-box {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-left: 2rem
}

#message-content {
    width: 95%;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    height: 90%;
    overflow: auto;
    padding: 1rem;
    justify-content: flex-end;
}

#message-content::-webkit-scrollbar {
    width: 0.5rem;
}

#message-content::-webkit-scrollbar-track {
    background-color: rgba(128, 128, 128, 0.3);
    /* Gray background with transparency */
    border-radius: 1rem;
}

#message-content::-webkit-scrollbar-thumb {
    background-color: #000;
    /* Black scrollbar */
    border-radius: 1rem;
    /* Rounded corners */
}
</style>