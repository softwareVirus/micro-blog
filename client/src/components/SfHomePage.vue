<template>
  <div class="home-page">
    <h1>
      MICRO BLOG
    </h1>
    <p ref="paragraph">
      Your mini blog website
    </p>
  </div>
</template>

<script>
export default {
  name: 'SfHomePage',
  mounted() {
    const paragraph = this.$refs.paragraph;
    paragraph.addEventListener('animationstart', () => {
      // Set visibility to hidden after the animation is finished
      paragraph.style.visibility = 'visible';
    });
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.home-page > h1 {
  font-size: 12rem;
  margin: 1rem;
  animation: downToTopSlide 1s;
}

.home-page > p {
  margin: 0;
  font-size: 1.75rem;
  animation: downToTopSlide 1s;
  visibility: hidden; /* Initially hide the element */
  animation-delay: 0.75s;
}

.home-page {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 12rem);
  align-items: center;
  justify-content: center;
}

@keyframes downToTopSlide {
  from {
    transform: translateY(64px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>
