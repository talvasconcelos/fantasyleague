const initialState = {
  participant: {},
  hasTeam: false,
  team: [],
  formation: '',
  lineUp: [],
  players: [],
  eleven: [],
  subs: []
}

const state = new StateStore(initialState)

const competitionPage = async () => {
  await pitch('static/components/pitch/pitch.html')
  await pitchPlayer('static/components/pitch-player/pitch-player.html')

  new Vue({
    el: '#vue',
    mixins: [windowMixin],
    delimiters: ['${', '}'],
    data: function () {
      return {
        state,
        teamColumns: [
          {label: 'Name', align: 'left', field: 'name'},
          {label: 'Position', align: 'left', field: 'position'},
          {label: 'Points', align: 'left', field: 'points', sortable: true}
        ],
        selected: [],
        playersColumns: [
          // {label: 'ID', align: 'left', field: 'id'},
          {label: 'Name', align: 'left', field: 'name'},
          {label: 'Position', align: 'left', field: 'position', sortable: true},
          {label: 'Team', align: 'left', field: 'team', sortable: true}
        ],
        playersPagination: {
          rowsPerPage: 0
        },
        filter: '',
        filterPosition: 'All',
        positionOptions: [
          'All',
          'Goalkeeper',
          'Defender',
          'Midfielder',
          'Attacker'
        ]
      }
    },
    watch: {},
    computed: {
      filteredPlayers() {
        let players = state.players

        if (this.filterPosition !== 'All') {
          players = players.filter(
            player =>
              player.position.toLowerCase() ===
              this.filterPosition.toLowerCase()
          )
        }
        if (this.filter && this.filter.length > 2) {
          players = state.players.filter(player =>
            player.name.toLowerCase().includes(this.filter.toLowerCase())
          )
        }

        return Object.freeze(players)
      },
      eleven() {
        return state.eleven
      },
      subs() {
        return state.subs
      }
    },
    methods: {
      async getLeaguePlayers() {
        const {data} = await LNbits.api.request(
          'GET',
          `/fantasyleague/api/v1/competition/${state.participant.fantasyleague_id}/players`
        )
        // this.players = [...data]
        state.updateState('players', [...data])
      },
      selectedFn(details) {
        console.log('Selected:', details)
        state.updateState('team', [...state.team, ...details.rows])
      },
      addToTeam(team) {
        console.log('Add to team:', team)
        state.team = team.map(player => {
          return state.players.find(p => p.id == player)
        })
      },
      async saveTeam() {
        if (state.hasTeam) return await this.updateTeam()
        try {
          const wallet = _.findWhere(this.g.user.wallets, {
            id: state.participant.wallet
          })
          const {data} = await LNbits.api.request(
            'POST',
            `/fantasyleague/api/v1/participants/${state.participant.id}/team`,
            wallet.adminkey,
            {
              formation: state.formation,
              team: state.team.map(player => player.id)
            }
          )
          if (data) {
            state.hasTeam = true
          }
        } catch (error) {
          console.log(error)
        }
      },
      async updateTeam() {
        try {
          const wallet = _.findWhere(this.g.user.wallets, {
            id: this.participant.wallet
          })
          const {data} = await LNbits.api.request(
            'PUT',
            `/fantasyleague/api/v1/participants/${this.participant.id}/team`,
            wallet.adminkey,
            {
              formation: state.formation,
              team: state.team.map(player => player.id)
            }
          )
        } catch (error) {
          console.log(error)
        }
      },
      async updateLineUp() {
        let formationChanged = state.participant.formation !== state.formation
        try {
          const wallet = _.findWhere(this.g.user.wallets, {
            id: state.participant.wallet
          })
          const {data} = await LNbits.api.request(
            'PUT',
            `/fantasyleague/api/v1/participants/${state.participant.id}/lineup${
              formationChanged ? '?formation=' + state.formation : ''
            }`,
            wallet.adminkey,
            {
              lineup: state.lineUp
            }
          )
        } catch (error) {
          console.log(error)
        }
      }
    },
    async created() {
      state.setState({
        participant,
        team,
        formation: participant.formation || '4-4-2',
        lineUp: participant.lineup.split(',')
      })
      if (team.length > 0) {
        state.hasTeam = true
      }

      const unsubscribe = state.subscribe(newState => {
        console.log('State changed:', newState)
      })
      this.formation = state.formation
      // this.participant = participant

      // this.team = team
      // if (this.team.length > 0) {
      //   this.hasTeam = true
      // }
      // this.formation = this.participant.formation || '4-4-2'
      // this.lineUp = this.participant.lineup
      // .map(id => this.team.find(player => player.id == id))
      // .filter(player => player)
      await this.getLeaguePlayers()
    }
  })
}

competitionPage()
