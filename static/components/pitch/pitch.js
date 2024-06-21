async function pitch(path) {
  const template = await loadTemplateAsync(path)

  Vue.component('pitch', {
    name: 'pitch',
    props: ['team'],
    template,

    watch: {
      immediate: true,
      team() {
        this.updateTeam()
      }
    },

    data: function () {
      return {
        state,
        goalkeepers: Array(2).fill(null),
        defenders: Array(5).fill(null),
        midfielders: Array(5).fill(null),
        forwards: Array(3).fill(null),
        startingEleven: {},
        substitutes: [],
        position: ['attacker', 'midfielder', 'defender', 'goalkeeper'],
        formation: state.formation,
        formations: ['4-4-2', '4-3-3', '3-5-2', '5-3-2', '4-5-1', '3-4-3']
        // team: state.team
      }
    },
    computed: {
      formationArr() {
        return this.formation.split('-').map(Number)
      }
    },
    methods: {
      filteredLineup(position, menu = false) {
        let playerList = state.team.filter(
          player => player.position.toLowerCase() === position.toLowerCase()
        )
        if (menu) {
          playerList = playerList.filter(
            player => !state.startingEleven[position].includes(player)
          )
        }
        return playerList
      },
      filteredPositions(position, menu = false) {
        let playerList = state.players.filter(
          player => player.position.toLowerCase() === position.toLowerCase()
        )
        if (menu) {
          playerList = playerList.filter(player => !state.team.includes(player))
        }
        return playerList
      },
      handleFormationChange(val) {
        state.formation = val
        this.formation = val
        this.updateLineup()
      },
      addToLineup(player_id, idx, pos) {
        // replace player in state.startingEleven with player with player_id
        // add replaced player to state.substitutes

        const {goalkeeper, defender, midfielder, attacker} =
          state.startingEleven
        const subs = [...state.substitutes]

        const player = state.team.find(p => p.id == player_id)
        const replacing = state.startingEleven[pos][idx]

        subs.splice(subs.indexOf(player), 1, replacing)

        switch (pos) {
          case 'goalkeeper':
            goalkeeper[idx] = player
            break
          case 'defender':
            defender[idx] = player
            break
          case 'midfielder':
            midfielder[idx] = player
            break
          default:
            attacker[idx] = player
            break
        }

        let lineup = [
          ...goalkeeper,
          ...defender,
          ...midfielder,
          ...attacker,
          ...subs
        ].map(player => player.id)
        console.log('lineup', lineup)
        state.updateState('lineUp', lineup)

        this.updateLineup()
      },
      addPlayer(player, idx, pos) {
        console.log('add player')
        switch (pos) {
          case 'goalkeeper':
            this.goalkeepers[idx] = player
            break
          case 'defender':
            this.defenders[idx] = player
            break
          case 'midfielder':
            this.midfielders[idx] = player
            break
          case 'attacker':
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
        // this.$nextTick(() => {
        //   this.team = state.team
        // })
      },
      emitUpdateLineup() {
        this.$emit('update-lineup')
        // this.updateLineup()
      },
      updateLineup() {
        if (state.team.length < 15) return
        let team = [...state.team]
        if (state.lineUp.length > 0) {
          team = state.lineUp.map(player => {
            return state.team.find(p => p.id == player)
          })
        }
        let lineup = constructLineUp(state.formation, team)

        state.updateState('startingEleven', {
          goalkeeper: lineup.get('goalkeepers'),
          defender: lineup.get('defenders'),
          midfielder: lineup.get('midfielders'),
          attacker: lineup.get('attackers')
        })
        state.updateState('substitutes', lineup.get('substitutes'))

        const eleven = [
          ...state.startingEleven.goalkeeper,
          ...state.startingEleven.defender,
          ...state.startingEleven.midfielder,
          ...state.startingEleven.attacker
        ]
        state.setState({
          eleven,
          subs: [...state.substitutes],
          lineUp: [...eleven, ...state.substitutes].map(player => player.id)
        })
      },
      updateTeam() {
        if (state.hasTeam) return
        // console.log('update team', this.team)
        // // Reset the arrays with null values
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
        const goalkeepers = state.team.filter(
          player => player.position === 'Goalkeeper'
        )
        const defenders = state.team.filter(
          player => player.position === 'Defender'
        )
        const midfielders = state.team.filter(
          player => player.position === 'Midfielder'
        )
        const forwards = state.team.filter(
          player => player.position === 'Attacker'
        )

        // Fill the position arrays with the filtered players
        this.goalkeepers = [...fillPosition(this.goalkeepers, goalkeepers, 2)]
        this.defenders = [...fillPosition(this.defenders, defenders, 5)]
        this.midfielders = [...fillPosition(this.midfielders, midfielders, 5)]
        this.forwards = [...fillPosition(this.forwards, forwards, 3)]
        console.log(
          'update team',
          this.goalkeepers,
          this.defenders,
          this.midfielders,
          this.forwards
        )
        this.updateLineup()
      }
    },
    async created() {
      if (state.hasTeam) {
        this.updateLineup()
      } else {
        this.updateTeam()
      }
    }
  })
}
