async function pitch(path) {
  const template = await loadTemplateAsync(path)

  Vue.component('pitch', {
    name: 'pitch',
    props: ['pitch-src', 'formation', 'team'],
    template,

    data: function () {
      return {}
    },
    methods: {},
    async created() {
      console.log(this.formation)
    }
  })
}
