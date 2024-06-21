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
          {name: 'name', label: 'Name', align: 'left', field: 'name'},
          {
            name: 'posittion',
            label: 'Position',
            align: 'left',
            field: 'position',
            sortable: true
          },
          {
            name: 'team',
            label: 'Team',
            align: 'left',
            field: 'team',
            sortable: true
          },
          {
            name: 'points',
            label: 'Points',
            align: 'left',
            field: 'points',
            sortable: true
          }
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
        ],
        tab: 'team',
        leaderBoard: [],
        boardColumns: {
          columns: [
            {label: 'Name', align: 'left', field: 'name'},
            {label: 'Formation', align: 'left', field: 'formation'},
            {
              name: 'total_points',
              label: 'Points',
              align: 'left',
              field: 'total_points',
              sortable: true
            }
          ],
          pagination: {
            sortBy: 'total_points',
            rowsPerPage: 20,
            page: 1,
            descending: true,
            rowsNumber: 10
          }
        }
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
        state.updateState('players', [...data])
      },
      pickRandomTeam() {
        // pick 15 random players (2 goalkeepers, 5 defenders, 5 midfielders, 3 attackers)

        const players = state.players
        const goalkeepers = players.filter(
          player => player.position === 'Goalkeeper'
        )
        const defenders = players.filter(
          player => player.position === 'Defender'
        )
        const midfielders = players.filter(
          player => player.position === 'Midfielder'
        )
        const attackers = players.filter(
          player => player.position === 'Attacker'
        )

        const team = [
          ..._.sample(goalkeepers, 2),
          ..._.sample(defenders, 5),
          ..._.sample(midfielders, 5),
          ..._.sample(attackers, 3)
        ]

        state.updateState('team', team)
        this.selected = state.team
      },
      selectedFn(details) {
        const teamMap = new Map(state.team.map(player => [player.id, player]))
        if (teamMap.has(details.keys[0])) {
          teamMap.delete(details.keys[0])
        } else {
          teamMap.set(details.keys[0], details.rows[0])
        }
        state.updateState('team', [...teamMap.values()])
      },
      addToTeam(team) {
        state.team = team.map(player => {
          return state.players.find(p => p.id == player)
        })
        this.selected = state.team
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
          if (data.message) {
            state.updateState('hasTeam', true)
          }
          return
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
        hasTeam: false,
        startingEleven: {},
        substitutes: [],
        formation: participant.formation || '4-4-2',
        lineUp: participant.lineup ? participant.lineup.split(',') : []
      })
      if (team.length > 0) {
        state.hasTeam = true
      }

      // const unsubscribe = state.subscribe(newState => {
      //   //console.log('State changed:', newState)
      //   // this.$forceUpdate()
      // })
      this.formation = state.formation
      this.leaderBoard = board.sort((a, b) => b.total_points - a.total_points)

      await this.getLeaguePlayers()
    }
  })
}

competitionPage()
