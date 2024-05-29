async function pitch(path) {
  const template = await loadTemplateAsync(path)

  Vue.component('pitch', {
    name: 'pitch',
    props: ['pitch-src', 'formation', 'team', 'players', 'has-team'],
    template,

    watch: {
      immediate: true,
      team() {
        console.log('team changed')
        // console.log(this.team)
        this.updateTeam()
      }
    },

    data: function () {
      return {
        goalkeepers: Array(2).fill(null),
        defenders: Array(5).fill(null),
        midfielders: Array(5).fill(null),
        forwards: Array(3).fill(null)
      }
    },
    computed: {},
    methods: {
      formationArr() {
        return this.formation.split('-').map(Number)
      },
      filteredPositions(position, menu = false) {
        let playerList = this.players.filter(
          player => player.position.toLowerCase() === position.toLowerCase()
        )
        if (menu) {
          playerList = playerList.filter(player => !this.team.includes(player))
        }
        return playerList
      },
      addPlayer(player, idx, pos) {
        switch (pos) {
          case 'goalkeeper':
            this.goalkeepers[idx] = player
            break
          case 'defence':
            this.defenders[idx] = player
            break
          case 'midfield':
            this.midfielders[idx] = player
            break
          case 'offence':
            this.forwards[idx] = player
            break
        }
        let team = [
          ...this.goalkeepers,
          ...this.defenders,
          ...this.midfielders,
          ...this.forwards
        ].filter(player => player !== null)
        this.$emit('add-player', team)
        // this.$nextTick(() => this.updateTeam())
      },
      updateTeam() {
        // Reset the arrays with null values
        this.goalkeepers.fill(null)
        this.defenders.fill(null)
        this.midfielders.fill(null)
        this.forwards.fill(null)

        // Function to fill a position array
        const fillPosition = (array, players, max) => {
          players.forEach((player, index) => {
            if (index < max) {
              array[index] = player.id
            }
          })
          return array
        }

        // Filter players by position
        const goalkeepers = this.team.filter(
          player => player.position === 'Goalkeeper'
        )
        const defenders = this.team.filter(
          player => player.position === 'Defence'
        )
        const midfielders = this.team.filter(
          player => player.position === 'Midfield'
        )
        const forwards = this.team.filter(
          player => player.position === 'Offence'
        )

        // Fill the position arrays with the filtered players
        this.goalkeepers = [...fillPosition(this.goalkeepers, goalkeepers, 2)]
        this.defenders = [...fillPosition(this.defenders, defenders, 5)]
        this.midfielders = [...fillPosition(this.midfielders, midfielders, 5)]
        this.forwards = [...fillPosition(this.forwards, forwards, 3)]
      }
    },
    async created() {
      this.updateTeam()
    }
  })
}
