async function settings(path) {
  const template = await loadTemplateAsync(path)
  Vue.component('settings', {
    name: 'settings',
    props: ['save-settings', 'apikey'],
    template,

    data: function () {
      return {
        footballdata_api_key: null
      }
    },
    methods: {
      emitSettings() {
        let data = {
          api_key: this.footballdata_api_key
        }
        this.$emit('save-settings', data)
      }
    },
    async created() {
      this.footballdata_api_key = this.apikey
    }
  })
}
