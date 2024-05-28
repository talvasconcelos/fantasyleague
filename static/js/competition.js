const competitionPage = async () => {
  await pitch('static/components/pitch/pitch.html')

  new Vue({
    el: '#vue',
    mixins: [windowMixin],
    delimiters: ['${', '}'],
    data: function () {
      return {
        participant: {},
        league: {},
        team: [],
        formation: '',
        teamColumns: [
          {label: 'Name', align: 'left', field: 'name'},
          {label: 'Position', align: 'left', field: 'position'},
          {label: 'Points', align: 'left', field: 'points', sortable: true}
        ],
        players: [],
        playersColumns: [
          // {label: 'ID', align: 'left', field: 'id'},
          {label: 'Name', align: 'left', field: 'name'},
          {label: 'Position', align: 'left', field: 'position', sortable: true},
          {label: 'Team', align: 'left', field: 'team'}
        ],
        playersPagination: {
          rowsPerPage: 0
        },
        filter: '',
        filterPosition: 'All',
        positionOptions: [
          'All',
          'Goalkeeper',
          'Defence',
          'Midfield',
          'Offence'
        ],
        formations: {}
      }
    },
    watch: {},
    computed: {
      selectedFormation() {
        return this.formations[this.formation]
      },
      filteredPlayers() {
        let players = this.players
        if (this.filterPosition !== 'All') {
          players = players.filter(
            player => player.position === this.filterPosition
          )
        }
        if (this.filter && this.filter.length > 2) {
          players = this.players.filter(player =>
            player.name.toLowerCase().includes(this.filter.toLowerCase())
          )
        }

        return Object.freeze(players)
      }
    },
    methods: {
      async getLeaguePlayers() {
        const {data} = await LNbits.api.request(
          'GET',
          `/fantasyleague/api/v1/competition/${this.league.id}/players`
        )
        this.players = [...data]
        console.log(this.players)
      },
      async saveTeam() {
        try {
          const wallet = _.findWhere(this.g.user.wallets, {
            id: this.participant.wallet
          })
          const {data} = await LNbits.api.request(
            'POST',
            `/fantasyleague/api/v1/participants/${this.participant.id}/team`,
            wallet.adminkey,
            {
              formation: this.formation,
              team: this.team.map(player => player.id)
            }
          )
          console.log(data)
        } catch (error) {
          console.log(error)
        }
      }
    },
    async created() {
      this.participant = participant
      this.league = league
      this.team = team
      this.pitchSrc = pitchSrc
      this.formations = formations()
      this.formation = this.participant.formation || '4-4-2'
      console.log(this.team)
      await this.getLeaguePlayers()
    }
  })
}

competitionPage()