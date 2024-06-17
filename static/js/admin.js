const adminPage = async () => {
  await settings('static/components/settings/settings.html')

  new Vue({
    el: '#vue',
    mixins: [windowMixin],
    delimiters: ['${', '}'],
    data: function () {
      return {
        api_key: '',
        competitionDialog: {
          show: false,
          data: {}
        },
        competitions: [],
        competitionOptions: [],
        filter: '',
        leagues: [],
        selectedLeague: [],
        loading: false,
        leaguesColumns: [
          {
            label: 'ID',
            align: 'left',
            field: 'id'
          },
          {name: 'name', align: 'left', label: 'Name', field: 'name'},
          {
            name: 'type',
            label: 'Type',
            field: 'competition_type',
            sortable: true
          },
          {name: 'start', label: 'Start', field: 'season_start'},
          {name: 'end', label: 'End', field: 'season_end'},
          {name: 'buyin', label: 'Buy In', field: 'buy_in'},
          {
            name: 'fee',
            label: 'Fee',
            field: 'fee',
            format: val => `${val ? val * 100 : 0}%`
          },
          {name: 'ended', label: 'Status', field: 'has_ended', sortable: true},
          {
            name: 'participants',
            label: 'Participants',
            field: 'num_participants'
          }
        ]
      }
    },
    computed: {
      displayCompetition() {
        const code = this.competitionDialog.data.competition_code
        if (!code) return ''
        const comp = this.competitions.find(c => c.league.id === code)
        return `${comp.league.name} (${comp.country.name})`
      }
    },
    methods: {
      saveSettings(data) {
        LNbits.api
          .request(
            'POST',
            '/fantasyleague/api/v1/settings',
            this.g.user.wallets[0].adminkey,
            data
          )
          .then(res => {
            this.api_key = res.data.api_key
            this.$q.notify({
              type: 'positive',
              message: 'Settings saved',
              timeout: 5000
            })
          })
          .catch(error => {
            console.warn(error)
            LNbits.utils.notifyApiError(error)
          })
      },
      async openCompetitionDialog() {
        try {
          await this.getAvailableCompetitions()
          this.competitionOptions = this.competitions
            .map(c => ({
              label: c.league.name,
              value: c.league.id,
              type: c.league.type,
              image: c.league.logo,
              area: c.country.name,
              startDate: c.seasons[0].start,
              endDate: c.seasons[0].end
            }))
            .sort((a, b) => {
              // sort by start date closer to today
              return new Date(b.startDate) - new Date(a.startDate)
            })
          this.competitionDialog.show = true
        } catch (error) {
          console.warn(error)
          LNbits.utils.notifyApiError(error)
        }
      },
      closeCompetitionDialog() {
        this.competitionDialog.show = false
      },
      async getLeagues() {
        try {
          const leagues = await LNbits.api.request(
            'GET',
            '/fantasyleague/api/v1/competition?all_wallets=true',
            this.g.user.wallets[0].adminkey
          )
          if (leagues.data) {
            this.leagues = leagues.data
          }
        } catch (error) {
          console.warn(error)
          LNbits.utils.notifyApiError(error)
        }
      },
      filterCompetitions(val, update, abort) {
        update(() => {
          const searchTerm = val.toLowerCase()
          this.competitionOptions = this.competitionOptions.filter(c =>
            c.label.toLowerCase().includes(searchTerm)
          )
        })
      },
      async getAvailableCompetitions() {
        if (!this.api_key) return
        const {data} = await LNbits.api.request(
          'GET',
          '/fantasyleague/api/v1/eligible',
          this.g.user.wallets[0].adminkey
        )
        this.competitions = [...data]
      },
      async submitCompetition() {
        this.loading = true
        let comp = this.competitions.find(
          c => c.league.id === this.competitionDialog.data.competition_code
        )
        let dialog = this.competitionDialog.data
        dialog.dismissMsg = this.$q.notify({
          message: 'Creating league, fetching players... Please wait!',
          timeout: 0
        })
        let season = comp.seasons[0]

        let data = {
          wallet: dialog.wallet,
          name: dialog.name,
          description: dialog.description,
          competition_type: comp.league.type,
          competition_code: comp.league.id,
          competition_logo: comp.league.logo,
          season_start: season.start,
          season_end: season.end,
          season: season.year,
          buy_in: dialog.buy_in,
          fee: dialog.fee
        }
        dialog.first_place && (data.first_place = dialog.first_place / 100)
        dialog.second_place && (data.second_place = dialog.second_place / 100)
        dialog.third_place && (data.third_place = dialog.third_place / 100)
        dialog.matchday_winner &&
          (data.matchday_winner = dialog.matchday_winner / 100)
        try {
          const league = await LNbits.api.request(
            'POST',
            '/fantasyleague/api/v1/competition',
            this.g.user.wallets[0].adminkey,
            data
          )
          if (league.data) {
            dialog.dismissMsg()
            this.$q.notify({
              type: 'positive',
              message: 'League created',
              timeout: 5000
            })
            this.loading = false
            this.competitionDialog.show = false
            this.leagues.push(league.data)
            console.log(this.leagues)
          }
        } catch (error) {
          console.warn(error)
          this.loading = false
          LNbits.utils.notifyApiError(error)
        }
      },
      deleteCompetition(league_id) {
        LNbits.utils
          .confirmDialog('Are you sure you want to delete this competition?')
          .onOk(() => {
            LNbits.api
              .request(
                'DELETE',
                `/fantasyleague/api/v1/competition/${league_id}`,
                this.g.user.wallets[0].adminkey
              )
              .then(() => {
                this.leagues = this.leagues.filter(l => l.id !== league_id)
                this.$q.notify({
                  type: 'positive',
                  message: 'Competition deleted',
                  timeout: 5000
                })
              })
              .catch(error => {
                console.warn(error)
                LNbits.utils.notifyApiError(error)
              })
          })
      },
      async refreshPlayers(league_id) {
        LNbits.utils
          .confirmDialog(
            'Are you sure you want to refresh players? \nThis will get all players from the API again.'
          )
          .onOk(() => {
            LNbits.api
              .request(
                'GET',
                `/fantasyleague/api/v1/competition/${league_id}/players/update`,
                this.g.user.wallets[0].adminkey
              )
              .then(() => {
                this.$q.notify({
                  type: 'positive',
                  message: 'Players refreshed',
                  timeout: 5000
                })
              })
              .catch(error => {
                console.warn(error)
                LNbits.utils.notifyApiError(error)
              })
          })
      }
    },
    async created() {
      const settings = await LNbits.api.request(
        'GET',
        '/fantasyleague/api/v1/settings',
        this.g.user.wallets[0].adminkey
      )
      if (settings.data) {
        this.api_key = settings.data.api_key
      }
      await this.getLeagues()
      // await this.getAvailableCompetitions()
      // this.competitionOptions = this.competitions
      //   .map(c => ({
      //     label: c.league.name,
      //     value: c.league.id,
      //     type: c.league.type,
      //     image: c.league.logo,
      //     area: c.country.name,
      //     startDate: c.seasons[0].start,
      //     endDate: c.seasons[0].end
      //   }))
      //   .sort((a, b) => {
      //     // sort by start date closer to today
      //     return new Date(b.startDate) - new Date(a.startDate)
      //   })
    }
  })
}

adminPage()
