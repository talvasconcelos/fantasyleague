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
        },
        playerOut: null,
        playerIn: null,
        transfers: [],
        transferColumns: [
          {label: 'ID', align: 'left', field: 'id'},
          {
            label: 'Player Out',
            align: 'left',
            field: 'player_out_id',
            format: (val, row) => `${state.players.find(p => p.id == val).name}`
          },
          {
            label: 'Player In',
            align: 'left',
            field: 'player_in_id',
            format: (val, row) => `${state.players.find(p => p.id == val).name}`
          },
          {
            name: 'gameweek',
            label: 'Matchday',
            align: 'left',
            field: 'gameweek',
            sortable: true
          },
          {name: 'cost', label: 'Cost', align: 'left', field: 'cost'},
          {
            name: 'transfer_date',
            label: 'Date',
            align: 'left',
            field: 'transfer_date',
            sortable: true,
            format: val =>
              Quasar.utils.date.formatDate(
                new Date(val * 1000),
                'YYYY-MM-DD HH:mm'
              )
          }
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
      },
      transferWindowOpen() {
        return Date.now() < new Date(transferWindow)
      },
      transferPlayersList() {
        if (!this.playerOut)
          return state.players
            .filter(player => !state.team.find(p => p.id === player.id))
            .sort((a, b) => b.points - a.points)
        return state.players
          .filter(player => !state.team.find(p => p.id === player.id))
          .filter(player => player.position == this.playerOut.position)
          .filter(player => player.id !== this.playerOut.id)
          .sort((a, b) => b.points - a.points)
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
      async getParticipant() {
        try {
          const wallet = _.findWhere(this.g.user.wallets, {
            id: state.participant.wallet
          })
          const {data} = await LNbits.api.request(
            'GET',
            `/fantasyleague/api/v1/participant/${state.participant.id}`,
            wallet.adminkey
          )
          state.updateState('participant', data)
          state.updateState('lineUp', data.lineup.split(','))
        } catch (error) {
          LNbits.utils.notifyApiError(error)
        }
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
          if (data) {
            state.setState({
              hasTeam: true,
              participant: data,
              formation: data.formation,
              lineUp: data.lineup ? data.lineup.split(',') : []
            })
            this.$q.notify({
              message: 'Team saved successfully',
              color: 'positive',
              position: 'bottom'
            })
            if (!data.lineup) {
              this.updateLineUp()
            }
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
          if (data) {
            state.setState({
              participant: data,
              formation: data.formation,
              lineUp: data.lineup.split(',')
            })
            this.$q.notify({
              message: 'Lineup saved successfully',
              color: 'positive',
              position: 'bottom'
            })
          }
        } catch (error) {
          LNbits.utils.notifyApiError(error)
        }
      },
      selectPlayerOut(player = null) {
        if (this.playerOut && this.playerOut.id === player.id) {
          this.playerOut = null
          return
        }
        this.playerOut = player
      },
      selectPlayerIn(player = null) {
        if (this.playerIn && this.playerIn.id === player.id) {
          this.playerIn = null
          return
        }
        this.playerIn = player
      },
      async getTransfers() {
        try {
          const wallet = _.findWhere(this.g.user.wallets, {
            id: state.participant.wallet
          })
          const {data} = await LNbits.api.request(
            'GET',
            `/fantasyleague/api/v1/transfers/${state.participant.id}`,
            wallet.inkey
          )
          this.transfers = data
        } catch (error) {
          console.log(error)
        }
      },
      confirmTransfer() {
        this.$q
          .dialog({
            title: 'Transfer Confirmation',
            message: `Transfer <b>${this.playerOut.name}</b> for <b>${this.playerIn.name}</b>? <br> Please note that you can only make <b>1 free transfer per matchday</b>, additional transfers will cost you <b>4 points each</b>!`,
            cancel: true,
            html: true
          })
          .onOk(() => this.createTransfer())
          .onCancel(() => {
            this.playerOut = null
            this.playerIn = null
          })
      },
      async createTransfer() {
        if (this.playerIn == null || this.playerOut == null) return
        try {
          const wallet = _.findWhere(this.g.user.wallets, {
            id: state.participant.wallet
          })
          const {data} = await LNbits.api.request(
            'POST',
            `/fantasyleague/api/v1/transfers`,
            wallet.adminkey,
            {
              participant_id: state.participant.id,
              player_out_id: this.playerOut.id,
              player_in_id: this.playerIn.id
            }
          )

          const teamMap = new Map(state.team.map(player => [player.id, player]))
          teamMap.delete(this.playerOut.id)
          teamMap.set(this.playerIn.id, this.playerIn)
          state.updateState('team', [...teamMap.values()])
          this.playerOut = null
          this.playerIn = null
          this.transfers = [...this.transfers, data]
          this.$q.notify({
            message: 'Transfer successful',
            color: 'positive',
            position: 'bottom'
          })
          await this.getParticipant()
        } catch (error) {
          LNbits.utils.notifyApiError(error)
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

      // console.log(
      //   transferWindow,
      //   new Date(transferWindow),
      //   Date.now() > new Date(transferWindow)
      // )
      // console.log('team', team)

      // const unsubscribe = state.subscribe(newState => {
      //   //console.log('State changed:', newState)
      //   // this.$forceUpdate()
      // })
      this.formation = state.formation
      this.leaderBoard = board.sort((a, b) => b.total_points - a.total_points)

      await this.getLeaguePlayers()
      await this.getTransfers()
    }
  })
}

competitionPage()
