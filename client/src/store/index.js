import Vuex from "vuex";
import axios from "axios";
import Vue from "vue";
import router from "@/router";

Vue.use(Vuex);

axios.defaults.baseURL = "http://127.0.0.1:5000/";

async function refreshToken() {
  try {
    const oldRefreshToken = localStorage.getItem("refresh_token");
    const response = await axios.post("/refresh_token", {
      refresh_token: oldRefreshToken,
    });

    const { access_token: accessToken, refresh_token: refreshToken } =
      response.data;
    // Save the tokens in local storage or another secure storage option
    localStorage.setItem("access_token", accessToken);
    localStorage.setItem("refresh_token", refreshToken);

    return accessToken;
  } catch (error) {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
    console.error("Error refreshing token:", error);
    throw error;
  }
}

const axiosApiInstance = axios.create();
// Request interceptor for API calls
axiosApiInstance.interceptors.request.use(
  async (config) => {
    console.log(config);
    const key = localStorage.getItem("access_token");
    config.headers = {
      Authorization: `Bearer ${key}`,
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET,PUT,POST,DELETE,PATCH,OPTIONS",
    };
    return config;
  },
  (error) => {
    Promise.reject(error);
  }
);
// Response interceptor for API calls
axiosApiInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  async function (error) {
    const originalRequest = error.config;
    console.log(error);
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const access_token = refreshToken();
      axiosApiInstance.defaults.headers.common["Authorization"] =
        "Bearer " + access_token;
      return axiosApiInstance(originalRequest);
    }
    return Promise.reject(error);
  }
);

axiosApiInstance.defaults.baseURL = "http://127.0.0.1:5000/";

export const store = new Vuex.Store({
  state: {
    user: null,
    posts: [],
    currentPost: null,
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setPosts(state, posts) {
      state.posts = posts;
    },
    setComments(state, comments) {
      state.comments = comments;
    },
    setCurrentPost(state, post) {
      state.currentPost = post;
    },
  },
  actions: {
    login: async function ({ commit, state }, user) {
      try {
        console.log(state);
        const { email, password } = user;
        const response = await axios.post("/login", { email, password });
        commit("setUser", response.data.user);
        localStorage.setItem("access_token", response.data.access_token);
        localStorage.setItem("refresh_token", response.data.refresh_token);
        localStorage.setItem("user", JSON.stringify(response.data.user));
      } catch (error) {
        return error;
      }
    },
    signup: async function ({ commit, state }, user) {
      try {
        console.log(state);
        const { firstName, lastName, email, password } = user;
        const response = await axiosApiInstance.post("/signup", {
          first_name: firstName,
          last_name: lastName,
          email,
          password,
        });
        commit("setUser", response.data.user);
        localStorage.setItem("access_token", response.data.access_token);
        localStorage.setItem("refresh_token", response.data.refresh_token);
        localStorage.setItem("user", JSON.stringify(response.data.user));
      } catch (error) {
        console.log(error);
        return error;
      }
    },
    logout: async function ({ commit }) {
      try {
        await axiosApiInstance.delete("/logout");
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user");
        commit("setPosts", []);
        commit("currentPost", null);
        commit("setUser", null);
        router.push({ name: "/login" });
      } catch (error) {
        return error;
      }
    },
    createPost: async function (_, post) {
      try {
        const response = await axiosApiInstance.post("/posts", post);

        console.log(response);
      } catch (error) {
        console.log(error);
      }
    },
    getPosts: async function ({ commit }) {
      try {
        const response = await axiosApiInstance.get("/posts");
        console.log(response);
        commit(
          "setPosts",
          response.data.map((post) => {
            post.author.firstName = post.author.first_name;
            post.author.lastName = post.author.last_name;
            delete post.author.first_name;
            delete post.author.last_name;
            return post;
          })
        );
        return response.data;
      } catch (error) {
        console.log(error);
        return [];
      }
    },
    getPost: async function ({ commit, state }, postId) {
      try {
        const response = await axiosApiInstance.get(`/posts/${postId}`);
        const comments = await axiosApiInstance.get(
          `/posts/${response.data.id}/comments`
        );
        console.log(comments);
        response.data.author.firstName = response.data.author.first_name;
        response.data.author.lastName = response.data.author.last_name;
        delete response.data.author.first_name;
        delete response.data.author.last_name;
        commit("setCurrentPost", {
          ...response.data,
          comments: comments.data.map((comment) => {
            comment.author.firstName = comment.author.first_name;
            comment.author.lastName = comment.author.last_name;
            comment.childComments = [];
            comment.parentComment = comment.parent_comment;
            comment.totalNumberOfChildComment =
              comment.total_number_of_child_comment;
            delete comment.parent_comment;
            delete comment.author.first_name;
            delete comment.author.last_name;
            delete comment.total_number_of_child_comment;
            return comment;
          }),
        });
        console.log(state.currentPost);
        return response.data;
      } catch (error) {
        commit("setCurrentPost", null);
        console.log(error);
        return [];
      }
    },
    getComments: async function ({ state }, { postId, commentId }) {
      try {
        const response = await axiosApiInstance.get(
          `/posts/${postId}/comments/${commentId}`
        );
        let post = state.currentPost;
        let comment = post.comments.find((comment) => comment.id === commentId);
        console.log(response, comment);
        comment.childComments.push(
          ...response.data.map((comment) => {
            comment.author.firstName = comment.author.first_name;
            comment.author.lastName = comment.author.last_name;
            comment.parentComment = comment.parent_comment;
            comment.totalNumberOfChildComment =
              comment.total_number_of_child_comment;
            delete comment.parent_comment;
            delete comment.author.first_name;
            delete comment.author.last_name;
            delete comment.total_number_of_child_comment;
            return comment;
          })
        );
        return response.data;
      } catch (error) {
        console.log(error);
        return [];
      }
    },
    createComment: async function (
      { state },
      { content, postId, parentComment }
    ) {
      try {
        const response = await axiosApiInstance.post(
          `/posts/${postId}/comments${
            parentComment === null ? "" : "/" + parentComment
          }`,
          {
            content: content,
          }
        );
        let comment = response.data;
        comment.author.firstName = comment.author.first_name;
        comment.author.lastName = comment.author.last_name;
        comment.parentComment = comment.parent_comment;
        comment.totalNumberOfChildComment =
          comment.total_number_of_child_comment;
        if (comment.parent_comment === null) comment.childComments = [];
        delete comment.author.first_name;
        delete comment.total_number_of_child_comment;
        delete comment.parent_comment;
        delete comment.author.last_name;
        let post = state.currentPost;

        console.log(response);
        if (parentComment === null) {
          if (post) {
            post.comments.push(comment);
          }
        } else {
          if (post) {
            let parent_comment = post.comments.find(
              (item) => item.id === parentComment
            );
            console.log(parent_comment);
            parent_comment.childComments.push(comment);
          }
        }
        return response.data;
      } catch (error) {
        console.log(error);
        return [];
      }
    },
    increaseVote: async function ({ state }, postId) {
      try {
        await axiosApiInstance.post("/vote/" + postId);
        state.currentPost.votes.push(state.user.id);
      } catch (error) {
        console.log(error);
        throw Error;
      }
    },
    decreaseVote: async function ({ state }, postId) {
      try {
        await axiosApiInstance.delete("/vote/" + postId);
        state.currentPost.votes = state.currentPost.votes.filter((vote) => vote != state.user.id);
      } catch (error) {
        console.log(error);
        throw Error;
      }
    },
    removeCurrentPost: function ({ commit }) {
      commit("setCurrentPost", null);
    },
    deletePost: async function ({ commit, state }, postId) {
      try {
        await axiosApiInstance.delete("/posts/" + postId);
        commit(
          "setPosts",
          state.posts.filter((post) => post.id !== postId)
        );
      } catch (error) {
        console.log(error);
      }
    },
  },
  modules: {},
});

export default async function main(store) {
  try {
    let user = JSON.parse(localStorage.getItem("user"));
    console.log("here2");
    if (user === null) {
      console.log(user);
      localStorage.clear();
      return store;
    } else {
      store.state.user = user;
    }
  } catch (e) {
    console.log(e);
  }
  console.log("here");
  return store;
}
