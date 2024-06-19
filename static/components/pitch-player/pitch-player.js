async function pitchPlayer(path) {
  const template = await loadTemplateAsync(path)

  Vue.component('pitch-player', {
    name: 'pitch-player',
    props: ['pos', 'filtered-positions', 'index', 'player', 'ping'],
    template,

    watch: {
      immediate: true,
      player() {
        this.updatePlayer()
      }
    },

    data() {
      return {
        activePlayer: null,
      }
    },
    computed: {
      players() {
        return this.filteredPositions(this.pos)
      },
      playersMenu() {
        return this.filteredPositions(this.pos, true)
      }
    },
    methods: {
      handleSelection(player) {
        // this.activePlayer = this.players.find(p => p.id == player)
        this.$emit('add-player', player, this.index, this.pos)
      },
      updatePlayer() {
        this.activePlayer = this.players.find(p => p.id == this.player)
      }
    },
    async created() {
      this.updatePlayer()
    }
  })
}
